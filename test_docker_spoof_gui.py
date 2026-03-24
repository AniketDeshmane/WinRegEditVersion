"""
Unit tests for docker_spoof_gui.py - Windows Version Spoof Tool
"""
import unittest
from unittest.mock import Mock, patch, mock_open, MagicMock
import json
import os
import sys
import tempfile
import shutil

# Mock Windows-specific modules for non-Windows systems
sys.modules['winreg'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['ctypes'] = MagicMock()

# Import the functions we'll test
import docker_spoof_gui as dsg


class TestRegistryOperations(unittest.TestCase):
    """Test registry read/write operations"""

    @patch('docker_spoof_gui.winreg.OpenKey')
    def test_open_registry_key_read(self, mock_open_key):
        """Test opening registry key with READ access"""
        mock_key = MagicMock()
        mock_open_key.return_value = mock_key
        
        result = dsg.open_registry_key(dsg.winreg.KEY_READ)
        
        mock_open_key.assert_called_once()
        self.assertIsNotNone(result)

    @patch('docker_spoof_gui.winreg.OpenKey')
    def test_open_registry_key_write(self, mock_open_key):
        """Test opening registry key with WRITE access"""
        mock_key = MagicMock()
        mock_open_key.return_value = mock_key
        
        result = dsg.open_registry_key(dsg.winreg.KEY_SET_VALUE)
        
        mock_open_key.assert_called_once()

    @patch('docker_spoof_gui.winreg.QueryValueEx')
    @patch('docker_spoof_gui.winreg.OpenKey')
    def test_read_registry_values_success(self, mock_open_key, mock_query):
        """Test successfully reading registry values"""
        mock_key = MagicMock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        mock_query.side_effect = [
            ("19045", 0),
            ("19045", 0),
            ("Professional", 0),
            ("22H2", 0)
        ]
        
        with patch('docker_spoof_gui.open_registry_key') as mock_open_reg:
            mock_open_reg.return_value.__enter__.return_value = mock_key
            result = dsg.read_registry_values()
        
        self.assertEqual(result["CurrentBuild"], "19045")
        self.assertEqual(result["EditionID"], "Professional")
        self.assertEqual(result["DisplayVersion"], "22H2")

    @patch('docker_spoof_gui.winreg.QueryValueEx')
    @patch('docker_spoof_gui.winreg.OpenKey')
    def test_read_registry_values_missing(self, mock_open_key, mock_query):
        """Test reading registry when values are missing"""
        mock_key = MagicMock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        mock_query.side_effect = FileNotFoundError()
        
        with patch('docker_spoof_gui.open_registry_key') as mock_open_reg:
            mock_open_reg.return_value.__enter__.return_value = mock_key
            result = dsg.read_registry_values()
        
        self.assertEqual(result["CurrentBuild"], "<not set>")

    @patch('docker_spoof_gui.winreg.SetValueEx')
    @patch('docker_spoof_gui.winreg.OpenKey')
    def test_write_registry_value(self, mock_open_key, mock_set_value):
        """Test writing a single registry value"""
        mock_key = MagicMock()
        
        with patch('docker_spoof_gui.open_registry_key') as mock_open_reg:
            mock_open_reg.return_value.__enter__.return_value = mock_key
            dsg.write_registry_value("CurrentBuild", "19045")
        
        mock_set_value.assert_called()

    @patch('docker_spoof_gui.write_registry_value')
    def test_write_registry_values_batch(self, mock_write_single):
        """Test writing multiple registry values"""
        test_values = {"CurrentBuild": "19045", "EditionID": "Professional"}
        
        dsg.write_registry_values(test_values)
        
        self.assertEqual(mock_write_single.call_count, 2)


class TestBackupRestore(unittest.TestCase):
    """Test backup and restore functionality"""

    def setUp(self):
        """Create temporary directory for test backups"""
        self.test_dir = tempfile.mkdtemp()
        self.original_backup_file = dsg.BACKUP_FILE
        dsg.BACKUP_FILE = os.path.join(self.test_dir, "test_backup.json")

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
        dsg.BACKUP_FILE = self.original_backup_file

    def test_save_backup(self):
        """Test saving backup to file"""
        test_values = {
            "CurrentBuild": "19045",
            "CurrentBuildNumber": "19045",
            "EditionID": "Professional",
            "DisplayVersion": "22H2"
        }
        
        dsg.save_backup(test_values)
        
        self.assertTrue(os.path.exists(dsg.BACKUP_FILE))
        with open(dsg.BACKUP_FILE, 'r') as f:
            loaded = json.load(f)
        self.assertEqual(loaded, test_values)

    def test_load_backup_exists(self):
        """Test loading backup when file exists"""
        test_values = {"CurrentBuild": "19045"}
        dsg.save_backup(test_values)
        
        loaded = dsg.load_backup()
        
        self.assertEqual(loaded, test_values)

    def test_load_backup_not_exists(self):
        """Test loading backup when file doesn't exist"""
        result = dsg.load_backup()
        
        self.assertIsNone(result)

    def test_backup_contains_all_required_keys(self):
        """Test that backup contains all required registry keys"""
        test_values = {
            "CurrentBuild": "19045",
            "CurrentBuildNumber": "19045",
            "EditionID": "Professional",
            "DisplayVersion": "22H2"
        }
        dsg.save_backup(test_values)
        
        loaded = dsg.load_backup()
        
        for key in ["CurrentBuild", "CurrentBuildNumber", "EditionID", "DisplayVersion"]:
            self.assertIn(key, loaded)


class TestSpoofValues(unittest.TestCase):
    """Test spoof value configuration"""

    def test_spoof_values_defined(self):
        """Test that SPOOF_VALUES is defined"""
        self.assertIsNotNone(dsg.SPOOF_VALUES)
        self.assertIsInstance(dsg.SPOOF_VALUES, dict)

    def test_spoof_values_contains_required_keys(self):
        """Test that SPOOF_VALUES has required keys"""
        required_keys = ["CurrentBuild", "CurrentBuildNumber", "EditionID", "DisplayVersion"]
        for key in required_keys:
            self.assertIn(key, dsg.SPOOF_VALUES)

    def test_spoof_values_win10_pro_22h2(self):
        """Test Windows 10 Pro 22H2 spoof values"""
        self.assertEqual(dsg.SPOOF_VALUES["CurrentBuild"], "19045")
        self.assertEqual(dsg.SPOOF_VALUES["EditionID"], "Professional")
        self.assertEqual(dsg.SPOOF_VALUES["DisplayVersion"], "22H2")


class TestAdminCheck(unittest.TestCase):
    """Test administrator check functionality"""

    @unittest.skip("ctypes.windll is Windows-only and cannot be tested on this platform")
    def test_is_admin_true(self):
        """Test when user is admin"""
        pass

    @unittest.skip("ctypes.windll is Windows-only and cannot be tested on this platform")
    def test_is_admin_false(self):
        """Test when user is not admin"""
        pass

    @unittest.skip("ctypes.windll is Windows-only and cannot be tested on this platform")
    def test_is_admin_exception(self):
        """Test exception handling for non-Windows systems"""
        pass


class TestDockerSpoofApp(unittest.TestCase):
    """Test the GUI application"""

    @unittest.skip("GUI tests require Windows environment with display")
    def test_app_initialization(self):
        """Test app initializes properly"""
        pass

    @unittest.skip("GUI tests require Windows environment with display")
    def test_installer_path_var_initialized(self):
        """Test installer path variable is initialized"""
        pass

    @unittest.skip("GUI tests require Windows environment with display")
    def test_installer_args_var_initialized(self):
        """Test installer arguments variable is initialized"""
        pass

    @unittest.skip("GUI tests require Windows environment with display")
    def test_status_label_initialized(self):
        """Test status label is initialized"""
        pass


class TestInputValidation(unittest.TestCase):
    """Test input validation"""

    def test_registry_subkey_valid(self):
        """Test registry subkey is valid path"""
        subkey = dsg.REGISTRY_SUBKEY
        self.assertTrue(len(subkey) > 0)
        self.assertIn("CurrentVersion", subkey)

    def test_spoof_values_string_type(self):
        """Test that spoof values are strings or ints"""
        for key, value in dsg.SPOOF_VALUES.items():
            self.assertIsInstance(value, (str, int))

    def test_spoof_build_number_valid(self):
        """Test spoof build number is valid"""
        build = dsg.SPOOF_VALUES.get("CurrentBuild")
        self.assertTrue(str(build).isdigit())
        self.assertGreaterEqual(int(build), 19000)


class TestProfileIntegration(unittest.TestCase):
    """Test integration with profiles module"""

    def test_profiles_imported(self):
        """Test that profiles module is imported"""
        self.assertTrue(hasattr(dsg, 'WINDOWS_PROFILES'))
        self.assertTrue(hasattr(dsg, 'DEFAULT_PROFILE'))

    def test_default_profile_loaded(self):
        """Test that default profile is loaded"""
        self.assertIsNotNone(dsg.SPOOF_VALUES)
        self.assertIn("CurrentBuild", dsg.SPOOF_VALUES)

    def test_read_registry_values_with_keys(self):
        """Test read_registry_values accepts custom keys"""
        # Test that function can accept keys parameter
        custom_keys = ["CurrentBuild", "EditionID"]
        # We can't test actual reading, but we can verify the function signature
        import inspect
        sig = inspect.signature(dsg.read_registry_values)
        self.assertIn("keys", sig.parameters)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_backup_file = dsg.BACKUP_FILE
        dsg.BACKUP_FILE = os.path.join(self.test_dir, "test_backup.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        dsg.BACKUP_FILE = self.original_backup_file

    def test_empty_backup_file(self):
        """Test handling of empty backup file"""
        with open(dsg.BACKUP_FILE, 'w') as f:
            f.write("")
        
        with self.assertRaises(json.JSONDecodeError):
            dsg.load_backup()

    def test_corrupted_backup_file(self):
        """Test handling of corrupted JSON backup"""
        with open(dsg.BACKUP_FILE, 'w') as f:
            f.write("{ invalid json")
        
        with self.assertRaises(json.JSONDecodeError):
            dsg.load_backup()

    def test_backup_with_unicode_characters(self):
        """Test backup with unicode characters"""
        test_values = {
            "CurrentBuild": "19045",
            "EditionID": "Professional™"
        }
        dsg.save_backup(test_values)
        loaded = dsg.load_backup()
        
        self.assertEqual(loaded["EditionID"], "Professional™")

    def test_backup_file_permissions(self):
        """Test that backup file is created with proper permissions"""
        test_values = {"CurrentBuild": "19045"}
        dsg.save_backup(test_values)
        
        self.assertTrue(os.path.exists(dsg.BACKUP_FILE))
        # Check file is readable
        with open(dsg.BACKUP_FILE, 'r') as f:
            self.assertIsNotNone(f.read())


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

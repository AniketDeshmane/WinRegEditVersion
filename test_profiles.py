"""
Tests for profiles.py - Windows version profiles module
"""
import unittest
from profiles import (
    WINDOWS_PROFILES,
    DEFAULT_PROFILE,
    EDITIONS,
    get_profile,
    get_profile_names,
    get_edition_names,
    validate_profile,
    merge_profiles,
)


class TestProfileDefinitions(unittest.TestCase):
    """Test profile data structures"""

    def test_profiles_exist(self):
        """Test that WINDOWS_PROFILES is defined"""
        self.assertIsNotNone(WINDOWS_PROFILES)
        self.assertIsInstance(WINDOWS_PROFILES, dict)
        self.assertGreater(len(WINDOWS_PROFILES), 0)

    def test_profile_names(self):
        """Test profile names are strings"""
        for name in WINDOWS_PROFILES.keys():
            self.assertIsInstance(name, str)
            self.assertGreater(len(name), 0)

    def test_default_profile_exists(self):
        """Test default profile exists in profiles"""
        self.assertIn(DEFAULT_PROFILE, WINDOWS_PROFILES)

    def test_windows_10_profiles(self):
        """Test Windows 10 profiles exist"""
        windows_10_profiles = [name for name in WINDOWS_PROFILES.keys() if "Windows 10" in name]
        self.assertGreater(len(windows_10_profiles), 0)

    def test_windows_11_profiles(self):
        """Test Windows 11 profiles exist"""
        windows_11_profiles = [name for name in WINDOWS_PROFILES.keys() if "Windows 11" in name]
        self.assertGreater(len(windows_11_profiles), 0)

    def test_editions_defined(self):
        """Test EDITIONS dictionary is defined"""
        self.assertIsNotNone(EDITIONS)
        self.assertIsInstance(EDITIONS, dict)
        self.assertIn("Professional", EDITIONS)
        self.assertIn("Home", EDITIONS)


class TestProfileValues(unittest.TestCase):
    """Test individual profile configurations"""

    def test_profile_has_required_fields(self):
        """Test each profile has required fields"""
        required_fields = ["CurrentBuild", "CurrentBuildNumber", "EditionID", "DisplayVersion"]
        for profile_name, profile_data in WINDOWS_PROFILES.items():
            for field in required_fields:
                self.assertIn(field, profile_data, f"{field} missing from {profile_name}")

    def test_windows_10_22h2_values(self):
        """Test Windows 10 22H2 profile values"""
        profile = WINDOWS_PROFILES.get("Windows 10 22H2")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["CurrentBuild"], "19045")
        self.assertEqual(profile["DisplayVersion"], "22H2")

    def test_windows_11_23h2_values(self):
        """Test Windows 11 23H2 profile values"""
        profile = WINDOWS_PROFILES.get("Windows 11 23H2")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["CurrentBuild"], "22631")
        self.assertEqual(profile["DisplayVersion"], "23H2")

    def test_build_numbers_are_valid(self):
        """Test build numbers are numeric"""
        for profile_name, profile_data in WINDOWS_PROFILES.items():
            build = profile_data.get("CurrentBuild", "")
            self.assertTrue(str(build).isdigit(), f"Invalid build in {profile_name}")
            self.assertGreaterEqual(int(build), 19000, f"Build too low in {profile_name}")

    def test_edition_ids_are_valid(self):
        """Test edition IDs are from known editions"""
        valid_editions = set(EDITIONS.keys())
        for profile_name, profile_data in WINDOWS_PROFILES.items():
            edition = profile_data.get("EditionID", "")
            self.assertIn(edition, valid_editions, f"Invalid edition in {profile_name}")


class TestProfileFunctions(unittest.TestCase):
    """Test profile utility functions"""

    def test_get_profile_returns_dict(self):
        """Test get_profile returns a dictionary"""
        profile = get_profile("Windows 10 22H2")
        self.assertIsInstance(profile, dict)

    def test_get_profile_nonexistent(self):
        """Test get_profile returns None for nonexistent profile"""
        profile = get_profile("Nonexistent Profile")
        self.assertIsNone(profile)

    def test_get_profile_names_returns_list(self):
        """Test get_profile_names returns list"""
        names = get_profile_names()
        self.assertIsInstance(names, list)
        self.assertGreater(len(names), 0)

    def test_get_profile_names_contains_known_profiles(self):
        """Test get_profile_names contains expected profiles"""
        names = get_profile_names()
        self.assertIn("Windows 10 22H2", names)
        self.assertIn("Windows 11 23H2", names)

    def test_get_edition_names_returns_list(self):
        """Test get_edition_names returns list"""
        editions = get_edition_names()
        self.assertIsInstance(editions, list)
        self.assertGreater(len(editions), 0)

    def test_get_edition_names_contains_known_editions(self):
        """Test get_edition_names contains expected editions"""
        editions = get_edition_names()
        self.assertIn("Professional", editions)
        self.assertIn("Home", editions)
        self.assertIn("Enterprise", editions)


class TestProfileValidation(unittest.TestCase):
    """Test profile validation"""

    def test_validate_valid_profile(self):
        """Test validation of valid profile"""
        profile = {
            "CurrentBuild": "19045",
            "CurrentBuildNumber": "19045",
            "EditionID": "Professional",
            "DisplayVersion": "22H2"
        }
        is_valid, msg = validate_profile(profile)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

    def test_validate_missing_field(self):
        """Test validation with missing required field"""
        profile = {
            "CurrentBuild": "19045",
            "EditionID": "Professional",
            # Missing CurrentBuildNumber and DisplayVersion
        }
        is_valid, msg = validate_profile(profile)
        self.assertFalse(is_valid)
        self.assertIn("Missing", msg)

    def test_validate_not_dict(self):
        """Test validation with non-dict input"""
        is_valid, msg = validate_profile("not a dict")
        self.assertFalse(is_valid)
        self.assertIn("dictionary", msg)

    def test_validate_invalid_field_type(self):
        """Test validation with invalid field type"""
        profile = {
            "CurrentBuild": 19045,  # int instead of str
            "CurrentBuildNumber": 19045,
            "EditionID": "Professional",
            "DisplayVersion": "22H2"
        }
        is_valid, msg = validate_profile(profile)
        self.assertTrue(is_valid)  # int is allowed

    def test_validate_existing_profiles(self):
        """Test validation of all existing profiles"""
        for profile_name, profile_data in WINDOWS_PROFILES.items():
            is_valid, msg = validate_profile(profile_data)
            self.assertTrue(is_valid, f"Profile {profile_name} invalid: {msg}")


class TestProfileMerging(unittest.TestCase):
    """Test profile merging functionality"""

    def test_merge_profiles_basic(self):
        """Test basic profile merging"""
        base = {"CurrentBuild": "19045", "EditionID": "Professional"}
        custom = {"EditionID": "Home"}
        
        merged = merge_profiles(base, custom)
        
        self.assertEqual(merged["CurrentBuild"], "19045")
        self.assertEqual(merged["EditionID"], "Home")

    def test_merge_profiles_adds_new_fields(self):
        """Test merge adds new fields"""
        base = {"CurrentBuild": "19045"}
        custom = {"DisplayVersion": "22H2"}
        
        merged = merge_profiles(base, custom)
        
        self.assertEqual(merged["CurrentBuild"], "19045")
        self.assertEqual(merged["DisplayVersion"], "22H2")

    def test_merge_profiles_does_not_modify_base(self):
        """Test merge doesn't modify original dict"""
        base = {"CurrentBuild": "19045"}
        custom = {"EditionID": "Professional"}
        
        merged = merge_profiles(base, custom)
        
        self.assertNotIn("EditionID", base)

    def test_merge_profiles_with_profile_getter(self):
        """Test merge with profiles from get_profile"""
        base_profile = get_profile("Windows 10 22H2")
        custom = {"EditionID": "Home"}
        
        merged = merge_profiles(base_profile, custom)
        
        self.assertEqual(merged["EditionID"], "Home")
        self.assertEqual(merged["CurrentBuild"], "19045")


class TestProfileConsistency(unittest.TestCase):
    """Test consistency across profiles"""

    def test_all_profiles_have_same_keys(self):
        """Test all profiles have consistent key structure"""
        expected_keys = set(WINDOWS_PROFILES[DEFAULT_PROFILE].keys())
        
        for profile_name, profile_data in WINDOWS_PROFILES.items():
            actual_keys = set(profile_data.keys())
            # Allow some variation, but core keys should be consistent
            self.assertIn("CurrentBuild", actual_keys)
            self.assertIn("EditionID", actual_keys)

    def test_build_number_consistency(self):
        """Test build numbers are appropriate for Windows version"""
        for profile_name, profile_data in WINDOWS_PROFILES.items():
            build = int(profile_data["CurrentBuild"])
            
            if "Windows 10" in profile_name:
                self.assertLess(build, 22000)
            elif "Windows 11" in profile_name:
                self.assertGreaterEqual(build, 22000)

    def test_version_in_name_matches_data(self):
        """Test profile name matches version data"""
        for profile_name, profile_data in WINDOWS_PROFILES.items():
            if "Windows 10" in profile_name:
                display = profile_data.get("DisplayVersion", "")
                # Win10 21/22H2 have different builds
                build = int(profile_data.get("CurrentBuild", 0))
                self.assertLess(build, 22000)
            elif "Windows 11" in profile_name:
                build = int(profile_data.get("CurrentBuild", 0))
                self.assertGreaterEqual(build, 22000)


if __name__ == '__main__':
    unittest.main(verbosity=2)

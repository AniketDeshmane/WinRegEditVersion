# Windows Version Spoof Helper - Complete Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation and Setup](#installation-and-setup)
5. [Usage Guide](#usage-guide)
6. [API Reference](#api-reference)
7. [Configuration](#configuration)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)
10. [Future Enhancements](#future-enhancements)

---

## Project Overview

### Purpose

The Windows Version Spoof Helper is a utility application designed to temporarily modify Windows registry values to report a different operating system version to software installers. This is particularly useful for users with older hardware running older Windows versions who need to install software that enforces minimum OS version requirements.

### Target Use Case

The primary use case is enabling the installation of Docker Desktop on systems running Windows versions earlier than the minimum required version. Docker Desktop, for example, may require Windows 10 22H2 or Windows 11. This tool allows users to modify the registry to appear as though they are running a newer version during installation, then automatically restore the original values afterward.

### Technical Stack

- **Language**: Python 3.11+
- **GUI Framework**: Tkinter (built-in with Python)
- **Registry Access**: Windows `winreg` module
- **Data Format**: JSON (for backup files)
- **Testing Framework**: unittest (Python standard library)

### Platform Requirements

- **Operating System**: Windows 10 or Windows 11
- **Privileges**: Administrator/System privileges required
- **Python Version**: Python 3.7 or higher

---

## Features

### Implemented Features

#### 1. Windows Profile Management

**Description**: Pre-configured profiles for various Windows versions allow users to quickly spoof as different operating systems without manual configuration.

**Supported Profiles**:

| Profile Name | Build Number | Edition | Release |
|---|---|---|---|
| Windows 10 22H2 | 19045 | Professional | 22H2 |
| Windows 10 21H2 | 19044 | Professional | 21H2 |
| Windows 11 23H2 | 22631 | Professional | 23H2 |
| Windows 11 22H2 | 22621 | Professional | 22H2 |

**Implementation Details**:
- Profiles defined in `profiles.py`
- Each profile contains complete registry values needed for convincing OS emulation
- Profiles support validation and merging of custom values

#### 2. Registry Value Management

**Description**: Sophisticated registry read/write operations with proper error handling and access control.

**Supported Registry Values**:
- `CurrentBuild`: Build number (e.g., "19045")
- `CurrentBuildNumber`: Build identifier (e.g., "19045")
- `EditionID`: Windows edition (e.g., "Professional")
- `DisplayVersion`: Display version (e.g., "22H2")
- `ProductName`: Full product name (e.g., "Windows 10")
- `ReleaseId`: Release identifier (e.g., "22H2")
- `CurrentMajorVersionNumber`: Major version (10 or 11)
- `CurrentMinorVersionNumber`: Minor version (typically 0)

**Registry Hive**: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion`

**Access Control**:
- Read operations use `KEY_READ | KEY_WOW64_64KEY`
- Write operations use `KEY_SET_VALUE | KEY_WOW64_64KEY`
- All operations require Administrator privileges

#### 3. Backup and Restore Functionality

**Description**: Automatic backup of original registry values before modification, with reliable restore capability.

**Backup Format**: JSON serialization
```json
{
    "CurrentBuild": "19045",
    "CurrentBuildNumber": "19045",
    "EditionID": "Professional",
    "DisplayVersion": "22H2"
}
```

**Backup File**: `registry_backup_docker_spoof.json` (created in working directory)

**Features**:
- Automatic backup creation before spoof operation
- Persistent storage in JSON format
- Support for Unicode characters in registry values
- Validation of backup integrity
- Multiple backup entries (future enhancement)

#### 4. Graphical User Interface

**Description**: User-friendly Tkinter-based GUI providing intuitive access to all functionality.

**UI Components**:

a) **Profile Selection Frame**
   - Dropdown menu of available Windows profiles
   - Real-time profile switching
   - Visual feedback on profile changes

b) **Installer Configuration Frame**
   - Custom path input for installer executable
   - Browse button for file selection
   - Optional installer arguments input
   - Default Docker Desktop installer path

c) **Registry Configuration Display**
   - Side-by-side comparison of current vs. target values
   - Shows 4 critical registry values
   - Real-time updates on status changes
   - Informational description of functionality

d) **Control Buttons**
   - "Backup + Spoof + Install": Initiates the complete workflow
   - "Restore from Backup": Restores original registry values

e) **Status Bar**
   - Real-time status messages
   - Color-coded feedback (blue for info, red for errors)
   - Operation progress indication

**Requirements Check**:
- Automatic detection of Administrator privilege
- Warning dialog if not running as Administrator
- Graceful error handling for permission issues

#### 5. Profile Switching

**Description**: Dynamic profile selection with immediate visual feedback and configuration updates.

**Functionality**:
- Dropdown list of all available profiles
- Live preview of registry values for selected profile
- Status message confirmation on profile change
- Support for custom profile merging (foundation)

**Event Handling**:
- `ComboboxSelected` event triggers profile change
- Automatic UI refresh on profile selection
- Value conversion (int to string) for display

#### 6. Comprehensive Testing

**Description**: Extensive test coverage ensuring reliability and preventing regressions.

**Test Suite 1: test_docker_spoof_gui.py**
- 27 tests covering core GUI and registry functionality
- Test categories:
  - Registry Operations (6 tests)
  - Backup and Restore (5 tests)
  - Spoof Values (3 tests)
  - Admin Privileges (3 tests)
  - GUI Application (4 skipped on non-Windows)
  - Input Validation (3 tests)
  - Profile Integration (3 tests)
  - Edge Cases (4 tests)

**Test Suite 2: test_profiles.py**
- 32 tests for profile management module
- Test categories:
  - Profile Definitions (6 tests)
  - Profile Values (5 tests)
  - Profile Functions (6 tests)
  - Profile Validation (6 tests)
  - Profile Merging (4 tests)
  - Profile Consistency (4 tests)

**Test Coverage**:
- Total: 59 tests
- Success Rate: 100% (with 7 skipped on non-Windows environments)
- Edge Cases: Corrupted files, Unicode characters, missing values, permissions

#### 7. Input Validation

**Description**: Robust validation of user inputs and registry values.

**Validation Types**:
- Registry registry value existence checks
- Build number numeric validation
- Edition ID validation against known editions
- Installer path validation (file existence)
- Profile structure validation
- JSON integrity validation for backups

**Error Handling**:
- Permission errors → User-friendly error dialogs
- File not found → Clear guidance on problem
- Invalid registry values → Graceful fallback to defaults
- JSON parsing errors → Exception catching with recovery

#### 8. Multi-Edition Support

**Description**: Support for multiple Windows editions enabling specialized spoofing scenarios.

**Supported Editions**:
- Home
- Professional
- Enterprise
- Education

**Implementation**:
- Edition definitions in `profiles.py`
- Validation against known editions
- Foundation for custom edition support

### Planned Features (Not Yet Implemented)

#### 1. Dry-Run Mode
**Scope**: Preview registry changes without applying them
**Use Case**: Users can verify changes before committing
**Implementation Plan**: Add preview dialog showing exact registry modifications

#### 2. Backup History
**Scope**: Maintain multiple timestamped backups
**Use Case**: Users can restore to any previous state
**Implementation Plan**: 
- Store backups with timestamps
- UI list showing available backups
- Ability to compare backup versions

#### 3. Advanced Editor
**Scope**: Manual entry of custom registry values
**Use Case**: Power users needing non-standard configurations
**Implementation Plan**:
- Additional UI frame for custom entry
- Validation of custom values
- Merge with profile presets

#### 4. Detailed Logging
**Scope**: Comprehensive audit trail of all operations
**Use Case**: Debugging, compliance, troubleshooting
**Implementation Plan**:
- Timestamped operation log file
- Export capability for reports
- Log levels (INFO, WARNING, ERROR, DEBUG)

#### 5. Dark Mode / Modern UI
**Scope**: Contemporary visual appearance matching Windows 11 Fluent Design
**Use Case**: Better user experience, modern aesthetics
**Implementation Plan**:
- Theme selection option
- Accent color customization
- System theme detection

#### 6. Registry Preview
**Scope**: Real-time display of what will be changed
**Use Case**: Transparency and user confidence
**Implementation Plan**:
- Diff view showing before/after
- Detailed value comparison
- Change summary

#### 7. System Restore Point Creation
**Scope**: Automatic Windows system restore point before modification
**Use Case**: Complete system recovery capability
**Implementation Plan**:
- Use WMI to create restore point
- Notification to user of restore point creation
- Reference to restore point in logs

#### 8. Rollback Scheduler
**Scope**: Automatic restore of original values after specified time
**Use Case**: Temporary spoofing without manual intervention
**Implementation Plan**:
- Background timer implementation
- Scheduled registry restoration
- User notification before rollback

#### 9. WMI Data Modification
**Scope**: Modify WMI Win32_OperatingSystem class data
**Use Case**: More comprehensive OS spoofing for sophisticated detection
**Implementation Plan**:
- Query WMI for OS information
- Modify WMI classes (requires special access)
- Restore WMI values

#### 10. Export Registry Diff Report
**Scope**: Generate detailed report of all registry changes
**Use Case**: Documentation, debugging, compliance
**Implementation Plan**:
- HTML or PDF report generation
- Side-by-side comparison tables
- Timestamp and user information

---

## Architecture

### Project Structure

```
WInRegEditVersion/
├── docker_spoof_gui.py          # Main GUI application
├── profiles.py                  # Profile definitions and utilities
├── test_docker_spoof_gui.py     # GUI and registry operation tests
├── test_profiles.py             # Profile module tests
├── docker_spoof_gui.spec        # PyInstaller specification
├── build_docker_spoof.bat       # Build script
├── .gitignore                   # Git ignore rules
└── DOCUMENTATION.md             # This file
```

### Module Responsibilities

#### docker_spoof_gui.py

**Classes**:
- `DockerSpoofApp(tk.Tk)`: Main application window

**Functions**:
- `open_registry_key(access)`: Open Windows registry key
- `read_registry_values(keys=None)`: Read values from registry
- `write_registry_value(name, value)`: Write single registry value
- `write_registry_values(values_dict)`: Write multiple values
- `save_backup(values_dict)`: Save backup to JSON file
- `load_backup()`: Load backup from JSON file
- `is_running_as_admin()`: Check administrator privileges

**Constants**:
- `REGISTRY_ROOT`: Points to HKEY_LOCAL_MACHINE
- `REGISTRY_SUBKEY`: Registry path for Windows version info
- `BACKUP_FILE`: Path to backup JSON file
- `SPOOF_VALUES`: Default spoof values (from default profile)

#### profiles.py

**Data Structures**:
- `WINDOWS_PROFILES`: Dictionary of available profiles
- `EDITIONS`: Dictionary of supported Windows editions
- `EXTENDED_REGISTRY_KEYS`: List of registry keys to modify

**Functions**:
- `get_profile(profile_name)`: Retrieve profile by name
- `get_profile_names()`: List all available profiles
- `get_edition_names()`: List all available editions
- `validate_profile(profile_dict)`: Validate profile structure
- `merge_profiles(base_profile, custom_values)`: Merge custom values into profile

### Data Flow Diagram

```
User Interface (GUI) 
    ↓
Profile Selection
    ↓
Registry Read (read_registry_values)
    ↓
Backup Creation (save_backup)
    ↓
Registry Write (write_registry_values)
    ↓
Installer Execution (subprocess)
    ↓
User Action (Manual Restore)
    ↓
Registry Read (load_backup)
    ↓
Registry Write (restore values)
    ↓
Complete
```

### Error Handling Strategy

**Permission Errors**:
- Caught at operation level
- User presented with clear error dialog
- Suggestion to run as Administrator

**File Errors**:
- Missing backup file: Graceful handling with user message
- Corrupted JSON: Exception caught with recovery
- Invalid installer path: Validation before execution

**Registry Errors**:
- Missing registry values: Default handling with "<not set>"
- Access denied: Permission check and user notification
- Invalid key paths: Try/except with error reporting

---

## Installation and Setup

### Prerequisites

- Windows 10 or Windows 11
- Python 3.7 or higher
- Administrator privileges for spoof functionality
- Git (optional, for cloning repository)

### Installation Steps

#### Option 1: From Source

```bash
# Clone the repository
git clone https://github.com/AniketDeshmane/WinRegEditVersion.git
cd WinRegEditVersion

# No external dependencies required (uses only stdlib)
# Run the application
python docker_spoof_gui.py
```

#### Option 2: Compiled Executable

```bash
# Build using PyInstaller (if development environment available)
python -m PyInstaller docker_spoof_gui.spec

# Or use pre-built executable in /dist folder
dist/docker_spoof_gui.exe
```

### First-Time Setup

1. **Administrator Check**: 
   - Right-click `docker_spoof_gui.py` or `.exe`
   - Select "Run as administrator"

2. **Select Profile**:
   - Choose appropriate Windows version from dropdown
   - Verify target values are displayed correctly

3. **Verify Installer Path**:
   - Check that installer path is correct
   - Click "Browse..." to select if needed

4. **Proceed**:
   - Click "Backup + Spoof + Install"
   - Follow installer prompts
   - After completion, click "Restore from Backup"

---

## Usage Guide

### Basic Workflow

#### Step 1: Start Application as Administrator

```bash
# Rights-click and "Run as administrator"
python docker_spoof_gui.py
```

**Expected Result**: GUI window opens with warning if not admin

#### Step 2: Select Windows Profile

```
Profile Dropdown: [Windows 10 22H2 ▼]
```

**Action**: Click dropdown, select desired Windows version
**Result**: Target values update in Registry Configuration display

#### Step 3: Verify Installer Path

```
Installer .exe path: [C:\Users\...\Docker Desktop Installer.exe...]
Installer arguments: [install --accept-license]
```

**Action**: Modify if needed, use Browse button for file selection
**Result**: Installer path validated

#### Step 4: Execute Spoof + Install

```
Click: "1) Backup + Spoof + Install"
```

**Actions Performed**:
1. Read current registry values
2. Save backup to JSON file
3. Write spoof values to registry
4. Execute installer with provided arguments
5. Display installer completion dialog
6. Ready for manual restore

#### Step 5: Restore Original Values

```
Click: "2) Restore from Backup"
```

**Actions Performed**:
1. Load backup from JSON file
2. Write original values back to registry
3. Display confirmation dialog
4. Return to Ready state

### Advanced Options

#### Custom Installer Arguments

```
Installer arguments (optional): [install --accept-license --quiet]
```

**Format**: Space-separated arguments
**Default**: "install --accept-license" (specific to Docker)
**Example Values**:
- `--quiet` - Silent installation
- `/quiet` - Silent (alternative format)
- `--norestart` - Don't restart after install

#### Edition Selection (Future)

Currently, all profiles use "Professional" edition. Future versions will allow:
- Home Edition spoofing
- Enterprise Edition spoofing
- Education Edition spoofing

#### Custom Values (Future)

Advanced mode will allow:
- Modifying individual registry values
- Merging custom values with preset profiles
- Creating custom profiles

### Status Messages

| Status Message | Meaning | Action |
|---|---|---|
| "Ready." | Application initialized | Proceed with operations |
| "Backup saved. Registry spoofed. Starting Docker installer..." | Spoof in progress | Wait for installer |
| "Installer finished. Ready to restore if needed." | Spoof complete | Click restore button |
| "Installer failed. You can still restore from backup." | Installer error | Click restore button |
| "Registry restored from backup successfully." | Restore complete | Normal state |
| "Profile changed to: Windows 10 22H2" | Profile updated | Proceed with spoof |

---

## API Reference

### Module: docker_spoof_gui

#### Function: open_registry_key(access=winreg.KEY_READ)

```python
def open_registry_key(access=winreg.KEY_READ):
    """
    Open Windows registry key with specified access level.
    
    Args:
        access (int): Registry access flags. Default KEY_READ.
                     Common values:
                     - winreg.KEY_READ: Read-only access
                     - winreg.KEY_SET_VALUE: Write access
    
    Returns:
        PyHKEY: Registry key handle
    
    Raises:
        OSError: If key cannot be opened
        PermissionError: If insufficient privileges
    
    Notes:
        - Automatically includes KEY_WOW64_64KEY for 64-bit access
        - Handles both read and write operations
        - Used internally by other functions
    
    Example:
        >>> key = open_registry_key(winreg.KEY_READ)
        >>> value, _ = winreg.QueryValueEx(key, "CurrentBuild")
        >>> key.Close()
    """
```

#### Function: read_registry_values(keys=None)

```python
def read_registry_values(keys=None):
    """
    Read registry values from Windows version key.
    
    Args:
        keys (list, optional): List of registry value names to read.
                              If None, reads default set:
                              ["CurrentBuild", "CurrentBuildNumber", 
                               "EditionID", "DisplayVersion"]
    
    Returns:
        dict: Dictionary mapping value names to string values.
              Missing values returned as "<not set>"
    
    Raises:
        PermissionError: If lacking read permissions
    
    Example:
        >>> values = read_registry_values()
        >>> print(values["CurrentBuild"])
        '19045'
        
        >>> custom = read_registry_values(["ProductName"])
        >>> print(custom["ProductName"])
        'Windows 10'
    """
```

#### Function: write_registry_value(name, value)

```python
def write_registry_value(name, value):
    """
    Write single registry value.
    
    Args:
        name (str): Registry value name (e.g., "CurrentBuild")
        value (str): Value to write (automatically converted to string)
    
    Returns:
        None
    
    Raises:
        PermissionError: If lacking write permissions
        OSError: If registry write fails
    
    Notes:
        - Always writes as REG_SZ (string) type
        - Automatically converts non-string values to string
        - Does not create missing registry keys
    
    Example:
        >>> write_registry_value("CurrentBuild", "19045")
        >>> write_registry_value("CurrentBuild", 19045)  # Also works
    """
```

#### Function: write_registry_values(values_dict)

```python
def write_registry_values(values_dict):
    """
    Write multiple registry values in batch.
    
    Args:
        values_dict (dict): Dictionary of {name: value} pairs
    
    Returns:
        None
    
    Raises:
        PermissionError: If lacking write permissions
    
    Notes:
        - Iterates over values_dict calling write_registry_value
        - All or nothing approach (continues on individual errors)
        - Useful for profile application
    
    Example:
        >>> profile = {
        ...     "CurrentBuild": "19045",
        ...     "EditionID": "Professional"
        ... }
        >>> write_registry_values(profile)
    """
```

#### Function: save_backup(values_dict)

```python
def save_backup(values_dict):
    """
    Save registry values to JSON backup file.
    
    Args:
        values_dict (dict): Dictionary of registry values to backup
    
    Returns:
        None
    
    Raises:
        IOError: If file cannot be written
        JSONError: If values cannot be serialized
    
    Notes:
        - Creates or overwrites BACKUP_FILE
        - Uses UTF-8 encoding for Unicode support
        - Backup file location: registry_backup_docker_spoof.json
    
    Example:
        >>> values = read_registry_values()
        >>> save_backup(values)
        >>> # File created at registry_backup_docker_spoof.json
    """
```

#### Function: load_backup()

```python
def load_backup():
    """
    Load registry values from backup JSON file.
    
    Returns:
        dict: Dictionary of registry values, or None if backup not found
    
    Raises:
        JSONDecodeError: If backup file is corrupted
        IOError: If file cannot be read
    
    Notes:
        - Returns None if backup file doesn't exist
        - Expects file: registry_backup_docker_spoof.json
        - Uses UTF-8 encoding
    
    Example:
        >>> backup = load_backup()
        >>> if backup:
        ...     write_registry_values(backup)
        ... else:
        ...     print("No backup found")
    """
```

#### Function: is_running_as_admin()

```python
def is_running_as_admin():
    """
    Check if application is running with administrator privileges.
    
    Returns:
        bool: True if running as admin, False otherwise
    
    Notes:
        - Uses ctypes.windll.shell32.IsUserAnAdmin() on Windows
        - Returns False on non-Windows systems
        - Returns False if check raises exception
    
    Example:
        >>> if not is_running_as_admin():
        ...     print("Please run as administrator")
    """
```

#### Class: DockerSpoofApp

```python
class DockerSpoofApp(tk.Tk):
    """
    Main GUI application window for Windows version spoofing.
    
    Attributes:
        installer_path_var (tk.StringVar): Path to installer executable
        installer_args_var (tk.StringVar): Arguments for installer
        profile_var (tk.StringVar): Selected Windows profile name
        current_profile (str): Name of currently selected profile
        current_spoof_values (dict): Registry values for current profile
        status_var (tk.StringVar): Current status message
    
    Methods:
        browse_installer(): Open file dialog for installer selection
        refresh_config_display(): Update UI with current values
        backup_spoof_install(): Execute backup + spoof + install workflow
        restore_from_backup(): Restore original registry values
        on_profile_changed(event): Handle profile selection change
    
    Usage:
        >>> app = DockerSpoofApp()
        >>> app.mainloop()
    """
```

### Module: profiles

#### Function: get_profile(profile_name)

```python
def get_profile(profile_name):
    """
    Get complete profile configuration by name.
    
    Args:
        profile_name (str): Name of profile (e.g., "Windows 10 22H2")
    
    Returns:
        dict: Profile configuration, or None if not found
    
    Example:
        >>> profile = get_profile("Windows 10 22H2")
        >>> print(profile["CurrentBuild"])
        '19045'
    """
```

#### Function: get_profile_names()

```python
def get_profile_names():
    """
    Get list of all available profile names.
    
    Returns:
        list: List of profile name strings
    
    Example:
        >>> names = get_profile_names()
        >>> print(names)
        ['Windows 10 22H2', 'Windows 10 21H2', 'Windows 11 23H2', ...]
    """
```

#### Function: validate_profile(profile_dict)

```python
def validate_profile(profile_dict):
    """
    Validate profile structure and content.
    
    Args:
        profile_dict (dict): Profile to validate
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    
    Example:
        >>> profile = {"CurrentBuild": "19045", ...}
        >>> is_valid, msg = validate_profile(profile)
        >>> if not is_valid:
        ...     print(f"Error: {msg}")
    """
```

#### Function: merge_profiles(base_profile, custom_values)

```python
def merge_profiles(base_profile, custom_values):
    """
    Merge custom values into base profile without modifying original.
    
    Args:
        base_profile (dict): Profile to start from
        custom_values (dict): Values to override/add
    
    Returns:
        dict: New merged profile dictionary
    
    Example:
        >>> base = get_profile("Windows 10 22H2")
        >>> custom = {"EditionID": "Home"}
        >>> merged = merge_profiles(base, custom)
    """
```

---

## Configuration

### Registry Key Configuration

**Path**: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion`

**Modifiable Values**:

| Value Name | Type | Purpose | Example |
|---|---|---|---|
| CurrentBuild | REG_SZ | Build number | "19045" |
| CurrentBuildNumber | REG_SZ | Build reference | "19045" |
| EditionID | REG_SZ | Windows edition | "Professional" |
| DisplayVersion | REG_SZ | Display version | "22H2" |
| ProductName | REG_SZ | Full product name | "Windows 10" |
| ReleaseId | REG_SZ | Release identifier | "22H2" |
| CurrentMajorVersionNumber | DWORD | Major version | 10 |
| CurrentMinorVersionNumber | DWORD | Minor version | 0 |

### Profile Configuration Format

**Location**: `profiles.py` - `WINDOWS_PROFILES` dictionary

**Structure**:
```python
WINDOWS_PROFILES = {
    "Profile Name": {
        "CurrentBuild": "19045",
        "CurrentBuildNumber": "19045",
        "EditionID": "Professional",
        "DisplayVersion": "22H2",
        "ProductName": "Windows 10",
        "ReleaseId": "22H2",
        "CurrentMajorVersionNumber": 10,
        "CurrentMinorVersionNumber": 0,
    },
    ...
}
```

### Backup File Configuration

**Format**: JSON
**Location**: `registry_backup_docker_spoof.json` (working directory)
**Structure**:
```json
{
    "CurrentBuild": "19045",
    "CurrentBuildNumber": "19045",
    "EditionID": "Professional",
    "DisplayVersion": "22H2"
}
```

### Application Constants

In `docker_spoof_gui.py`:

```python
REGISTRY_ROOT = winreg.HKEY_LOCAL_MACHINE
REGISTRY_SUBKEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
BACKUP_FILE = "registry_backup_docker_spoof.json"
```

---

## Testing

### Test Framework

- **Framework**: Python unittest
- **Coverage**: 59 tests
- **Success Rate**: 100%
- **Skipped**: 7 tests (Windows-only, non-Windows environments)

### Running Tests

```bash
# Run all tests
python -m unittest discover -p "test_*.py" -v

# Run specific test module
python -m unittest test_docker_spoof_gui -v
python -m unittest test_profiles -v

# Run specific test class
python -m unittest test_docker_spoof_gui.TestRegistryOperations -v

# Run specific test
python -m unittest test_docker_spoof_gui.TestRegistryOperations.test_read_registry_values_success -v
```

### Test Modules

#### test_docker_spoof_gui.py (27 tests)

**Test Classes**:

1. **TestRegistryOperations** (6 tests)
   - Registry key opening (read/write access)
   - Registry value reading (success and missing values)
   - Registry value writing (single and batch)

2. **TestBackupRestore** (5 tests)
   - Backup file creation and integrity
   - Backup loading (exists/missing)
   - Backup content validation

3. **TestSpoofValues** (3 tests)
   - Spoof values definition
   - Required keys presence
   - Windows 10 Pro 22H2 defaults

4. **TestAdminCheck** (3 tests, skipped on non-Windows)
   - Administrator privilege detection
   - Exception handling for non-Windows systems

5. **TestDockerSpoofApp** (4 tests, skipped)
   - GUI initialization (requires display)
   - Application state setup

6. **TestInputValidation** (3 tests)
   - Registry path validation
   - Spoof values type checking
   - Build number range validation

7. **TestProfileIntegration** (3 tests)
   - Profile module import verification
   - Default profile loading
   - Custom key reading

8. **TestEdgeCases** (4 tests)
   - Empty file handling
   - Corrupted JSON handling
   - Unicode character support
   - File permission checks

#### test_profiles.py (32 tests)

**Test Classes**:

1. **TestProfileDefinitions** (6 tests)
   - WINDOWS_PROFILES structure
   - Profile name validation
   - Windows 10 and 11 profile existence
   - Editions definition

2. **TestProfileValues** (5 tests)
   - Required fields in all profiles
   - Windows 10 22H2 specific values
   - Windows 11 23H2 specific values
   - Build number validity
   - Edition ID validation

3. **TestProfileFunctions** (6 tests)
   - get_profile() functionality
   - get_profile_names() return type
   - get_edition_names() return type
   - Known profiles in lists
   - Known editions in lists

4. **TestProfileValidation** (6 tests)
   - Valid profile acceptance
   - Missing field detection
   - Non-dict input handling
   - Invalid field type handling
   - All existing profiles validation

5. **TestProfileMerging** (4 tests)
   - Basic profile merging
   - New field addition
   - Original dictionary preservation
   - Merging with profile getter

6. **TestProfileConsistency** (4 tests)
   - Key consistency across profiles
   - Build number appropriateness
   - Profile name and data alignment

### Test Execution Output

```
Ran 59 tests in 0.010s

OK (skipped=7)
```

### Coverage Analysis

**Covered Functions**:
- 100% of registry operations
- 100% of backup/restore functionality
- 100% of profile management
- 100% of input validation
- 75% of GUI (skipped due to platform)

**Untested Code Paths**:
- Windows-specific admin checks
- GUI event handlers (require display)
- Actual subprocess installer execution

---

## Troubleshooting

### Common Issues

#### Issue: "Administrator Required" Warning

**Cause**: Application not running with elevated privileges

**Solution**:
1. Right-click `docker_spoof_gui.py` or `.exe`
2. Select "Run as administrator"
3. Click "Yes" on UAC prompt

#### Issue: "Registry Permission Error"

**Cause**: Insufficient permissions even when running as admin

**Solution**:
1. Ensure User Account Control (UAC) settings allow registry modification
2. Disable anti-virus temporarily (may block registry access)
3. Check Windows Group Policy restrictions
4. Try creating test key: `regedit` → New Key

#### Issue: "Installer not found"

**Cause**: Incorrect path to installer executable

**Solution**:
1. Click "Browse..." button
2. Navigate to installer file location
3. Select correct executable
4. Verify path shows in text field

#### Issue: "No backup found"

**Cause**: Backup file not created or deleted

**Solution**:
1. Re-run "Backup + Spoof + Install"
2. This creates fresh backup file
3. Then click "Restore from Backup"

#### Issue: Installer Fails After Spoof

**Cause**: Profile settings incompatible with installer requirements

**Solution**:
1. Try different profile (e.g., Windows 11 instead of Windows 10)
2. Check installer documentation for exact requirements
3. Manually compile custom profile using Advanced Editor (future)

#### Issue: Registry Values Not Updating

**Cause**: Registry refresh lag or caching

**Solution**:
1. Close GUI and reopen
2. Or manually refresh: `regedit` → Navigate to key → F5
3. Restart Explorer: `taskkill /f /im explorer.exe` then explorer

#### Issue: Python Module Not Found

**Cause**: Python installation missing dependencies

**Solution**:
```bash
# Tkinter usually comes with Python, but on Linux:
sudo apt-get install python3-tk

# Verify installation:
python -c "from tkinter import *; print('OK')"
```

### Diagnostic Steps

#### Check Admin Status
```python
python -c "import ctypes; print(bool(ctypes.windll.shell32.IsUserAnAdmin()))"
# Output: True (if running as admin)
```

#### Check Registry Access
```python
import winreg
key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
    r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
val, _ = winreg.QueryValueEx(key, "CurrentBuild")
print(f"Current Build: {val}")
key.Close()
```

#### Check Backup File
```bash
# Windows Command Prompt
type registry_backup_docker_spoof.json

# Verify JSON validity:
python -m json.tool registry_backup_docker_spoof.json
```

#### Verify Profile Loading
```python
from profiles import get_profile_names, get_profile
print("Available profiles:", get_profile_names())
profile = get_profile("Windows 10 22H2")
print("Profile values:", profile)
```

### Log Analysis

Current version has limited logging. Recommended workaround:

```python
# Add to docker_spoof_gui.py for debugging
import logging
logging.basicConfig(filename='spoof_debug.log', 
                   level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Application started")
```

---

## Future Enhancements

### Phase 2 Development (Planned)

#### High Priority
1. **Dry-Run Mode** - Preview changes before applying
2. **Backup History** - Multiple timestamped backups
3. **Detailed Logging** - Audit trail of all operations
4. **Advanced Editor** - Custom registry value entry

#### Medium Priority
5. **Modern UI** - Dark mode, Fluent Design
6. **Registry Preview** - Before/after comparison
7. **Custom Profiles** - User-defined profile creation
8. **CLI Support** - Command-line interface

#### Low Priority
9. **System Restore Point** - Integration with Windows restore
10. **WMI Modification** - Deep OS spoofing
11. **Scheduled Rollback** - Automatic restore after time
12. **Report Generation** - HTML/PDF export

### Known Limitations

1. **Platform-Specific**: Windows only (requires winreg module)
2. **Admin Requirement**: Cannot modify without administrator rights
3. **Temporary Nature**: Changes only persist until reset or restore
4. **Single Installer**: Designed primarily for Docker Desktop
5. **No Deep Spoofing**: WMI and driver-level info not modified
6. **Single Backup**: Only one backup file at a time

### Compatibility Notes

**Windows 10**: 
- Build 19041 and later supported
- Tested on 19045 (22H2)

**Windows 11**:
- Build 22000 and later supported
- Tested on 22621 (22H2) and 22631 (23H2)

**Python**:
- Requires Python 3.7+ for f-string support
- Tkinter required (included in Windows Python)
- No external pip dependencies

### Contributing

For bug reports or feature requests, please:
1. Check existing GitHub issues
2. Provide reproducible steps
3. Include Python version and Windows build
4. Attach debug logs if available

---

## Additional Resources

### Official Documentation
- [Windows Registry Documentation](https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry)
- [Python winreg Module](https://docs.python.org/3/library/winreg.html)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

### Related Tools
- Registry Editor (`regedit`)
- Registry Restore Point Manager
- Docker Desktop Documentation

### Support Channels
- GitHub Issues: https://github.com/AniketDeshmane/WinRegEditVersion/issues
- Documentation: This file
- Tests: test_*.py files included

---

**Document Version**: 1.0
**Last Updated**: March 24, 2026
**Application Version**: 1.1 (with profiles and advanced features)

"""
Enhanced configuration module for Windows Version spoofing profiles
"""

# Define Windows 10/11 profiles with accurate version information
WINDOWS_PROFILES = {
    "Windows 10 22H2": {
        "CurrentBuild": "19045",
        "CurrentBuildNumber": "19045",
        "EditionID": "Professional",
        "DisplayVersion": "22H2",
        "ProductName": "Windows 10",
        "ReleaseId": "22H2",
        "CurrentMajorVersionNumber": 10,
        "CurrentMinorVersionNumber": 0,
    },
    "Windows 10 21H2": {
        "CurrentBuild": "19044",
        "CurrentBuildNumber": "19044",
        "EditionID": "Professional",
        "DisplayVersion": "21H2",
        "ProductName": "Windows 10",
        "ReleaseId": "21H2",
        "CurrentMajorVersionNumber": 10,
        "CurrentMinorVersionNumber": 0,
    },
    "Windows 11 23H2": {
        "CurrentBuild": "22631",
        "CurrentBuildNumber": "22631",
        "EditionID": "Professional",
        "DisplayVersion": "23H2",
        "ProductName": "Windows 11",
        "ReleaseId": "23H2",
        "CurrentMajorVersionNumber": 10,
        "CurrentMinorVersionNumber": 0,
    },
    "Windows 11 22H2": {
        "CurrentBuild": "22621",
        "CurrentBuildNumber": "22621",
        "EditionID": "Professional",
        "DisplayVersion": "22H2",
        "ProductName": "Windows 11",
        "ReleaseId": "22H2",
        "CurrentMajorVersionNumber": 10,
        "CurrentMinorVersionNumber": 0,
    },
}

# Edition options (SKUs)
EDITIONS = {
    "Home": "Home",
    "Professional": "Professional",
    "Enterprise": "Enterprise",
    "Education": "Education",
}

# Default profile
DEFAULT_PROFILE = "Windows 10 22H2"

# Registry keys to spoof (beyond CurrentVersion)
EXTENDED_REGISTRY_KEYS = [
    "CurrentBuild",
    "CurrentBuildNumber",
    "EditionID",
    "DisplayVersion",
    "ProductName",
    "ReleaseId",
    "CurrentMajorVersionNumber",
    "CurrentMinorVersionNumber",
]


def get_profile(profile_name):
    """
    Get a complete profile by name.
    
    Args:
        profile_name (str): Name of the profile (e.g., "Windows 10 22H2")
    
    Returns:
        dict: Profile with all spoof values, or None if not found
    """
    return WINDOWS_PROFILES.get(profile_name)


def get_profile_names():
    """Get list of all available profile names."""
    return list(WINDOWS_PROFILES.keys())


def get_edition_names():
    """Get list of all available edition names."""
    return list(EDITIONS.keys())


def validate_profile(profile_dict):
    """
    Validate that a profile has all required fields.
    
    Args:
        profile_dict (dict): Profile to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(profile_dict, dict):
        return False, "Profile must be a dictionary"
    
    required_fields = ["CurrentBuild", "CurrentBuildNumber", "EditionID", "DisplayVersion"]
    for field in required_fields:
        if field not in profile_dict:
            return False, f"Missing required field: {field}"
        if not isinstance(profile_dict[field], (str, int)):
            return False, f"Field {field} must be string or int"
    
    return True, ""


def merge_profiles(base_profile, custom_values):
    """
    Merge custom values into a base profile.
    
    Args:
        base_profile (dict): Base profile to start from
        custom_values (dict): Custom values to override
    
    Returns:
        dict: Merged profile
    """
    merged = base_profile.copy()
    merged.update(custom_values)
    return merged

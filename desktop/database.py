"""
Dummy database module for desktop game
Desktop game uses API client instead of direct database access
"""

def check_login(username, password):
    """
    Dummy login function
    Desktop game should use API client for authentication
    """
    # For now, allow any login (offline mode)
    # In production, this should call API
    return True if username and password else False

def register_user(username, password):
    """
    Dummy register function
    Desktop game should use API client for registration
    """
    # For now, allow any registration (offline mode)
    return True if username and password else False

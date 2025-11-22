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

def create_user(username, password):
    """
    Alias for register_user
    """
    return register_user(username, password)

def save_score(username, score):
    """
    Dummy save_score function
    Desktop game handles score saving in main.py via LocalStorage
    """
    return True

def get_best_score(username):
    """
    Dummy get_best_score function
    """
    return 0

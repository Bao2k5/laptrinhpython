"""
Dummy database module for desktop game
Desktop game uses API client instead of direct database access
"""

def check_login(username, password):
    """
    Check login and auto-create user if not exists
    """
    if not username or not password:
        return False
    
    try:
        from api_client import login_user, register_user
        
        # Try to login first
        if login_user(username, password):
            return True
        
        # If login fails, try to register (auto-create account)
        if register_user(username, password):
            # After successful registration, login again
            return login_user(username, password)
        
        return False
    except Exception as e:
        # Offline mode: allow login without server
        print(f"Offline mode: {e}")
        return True

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

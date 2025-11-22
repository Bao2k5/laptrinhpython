import json
import os
import base64
from typing import List, Dict, Optional
from datetime import datetime

class LocalStorage:
    """Quản lý lưu trữ điểm local khi offline"""
    
    def __init__(self, filename: str = "game_data.json"):
        self.filename = filename
        self.default_data = {
            "username": "Guest",
            "high_score": 0,
            "total_games": 0,
            "coins": 0,
            "current_skin": "yellow",
            "inventory": ["yellow"],
            "pending_sync": [],
            "saved_accounts": [],
            "settings": {
                "sound": True,
                "music": True
            }
        }
        self.data = self.load()
    
    def load(self) -> Dict:
        """Load dữ liệu từ file JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with default to ensure all keys exist
                    for k, v in self.default_data.items():
                        if k not in loaded:
                            loaded[k] = v
                    return loaded
            except:
                return self.default_data.copy()
        return self.default_data.copy()
    
    def save(self):
        """Lưu dữ liệu vào file JSON"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    # --- GETTERS ---
    def get_username(self) -> str:
        return self.data.get("username", "Guest")
    
    def get_high_score(self) -> int:
        return self.data.get("high_score", 0)
    
    def get_coins(self) -> int:
        return self.data.get("coins", 0)
    
    def get_current_skin(self) -> str:
        return self.data.get("current_skin", "yellow")
    
    def get_inventory(self) -> List[str]:
        return self.data.get("inventory", ["yellow"])
    
    def get_pending_sync(self) -> List[Dict]:
        return self.data.get("pending_sync", [])
    
    def get_stats(self) -> Dict:
        return {
            "high_score": self.get_high_score(),
            "total_games": self.data.get("total_games", 0),
            "coins": self.get_coins(),
            "pending_sync": len(self.get_pending_sync())
        }

    # --- SETTERS ---
    def set_username(self, username: str):
        self.data["username"] = username
        self.save()
    
    def update_high_score(self, score: int) -> bool:
        if score > self.data["high_score"]:
            self.data["high_score"] = score
            self.save()
            return True
        return False
    
    def increment_games(self):
        self.data["total_games"] = self.data.get("total_games", 0) + 1
        self.save()
    
    def add_coins(self, amount: int):
        self.data["coins"] = self.data.get("coins", 0) + amount
        self.save()
        return self.data["coins"]
    
    def spend_coins(self, amount: int) -> bool:
        if self.data.get("coins", 0) >= amount:
            self.data["coins"] -= amount
            self.save()
            return True
        return False
    
    def unlock_skin(self, skin_name: str):
        if skin_name not in self.data.get("inventory", []):
            self.data["inventory"].append(skin_name)
            self.save()
    
    def set_skin(self, skin_name: str) -> bool:
        if skin_name in self.data.get("inventory", []):
            self.data["current_skin"] = skin_name
            self.save()
            return True
        return False

    def add_pending_sync(self, username: str, score: int):
        self.data["pending_sync"].append({
            "username": username,
            "score": score,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def remove_synced_score(self, index: int):
        if 0 <= index < len(self.data["pending_sync"]):
            self.data["pending_sync"].pop(index)
            self.save()
    
    # --- CREDENTIAL MANAGEMENT ---
    def _encode_password(self, password: str) -> str:
        """Encode password using base64"""
        return base64.b64encode(password.encode()).decode()
    
    def _decode_password(self, encoded: str) -> str:
        """Decode password from base64"""
        try:
            return base64.b64decode(encoded.encode()).decode()
        except:
            return ""
    
    def save_credentials(self, username: str, password: str):
        """Save login credentials (password is base64 encoded)"""
        saved_accounts = self.data.get("saved_accounts", [])
        
        # Check if account already exists
        for account in saved_accounts:
            if account["username"] == username:
                # Update password
                account["password_encoded"] = self._encode_password(password)
                self.save()
                return
        
        # Add new account
        saved_accounts.append({
            "username": username,
            "password_encoded": self._encode_password(password)
        })
        self.data["saved_accounts"] = saved_accounts
        self.save()
    
    def get_saved_accounts(self) -> List[str]:
        """Get list of saved usernames"""
        saved_accounts = self.data.get("saved_accounts", [])
        return [acc["username"] for acc in saved_accounts]
    
    def get_credentials(self, username: str) -> Optional[Dict[str, str]]:
        """Get credentials for a saved account"""
        saved_accounts = self.data.get("saved_accounts", [])
        for account in saved_accounts:
            if account["username"] == username:
                return {
                    "username": username,
                    "password": self._decode_password(account["password_encoded"])
                }
        return None
    
    def remove_credentials(self, username: str):
        """Remove saved credentials for an account"""
        saved_accounts = self.data.get("saved_accounts", [])
        self.data["saved_accounts"] = [acc for acc in saved_accounts if acc["username"] != username]
        self.save()

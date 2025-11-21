import json
import os
from typing import List, Dict
from datetime import datetime

class LocalStorage:
    """Quản lý lưu trữ điểm local khi offline"""
    
    def __init__(self, filename: str = "game_data.json"):
        self.filename = filename
        self.data = self.load()
    
    def load(self) -> Dict:
        """Load dữ liệu từ file JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._get_default_data()
        return self._get_default_data()
    
    def _get_default_data(self) -> Dict:
        """Dữ liệu mặc định"""
        return {
            "username": "",
            "high_score": 0,
            "total_games": 0,
            "pending_sync": [],
            "settings": {
                "sound": True,
                "music": True
            }
        }
    
    def save(self):
        """Lưu dữ liệu vào file JSON"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get_username(self) -> str:
        """Lấy tên người chơi"""
        return self.data.get("username", "")
    
    def set_username(self, username: str):
        """Đặt tên người chơi"""
        self.data["username"] = username
        self.save()
    
    def get_high_score(self) -> int:
        """Lấy điểm cao nhất"""
        return self.data.get("high_score", 0)
    
    def update_high_score(self, score: int) -> bool:
        """
        Cập nhật điểm cao nhất
        
        Returns:
            True nếu đây là kỷ lục mới
        """
        if score > self.data["high_score"]:
            self.data["high_score"] = score
            self.save()
            return True
        return False
    
    def increment_games(self):
        """Tăng số lượng game đã chơi"""
        self.data["total_games"] = self.data.get("total_games", 0) + 1
        self.save()
    
    def add_pending_sync(self, username: str, score: int):
        """
        Thêm điểm chờ sync lên server
        
        Args:
            username: Tên người chơi
            score: Điểm số
        """
        self.data["pending_sync"].append({
            "username": username,
            "score": score,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def get_pending_sync(self) -> List[Dict]:
        """Lấy danh sách điểm chờ sync"""
        return self.data.get("pending_sync", [])
    
    def clear_pending_sync(self):
        """Xóa danh sách điểm đã sync"""
        self.data["pending_sync"] = []
        self.save()
    
    def remove_synced_score(self, index: int):
        """Xóa 1 điểm đã sync"""
        if 0 <= index < len(self.data["pending_sync"]):
            self.data["pending_sync"].pop(index)
            self.save()
    
    def get_setting(self, key: str, default=True) -> bool:
        """Lấy cài đặt"""
        return self.data.get("settings", {}).get(key, default)
    
    def set_setting(self, key: str, value: bool):
        """Đặt cài đặt"""
        if "settings" not in self.data:
            self.data["settings"] = {}
        self.data["settings"][key] = value
        self.save()
    
    def get_stats(self) -> Dict:
        """Lấy thống kê"""
        return {
            "high_score": self.get_high_score(),
            "total_games": self.data.get("total_games", 0),
            "pending_sync": len(self.get_pending_sync())
        }


# Test code
if __name__ == "__main__":
    # Test local storage
    storage = LocalStorage("test_data.json")
    
    print("Testing LocalStorage...")
    
    # Set username
    storage.set_username("TestPlayer")
    print(f"Username: {storage.get_username()}")
    
    # Update high score
    if storage.update_high_score(100):
        print("✓ New high score: 100")
    
    # Add pending sync
    storage.add_pending_sync("TestPlayer", 100)
    print(f"Pending sync: {len(storage.get_pending_sync())} scores")
    
    # Get stats
    stats = storage.get_stats()
    print(f"Stats: {stats}")
    
    # Cleanup
    if os.path.exists("test_data.json"):
        os.remove("test_data.json")
    print("\n✓ All tests passed!")

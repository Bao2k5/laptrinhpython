import requests
import json
from typing import List, Dict, Optional

class APIClient:
    """Client để kết nối với API server và sync điểm"""
    
    def __init__(self, base_url: str = "https://flappybird-duatop.onrender.com"):
        self.base_url = base_url
        self.is_online = False
        self.timeout = 5  # seconds
    
    def check_connection(self) -> bool:
        """Kiểm tra kết nối internet và server"""
        try:
            response = requests.get(
                f"{self.base_url}/api/scores",
                timeout=2
            )
            self.is_online = response.status_code == 200
        except:
            self.is_online = False
        return self.is_online
    
    def submit_score(self, username: str, score: int, device_id: str = None) -> bool:
        """
        Gửi điểm lên server
        
        Args:
            username: Tên người chơi
            score: Điểm số
            device_id: ID thiết bị (optional)
            
        Returns:
            True nếu gửi thành công, False nếu thất bại
        """
        if not self.check_connection():
            return False
        
        try:
            payload = {"username": username, "score": score}
            if device_id:
                payload["device_id"] = device_id
                
            response = requests.post(
                f"{self.base_url}/api/score",
                json=payload,
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error submitting score: {e}")
            return False
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """
        Lấy bảng xếp hạng từ server
        
        Args:
            limit: Số lượng người chơi top (mặc định 10)
            
        Returns:
            List các dict chứa thông tin người chơi và điểm
            Format: [{"username": "...", "score": 123}, ...]
        """
        if not self.check_connection():
            return []
        
        try:
            response = requests.get(
                f"{self.base_url}/api/scores",
                params={"limit": limit},
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []
    
    def login(self, username: str, password: str) -> bool:
        """
        Đăng nhập (nếu cần)
        
        Args:
            username: Tên đăng nhập
            password: Mật khẩu
            
        Returns:
            True nếu đăng nhập thành công
        """
        if not self.check_connection():
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/api/login",
                json={"username": username, "password": password},
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error logging in: {e}")
            return False
    
    def register(self, username: str, password: str) -> bool:
        """
        Đăng ký tài khoản mới
        
        Args:
            username: Tên đăng nhập
            password: Mật khẩu
            
        Returns:
            True nếu đăng ký thành công
        """
        if not self.check_connection():
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/api/register",
                json={"username": username, "password": password},
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error registering: {e}")
            return False


# Test code
if __name__ == "__main__":
    # Test API client
    client = APIClient()
    
    print("Testing connection...")
    if client.check_connection():
        print("✓ Connected to server")
        
        # Test get leaderboard
        print("\nGetting leaderboard...")
        leaderboard = client.get_leaderboard(5)
        for i, player in enumerate(leaderboard, 1):
            print(f"{i}. {player['username']}: {player['score']}")
    else:
        print("✗ Cannot connect to server (offline mode)")

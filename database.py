"""
Database Manager cho Flappy Bird AI Game
Lưu trữ: High scores, AI statistics, Game history
"""
from pymongo import MongoClient
from datetime import datetime
import os

class FlappyBirdDB:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """
        Khởi tạo kết nối MongoDB

        Args:
            connection_string: MongoDB URI
                - Local: "mongodb://localhost:27017/"
                - Atlas (Cloud): "mongodb+srv://username:password@cluster.mongodb.net/"
        """
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client['flappybird_ai']

            # Collections
            self.high_scores = self.db['high_scores']
            self.ai_stats = self.db['ai_statistics']
            self.game_history = self.db['game_history']

            # Tạo indexes để tìm kiếm nhanh
            self.high_scores.create_index([("score", -1)])  # Sắp xếp theo điểm giảm dần
            self.ai_stats.create_index([("generation", 1)])
            self.game_history.create_index([("timestamp", -1)])

            print("✅ Kết nối MongoDB thành công!")
            print(f"📊 Database: {self.db.name}")
            print(f"📁 Collections: high_scores, ai_statistics, game_history")

        except Exception as e:
            print(f"❌ Lỗi kết nối MongoDB: {e}")
            print("\n💡 Hướng dẫn:")
            print("   1. Cài MongoDB: https://www.mongodb.com/try/download/community")
            print("   2. Hoặc dùng MongoDB Atlas (free): https://www.mongodb.com/cloud/atlas")
            print("   3. Hoặc chạy MongoDB trong Docker:")
            print("      docker run -d -p 27017:27017 mongo")
            self.client = None

    # ==================== HIGH SCORES ====================

    def save_high_score(self, player_name, score, level_reached, generation=None):
        """
        Lưu điểm cao

        Args:
            player_name: Tên người chơi hoặc "AI"
            score: Điểm số đạt được
            level_reached: Level cao nhất đạt được (1-4)
            generation: Thế hệ AI (nếu là AI chơi)
        """
        if not self.client:
            return None

        record = {
            "player_name": player_name,
            "score": score,
            "level_reached": level_reached,
            "generation": generation,
            "timestamp": datetime.now(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        result = self.high_scores.insert_one(record)
        print(f"✅ Đã lưu high score: {player_name} - {score} điểm")
        return result.inserted_id

    def get_top_scores(self, limit=10):
        """Lấy top điểm cao nhất"""
        if not self.client:
            return []

        scores = self.high_scores.find().sort("score", -1).limit(limit)
        return list(scores)

    def get_player_best_score(self, player_name):
        """Lấy điểm cao nhất của một người chơi"""
        if not self.client:
            return None

        score = self.high_scores.find_one(
            {"player_name": player_name},
            sort=[("score", -1)]
        )
        return score

    # ==================== AI STATISTICS ====================

    def save_ai_generation(self, generation, best_score, avg_fitness, num_birds, level_reached):
        """
        Lưu thống kê mỗi thế hệ AI

        Args:
            generation: Số thế hệ
            best_score: Điểm cao nhất của thế hệ
            avg_fitness: Fitness trung bình
            num_birds: Số con chim trong thế hệ
            level_reached: Level cao nhất đạt được
        """
        if not self.client:
            return None

        record = {
            "generation": generation,
            "best_score": best_score,
            "average_fitness": avg_fitness,
            "num_birds": num_birds,
            "level_reached": level_reached,
            "timestamp": datetime.now()
        }

        result = self.ai_stats.insert_one(record)
        return result.inserted_id

    def get_ai_progress(self):
        """Lấy tiến độ học của AI qua các thế hệ"""
        if not self.client:
            return []

        stats = self.ai_stats.find().sort("generation", 1)
        return list(stats)

    def get_best_generation(self):
        """Lấy thế hệ AI tốt nhất"""
        if not self.client:
            return None

        best = self.ai_stats.find_one(sort=[("best_score", -1)])
        return best

    # ==================== GAME HISTORY ====================

    def save_game_session(self, session_data):
        """
        Lưu một phiên chơi game

        Args:
            session_data: Dict chứa thông tin phiên chơi
                - start_time: Thời gian bắt đầu
                - end_time: Thời gian kết thúc
                - total_generations: Tổng số thế hệ
                - highest_score: Điểm cao nhất
                - total_birds: Tổng số chim đã chơi
        """
        if not self.client:
            return None

        session_data['timestamp'] = datetime.now()
        result = self.game_history.insert_one(session_data)
        print(f"✅ Đã lưu game session")
        return result.inserted_id

    def get_recent_sessions(self, limit=10):
        """Lấy các phiên chơi gần đây"""
        if not self.client:
            return []

        sessions = self.game_history.find().sort("timestamp", -1).limit(limit)
        return list(sessions)

    # ==================== STATISTICS ====================

    def get_total_stats(self):
        """Lấy thống kê tổng quan"""
        if not self.client:
            return None

        stats = {
            "total_games": self.game_history.count_documents({}),
            "total_high_scores": self.high_scores.count_documents({}),
            "total_generations": self.ai_stats.count_documents({}),
            "highest_score_ever": None,
            "best_ai_generation": None
        }

        # Điểm cao nhất mọi thời đại
        top_score = self.high_scores.find_one(sort=[("score", -1)])
        if top_score:
            stats["highest_score_ever"] = {
                "score": top_score.get("score"),
                "player": top_score.get("player_name"),
                "date": top_score.get("date")
            }

        # Thế hệ AI tốt nhất
        best_gen = self.get_best_generation()
        if best_gen:
            stats["best_ai_generation"] = {
                "generation": best_gen.get("generation"),
                "score": best_gen.get("best_score")
            }

        return stats

    def clear_all_data(self):
        """Xóa toàn bộ dữ liệu (cẩn thận!)"""
        if not self.client:
            return

        self.high_scores.delete_many({})
        self.ai_stats.delete_many({})
        self.game_history.delete_many({})
        print("⚠️  Đã xóa toàn bộ dữ liệu!")

    def close(self):
        """Đóng kết nối"""
        if self.client:
            self.client.close()
            print("👋 Đã đóng kết nối MongoDB")


# ==================== DEMO USAGE ====================

if __name__ == "__main__":
    print("🎮 DEMO: Flappy Bird Database Manager")
    print("=" * 60)

    # Khởi tạo database
    db = FlappyBirdDB()

    if db.client:
        print("\n1️⃣ Lưu điểm cao:")
        db.save_high_score("Player1", 45, 2)
        db.save_high_score("AI", 127, 3, generation=15)
        db.save_high_score("Player2", 78, 2)

        print("\n2️⃣ Lấy top 5 điểm cao:")
        top_scores = db.get_top_scores(5)
        for i, score in enumerate(top_scores, 1):
            print(f"   {i}. {score['player_name']}: {score['score']} điểm (Level {score['level_reached']})")

        print("\n3️⃣ Lưu thống kê AI:")
        db.save_ai_generation(1, 25, 12.5, 15, 1)
        db.save_ai_generation(2, 58, 28.3, 15, 2)
        db.save_ai_generation(3, 127, 65.8, 15, 3)

        print("\n4️⃣ Lấy thế hệ AI tốt nhất:")
        best_gen = db.get_best_generation()
        if best_gen:
            print(f"   Gen {best_gen['generation']}: {best_gen['best_score']} điểm")

        print("\n5️⃣ Thống kê tổng quan:")
        stats = db.get_total_stats()
        print(f"   📊 Tổng số game: {stats['total_games']}")
        print(f"   🏆 Điểm cao nhất: {stats.get('highest_score_ever', {}).get('score', 0)}")

        print("\n6️⃣ Lưu game session:")
        session = {
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "total_generations": 50,
            "highest_score": 127,
            "total_birds": 750
        }
        db.save_game_session(session)

        # Đóng kết nối
        db.close()

    print("\n" + "=" * 60)
    print("✅ DEMO hoàn tất!")


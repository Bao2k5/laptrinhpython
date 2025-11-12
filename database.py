"""
Database Manager cho Flappy Bird AI Game
Luu tru: High scores, AI statistics, Game history
"""
from pymongo import MongoClient
from datetime import datetime
import os

class FlappyBirdDB:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """
        Khoi tao ket noi MongoDB

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

            # Tao indexes de tim kiem nhanh
            self.high_scores.create_index([("score", -1)])  # Sap xep theo diem giam dan
            self.ai_stats.create_index([("generation", 1)])
            self.game_history.create_index([("timestamp", -1)])

            print("Ket noi MongoDB thanh cong!")
            print(f"Database: {self.db.name}")
            print(f"Collections: high_scores, ai_statistics, game_history")

        except Exception as e:
            print(f"Loi ket noi MongoDB: {e}")
            print("\nHuong dan:")
            print("   1. Cai MongoDB: https://www.mongodb.com/try/download/community")
            print("   2. Hoac dung MongoDB Atlas (free): https://www.mongodb.com/cloud/atlas")
            print("   3. Hoac chay MongoDB trong Docker:")
            print("      docker run -d -p 27017:27017 mongo")
            self.client = None

    # ==================== HIGH SCORES ====================

    def save_high_score(self, player_name, score, level_reached, generation=None):
        """
        Luu diem cao

        Args:
            player_name: Ten nguoi choi hoac "AI"
            score: Diem so dat duoc
            level_reached: Level cao nhat dat duoc (1-4)
            generation: The he AI (neu la AI choi)
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
        print(f"Da luu high score: {player_name} - {score} diem")
        return result.inserted_id

    def get_top_scores(self, limit=10):
        """Lay top diem cao nhat"""
        if not self.client:
            return []

        scores = self.high_scores.find().sort("score", -1).limit(limit)
        return list(scores)

    def get_player_best_score(self, player_name):
        """Lay diem cao nhat cua mot nguoi choi"""
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
        Luu thong ke moi the he AI

        Args:
            generation: So the he
            best_score: Diem cao nhat cua the he
            avg_fitness: Fitness trung binh
            num_birds: So con chim trong the he
            level_reached: Level cao nhat dat duoc
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
        """Lay tien do hoc cua AI qua cac the he"""
        if not self.client:
            return []

        stats = self.ai_stats.find().sort("generation", 1)
        return list(stats)

    def get_best_generation(self):
        """Lay the he AI tot nhat"""
        if not self.client:
            return None

        best = self.ai_stats.find_one(sort=[("best_score", -1)])
        return best

    # ==================== GAME HISTORY ====================

    def save_game_session(self, session_data):
        """
        Luu mot phien choi game

        Args:
            session_data: Dict chua thong tin phien choi
                - start_time: Thoi gian bat dau
                - end_time: Thoi gian ket thuc
                - total_generations: Tong so the he
                - highest_score: Diem cao nhat
                - total_birds: Tong so chim da choi
        """
        if not self.client:
            return None

        session_data['timestamp'] = datetime.now()
        result = self.game_history.insert_one(session_data)
        print(f"Da luu game session")
        return result.inserted_id

    def get_recent_sessions(self, limit=10):
        """Lay cac phien choi gan day"""
        if not self.client:
            return []

        sessions = self.game_history.find().sort("timestamp", -1).limit(limit)
        return list(sessions)

    # ==================== STATISTICS ====================

    def get_total_stats(self):
        """Lay thong ke tong quan"""
        if not self.client:
            return None

        stats = {
            "total_games": self.game_history.count_documents({}),
            "total_high_scores": self.high_scores.count_documents({}),
            "total_generations": self.ai_stats.count_documents({}),
            "highest_score_ever": None,
            "best_ai_generation": None
        }

        # Diem cao nhat moi thoi dai
        top_score = self.high_scores.find_one(sort=[("score", -1)])
        if top_score:
            stats["highest_score_ever"] = {
                "score": top_score.get("score"),
                "player": top_score.get("player_name"),
                "date": top_score.get("date")
            }

        # The he AI tot nhat
        best_gen = self.get_best_generation()
        if best_gen:
            stats["best_ai_generation"] = {
                "generation": best_gen.get("generation"),
                "score": best_gen.get("best_score")
            }

        return stats

    def clear_all_data(self):
        """Xoa toan bo du lieu (can than!)"""
        if not self.client:
            return

        self.high_scores.delete_many({})
        self.ai_stats.delete_many({})
        self.game_history.delete_many({})
        print("Da xoa toan bo du lieu!")

    def close(self):
        """Dong ket noi"""
        if self.client:
            self.client.close()
            print("Da dong ket noi MongoDB")


# ==================== DEMO USAGE ====================

if __name__ == "__main__":
    print("DEMO: Flappy Bird Database Manager")
    print("=" * 60)

    # Khoi tao database
    db = FlappyBirdDB()

    if db.client:
        print("\n1. Luu diem cao:")
        db.save_high_score("Player1", 45, 2)
        db.save_high_score("AI", 127, 3, generation=15)
        db.save_high_score("Player2", 78, 2)

        print("\n2. Lay top 5 diem cao:")
        top_scores = db.get_top_scores(5)
        for i, score in enumerate(top_scores, 1):
            print(f"   {i}. {score['player_name']}: {score['score']} diem (Level {score['level_reached']})")

        print("\n3. Luu thong ke AI:")
        db.save_ai_generation(1, 25, 12.5, 15, 1)
        db.save_ai_generation(2, 58, 28.3, 15, 2)
        db.save_ai_generation(3, 127, 65.8, 15, 3)

        print("\n4. Lay the he AI tot nhat:")
        best_gen = db.get_best_generation()
        if best_gen:
            print(f"   Gen {best_gen['generation']}: {best_gen['best_score']} diem")

        print("\n5. Thong ke tong quan:")
        stats = db.get_total_stats()
        print(f"   Tong so game: {stats['total_games']}")
        print(f"   Diem cao nhat: {stats.get('highest_score_ever', {}).get('score', 0)}")

        print("\n6. Luu game session:")
        session = {
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "total_generations": 50,
            "highest_score": 127,
            "total_birds": 750
        }
        db.save_game_session(session)

        # Dong ket noi
        db.close()

    print("\n" + "=" * 60)
    print("DEMO hoan tat!")

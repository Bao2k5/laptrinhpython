"""
Settings Manager cho Flappy Bird
Quan ly: Volume, Graphics, FPS, Controls
"""

import json
import os

class Settings:
    """Class quan ly tat ca cai dat game"""

    CONFIG_FILE = "game_settings.json"

    # Default settings
    DEFAULT_SETTINGS = {
        "audio": {
            "master_volume": 0.7,
            "music_volume": 0.5,
            "sfx_volume": 0.8,
            "music_enabled": True,
            "sfx_enabled": True
        },
        "graphics": {
            "quality": "High",  # Low, Medium, High
            "fps": 60,
            "vsync": True,
            "fullscreen": False,
            "show_fps": False
        },
        "gameplay": {
            "difficulty": "Normal",  # Easy, Normal, Hard
            "show_hitboxes": False,
            "particles_enabled": True,
            "screen_shake": True
        },
        "controls": {
            "jump_key": "space",  # space, up, w
            "pause_key": "escape",
            "mouse_control": False
        },
        "player": {
            "name": "Player",
            "selected_bird": "blue"  # blue, red, yellow, orange, pink
        }
    }

    def __init__(self):
        """Khoi tao settings"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        """Load settings tu file"""
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge voi default (de co cac setting moi)
                    self._merge_settings(loaded)
                print(f"Settings loaded from {self.CONFIG_FILE}")
            else:
                print("No settings file found, using defaults")
                self.save()  # Tao file moi
        except Exception as e:
            print(f"Error loading settings: {e}")
            print("Using default settings")

    def save(self):
        """Luu settings vao file"""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            print(f"Settings saved to {self.CONFIG_FILE}")
        except Exception as e:
            print(f"Error saving settings: {e}")

    def _merge_settings(self, loaded):
        """Merge loaded settings voi default"""
        for category in self.DEFAULT_SETTINGS:
            if category in loaded:
                self.settings[category].update(loaded[category])

    def reset_to_default(self):
        """Reset ve cai dat mac dinh"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()
        print("Settings reset to default")

    # ==================== AUDIO SETTINGS ====================

    def get_master_volume(self):
        return self.settings["audio"]["master_volume"]

    def set_master_volume(self, volume):
        self.settings["audio"]["master_volume"] = max(0.0, min(1.0, volume))
        self.save()

    def get_music_volume(self):
        return self.settings["audio"]["music_volume"]

    def set_music_volume(self, volume):
        self.settings["audio"]["music_volume"] = max(0.0, min(1.0, volume))
        self.save()

    def get_sfx_volume(self):
        return self.settings["audio"]["sfx_volume"]

    def set_sfx_volume(self, volume):
        self.settings["audio"]["sfx_volume"] = max(0.0, min(1.0, volume))
        self.save()

    def is_music_enabled(self):
        return self.settings["audio"]["music_enabled"]

    def toggle_music(self):
        self.settings["audio"]["music_enabled"] = not self.settings["audio"]["music_enabled"]
        self.save()
        return self.settings["audio"]["music_enabled"]

    def is_sfx_enabled(self):
        return self.settings["audio"]["sfx_enabled"]

    def toggle_sfx(self):
        self.settings["audio"]["sfx_enabled"] = not self.settings["audio"]["sfx_enabled"]
        self.save()
        return self.settings["audio"]["sfx_enabled"]

    # ==================== GRAPHICS SETTINGS ====================

    def get_quality(self):
        return self.settings["graphics"]["quality"]

    def set_quality(self, quality):
        if quality in ["Low", "Medium", "High"]:
            self.settings["graphics"]["quality"] = quality
            self.save()

    def get_fps(self):
        return self.settings["graphics"]["fps"]

    def set_fps(self, fps):
        if fps in [30, 60, 120, 144]:
            self.settings["graphics"]["fps"] = fps
            self.save()

    def is_vsync_enabled(self):
        return self.settings["graphics"]["vsync"]

    def toggle_vsync(self):
        self.settings["graphics"]["vsync"] = not self.settings["graphics"]["vsync"]
        self.save()
        return self.settings["graphics"]["vsync"]

    def is_fullscreen(self):
        return self.settings["graphics"]["fullscreen"]

    def toggle_fullscreen(self):
        self.settings["graphics"]["fullscreen"] = not self.settings["graphics"]["fullscreen"]
        self.save()
        return self.settings["graphics"]["fullscreen"]

    def show_fps(self):
        return self.settings["graphics"]["show_fps"]

    def toggle_show_fps(self):
        self.settings["graphics"]["show_fps"] = not self.settings["graphics"]["show_fps"]
        self.save()
        return self.settings["graphics"]["show_fps"]

    # ==================== GAMEPLAY SETTINGS ====================

    def get_difficulty(self):
        return self.settings["gameplay"]["difficulty"]

    def set_difficulty(self, difficulty):
        if difficulty in ["Easy", "Normal", "Hard"]:
            self.settings["gameplay"]["difficulty"] = difficulty
            self.save()

    def show_hitboxes(self):
        return self.settings["gameplay"]["show_hitboxes"]

    def toggle_hitboxes(self):
        self.settings["gameplay"]["show_hitboxes"] = not self.settings["gameplay"]["show_hitboxes"]
        self.save()
        return self.settings["gameplay"]["show_hitboxes"]

    def are_particles_enabled(self):
        return self.settings["gameplay"]["particles_enabled"]

    def toggle_particles(self):
        self.settings["gameplay"]["particles_enabled"] = not self.settings["gameplay"]["particles_enabled"]
        self.save()
        return self.settings["gameplay"]["particles_enabled"]

    def is_screen_shake_enabled(self):
        return self.settings["gameplay"]["screen_shake"]

    def toggle_screen_shake(self):
        self.settings["gameplay"]["screen_shake"] = not self.settings["gameplay"]["screen_shake"]
        self.save()
        return self.settings["gameplay"]["screen_shake"]

    # ==================== CONTROLS SETTINGS ====================

    def get_jump_key(self):
        return self.settings["controls"]["jump_key"]

    def set_jump_key(self, key):
        self.settings["controls"]["jump_key"] = key
        self.save()

    def get_pause_key(self):
        return self.settings["controls"]["pause_key"]

    def is_mouse_control_enabled(self):
        return self.settings["controls"]["mouse_control"]

    def toggle_mouse_control(self):
        self.settings["controls"]["mouse_control"] = not self.settings["controls"]["mouse_control"]
        self.save()
        return self.settings["controls"]["mouse_control"]

    # ==================== PLAYER SETTINGS ====================

    def get_player_name(self):
        return self.settings["player"]["name"]

    def set_player_name(self, name):
        self.settings["player"]["name"] = name
        self.save()

    def get_selected_bird(self):
        return self.settings["player"]["selected_bird"]

    def set_selected_bird(self, bird):
        if bird in ["blue", "red", "yellow", "orange", "pink"]:
            self.settings["player"]["selected_bird"] = bird
            self.save()

    # ==================== UTILITY ====================

    def get_all_settings(self):
        """Tra ve tat ca settings"""
        return self.settings

    def print_settings(self):
        """In ra tat ca settings"""
        print("\nCurrent Settings:")
        print("=" * 50)
        for category, settings in self.settings.items():
            print(f"\n{category.upper()}:")
            for key, value in settings.items():
                print(f"  {key}: {value}")


# Global settings instance
_settings_instance = None

def get_settings():
    """Lay settings instance (singleton)"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance


# Test
if __name__ == "__main__":
    print("Settings Manager Test")
    print("=" * 50)

    # Tao settings
    settings = Settings()

    print("\n1. Default settings:")
    settings.print_settings()

    print("\n2. Test audio settings:")
    settings.set_master_volume(0.8)
    print(f"   Master volume: {settings.get_master_volume()}")

    settings.toggle_music()
    print(f"   Music enabled: {settings.is_music_enabled()}")

    print("\n3. Test graphics settings:")
    settings.set_quality("Medium")
    print(f"   Quality: {settings.get_quality()}")

    settings.set_fps(120)
    print(f"   FPS: {settings.get_fps()}")

    print("\n4. Test gameplay settings:")
    settings.set_difficulty("Hard")
    print(f"   Difficulty: {settings.get_difficulty()}")

    settings.toggle_particles()
    print(f"   Particles enabled: {settings.are_particles_enabled()}")

    print("\n5. Test player settings:")
    settings.set_player_name("TestPlayer")
    print(f"   Player name: {settings.get_player_name()}")

    settings.set_selected_bird("red")
    print(f"   Selected bird: {settings.get_selected_bird()}")

    print("\n6. Settings saved to game_settings.json")

    # Test singleton
    settings2 = get_settings()
    print(f"\n7. Singleton test: {settings2.get_player_name()}")

    print("\nSettings Manager ready!")


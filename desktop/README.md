# Flappy Bird - Desktop Edition v2.0
## Economy & Shop Update

### Features
- **Classic Gameplay**: Smooth Flappy Bird mechanics with pixel-perfect collision
- **Shop System**: Buy and equip different bird skins using collected coins
- **Coin Collection**: Gather coins during gameplay to unlock new birds
- **Bird Abilities**: Each bird has unique characteristics
  - **Yellow (Classic)**: Balanced gravity and jump force
  - **Blue (Azure)**: Floaty physics - easier to control (50 coins)
  - **Red (Crimson)**: Heavy physics but 2x score multiplier (100 coins)
- **Local Storage**: All progress saved locally (coins, owned skins, high scores)
- **Online Sync**: Scores sync to server when internet is available
- **Visual Enhancements**:
  - Random day/night backgrounds
  - Random pipe colors (green/red)
  - Smooth bird animations (3-frame flapping)
  - Parallax scrolling ground
  - Bird rotation based on velocity

### Installation & Running

1. **Install Dependencies**:
   ```bash
   pip install pygame
   ```

2. **Run the Game**:
   ```bash
   cd desktop
   python main.py
   ```

### Controls
- **SPACE** or **UP ARROW**: Flap/Jump
- **ESC**: Back to menu (from most screens)
- **LEFT/RIGHT ARROWS**: Navigate shop
- **ENTER/SPACE**: Buy/Select skin in shop

### Game Modes
- **PLAY**: Standard gameplay - collect coins and dodge pipes
- **SHOP**: Purchase and equip bird skins
- **SCORES**: View online leaderboard (when connected)
- **TRAIN**: AI training mode (experimental)

### File Structure
```
desktop/
  ├── main.py              # Entry point
  ├── game_utils.py        # Utility functions
  ├── local_storage.py     # Data persistence
  ├── api_client.py        # Server communication
  ├── scenes/
  │   ├── login_scene.py
  │   ├── menu_scene.py
  │   ├── play_scene.py    # Main gameplay
  │   ├── shop_scene.py    # Shop interface (NEW)
  │   ├── gameover_scene.py
  │   └── scores_scene.py
  └── assets/
      ├── bird sprites (yellow, blue, red)
      ├── backgrounds (day, night)
      ├── pipes (green, red)
      ├── sounds (flap, hit)
      └── UI elements
```

### Testing
Run automated tests:
```bash
python check_assets.py  # Verify all assets present
```

### Version History
- **v2.0** (Economy & Shop Update)
  - Added coin collection mechanic
  - New shop system with 3 bird skins
  - Unique bird abilities
  - Enhanced visual effects
- **v1.0** (Initial Release)
  - Basic Flappy Bird gameplay
  - Online leaderboard
  - Offline score storage

### Credits
- Original Flappy Bird by Dong Nguyen
- Sprites from https://github.com/samuelcust/flappy-bird-assets
- Built with Pygame

### License
Educational project - Not for commercial use

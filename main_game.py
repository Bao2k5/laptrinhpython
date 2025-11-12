"""
Main Game Launcher - Tich hop Keyboard, Breath Control, va AI
Chay file nay bang: python main_game.py hoac play.bat
"""
import pygame
import sys
import os

# Import tu game chinh
from menu import show_menu, show_instructions
from game import run, WIN_WIDTH, WIN_HEIGHT

def main():
    """Main launcher cho tat ca cac che do game"""
    pygame.init()

    # Show menu
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird - Choose Mode")

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    while True:
        choice = show_menu(screen)

        if choice == "exit":
            pygame.quit()
            sys.exit()

        elif choice == "help":
            cont = show_instructions(screen)
            if not cont:
                pygame.quit()
                sys.exit()

        elif choice == "start":
            # AI MODE
            pygame.display.set_caption("Flappy Bird - AI Mode (NEAT)")
            run(config_path)

        elif choice == "play":
            # PLAYER MODE - Don gian hon, chi dung SPACE
            pygame.display.set_caption("Flappy Bird - Player Mode")
            try:
                from simple_play import play_simple_mode
                play_simple_mode()
            except Exception as e:
                print(f"Loi: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    print("="*60)
    print("FLAPPY BIRD - MULTI-MODE GAME")
    print("="*60)
    print("Co san:")
    print("   PLAY - Choi bang SPACE hoac HOI THO")
    print("   AI - Xem AI hoc choi bang NEAT")
    print("="*60)

    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame bi dung boi nguoi dung")
    except Exception as e:
        print(f"\nLoi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("\nTam biet!")

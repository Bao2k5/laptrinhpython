from flask import Flask, render_template
import sys

# Guarded import: some environments (Render) don't have pygame installed.
# If pygame is missing, we set `pygame = None` so importing `main` doesn't fail.
try:
    import pygame
except Exception:
    pygame = None

# Expose a WSGI app so Render/Gunicorn can import `main:app`
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('web_game.html') if app.template_folder else 'Flappy Bird Web'


def run_desktop_game():
    import pygame
    from scenes.login_scene import LoginScene
    from scenes.register_scene import RegisterScene
    from scenes.menu_scene import MenuScene
    from scenes.play_scene import PlayScene
    from scenes.scores_scene import ScoresScene
    from scenes.gameover_scene import GameOverScene

    pygame.init()

    WIDTH, HEIGHT = 500, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird Python")

    clock = pygame.time.Clock()

    current_scene = "login"
    scene_data = {"player": None}


    def goto(scene_name, **kwargs):
        nonlocal current_scene, scene_data

        # Preserve player if not provided by new scene
        if "player" not in kwargs:
            kwargs["player"] = scene_data.get("player")

        scene_data = kwargs
        current_scene = scene_name


    while True:
        clock.tick(60)

        player = scene_data.get("player")

        if current_scene == "login":
            next_scene, data = LoginScene(screen).run()
            goto(next_scene, **data)

        elif current_scene == "register":
            next_scene, data = RegisterScene(screen).run()
            goto(next_scene, **data)

        elif current_scene == "menu":
            next_scene, data = MenuScene(screen, player).run()
            goto(next_scene, **data)

        elif current_scene == "play":
            next_scene, data = PlayScene(screen, player).run()
            goto(next_scene, **data)

        elif current_scene == "scores":
            player = scene_data.get("player")
            next_scene, data = ScoresScene(screen, player).run()
            goto(next_scene, **data)

        elif current_scene == "gameover":
            score = scene_data.get("score", 0)
            next_scene, data = GameOverScene(screen, player, score).run()
            goto(next_scene, **data)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run_desktop_game()

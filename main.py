import sys
import asyncio

# Guarded import: some environments (Render) don't have pygame installed.
# If pygame is missing, we set `pygame = None` so importing `main` doesn't fail.
try:
    import pygame
except Exception:
    pygame = None


async def run_desktop_game():
    import pygame
    from scenes.login_scene import LoginScene
    from scenes.register_scene import RegisterScene
    from scenes.menu_scene import MenuScene
    from scenes.play_scene import PlayScene
    from scenes.scores_scene import ScoresScene
    from scenes.gameover_scene import GameOverScene
    from scenes.train_scene import TrainScene

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
        # The outer loop doesn't need sleep(0) because it awaits the inner loops (scenes)
        # which already sleep.
        
        player = scene_data.get("player")

        if current_scene == "login":
            next_scene, data = await LoginScene(screen).run()
            goto(next_scene, **data)

        elif current_scene == "register":
            next_scene, data = await RegisterScene(screen).run()
            goto(next_scene, **data)

        elif current_scene == "menu":
            next_scene, data = await MenuScene(screen, player).run()
            goto(next_scene, **data)

        elif current_scene == "play":
            next_scene, data = await PlayScene(screen, player).run()
            goto(next_scene, **data)

        elif current_scene == "scores":
            player = scene_data.get("player")
            next_scene, data = await ScoresScene(screen, player).run()
            goto(next_scene, **data)

        elif current_scene == "gameover":
            score = scene_data.get("score", 0)
            next_scene, data = await GameOverScene(screen, player, score).run()
            goto(next_scene, **data)
            
        elif current_scene == "train":
            next_scene, data = await TrainScene(screen).run()
            goto(next_scene, **data)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    asyncio.run(run_desktop_game())

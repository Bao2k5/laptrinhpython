import os

def in_browser():
    try:
        import js  # pyodide/pygbag expose `js`
        return True
    except Exception:
        return False


def asset_path(*parts):
    """Return a path suitable for the current environment.
    - In browser (pygbag/pyodide) return a forward-slash joined relative path.
    - Locally return an absolute path relative to repo.
    """
    if in_browser():
        return "/".join(parts)
    base = os.path.dirname(__file__)
    return os.path.join(base, *parts)


def load_sound(path_without_ext):
    """Try to load sound with .ogg first then .wav. Returns pygame.mixer.Sound or None."""
    try:
        import pygame
    except Exception:
        return None

    # path_without_ext can be like 'assets/flap' or 'assets/flap.wav'
    base, ext = os.path.splitext(path_without_ext)
    if ext:
        candidates = [path_without_ext]
    else:
        candidates = [base + '.ogg', base + '.wav']

    for p in candidates:
        full = asset_path(p) if '/' in p else asset_path('assets', p)
        try:
            if os.path.exists(full) or in_browser():
                return pygame.mixer.Sound(full)
        except Exception:
            continue

    # Last resort: try original string
    try:
        return pygame.mixer.Sound(path_without_ext)
    except Exception:
        return None


def send_score_to_server(player_name, score, url=None):
    """Send score to server. Try requests (desktop) then JS fetch (browser)."""
    if url is None:
        url = "http://127.0.0.1:5000/api/score"

    # Try requests (desktop)
    try:
        import requests
        requests.post(url, json={"username": player_name, "score": score}, timeout=1.0)
        return True
    except Exception:
        pass

    # Try JS fetch (pyodide/pygbag)
    try:
        from js import fetch, JSON
        import asyncio

        async def _post():
            await fetch(url, {
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": JSON.stringify({"username": player_name, "score": score})
            })

        try:
            asyncio.ensure_future(_post())
        except Exception:
            # If cannot schedule, run sync-ish
            try:
                import pyodide
                pyodide.eval_code("(async () => { })()")
            except Exception:
                pass

        return True
    except Exception:
        return False

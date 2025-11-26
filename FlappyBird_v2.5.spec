# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['desktop\\main.py'],
    pathex=['desktop'],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[
        'api_client',
        'local_storage',
        'game_utils',
        'scenes',
        'scenes.login_scene',
        'scenes.register_scene',
        'scenes.menu_scene',
        'scenes.play_scene',
        'scenes.scores_scene',
        'scenes.gameover_scene',
        'scenes.train_scene',
        'scenes.shop_scene',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'AI'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FlappyBird_v2.5',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

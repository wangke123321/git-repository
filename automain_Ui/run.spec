# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['web_ui_auto_lib.element_behavior_handlers.check_behavior_handler',
             'web_ui_auto_lib.element_behavior_handlers.click_behavior_handler',
             'web_ui_auto_lib.element_behavior_handlers.close_behavior_handler',
             'web_ui_auto_lib.element_behavior_handlers.refresh_behavior_handler',
             'web_ui_auto_lib.element_behavior_handlers.input_behavior_handler',
             'web_ui_auto_lib.element_behavior_handlers.openurl_behavior_handler',
             'web_ui_auto_lib.element_behavior_handlers.screenshot_behavior_handler',
             'web_ui_auto_lib.element_behavior_handlers.move_behavior_handler',
             'web_ui_auto_lib.element_behavior_handlers.upload_behavior_handler',
	         'web_ui_auto_lib.element_behavior_handlers.quit_behavior_handler',
	         'web_ui_auto_lib.element_behavior_handlers.point_behavior_handler'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='run',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

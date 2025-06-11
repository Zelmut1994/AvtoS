# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\full_app.py'],
    pathex=[],
    binaries=[],
    datas=[('src/resources_rc.py', 'src'), ('src/database_simple.py', 'src'), ('src/styles_enhanced.py', 'src'), ('src/settings_manager.py', 'src'), ('src/settings_dialog.py', 'src'), ('src/ui_utils.py', 'src'), ('src/modern_widgets.py', 'src'), ('src/enhanced_widgets.py', 'src'), ('src/style_loader.py', 'src'), ('src/icon_loader.py', 'src'), ('src/database.py', 'src')],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'peewee'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='AutoParts',
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

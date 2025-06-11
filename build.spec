# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import PySide6
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs
import glob

block_cipher = None

# Собираем все подмодули PySide6
hiddenimports = collect_submodules('PySide6')

# Добавляем специфические импорты
hiddenimports.extend([
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'peewee',
])

# Собираем все DLL PySide6
qt_binaries = collect_dynamic_libs('PySide6')

# Определяем пути к плагинам Qt
qt_dir = os.path.dirname(PySide6.__file__)
qt_plugin_path = os.path.join(qt_dir, "plugins")
platforms_path = os.path.join(qt_plugin_path, "platforms")

# Явно добавляем все Qt6*.dll из PySide6
qt6_dlls = []
for dll in glob.glob(os.path.join(qt_dir, "Qt6*.dll")):
    qt6_dlls.append((dll, '.'))
# Явно добавляем системные библиотеки, если они есть
system_dlls = []
for dll in ["libEGL.dll", "libGLESv2.dll", "d3dcompiler_47.dll"]:
    dll_path = os.path.join(qt_dir, dll)
    if os.path.exists(dll_path):
        system_dlls.append((dll_path, '.'))

# Явно добавляем все файлы из platforms
platforms_files = []
for f in glob.glob(os.path.join(platforms_path, '*')):
    platforms_files.append((f, 'platforms'))

# Собираем все файлы плагинов Qt (кроме platforms)
qt_plugins = []
for root, dirs, files in os.walk(qt_plugin_path):
    for file in files:
        if file.endswith('.dll') and 'platforms' not in root:
            rel_path = os.path.relpath(root, qt_plugin_path)
            qt_plugins.append((os.path.join(root, file), rel_path))

# Создаем runtime hook для настройки путей Qt
runtime_hook = """
import os
import sys
from PySide6.QtCore import QCoreApplication

def qt_plugin_paths():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    plugin_path = os.path.join(base_path, 'platforms')
    if os.path.exists(plugin_path):
        QCoreApplication.addLibraryPath(plugin_path)
qt_plugin_paths()
"""
with open('qt_hook.py', 'w', encoding='utf-8') as f:
    f.write(runtime_hook)

datas = [
    ('src/resources_rc.py', 'src'),
    ('src/database_simple.py', 'src'),
    ('src/styles_enhanced.py', 'src'),
    ('src/settings_manager.py', 'src'),
    ('src/settings_dialog.py', 'src'),
    ('src/ui_utils.py', 'src'),
    ('src/modern_widgets.py', 'src'),
    ('src/enhanced_widgets.py', 'src'),
    ('src/style_loader.py', 'src'),
    ('src/icon_loader.py', 'src'),
    ('src/database.py', 'src'),
] + qt_plugins + platforms_files

a = Analysis(
    ['src/full_app.py'],
    pathex=[],
    binaries=qt_binaries + qt6_dlls + system_dlls,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['qt_hook.py'],
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
    [],
    exclude_binaries=True,
    name='AutoParts',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AutoParts',
) 
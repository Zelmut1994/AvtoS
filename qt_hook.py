
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

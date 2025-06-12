 """
 Диалог настроек приложения
 """
 
 import os
 from PySide6.QtWidgets import (
     QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
     QFormLayout, QGroupBox, QCheckBox, QSpinBox, QLineEdit,
     QPushButton, QFileDialog, QLabel, QComboBox, 
     QSlider, QDialogButtonBox, QMessageBox, QTextEdit, QSplitter
 )
 from PySide6.QtCore import Qt, QTimer
 from PySide6.QtGui import QFont, QPixmap
 
 from settings_manager import get_settings
 from modern_widgets import ModernButton, ModernGroupBox
 from ui_utils import apply_modern_styling
-from simple_icon_loader import SimpleIconLoader
+
 
 
 class SettingsDialog(QDialog):
     """Диалог настроек приложения"""
     
     def __init__(self, parent=None):
         super().__init__(parent)
-        self.settings = get_settings()
-        self.icon_loader = SimpleIconLoader()
+        self.settings = get_settings()
         self.init_ui()
         self.load_settings()
         self.setModal(True)
     
     def init_ui(self):
         """Инициализация интерфейса"""
         self.setWindowTitle("Настройки AutoParts")
         self.setMinimumSize(600, 500)
         self.resize(800, 600)
         
         # Основной layout
         layout = QVBoxLayout(self)
         layout.setSpacing(10)
         layout.setContentsMargins(15, 15, 15, 15)
         
         # Заголовок
         title_label = QLabel("⚙️ Настройки приложения")
         title_font = QFont()
         title_font.setPointSize(16)
         title_font.setBold(True)
         title_label.setFont(title_font)
         title_label.setAlignment(Qt.AlignCenter)
         layout.addWidget(title_label)
         
         # Вкладки настроек

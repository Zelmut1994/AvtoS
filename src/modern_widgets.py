"""
 Современные виджеты с SVG иконками
 """
 
 from PySide6.QtWidgets import (
     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
     QLineEdit, QTableWidget, QFrame, QGroupBox, QComboBox,
     QTableWidgetItem, QHeaderView, QAbstractItemView
 )
 from PySide6.QtCore import Qt, Signal, QTimer
 from PySide6.QtGui import QFont
 
-try:
-    # Пробуем сначала SVG загрузчик, потом простой
-    try:
-        from .icon_loader import get_icon, get_pixmap
-        ICONS_AVAILABLE = True
-        print("✅ SVG загрузчик иконок подключён")
-    except ImportError:
-        from .simple_icon_loader import get_icon, get_pixmap
-        ICONS_AVAILABLE = True
-        print("✅ Простой загрузчик иконок подключён")
-except ImportError:
-    print("⚠️ Загрузчик иконок недоступен, используются текстовые метки")
-    ICONS_AVAILABLE = False
+try:
+    from .icon_loader import get_icon, get_pixmap
+    ICONS_AVAILABLE = True
+    print("✅ Загрузчик иконок подключён")
+except Exception:
+    ICONS_AVAILABLE = False
+    print("⚠️ Загрузчик иконок недоступен, используются текстовые метки")
 
 
 class ModernButton(QPushButton):
     """Современная кнопка с SVG иконкой"""
     
     def __init__(self, text: str = "", icon_name: str = "", parent=None):
         super().__init__(text, parent)
         
         if icon_name and ICONS_AVAILABLE:
             self.setIcon(get_icon(icon_name))
         
         # Применяем современные стили
         self.setMinimumHeight(36)
         self.setStyleSheet("""
             QPushButton {
                 padding: 8px 16px;
                 border-radius: 6px;
                 font-weight: 500;
             }
         """)
 
 class ModernSearchBar(QWidget):
     """Современная строка поиска с иконкой"""
     
     textChanged = Signal(str)

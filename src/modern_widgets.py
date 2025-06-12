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

try:
    from .icon_loader import get_icon, get_pixmap
    ICONS_AVAILABLE = True
    print("✅ Загрузчик иконок подключён")
except Exception:
    ICONS_AVAILABLE = False
    print("⚠️ Загрузчик иконок недоступен, используются текстовые метки")


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
    
    def __init__(self, placeholder: str = "Поиск...", parent=None):
        super().__init__(parent)
        self.setup_ui(placeholder)
    
    def setup_ui(self, placeholder: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Иконка поиска
        if ICONS_AVAILABLE:
            icon_label = QLabel()
            icon_label.setPixmap(get_pixmap("search", "#666", 16))
            layout.addWidget(icon_label)
        else:
            icon_label = QLabel("🔍")
            layout.addWidget(icon_label)
        
        # Поле ввода
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.textChanged.connect(self.textChanged.emit)
        layout.addWidget(self.search_input)
        
        # Стили
        self.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 4px 12px;
            }
            QLineEdit {
                border: none;
                background: transparent;
                padding: 4px;
            }
        """)


class ModernCard(QFrame):
    """Современная карточка"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setup_ui(title)
    
    def setup_ui(self, title: str):
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 8px;
                }
            """)
            layout.addWidget(title_label)
        
        # Контейнер для содержимого
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
    
    def add_content(self, widget):
        """Добавить содержимое в карточку"""
        self.content_layout.addWidget(widget)


class ModernTable(QTableWidget):
    """Современная таблица с улучшенным стилем"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
    
    def setup_style(self):
        """Настройка стиля таблицы"""
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.setGridStyle(Qt.NoPen)
        
        # Настройка заголовков
        header = self.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setStyleSheet("""
            QHeaderView::section {
                background: #f5f5f5;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: 600;
            }
        """)
        
        # Стили таблицы
        self.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background: #e3f2fd;
                color: #1976d2;
            }
            QTableWidget::item:hover {
                background: #f5f5f5;
            }
        """)


class ModernGroupBox(QGroupBox):
    """Современный групповой блок"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(title, parent)
        self.setup_style()
    
    def setup_style(self):
        """Настройка стиля группового блока"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin: 12px 0px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                background: white;
                color: #333;
            }
        """)


class ModernComboBox(QComboBox):
    """Современный выпадающий список"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
    
    def setup_style(self):
        """Настройка стиля выпадающего списка"""
        self.setMinimumHeight(36)
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px 12px;
                background: white;
                min-width: 120px;
            }
            QComboBox:hover {
                border-color: #2196F3;
            }
            QComboBox:focus {
                border-color: #2196F3;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ddd;
                border-radius: 6px;
                background: white;
                selection-background-color: #e3f2fd;
            }
        """)


class ModernLineEdit(QLineEdit):
    """Современное поле ввода"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setup_style()
    
    def setup_style(self):
        """Настройка стиля поля ввода"""
        self.setMinimumHeight(36)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px 12px;
                background: white;
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #2196F3;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                outline: none;
                box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
            }
        """)


class StatusIndicator(QWidget):
    """Индикатор статуса с цветовой кодировкой"""
    
    def __init__(self, status: str = "normal", text: str = "", parent=None):
        super().__init__(parent)
        self.setup_ui(status, text)
    
    def setup_ui(self, status: str, text: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Цветовой индикатор
        indicator = QLabel("●")
        colors = {
            "success": "#4caf50",
            "warning": "#ff9800", 
            "error": "#f44336",
            "info": "#2196f3",
            "normal": "#9e9e9e"
        }
        
        color = colors.get(status, colors["normal"])
        indicator.setStyleSheet(f"color: {color}; font-size: 16px;")
        layout.addWidget(indicator)
        
        # Текст
        if text:
            text_label = QLabel(text)
            text_label.setStyleSheet("color: #666; font-size: 13px;")
            layout.addWidget(text_label)
        
        layout.addStretch()
        
        # Стиль контейнера
        self.setStyleSheet("""
            QWidget {
                background: #f9f9f9;
                border-radius: 12px;
            }
        """)


class LoadingSpinner(QLabel):
    """Анимированный индикатор загрузки"""
    
    def __init__(self, size: int = 24, parent=None):
        super().__init__(parent)
        self.size = size
        self.angle = 0
        self.setup_ui()
        
        # Таймер для анимации
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
    
    def setup_ui(self):
        """Настройка интерфейса спиннера"""
        self.setFixedSize(self.size, self.size)
        self.setText("⟳")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {self.size - 4}px;
                color: #2196F3;
            }}
        """)
    
    def start(self):
        """Запустить анимацию"""
        self.timer.start(100)  # Обновление каждые 100мс
    
    def stop(self):
        """Остановить анимацию"""
        self.timer.stop()
        self.angle = 0
    
    def rotate(self):
        """Поворот спиннера"""
        self.angle = (self.angle + 30) % 360
        # Простая анимация через изменение символа
        symbols = ["⟳", "⟲", "⟳", "⟲"]
        symbol_index = (self.angle // 90) % len(symbols)
        self.setText(symbols[symbol_index])


class ModernProgressBar(QWidget):
    """Современный прогресс-бар"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._maximum = 100
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        self.setMinimumHeight(8)
        self.setMaximumHeight(8)
        self.setStyleSheet("""
            QWidget {
                background: #e0e0e0;
                border-radius: 4px;
            }
        """)
    
    def setValue(self, value: int):
        """Установить значение прогресса"""
        self._value = max(0, min(value, self._maximum))
        self.update()
    
    def setMaximum(self, maximum: int):
        """Установить максимальное значение"""
        self._maximum = max(1, maximum)
        self.update()
    
    def value(self) -> int:
        """Получить текущее значение"""
        return self._value
    
    def maximum(self) -> int:
        """Получить максимальное значение"""
        return self._maximum
    
    def paintEvent(self, event):
        """Отрисовка прогресс-бара"""
        super().paintEvent(event)
        
        if self._maximum <= 0:
            return
        
        from PySide6.QtGui import QPainter, QColor
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Фон
        painter.setBrush(QColor("#e0e0e0"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 4, 4)
        
        # Прогресс
        if self._value > 0:
            progress_width = int((self._value / self._maximum) * self.width())
            progress_rect = self.rect()
            progress_rect.setWidth(progress_width)
            
            painter.setBrush(QColor("#2196F3"))
            painter.drawRoundedRect(progress_rect, 4, 4)

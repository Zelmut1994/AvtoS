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
    # Пробуем сначала SVG загрузчик, потом простой
    try:
        from .icon_loader import get_icon, get_pixmap
        ICONS_AVAILABLE = True
        print("✅ SVG загрузчик иконок подключён")
    except ImportError:
        from .simple_icon_loader import get_icon, get_pixmap
        ICONS_AVAILABLE = True
        print("✅ Простой загрузчик иконок подключён")
except ImportError:
    print("⚠️ Загрузчик иконок недоступен, используются текстовые метки")
    ICONS_AVAILABLE = False


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
    searchTriggered = Signal(str)
    
    def __init__(self, placeholder: str = "Поиск...", parent=None):
        super().__init__(parent)
        self.setup_ui(placeholder)
    
    def setup_ui(self, placeholder: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Поле поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.textChanged.connect(self.textChanged.emit)
        self.search_input.returnPressed.connect(self._on_search)
        
        # Кнопка поиска
        self.search_button = ModernButton("", "search")
        self.search_button.setMaximumWidth(40)
        self.search_button.clicked.connect(self._on_search)
        
        # Кнопка очистки
        self.clear_button = ModernButton("", "delete")
        self.clear_button.setMaximumWidth(40)
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.setVisible(False)
        
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.clear_button)
        
        # Показывать кнопку очистки только когда есть текст
        self.search_input.textChanged.connect(self._update_clear_button)
    
    def _on_search(self):
        text = self.search_input.text().strip()
        self.searchTriggered.emit(text)
    
    def _update_clear_button(self, text: str):
        self.clear_button.setVisible(bool(text.strip()))
    
    def clear(self):
        self.search_input.clear()
        self.search_input.setFocus()
    
    def text(self) -> str:
        return self.search_input.text()

class ActionButtonGroup(QWidget):
    """Группа кнопок действий"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.buttons = {}
    
    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)
    
    def add_action(self, name: str, text: str, icon_name: str = "", 
                   callback=None, style_class: str = ""):
        """Добавить кнопку действия"""
        button = ModernButton(text, icon_name)
        
        if style_class:
            button.setProperty("styleClass", style_class)
        
        if callback:
            button.clicked.connect(callback)
        
        self.buttons[name] = button
        self.layout.addWidget(button)
        return button
    
    def get_button(self, name: str) -> QPushButton:
        """Получить кнопку по имени"""
        return self.buttons.get(name)
    
    def set_enabled(self, name: str, enabled: bool):
        """Включить/выключить кнопку"""
        button = self.get_button(name)
        if button:
            button.setEnabled(enabled)

class ModernDataTable(QTableWidget):
    """Современная таблица данных"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_table()
    
    def setup_table(self):
        # Настройки таблицы
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Настройки заголовков
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        
        # Стили
        self.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #e3f2fd;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: 600;
            }
        """)
    
    def set_data(self, headers: list, data: list):
        """Установить данные в таблицу"""
        self.setRowCount(len(data))
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.setItem(row_idx, col_idx, item)

class ModernStatCard(QFrame):
    """Современная карточка статистики"""
    
    def __init__(self, title: str, value: str, icon_name: str = "", 
                 color: str = "#2196F3", parent=None):
        super().__init__(parent)
        self.setup_ui(title, value, icon_name, color)
    
    def setup_ui(self, title: str, value: str, icon_name: str, color: str):
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(f"""
            QFrame {{
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                background-color: white;
                padding: 16px;
            }}
            QLabel#value {{
                color: {color};
                font-size: 24pt;
                font-weight: 700;
            }}
            QLabel#title {{
                color: #666;
                font-size: 10pt;
                font-weight: 500;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Заголовок с иконкой
        header_layout = QHBoxLayout()
        
        if icon_name and ICONS_AVAILABLE:
            icon_label = QLabel()
            icon_label.setPixmap(get_pixmap(icon_name, color, 20))
            header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setObjectName("title")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Значение
        self.value_label = QLabel(value)
        self.value_label.setObjectName("value")
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
    
    def update_value(self, new_value: str):
        """Обновить значение"""
        self.value_label.setText(new_value)

class ModernGroupBox(QGroupBox):
    """Современная группа с иконкой"""
    
    def __init__(self, title: str, icon_name: str = "", parent=None):
        if icon_name and not ICONS_AVAILABLE:
            # Fallback на эмоджи если SVG недоступны
            emoji_map = {
                'parts': '🔧', 'sales': '💰', 'reports': '📊',
                'search': '🔍', 'cart': '🛒'
            }
            icon_text = emoji_map.get(icon_name, '📁')
            title = f"{icon_text} {title}"
        
        super().__init__(title, parent)
        
        # Стили
        self.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 11pt;
                color: #1976d2;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                margin-top: 20px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 15px;
                background: white;
                border-radius: 6px;
                margin-left: 10px;
            }
        """)

class ModernToolbar(QWidget):
    """Современная панель инструментов"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.actions = {}
    
    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(16, 8, 16, 8)
        self.layout.setSpacing(8)
        
        # Стили панели
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
    
    def add_action(self, name: str, text: str, icon_name: str = "", 
                   callback=None) -> QPushButton:
        """Добавить действие в панель"""
        button = ModernButton(text, icon_name)
        
        if callback:
            button.clicked.connect(callback)
        
        self.actions[name] = button
        self.layout.addWidget(button)
        return button
    
    def add_spacer(self):
        """Добавить растягивающийся промежуток"""
        self.layout.addStretch()
    
    def add_widget(self, widget: QWidget):
        """Добавить произвольный виджет"""
        self.layout.addWidget(widget)

# Пример использования современных виджетов
class ModernWindow(QWidget):
    """Пример окна с современными виджетами"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Панель инструментов
        toolbar = ModernToolbar()
        toolbar.add_action("add", "Добавить", "add")
        toolbar.add_action("edit", "Редактировать", "edit")
        toolbar.add_action("delete", "Удалить", "delete")
        toolbar.add_spacer()
        
        # Поиск
        search_bar = ModernSearchBar("Поиск товаров...")
        toolbar.add_widget(search_bar)
        
        layout.addWidget(toolbar)
        
        # Основное содержимое
        main_layout = QHBoxLayout()
        
        # Левая панель со статистикой
        left_panel = QVBoxLayout()
        
        stats_group = ModernGroupBox("Статистика", "reports")
        stats_layout = QVBoxLayout(stats_group)
        
        # Карточки статистики
        parts_card = ModernStatCard("Всего запчастей", "150", "parts")
        sales_card = ModernStatCard("Продажи", "50 000 ₽", "sales", "#4CAF50")
        
        stats_layout.addWidget(parts_card)
        stats_layout.addWidget(sales_card)
        
        left_panel.addWidget(stats_group)
        left_panel.addStretch()
        
        # Правая панель с таблицей
        right_panel = QVBoxLayout()
        
        table_group = ModernGroupBox("Данные", "parts")
        table_layout = QVBoxLayout(table_group)
        
        # Таблица
        table = ModernDataTable()
        table.set_data(
            ["ID", "Название", "Цена"],
            [["1", "Фильтр масляный", "500"], ["2", "Свеча зажигания", "300"]]
        )
        
        table_layout.addWidget(table)
        
        # Кнопки действий
        actions = ActionButtonGroup()
        actions.add_action("refresh", "Обновить", "refresh")
        actions.add_action("export", "Экспорт", "export")
        
        table_layout.addWidget(actions)
        
        right_panel.addWidget(table_group)
        
        # Компоновка
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)
        
        layout.addLayout(main_layout)
        
        self.setWindowTitle("Современные виджеты AutoParts")
        self.resize(800, 600) 
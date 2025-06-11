# -*- coding: utf-8 -*-
"""
Улучшенные виджеты для современного интерфейса
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QIcon
from styles_enhanced import ENHANCED_COLORS, ICONS

class StatCard(QFrame):
    """Карточка статистики"""
    
    def __init__(self, title, value, icon="📊", color="primary"):
        super().__init__()
        self.setProperty("class", "stat-card")
        self.setup_ui(title, value, icon, color)
    
    def setup_ui(self, title, value, icon, color):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Заголовок с иконкой
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"font-size: 20pt; color: {ENHANCED_COLORS.get(color, '#2196F3')};")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setProperty("class", "stat-label")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Значение
        value_label = QLabel(str(value))
        value_label.setProperty("class", "stat-value")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
    
    def update_value(self, new_value):
        """Обновить значение карточки"""
        value_label = self.findChild(QLabel)
        if value_label and hasattr(value_label, 'property') and value_label.property("class") == "stat-value":
            value_label.setText(str(new_value))

class EnhancedNotificationBar(QFrame):
    """Улучшенная панель уведомлений"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "notification")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Иконка предупреждения
        icon_label = QLabel("⚠️")
        icon_label.setStyleSheet("font-size: 18pt;")
        layout.addWidget(icon_label)
        
        # Текст уведомления
        self.message_label = QLabel()
        self.message_label.setStyleSheet("font-weight: 500; color: #FF8F00;")
        layout.addWidget(self.message_label)
        
        layout.addStretch()
        
        # Кнопка действия
        self.action_button = QPushButton("Подробнее")
        self.action_button.setProperty("class", "small")
        self.action_button.setProperty("class", "warning")
        layout.addWidget(self.action_button)
        
        # Кнопка закрытия
        close_button = QPushButton("❌")
        close_button.setProperty("class", "small")
        close_button.setMaximumWidth(30)
        close_button.clicked.connect(self.hide)
        layout.addWidget(close_button)
    
    def set_message(self, message, action_callback=None):
        """Установить сообщение и callback для кнопки действия"""
        self.message_label.setText(message)
        
        if action_callback:
            self.action_button.clicked.connect(action_callback)
            self.action_button.show()
        else:
            self.action_button.hide()

class ModernSearchBar(QFrame):
    """Современная панель поиска"""
    
    def __init__(self, placeholder="Поиск...", parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setup_ui(placeholder)
    
    def setup_ui(self, placeholder):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Иконка поиска
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 16pt; color: #757575;")
        layout.addWidget(search_icon)
        
        # Поле поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.setStyleSheet("border: none; background: transparent; font-size: 10pt;")
        layout.addWidget(self.search_input)
        
        # Кнопка очистки
        self.clear_button = QPushButton("❌")
        self.clear_button.setProperty("class", "small")
        self.clear_button.setMaximumWidth(25)
        self.clear_button.clicked.connect(self.clear_search)
        self.clear_button.hide()
        layout.addWidget(self.clear_button)
        
        # Показывать кнопку очистки только при наличии текста
        self.search_input.textChanged.connect(self.on_text_changed)
    
    def on_text_changed(self, text):
        """Показать/скрыть кнопку очистки"""
        if text:
            self.clear_button.show()
        else:
            self.clear_button.hide()
    
    def clear_search(self):
        """Очистить поиск"""
        self.search_input.clear()
    
    def get_text(self):
        """Получить текст поиска"""
        return self.search_input.text()
    
    def connect_search(self, callback):
        """Подключить callback к изменению текста"""
        self.search_input.textChanged.connect(callback)

class ActionButtonGroup(QFrame):
    """Группа кнопок действий"""
    
    def __init__(self, buttons_config, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setup_ui(buttons_config)
    
    def setup_ui(self, buttons_config):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        for config in buttons_config:
            button = QPushButton(config['text'])
            
            # Применяем стили
            if 'class' in config:
                button.setProperty("class", config['class'])
            
            if 'callback' in config:
                button.clicked.connect(config['callback'])
            
            if 'enabled' in config:
                button.setEnabled(config['enabled'])
            
            if 'tooltip' in config:
                button.setToolTip(config['tooltip'])
            
            layout.addWidget(button)
        
        layout.addStretch()

class DataTable(QTableWidget):
    """Улучшенная таблица данных"""
    
    def __init__(self, headers, parent=None):
        super().__init__(parent)
        self.setup_table(headers)
    
    def setup_table(self, headers):
        """Настройка таблицы"""
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Настройка заголовков
        header = self.horizontalHeader()
        for i, header_text in enumerate(headers):
            if i == 0:  # ID обычно первая колонка
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            elif "Наименование" in header_text or "Название" in header_text:
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        # Общие настройки
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
    
    def add_data_row(self, data, row_color=None):
        """Добавить строку данных"""
        row = self.rowCount()
        self.insertRow(row)
        
        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            self.setItem(row, col, item)
            
            if row_color:
                item.setBackground(row_color)
    
    def clear_data(self):
        """Очистить данные таблицы"""
        self.setRowCount(0)

class SummaryPanel(QFrame):
    """Панель сводки"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setup_ui(title)
    
    def setup_ui(self, title):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title_label = QLabel(title)
        title_label.setProperty("class", "subsection-title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Контейнер для статистических карточек
        self.stats_layout = QHBoxLayout()
        layout.addLayout(self.stats_layout)
    
    def add_stat(self, title, value, icon="📊", color="primary"):
        """Добавить статистику"""
        stat_card = StatCard(title, value, icon, color)
        self.stats_layout.addWidget(stat_card)
        return stat_card
    
    def add_spacer(self):
        """Добавить разделитель"""
        self.stats_layout.addStretch()

class ModernDialog(QDialog):
    """Современный диалог"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumSize(400, 300)
        self.setup_base_ui()
    
    def setup_base_ui(self):
        """Базовая настройка UI"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Контейнер для содержимого
        self.content_frame = QFrame()
        self.content_frame.setProperty("class", "card")
        self.content_layout = QVBoxLayout(self.content_frame)
        self.main_layout.addWidget(self.content_frame)
        
        # Кнопки
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)
    
    def add_content_widget(self, widget):
        """Добавить виджет в содержимое"""
        self.content_layout.addWidget(widget)
    
    def add_button(self, text, callback, button_class=""):
        """Добавить кнопку"""
        button = QPushButton(text)
        if button_class:
            button.setProperty("class", button_class)
        button.clicked.connect(callback)
        self.button_layout.addWidget(button)
        return button

class ProgressCard(QFrame):
    """Карточка с прогресс-баром"""
    
    def __init__(self, title, current, maximum, unit="", parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setup_ui(title, current, maximum, unit)
    
    def setup_ui(self, title, current, maximum, unit):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title_label = QLabel(title)
        title_label.setProperty("class", "stat-label")
        layout.addWidget(title_label)
        
        # Прогресс-бар
        self.progress = QProgressBar()
        self.progress.setMaximum(maximum)
        self.progress.setValue(current)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                text-align: center;
                background: #F5F5F5;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #4CAF50, stop: 1 #2E7D32);
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress)
        
        # Значения
        self.value_label = QLabel(f"{current} / {maximum} {unit}")
        self.value_label.setProperty("class", "stat-value")
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
    
    def update_progress(self, current, maximum=None, unit=""):
        """Обновить прогресс"""
        if maximum is not None:
            self.progress.setMaximum(maximum)
        
        self.progress.setValue(current)
        max_val = maximum if maximum is not None else self.progress.maximum()
        self.value_label.setText(f"{current} / {max_val} {unit}") 
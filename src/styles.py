# -*- coding: utf-8 -*-
"""
Стили для современного интерфейса приложения автозапчастей
"""

# Основная тема приложения
MAIN_STYLE = """
QMainWindow {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #f8f9fa, stop: 1 #e9ecef);
    color: #212529;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9pt;
}

/* Заголовок приложения */
QLabel#main_title {
    color: #1976D2;
    font-size: 24pt;
    font-weight: bold;
    padding: 20px;
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #E3F2FD, stop: 1 #BBDEFB);
    border-radius: 10px;
    margin: 5px;
}

/* Вкладки */
QTabWidget::pane {
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background: white;
    margin-top: 5px;
}

QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #F5F5F5, stop: 1 #E0E0E0);
    border: 2px solid #BDBDBD;
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    padding: 12px 20px;
    margin-right: 2px;
    font-weight: bold;
    color: #424242;
}

QTabBar::tab:selected {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #2196F3, stop: 1 #1976D2);
    color: white;
    border-color: #1565C0;
}

QTabBar::tab:hover:!selected {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #E3F2FD, stop: 1 #BBDEFB);
    color: #1976D2;
}
"""

# Стили для кнопок
BUTTON_STYLES = """
/* Основные кнопки */
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #42A5F5, stop: 1 #1E88E5);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
}

QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #64B5F6, stop: 1 #2196F3);
}

QPushButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #1976D2, stop: 1 #1565C0);
}

QPushButton:disabled {
    background: #E0E0E0;
    color: #9E9E9E;
}

/* Кнопки успеха (зеленые) */
QPushButton[class="success"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #66BB6A, stop: 1 #43A047);
}

QPushButton[class="success"]:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #81C784, stop: 1 #4CAF50);
}

/* Кнопки предупреждения (оранжевые) */
QPushButton[class="warning"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #FFA726, stop: 1 #FF9800);
}

QPushButton[class="warning"]:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #FFB74D, stop: 1 #FFA726);
}

/* Кнопки опасности (красные) */
QPushButton[class="danger"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #EF5350, stop: 1 #E53935);
}

QPushButton[class="danger"]:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #F44336, stop: 1 #D32F2F);
}

/* Маленькие кнопки */
QPushButton[class="small"] {
    padding: 4px 8px;
    font-size: 8pt;
    min-width: 30px;
}

/* Большие кнопки */
QPushButton[class="large"] {
    padding: 12px 24px;
    font-size: 11pt;
    min-width: 120px;
}
"""

# Стили для таблиц
TABLE_STYLES = """
QTableWidget {
    background-color: white;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    gridline-color: #F5F5F5;
    selection-background-color: #E3F2FD;
    selection-color: #1976D2;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #F0F0F0;
}

QTableWidget::item:selected {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #E3F2FD, stop: 1 #BBDEFB);
    color: #1976D2;
}

QTableWidget::item:hover {
    background-color: #F5F5F5;
}

QHeaderView::section {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #F8F9FA, stop: 1 #E9ECEF);
    color: #495057;
    border: 1px solid #DEE2E6;
    padding: 10px;
    font-weight: bold;
    text-align: center;
}

QHeaderView::section:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #E9ECEF, stop: 1 #DEE2E6);
}
"""

# Стили для форм
FORM_STYLES = """
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    border: 2px solid #E0E0E0;
    border-radius: 6px;
    padding: 8px;
    background: white;
    selection-background-color: #2196F3;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border-color: #2196F3;
    background: #F3F8FF;
}

QLineEdit:hover, QTextEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {
    border-color: #BDBDBD;
}

QComboBox::drop-down {
    border: none;
    background: transparent;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #757575;
    margin: 0 5px;
}

QComboBox QAbstractItemView {
    border: 2px solid #E0E0E0;
    border-radius: 6px;
    background: white;
    selection-background-color: #E3F2FD;
}
"""

# Стили для группировки
GROUP_STYLES = """
QGroupBox {
    font-weight: bold;
    color: #424242;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    margin: 10px 0;
    padding-top: 15px;
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #FAFAFA, stop: 1 #F5F5F5);
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px;
    color: #1976D2;
    background: white;
    border-radius: 4px;
}

QFrame[class="notification"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #FFF8E1, stop: 1 #FFF3C4);
    border: 2px solid #FFB300;
    border-radius: 8px;
    margin: 5px;
    padding: 5px;
}

QFrame[class="card"] {
    background: white;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    margin: 5px;
    padding: 10px;
}
"""

# Стили для специальных элементов
SPECIAL_STYLES = """
/* Статистические метки */
QLabel[class="stat-value"] {
    color: #1976D2;
    font-weight: bold;
    font-size: 11pt;
}

QLabel[class="stat-label"] {
    color: #666;
    font-size: 9pt;
}

/* Статус-бар */
QStatusBar {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #F8F9FA, stop: 1 #E9ECEF);
    border-top: 1px solid #DEE2E6;
    color: #495057;
    font-weight: bold;
}

/* Итоговые суммы */
QLabel[class="total"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #E8F5E8, stop: 1 #C8E6C9);
    border: 2px solid #4CAF50;
    border-radius: 8px;
    padding: 12px;
    font-size: 14pt;
    font-weight: bold;
    color: #2E7D32;
    text-align: center;
}

/* Разделители */
QSplitter::handle {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #E0E0E0, stop: 0.5 #BDBDBD, stop: 1 #E0E0E0);
    width: 3px;
    border-radius: 1px;
}

QSplitter::handle:hover {
    background: #2196F3;
}

/* Прокрутка */
QScrollBar:vertical {
    background: #F5F5F5;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #BDBDBD, stop: 1 #9E9E9E);
    border-radius: 6px;
    min-height: 20px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #2196F3, stop: 1 #1976D2);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""

# Анимационные эффекты (через CSS)
ANIMATION_STYLES = """
QPushButton {
    transition: all 0.2s ease;
}

QLineEdit, QTextEdit, QComboBox {
    transition: border-color 0.2s ease, background-color 0.2s ease;
}

QTableWidget::item {
    transition: background-color 0.2s ease;
}
"""

# Объединяем все стили
def get_complete_style():
    """Получить полный набор стилей"""
    return f"""
    {MAIN_STYLE}
    {BUTTON_STYLES}
    {TABLE_STYLES}
    {FORM_STYLES}
    {GROUP_STYLES}
    {SPECIAL_STYLES}
    {ANIMATION_STYLES}
    """

# Цветовая схема
COLORS = {
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'primary_light': '#BBDEFB',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
    'info': '#00BCD4',
    'light': '#F8F9FA',
    'dark': '#212529',
    'secondary': '#6C757D'
}

# Размеры
SIZES = {
    'border_radius': 8,
    'padding_small': 4,
    'padding_medium': 8,
    'padding_large': 12,
    'font_small': 8,
    'font_medium': 9,
    'font_large': 11
} 
# -*- coding: utf-8 -*-
"""
Расширенные стили для максимально современного интерфейса
"""

# Основная тема с улучшенными градиентами
ENHANCED_MAIN_STYLE = """
QMainWindow {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #f8f9fa, stop: 0.5 #f1f3f4, stop: 1 #e8eaed);
    color: #202124;
}

QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
    font-size: 9pt;
    font-weight: 400;
}

/* Улучшенный заголовок */
QLabel#main_title {
    color: #1565C0;
    font-size: 28pt;
    font-weight: 300;
    letter-spacing: -1px;
    padding: 25px;
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #E3F2FD, stop: 0.3 #BBDEFB, stop: 0.7 #90CAF9, stop: 1 #64B5F6);
    border-radius: 15px;
    margin: 8px;
    border: 1px solid rgba(25, 118, 210, 0.2);
}

/* Улучшенные вкладки */
QTabWidget::pane {
    border: none;
    background: transparent;
    margin-top: 10px;
    border-top: 3px solid #e8eaed;
    border-radius: 0 0 12px 12px;
    padding-top: 15px;
}

QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #ffffff, stop: 1 #f5f5f5);
    border: 2px solid #e0e0e0;
    border-bottom: none;
    border-radius: 12px 12px 0 0;
    padding: 15px 25px;
    margin-right: 3px;
    font-weight: 500;
    font-size: 10pt;
    color: #5f6368;
    min-width: 120px;
    text-align: center;
}

QTabBar::tab:selected {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #2196F3, stop: 0.5 #1976D2, stop: 1 #1565C0);
    color: white;
    border-color: #1565C0;
    font-weight: 600;
    /* transform убран - не поддерживается в QSS */
}

QTabBar::tab:hover:!selected {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #f8f9fa, stop: 1 #e3f2fd);
    color: #1976D2;
    border-color: #90CAF9;
}
"""

# Улучшенные кнопки с тенями
ENHANCED_BUTTON_STYLES = """
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #42A5F5, stop: 0.5 #2196F3, stop: 1 #1E88E5);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 9pt;
    min-width: 90px;
    text-align: center;
}

QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #64B5F6, stop: 0.5 #42A5F5, stop: 1 #2196F3);
    /* transform убран - не поддерживается в QSS */
}

QPushButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #1976D2, stop: 0.5 #1565C0, stop: 1 #0D47A1);
    /* transform убран - не поддерживается в QSS */
}

QPushButton:disabled {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #f5f5f5, stop: 1 #e0e0e0);
    color: #9e9e9e;
}

/* Кнопки успеха */
QPushButton[class="success"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #66BB6A, stop: 0.5 #4CAF50, stop: 1 #43A047);
}

QPushButton[class="success"]:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #81C784, stop: 0.5 #66BB6A, stop: 1 #4CAF50);
}

/* Кнопки предупреждения */
QPushButton[class="warning"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #FFB74D, stop: 0.5 #FFA726, stop: 1 #FF9800);
}

QPushButton[class="warning"]:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #FFCC02, stop: 0.5 #FFB74D, stop: 1 #FFA726);
}

/* Кнопки опасности */
QPushButton[class="danger"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #EF5350, stop: 0.5 #F44336, stop: 1 #E53935);
}

QPushButton[class="danger"]:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #FF5722, stop: 0.5 #EF5350, stop: 1 #F44336);
}

/* Большие кнопки */
QPushButton[class="large"] {
    padding: 15px 30px;
    font-size: 11pt;
    font-weight: 600;
    min-width: 150px;
    border-radius: 10px;
}

/* Маленькие кнопки */
QPushButton[class="small"] {
    padding: 6px 12px;
    font-size: 8pt;
    min-width: 50px;
    border-radius: 6px;
}
"""

# Улучшенные таблицы
ENHANCED_TABLE_STYLES = """
QTableWidget {
    background-color: white;
    border: none;
    border-radius: 12px;
    gridline-color: #f0f0f0;
    selection-background-color: #e3f2fd;
    selection-color: #1976d2;
    font-size: 9pt;
    alternate-background-color: #fafafa;
}

/* Отключаем зачеркивание для элементов таблиц (убран !important) */
QTableWidget * {
    color: #202124;
}

QTableWidget QTableWidgetItem {
    color: #202124;
}

QTableWidget::item {
    padding: 15px 12px;
    border-bottom: 1px solid #f0f0f0;
    border-right: 1px solid #f8f8f8;
    text-decoration: none;
}

QTableWidget::item:selected {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #e3f2fd, stop: 1 #bbdefb);
    color: #1976d2;
    border: none;
    text-decoration: none;
}

QTableWidget::item:hover {
    background-color: #f5f5f5;
    text-decoration: none;
}

QHeaderView::section {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #fafafa, stop: 1 #f0f0f0);
    color: #424242;
    border: none;
    border-right: 1px solid #e0e0e0;
    border-bottom: 2px solid #e0e0e0;
    padding: 15px 12px;
    font-weight: 600;
    font-size: 9pt;
    text-align: left;
}

QHeaderView::section:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #f0f0f0, stop: 1 #e8e8e8);
}

QHeaderView::section:first {
    border-top-left-radius: 12px;
}

QHeaderView::section:last {
    border-top-right-radius: 12px;
    border-right: none;
}
"""

# Улучшенные формы
ENHANCED_FORM_STYLES = """
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px;
    background: white;
    font-size: 10pt;
    selection-background-color: #2196f3;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #2196f3;
    background: #fafafa;
    outline: none;
}

QLineEdit:hover, QTextEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: #90caf9;
}

QComboBox {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px;
    background: white;
    font-size: 10pt;
    min-width: 100px;
}

QComboBox:focus {
    border-color: #2196f3;
    background: #fafafa;
}

QComboBox:hover {
    border-color: #90caf9;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
    background: transparent;
}

QComboBox::down-arrow {
    image: none;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 6px solid #757575;
    margin: 0 8px;
}

QComboBox QAbstractItemView {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    background: white;
    selection-background-color: #e3f2fd;
    padding: 5px;
}

QComboBox QAbstractItemView::item {
    padding: 10px;
    border-radius: 4px;
    margin: 2px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #f5f5f5;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}
"""

# Карточные группы
ENHANCED_GROUP_STYLES = """
QGroupBox {
    font-weight: 600;
    font-size: 11pt;
    color: #424242;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    margin: 15px 5px;
    padding-top: 20px;
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #ffffff, stop: 1 #fafafa);
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 5px 15px;
    color: #1976d2;
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-weight: 600;
}

/* Карточки */
QFrame[class="card"] {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    margin: 8px;
    padding: 20px;
}

QFrame[class="stat-card"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #ffffff, stop: 1 #f8f9fa);
    border: 1px solid #e8eaed;
    border-radius: 12px;
    padding: 20px;
    margin: 10px;
    min-height: 80px;
}

QFrame[class="notification"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #fff8e1, stop: 1 #fff3c4);
    border: 2px solid #ffb300;
    border-radius: 10px;
    margin: 8px;
    padding: 15px;
}
"""

# Специальные элементы
ENHANCED_SPECIAL_STYLES = """
/* Статистические метки */
QLabel[class="stat-value"] {
    color: #1976d2;
    font-weight: 700;
    font-size: 24pt;
    text-align: center;
}

QLabel[class="stat-label"] {
    color: #5f6368;
    font-size: 10pt;
    font-weight: 500;
    text-align: center;
    margin-top: 5px;
}

QLabel[class="section-title"] {
    color: #202124;
    font-size: 16pt;
    font-weight: 600;
    margin: 10px 0;
}

QLabel[class="subsection-title"] {
    color: #5f6368;
    font-size: 12pt;
    font-weight: 500;
    margin: 8px 0;
}

/* Итоговые суммы */
QLabel[class="total"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #e8f5e8, stop: 0.5 #c8e6c9, stop: 1 #a5d6a7);
    border: 2px solid #4caf50;
    border-radius: 12px;
    padding: 20px;
    font-size: 16pt;
    font-weight: 700;
    color: #1b5e20;
    text-align: center;
    margin: 10px;
}

/* Статус-бар */
QStatusBar {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #fafafa, stop: 1 #f0f0f0);
    border-top: 1px solid #e0e0e0;
    color: #5f6368;
    font-weight: 500;
    padding: 8px;
}

/* Разделители */
QSplitter::handle {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #f0f0f0, stop: 0.5 #e0e0e0, stop: 1 #f0f0f0);
    width: 4px;
    border-radius: 2px;
    margin: 2px;
}

QSplitter::handle:hover {
    background: #2196f3;
}

/* Прокрутка */
QScrollBar:vertical {
    background: #f8f9fa;
    width: 14px;
    border-radius: 7px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #e0e0e0, stop: 1 #bdbdbd);
    border-radius: 7px;
    min-height: 30px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #2196f3, stop: 1 #1976d2);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: #f8f9fa;
    height: 14px;
    border-radius: 7px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #e0e0e0, stop: 1 #bdbdbd);
    border-radius: 7px;
    min-width: 30px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #2196f3, stop: 1 #1976d2);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}
"""

# Диалоги
ENHANCED_DIALOG_STYLES = """
QDialog {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #fafafa, stop: 1 #f0f0f0);
    border-radius: 12px;
}

QDialogButtonBox QPushButton {
    min-width: 100px;
    padding: 10px 20px;
    margin: 5px;
}
"""

# Объединяем все стили
def get_enhanced_complete_style():
    """Получить полный набор улучшенных стилей"""
    # Пробуем использовать новый загрузчик стилей
    try:
        # Пробуем разные варианты импорта
        try:
            from .style_loader import StyleLoader
        except ImportError:
            from style_loader import StyleLoader
        
        modern_styles = StyleLoader.get_modern_styles()
        if modern_styles.strip():
            return modern_styles
    except ImportError:
        print("ℹ️ Загрузчик стилей недоступен, используем встроенные стили")
    except Exception as e:
        print(f"⚠️ Ошибка загрузки современных стилей: {e}")
    
    # Fallback на старые стили
    return f"""
    {ENHANCED_MAIN_STYLE}
    {ENHANCED_BUTTON_STYLES}
    {ENHANCED_TABLE_STYLES}
    {ENHANCED_FORM_STYLES}
    {ENHANCED_GROUP_STYLES}
    {ENHANCED_SPECIAL_STYLES}
    {ENHANCED_DIALOG_STYLES}
    """

# Расширенная цветовая схема
ENHANCED_COLORS = {
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'primary_light': '#BBDEFB',
    'primary_pale': '#E3F2FD',
    'success': '#4CAF50',
    'success_light': '#81C784',
    'warning': '#FF9800',
    'warning_light': '#FFB74D',
    'danger': '#F44336',
    'danger_light': '#EF5350',
    'info': '#00BCD4',
    'light': '#FAFAFA',
    'lighter': '#F8F9FA',
    'dark': '#202124',
    'secondary': '#5F6368',
    'border': '#E0E0E0',
    'border_light': '#F0F0F0'
}

# Иконки для разных элементов
ICONS = {
    'parts': '🔧',
    'sales': '💰', 
    'receipts': '📦',
    'reports': '📊',
    'search': '🔍',
    'add': '➕',
    'edit': '✏️',
    'delete': '🗑️',
    'save': '💾',
    'cart': '🛒',
    'checkout': '💳',
    'refresh': '🔄',
    'export': '📤',
    'import': '📥',
    'settings': '⚙️',
    'info': 'ℹ️',
    'warning': '⚠️',
    'success': '✅',
    'error': '❌',
    'money': '💵',
    'stats': '📈',
    'calendar': '📅',
    'document': '📄',
    'folder': '📁'
} 
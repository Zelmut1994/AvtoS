# -*- coding: utf-8 -*-
"""
Утилиты для создания красивого UI
"""

from PySide6.QtWidgets import QGroupBox, QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

def create_card_widget():
    """Создать карту-виджет с современным стилем"""
    card = QFrame()
    card.setProperty("class", "card")
    return card

def create_stat_card(title, value, icon="📊"):
    """Создать карту статистики"""
    card = create_card_widget()
    layout = QVBoxLayout(card)
    layout.setSpacing(5)
    
    # Иконка и заголовок
    header = QHBoxLayout()
    header.addWidget(QLabel(icon))
    title_label = QLabel(title)
    title_label.setProperty("class", "stat-label")
    header.addWidget(title_label)
    header.addStretch()
    layout.addLayout(header)
    
    # Значение
    value_label = QLabel(str(value))
    value_label.setProperty("class", "stat-value")
    value_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(value_label)
    
    return card

def create_styled_group(title, icon="📁"):
    """Создать стильную группу"""
    group = QGroupBox(f"{icon} {title}")
    return group

def create_notification_frame():
    """Создать фрейм уведомления"""
    frame = QFrame()
    frame.setProperty("class", "notification")
    return frame

def add_icons_to_headers():
    """Словарь иконок для заголовков (устарело - используйте modern_widgets)"""
    return {
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
        'warning': '⚠️',
        'success': '✅',
        'error': '❌',
        'info': 'ℹ️'
    }

# Новые функции для современных виджетов
def get_modern_button(text: str, icon_name: str = "", style_class: str = ""):
    """Создать современную кнопку с иконкой"""
    try:
        from .modern_widgets import ModernButton
        button = ModernButton(text, icon_name)
        if style_class:
            button.setProperty("styleClass", style_class)
        return button
    except ImportError:
        from PySide6.QtWidgets import QPushButton
        return QPushButton(f"{add_icons_to_headers().get(icon_name, '')} {text}")

def get_modern_search_bar(placeholder: str = "Поиск..."):
    """Создать современную строку поиска"""
    try:
        from .modern_widgets import ModernSearchBar
        return ModernSearchBar(placeholder)
    except ImportError:
        from PySide6.QtWidgets import QLineEdit
        search = QLineEdit()
        search.setPlaceholderText(placeholder)
        return search

def style_button(button, button_type="default"):
    """Применить стиль к кнопке"""
    type_mapping = {
        'success': 'success',
        'warning': 'warning', 
        'danger': 'danger',
        'primary': '',
        'large': 'large',
        'small': 'small'
    }
    
    if button_type in type_mapping:
        if type_mapping[button_type]:
            button.setProperty("class", type_mapping[button_type])

def create_modern_table_style():
    """Получить стили для современных таблиц"""
    return """
    QTableWidget {
        background-color: white;
        border: 2px solid #E0E0E0;
        border-radius: 12px;
        gridline-color: #F5F5F5;
        selection-background-color: #E3F2FD;
        selection-color: #1976D2;
        font-size: 9pt;
    }
    
    QTableWidget::item {
        padding: 12px 8px;
        border-bottom: 1px solid #F0F0F0;
    }
    
    QTableWidget::item:selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #E3F2FD, stop: 1 #BBDEFB);
        color: #1976D2;
        border: none;
    }
    
    QTableWidget::item:hover {
        background-color: #F8F9FA;
    }
    
    QHeaderView::section {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #F8F9FA, stop: 1 #E9ECEF);
        color: #495057;
        border: 1px solid #DEE2E6;
        padding: 12px 8px;
        font-weight: bold;
        text-align: center;
        font-size: 9pt;
    }
    
    QHeaderView::section:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #E9ECEF, stop: 1 #DEE2E6);
    }
    """

def apply_modern_styling(widget):
    """Применить современные стили к виджету"""
    try:
        from styles_enhanced import get_enhanced_complete_style
        widget.setStyleSheet(get_enhanced_complete_style())
    except ImportError:
        # Базовые стили если enhanced стили недоступны
        widget.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                color: #212529;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                color: #495057;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #212529;
                border-bottom: 2px solid #007bff;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """) 
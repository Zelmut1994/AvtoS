"""
Простой загрузчик иконок без SVG зависимостей
"""

from typing import Dict
from PySide6.QtGui import QIcon, QPixmap, QPainter, QFont, QColor
from PySide6.QtCore import Qt, QRect


class SimpleIconLoader:
    """Простой загрузчик иконок с текстовыми символами"""
    
    _icon_cache: Dict[str, QIcon] = {}
    
    # Мапинг иконок к Unicode символам
    ICON_SYMBOLS = {
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
    
    @classmethod
    def get_icon(cls, icon_name: str, color: str = "#2196F3", size: int = 24) -> QIcon:
        """
        Получить QIcon с текстовым символом
        
        Args:
            icon_name: Имя иконки
            color: Цвет иконки (не используется для эмоджи)
            size: Размер иконки в пикселях
            
        Returns:
            QIcon объект
        """
        cache_key = f"{icon_name}_{size}"
        
        if cache_key in cls._icon_cache:
            return cls._icon_cache[cache_key]
        
        symbol = cls.ICON_SYMBOLS.get(icon_name, '📁')
        
        # Гарантируем, что размер корректный
        size = max(1, size) 
        
        # Создаем пиксмап с символом
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        # Проверяем, что пиксмап создан успешно
        if pixmap.isNull():
            print(f"⚠️ Ошибка: не удалось создать QPixmap для иконки '{icon_name}' размером {size}x{size}")
            # Возвращаем пустую иконку как fallback
            return QIcon()

        painter = QPainter()
        # Используем явный begin/end для безопасной отрисовки
        if painter.begin(pixmap):
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Настраиваем шрифт
            font = QFont()
            font.setPixelSize(int(size * 0.8))  # 80% от размера
            painter.setFont(font)
            
            # Рисуем символ по центру
            rect = QRect(0, 0, size, size)
            painter.drawText(rect, Qt.AlignCenter, symbol)
            painter.end()
        else:
            print(f"⚠️ Ошибка: QPainter.begin() не удался для иконки '{icon_name}'")

        icon = QIcon(pixmap)
        cls._icon_cache[cache_key] = icon
        return icon
    
    @classmethod
    def get_pixmap(cls, icon_name: str, color: str = "#2196F3", size: int = 24) -> QPixmap:
        """Получить QPixmap с иконкой"""
        icon = cls.get_icon(icon_name, color, size)
        return icon.pixmap(size, size)
    
    @classmethod
    def clear_cache(cls):
        """Очистить кэш иконок"""
        cls._icon_cache.clear()

# Удобные функции
def get_icon(name: str, color: str = "#2196F3", size: int = 24) -> QIcon:
    """Быстрый доступ к получению иконки"""
    return SimpleIconLoader.get_icon(name, color, size)

def get_pixmap(name: str, color: str = "#2196F3", size: int = 24) -> QPixmap:
    """Быстрый доступ к получению пиксмапа"""
    return SimpleIconLoader.get_pixmap(name, color, size) 
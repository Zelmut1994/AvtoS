"""
Загрузчик SVG иконок
"""

import os
from typing import Dict, Optional
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtSvg import QSvgRenderer


class IconLoader:
    """Загрузчик SVG иконок"""
    
    _icon_cache: Dict[str, QIcon] = {}
    _icon_paths: Dict[str, str] = {}
    
    @classmethod
    def _initialize_paths(cls):
        """Инициализация путей к иконкам"""
        if cls._icon_paths:
            return
            
        # Мапинг имён иконок к файлам
        icon_mapping = {
            'parts': 'parts.svg',
            'sales': 'sales.svg', 
            'receipts': 'parts.svg',  # Используем иконку запчастей
            'reports': 'reports.svg',
            'search': 'search.svg',
            'add': 'add.svg',
            'edit': 'edit.svg',
            'delete': 'delete.svg',
            'save': 'save.svg',
            'cart': 'cart.svg',
            'checkout': 'sales.svg',  # Используем иконку продаж
            'refresh': 'refresh.svg',
            'export': 'save.svg',  # Используем иконку сохранения
            'import': 'add.svg',   # Используем иконку добавления
            'settings': 'edit.svg',  # Используем иконку редактирования
            'info': 'reports.svg',   # Используем иконку отчётов
            'warning': 'reports.svg',
            'success': 'reports.svg',
            'error': 'delete.svg',   # Используем иконку удаления
            'money': 'sales.svg',
            'stats': 'reports.svg',
            'calendar': 'reports.svg',
            'document': 'reports.svg',
            'folder': 'reports.svg'
        }
        
        # Пробуем сначала ресурсы, потом файлы
        for name, filename in icon_mapping.items():
            # Ресурсный путь
            resource_path = f":/icons/{filename}"
            cls._icon_paths[name] = resource_path
            
            # Проверяем существование файла как fallback
            base_dir = os.path.dirname(os.path.dirname(__file__))
            filepath = os.path.join(base_dir, "resources", "icons", filename)
            if not os.path.exists(filepath):
                print(f"⚠️ Файл иконки не найден: {filepath}")

    @classmethod
    def get_icon(cls, icon_name: str, color: str = "#2196F3", size: int = 24) -> QIcon:
        """
        Получить QIcon из SVG файла
        
        Args:
            icon_name: Имя иконки
            color: Цвет иконки (CSS/hex)
            size: Размер иконки в пикселях
            
        Returns:
            QIcon объект
        """
        cls._initialize_paths()
        
        # Создаем уникальный ключ для кэша
        cache_key = f"{icon_name}_{color}_{size}"
        
        if cache_key in cls._icon_cache:
            return cls._icon_cache[cache_key]
        
        icon_path = cls._icon_paths.get(icon_name)
        if not icon_path:
            print(f"⚠️ Иконка '{icon_name}' не найдена")
            return cls._create_fallback_icon(size)
        
        try:
            # Пробуем сначала ресурсный путь, потом файловый
            renderer = QSvgRenderer(icon_path)
            
            # Если ресурс не работает, пробуем файл
            if not renderer.isValid():
                base_dir = os.path.dirname(os.path.dirname(__file__))
                file_path = os.path.join(base_dir, "resources", "icons", 
                                       os.path.basename(icon_path))
                if os.path.exists(file_path):
                    renderer = QSvgRenderer(file_path)
            
            if not renderer.isValid():
                print(f"⚠️ Не удалось загрузить SVG: {icon_path}")
                return cls._create_fallback_icon(size)
            
            # --- Безопасная отрисовка ---
            size = max(1, size) # Гарантируем, что размер не нулевой
            
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)

            if pixmap.isNull():
                print(f"⚠️ Ошибка: не удалось создать QPixmap для иконки '{icon_name}'")
                return QIcon()

            painter = QPainter()
            if painter.begin(pixmap):
                painter.setRenderHint(QPainter.Antialiasing, True)
                painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

                # Рисуем SVG
                renderer.render(painter)
                
                # Накладываем цвет, если он задан
                if color:
                    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
                    painter.fillRect(pixmap.rect(), QColor(color))
                
                painter.end()
            else:
                print(f"⚠️ Ошибка: QPainter.begin() не удался для иконки '{icon_name}'")

            icon = QIcon(pixmap)
            cls._icon_cache[cache_key] = icon
            return icon
            
        except Exception as e:
            print(f"❌ Ошибка загрузки иконки {icon_name}: {e}")
            return cls._create_fallback_icon(size)
    
    @classmethod
    def _create_fallback_icon(cls, size: int = 24) -> QIcon:
        """Создать запасную иконку"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.gray)
        return QIcon(pixmap)
    
    @classmethod
    def get_pixmap(cls, icon_name: str, color: str = "#2196F3", size: int = 24) -> QPixmap:
        """
        Получить QPixmap из SVG файла
        
        Args:
            icon_name: Имя иконки
            color: Цвет иконки
            size: Размер иконки
            
        Returns:
            QPixmap объект
        """
        icon = cls.get_icon(icon_name, color, size)
        return icon.pixmap(size, size)
    
    @classmethod
    def clear_cache(cls):
        """Очистить кэш иконок"""
        cls._icon_cache.clear()
    
    @classmethod
    def get_available_icons(cls) -> list:
        """Получить список доступных иконок"""
        cls._initialize_paths()
        return list(cls._icon_paths.keys())

# Удобные функции для быстрого доступа
def get_icon(name: str, color: str = "#2196F3", size: int = 24) -> QIcon:
    """Быстрый доступ к получению иконки"""
    return IconLoader.get_icon(name, color, size)

def get_pixmap(name: str, color: str = "#2196F3", size: int = 24) -> QPixmap:
    """Быстрый доступ к получению пиксмапа"""
    return IconLoader.get_pixmap(name, color, size) 
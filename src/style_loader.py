"""
Загрузчик стилей из QSS файлов
"""

import os
from typing import Optional
from PySide6.QtCore import QFile, QTextStream


class StyleLoader:
    """Загрузчик стилей из файлов"""
    
    @staticmethod
    def load_qss_from_file(filepath: str) -> str:
        """
        Загружает QSS стили из файла
        
        Args:
            filepath: Путь к QSS файлу
            
        Returns:
            Содержимое QSS файла как строка
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"❌ Ошибка загрузки стилей из {filepath}: {e}")
            return ""
    
    @staticmethod
    def load_qss_from_resource(resource_path: str) -> str:
        """
        Загружает QSS стили из ресурса Qt
        
        Args:
            resource_path: Путь к ресурсу (например, ":/styles/main.qss")
            
        Returns:
            Содержимое QSS файла как строка
        """
        try:
            file = QFile(resource_path)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                return stream.readAll()
            else:
                print(f"❌ Не удалось открыть ресурс: {resource_path}")
                return ""
        except Exception as e:
            print(f"❌ Ошибка загрузки стилей из ресурса {resource_path}: {e}")
            return ""
    
    @staticmethod
    def get_combined_styles(use_resources: bool = False) -> str:
        """
        Получает объединённые стили из всех QSS файлов
        
        Args:
            use_resources: Использовать ресурсы Qt (True) или файлы (False)
            
        Returns:
            Объединённые стили как строка
        """
        if use_resources:
            # Загрузка из скомпилированных ресурсов
            style_files = [
                ":/styles/main.qss",
                ":/styles/tabs.qss", 
                ":/styles/buttons.qss",
                ":/styles/tables.qss",
                ":/styles/forms.qss"
            ]
            
            combined_styles = ""
            for resource_path in style_files:
                style = StyleLoader.load_qss_from_resource(resource_path)
                if style:
                    combined_styles += f"\n/* {resource_path} */\n"
                    combined_styles += style + "\n"
            
            return combined_styles
        else:
            # Загрузка из файлов (для разработки)
            base_dir = os.path.dirname(os.path.dirname(__file__))  # корень проекта
            style_dir = os.path.join(base_dir, "resources", "styles")
            
            style_files = [
                "main.qss",
                "tabs.qss",
                "buttons.qss", 
                "tables.qss",
                "forms.qss"
            ]
            
            combined_styles = ""
            for filename in style_files:
                filepath = os.path.join(style_dir, filename)
                if os.path.exists(filepath):
                    style = StyleLoader.load_qss_from_file(filepath)
                    if style:
                        combined_styles += f"\n/* {filename} */\n"
                        combined_styles += style + "\n"
                else:
                    print(f"⚠️ Файл стилей не найден: {filepath}")
            
            return combined_styles

    @staticmethod
    def get_modern_styles() -> str:
        """
        Получает современные стили (основная функция для использования)
        
        Returns:
            Готовые к использованию стили
        """
        # Импортируем ресурсы (это подключает их к Qt)
        try:
            # Проверяем, что Qt приложение инициализировано
            from PySide6.QtWidgets import QApplication
            if QApplication.instance() is None:
                print("⚠️ Qt приложение не инициализировано, ресурсы могут не работать")
            
            import resources_rc
            print("✅ Ресурсы Qt подключены")
        except ImportError:
            print("⚠️ Скомпилированные ресурсы не найдены")
        
        # Сначала пытаемся загрузить из ресурсов, затем из файлов
        styles = StyleLoader.get_combined_styles(use_resources=True)
        
        if not styles.strip():
            print("ℹ️ Ресурсы не найдены, загружаем стили из файлов...")
            styles = StyleLoader.get_combined_styles(use_resources=False)
        
        if styles.strip():
            print("✅ Стили успешно загружены")
        else:
            print("❌ Не удалось загрузить стили")
            # Возвращаем базовые стили как fallback
            return StyleLoader._get_fallback_styles()
        
        return styles
    
    @staticmethod
    def _get_fallback_styles() -> str:
        """Базовые стили как резервный вариант"""
        return """
        QMainWindow {
            background-color: #f5f5f5;
            color: #333;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 9pt;
        }
        
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #1976D2;
        }
        
        QPushButton:pressed {
            background-color: #1565C0;
        }
        
        QTableWidget {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 6px;
            selection-background-color: #e3f2fd;
        }
        
        QLineEdit, QTextEdit, QComboBox {
            border: 2px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            background-color: white;
        }
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border-color: #2196F3;
        }
        """ 
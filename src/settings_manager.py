"""
Система управления настройками приложения
"""

import os
from typing import Any, Optional
from PySide6.QtCore import QSettings, QStandardPaths
from PySide6.QtWidgets import QApplication


class SettingsManager:
    """Менеджер настроек приложения"""
    
    def __init__(self):
        # Настройки Qt
        self.settings = QSettings("AutoParts", "AutoParts")
        
        # Пути по умолчанию
        self.app_data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        self.ensure_app_directories()
    
    def ensure_app_directories(self):
        """Создать необходимые директории приложения"""
        directories = [
            self.app_data_dir,
            os.path.join(self.app_data_dir, "backups"),
            os.path.join(self.app_data_dir, "exports"),
            os.path.join(self.app_data_dir, "logs")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    # === Настройки окна ===
    
    def save_window_geometry(self, window_name: str, geometry):
        """Сохранить геометрию окна"""
        self.settings.setValue(f"window_{window_name}/geometry", geometry)
    
    def load_window_geometry(self, window_name: str):
        """Загрузить геометрию окна"""
        return self.settings.value(f"window_{window_name}/geometry")
    
    def save_window_state(self, window_name: str, state):
        """Сохранить состояние окна (сплиттеры, панели)"""
        self.settings.setValue(f"window_{window_name}/state", state)
    
    def load_window_state(self, window_name: str):
        """Загрузить состояние окна"""
        return self.settings.value(f"window_{window_name}/state")
    
    # === Настройки интерфейса ===
    
    def get_interface_setting(self, key: str, default_value: Any = None) -> Any:
        """Получить настройку интерфейса"""
        return self.settings.value(f"interface/{key}", default_value)
    
    def set_interface_setting(self, key: str, value: Any):
        """Установить настройку интерфейса"""
        self.settings.setValue(f"interface/{key}", value)
    
    @property
    def show_welcome_dialog(self) -> bool:
        """Показывать диалог приветствия"""
        return self.get_interface_setting("show_welcome_dialog", True)
    
    @show_welcome_dialog.setter
    def show_welcome_dialog(self, value: bool):
        self.set_interface_setting("show_welcome_dialog", value)
    
    @property
    def auto_refresh_interval(self) -> int:
        """Интервал автообновления в секундах"""
        return self.get_interface_setting("auto_refresh_interval", 30)
    
    @auto_refresh_interval.setter
    def auto_refresh_interval(self, value: int):
        self.set_interface_setting("auto_refresh_interval", value)
    
    @property
    def items_per_page(self) -> int:
        """Количество элементов на странице"""
        return self.get_interface_setting("items_per_page", 50)
    
    @items_per_page.setter
    def items_per_page(self, value: int):
        self.set_interface_setting("items_per_page", value)
    
    @property
    def confirm_deletions(self) -> bool:
        """Подтверждать удаления"""
        return self.get_interface_setting("confirm_deletions", True)
    
    @confirm_deletions.setter
    def confirm_deletions(self, value: bool):
        self.set_interface_setting("confirm_deletions", value)
    
    # === Настройки базы данных ===
    
    def get_database_setting(self, key: str, default_value: Any = None) -> Any:
        """Получить настройку БД"""
        return self.settings.value(f"database/{key}", default_value)
    
    def set_database_setting(self, key: str, value: Any):
        """Установить настройку БД"""
        self.settings.setValue(f"database/{key}", value)
    
    @property
    def database_path(self) -> str:
        """Путь к файлу базы данных"""
        default_path = os.path.join(self.app_data_dir, "autoparts.db")
        return self.get_database_setting("path", default_path)
    
    @database_path.setter
    def database_path(self, value: str):
        self.set_database_setting("path", value)
    
    @property
    def auto_backup_enabled(self) -> bool:
        """Автоматическое резервное копирование включено"""
        return self.get_database_setting("auto_backup_enabled", True)
    
    @auto_backup_enabled.setter
    def auto_backup_enabled(self, value: bool):
        self.set_database_setting("auto_backup_enabled", value)
    
    @property
    def backup_interval_days(self) -> int:
        """Интервал резервного копирования в днях"""
        return self.get_database_setting("backup_interval_days", 7)
    
    @backup_interval_days.setter
    def backup_interval_days(self, value: int):
        self.set_database_setting("backup_interval_days", value)
    
    @property
    def max_backup_files(self) -> int:
        """Максимальное количество файлов резервных копий"""
        return self.get_database_setting("max_backup_files", 10)
    
    @max_backup_files.setter
    def max_backup_files(self, value: int):
        self.set_database_setting("max_backup_files", value)
    
    # === Настройки экспорта ===
    
    def get_export_setting(self, key: str, default_value: Any = None) -> Any:
        """Получить настройку экспорта"""
        return self.settings.value(f"export/{key}", default_value)
    
    def set_export_setting(self, key: str, value: Any):
        """Установить настройку экспорта"""
        self.settings.setValue(f"export/{key}", value)
    
    @property
    def default_export_format(self) -> str:
        """Формат экспорта по умолчанию"""
        return self.get_export_setting("default_format", "csv")
    
    @default_export_format.setter
    def default_export_format(self, value: str):
        self.set_export_setting("default_format", value)
    
    @property
    def export_directory(self) -> str:
        """Директория для экспорта"""
        default_dir = os.path.join(self.app_data_dir, "exports")
        return self.get_export_setting("directory", default_dir)
    
    @export_directory.setter
    def export_directory(self, value: str):
        self.set_export_setting("directory", value)
    
    # === Последние использованные значения ===
    
    def get_recent_value(self, key: str, default_value: Any = None) -> Any:
        """Получить последнее использованное значение"""
        return self.settings.value(f"recent/{key}", default_value)
    
    def set_recent_value(self, key: str, value: Any):
        """Установить последнее использованное значение"""
        self.settings.setValue(f"recent/{key}", value)
    
    def get_recent_files(self, max_files: int = 10) -> list:
        """Получить список недавних файлов"""
        recent = []
        for i in range(max_files):
            file_path = self.get_recent_value(f"file_{i}")
            if file_path and os.path.exists(file_path):
                recent.append(file_path)
        return recent
    
    def add_recent_file(self, file_path: str, max_files: int = 10):
        """Добавить файл в список недавних"""
        recent = self.get_recent_files(max_files)
        
        # Удаляем если уже есть
        if file_path in recent:
            recent.remove(file_path)
        
        # Добавляем в начало
        recent.insert(0, file_path)
        
        # Ограничиваем количество
        recent = recent[:max_files]
        
        # Сохраняем
        for i, path in enumerate(recent):
            self.set_recent_value(f"file_{i}", path)
        
        # Очищаем старые записи
        for i in range(len(recent), max_files):
            self.settings.remove(f"recent/file_{i}")
    
    # === Утилиты ===
    
    def reset_to_defaults(self):
        """Сбросить все настройки к значениям по умолчанию"""
        self.settings.clear()
        self.ensure_app_directories()
        print("✅ Настройки сброшены к значениям по умолчанию")
    
    def export_settings(self, file_path: str) -> bool:
        """Экспортировать настройки в файл"""
        try:
            # QSettings автоматически синхронизируется
            self.settings.sync()
            
            # Копируем файл настроек
            import shutil
            settings_file = self.settings.fileName()
            if os.path.exists(settings_file):
                shutil.copy2(settings_file, file_path)
                print(f"✅ Настройки экспортированы в {file_path}")
                return True
            else:
                print("⚠️ Файл настроек не найден")
                return False
        except Exception as e:
            print(f"❌ Ошибка экспорта настроек: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """Импортировать настройки из файла"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ Файл настроек не найден: {file_path}")
                return False
            
            # Создаём резервную копию текущих настроек
            backup_path = f"{self.settings.fileName()}.backup"
            import shutil
            if os.path.exists(self.settings.fileName()):
                shutil.copy2(self.settings.fileName(), backup_path)
            
            # Заменяем настройки
            shutil.copy2(file_path, self.settings.fileName())
            
            # Перезагружаем настройки
            self.settings.sync()
            
            print(f"✅ Настройки импортированы из {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка импорта настроек: {e}")
            return False
    
    def get_settings_info(self) -> dict:
        """Получить информацию о настройках"""
        return {
            "settings_file": self.settings.fileName(),
            "app_data_dir": self.app_data_dir,
            "database_path": self.database_path,
            "export_directory": self.export_directory,
            "auto_backup_enabled": self.auto_backup_enabled,
            "backup_interval_days": self.backup_interval_days,
            "items_per_page": self.items_per_page,
            "auto_refresh_interval": self.auto_refresh_interval
        }


# Глобальный экземпляр менеджера настроек
_settings_manager = None

def get_settings() -> SettingsManager:
    """Получить глобальный экземпляр менеджера настроек"""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager 
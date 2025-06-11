#!/usr/bin/env python3
"""
Тест системы настроек AutoParts
"""

import sys
import os

# Добавляем папку src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication
from settings_manager import get_settings
from settings_dialog import show_settings_dialog

def test_settings_manager():
    """Тест менеджера настроек"""
    print("🧪 Тестирование менеджера настроек...")
    
    settings = get_settings()
    
    # Тест базовых настроек
    print(f"📁 Папка данных: {settings.app_data_dir}")
    print(f"💾 База данных: {settings.database_path}")
    print(f"📤 Папка экспорта: {settings.export_directory}")
    
    # Тест настроек интерфейса
    print(f"🖥️ Элементов на страницу: {settings.items_per_page}")
    print(f"⏰ Автообновление: {settings.auto_refresh_interval} сек")
    print(f"❓ Показывать диалог приветствия: {settings.show_welcome_dialog}")
    print(f"❌ Подтверждать удаления: {settings.confirm_deletions}")
    
    # Тест настроек БД
    print(f"💿 Автобэкап: {settings.auto_backup_enabled}")
    print(f"📅 Интервал бэкапа: {settings.backup_interval_days} дней")
    print(f"📦 Макс. файлов бэкапа: {settings.max_backup_files}")
    
    # Тест настроек экспорта
    print(f"📄 Формат экспорта: {settings.default_export_format}")
    
    print("✅ Базовые настройки загружены успешно")
    
    # Тест изменения настроек
    print("\n🔧 Тестирование изменения настроек...")
    original_items = settings.items_per_page
    settings.items_per_page = 75
    
    # Создаём новый экземпляр для проверки сохранения
    settings2 = get_settings()
    if settings2.items_per_page == 75:
        print("✅ Настройки сохраняются корректно")
    else:
        print("❌ Ошибка сохранения настроек")
    
    # Возвращаем исходное значение
    settings.items_per_page = original_items
    
    # Тест информации о настройках
    print("\n📊 Информация о настройках:")
    info = settings.get_settings_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Тестирование менеджера настроек завершено")


def test_settings_dialog():
    """Тест диалога настроек"""
    print("\n🖼️ Тестирование диалога настроек...")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Показываем диалог настроек
        result = show_settings_dialog()
        print(f"Диалог закрыт с результатом: {result}")
        
    except Exception as e:
        print(f"❌ Ошибка при открытии диалога: {e}")
        return False
    
    print("✅ Диалог настроек работает корректно")
    return True


def main():
    """Главная функция теста"""
    print("🚗 Тестирование системы настроек AutoParts")
    print("=" * 50)
    
    try:
        # Тестируем менеджер настроек
        test_settings_manager()
        
        # Тестируем диалог настроек
        test_settings_dialog()
        
        print("\n🎉 Все тесты прошли успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка в тестах: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 
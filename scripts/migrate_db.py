#!/usr/bin/env python3
"""
Скрипт миграции базы данных для переименования поля model в car_model
"""

import sqlite3
import os
import shutil
from datetime import datetime

def get_data_dir():
    """Получить путь к директории данных"""
    if os.name == 'nt':  # Windows
        data_dir = os.path.join(os.environ.get('APPDATA', ''), 'AutoParts')
    else:
        data_dir = os.path.join(os.path.expanduser('~'), '.autoparts')
    return data_dir

def migrate_database():
    """Выполнить миграцию базы данных"""
    data_dir = get_data_dir()
    db_path = os.path.join(data_dir, 'autoparts.db')
    
    if not os.path.exists(db_path):
        print("❌ База данных не найдена. Создайте новую базу, запустив приложение.")
        return False
    
    # Создаём резервную копию
    backup_path = os.path.join(data_dir, f'autoparts_backup_before_migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
    shutil.copy2(db_path, backup_path)
    print(f"✅ Создана резервная копия: {backup_path}")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Проверяем, есть ли уже поле car_model
            cursor.execute("PRAGMA table_info(parts)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'car_model' in columns:
                print("✅ Поле car_model уже существует. Миграция не требуется.")
                return True
            
            if 'model' not in columns:
                print("❌ Поле model не найдено в таблице parts.")
                return False
            
            print("🔄 Выполняем миграцию: переименование model -> car_model...")
            
            # Шаг 1: Создаём новую таблицу с правильной структурой
            cursor.execute('''
            CREATE TABLE parts_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                brand TEXT NOT NULL,
                car_model TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                buy_price REAL NOT NULL,
                sell_price REAL NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            ''')
            
            # Шаг 2: Копируем данные из старой таблицы в новую
            cursor.execute('''
            INSERT INTO parts_new (
                id, article, name, brand, car_model, category, quantity, 
                buy_price, sell_price, description, created_at, updated_at
            )
            SELECT 
                id, article, name, brand, model, category, quantity, 
                buy_price, sell_price, description, created_at, updated_at
            FROM parts
            ''')
            
            # Шаг 3: Удаляем старую таблицу
            cursor.execute('DROP TABLE parts')
            
            # Шаг 4: Переименовываем новую таблицу
            cursor.execute('ALTER TABLE parts_new RENAME TO parts')
            
            conn.commit()
            print("✅ Миграция завершена успешно!")
            
            # Проверяем результат
            cursor.execute("SELECT COUNT(*) FROM parts")
            count = cursor.fetchone()[0]
            print(f"📊 Перенесено записей: {count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Ошибка миграции: {e}")
        
        # Восстанавливаем из резервной копии
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, db_path)
            print(f"🔄 База данных восстановлена из резервной копии")
        
        return False

def main():
    """Главная функция"""
    print("🚀 Запуск миграции базы данных AutoParts")
    print("Переименование поля 'model' в 'car_model' в таблице parts")
    print()
    
    if migrate_database():
        print("\n🎉 Миграция успешно завершена!")
        print("Теперь можно запускать приложение.")
    else:
        print("\n💥 Миграция не удалась!")
        print("Проверьте логи выше для диагностики.")

if __name__ == "__main__":
    main() 
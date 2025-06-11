import os
from peewee import SqliteDatabase

# Получаем путь к директории данных приложения
def get_data_dir():
    """Возвращает путь к директории данных приложения"""
    if os.name == 'nt':  # Windows
        data_dir = os.path.join(os.environ.get('APPDATA', ''), 'AutoParts')
    else:
        data_dir = os.path.join(os.path.expanduser('~'), '.autoparts')
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    return data_dir

# Путь к файлу базы данных
DB_PATH = os.path.join(get_data_dir(), 'autoparts.db')

# Инициализация базы данных
database = SqliteDatabase(DB_PATH)

def init_database():
    """Инициализация базы данных и создание таблиц"""
    from .part import Part
    from .sale import Sale, SaleItem
    
    database.connect()
    database.create_tables([Part, Sale, SaleItem], safe=True)
    database.close()
    
    print(f"База данных инициализирована: {DB_PATH}")

def get_database():
    """Возвращает объект базы данных"""
    return database 
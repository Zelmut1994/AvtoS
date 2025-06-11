import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

class SimpleDatabase:
    """Простая работа с базой данных SQLite"""
    
    def __init__(self):
        # Создаём папку для данных
        if os.name == 'nt':  # Windows
            data_dir = os.path.join(os.environ.get('APPDATA', ''), 'AutoParts')
        else:
            data_dir = os.path.join(os.path.expanduser('~'), '.autoparts')
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        self.db_path = os.path.join(data_dir, 'autoparts.db')
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Таблица запчастей
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS parts (
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
                
                # Таблица продаж
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    total REAL NOT NULL
                )
                ''')
                
                # Таблица позиций продаж
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER NOT NULL,
                    part_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    FOREIGN KEY (sale_id) REFERENCES sales (id),
                    FOREIGN KEY (part_id) REFERENCES parts (id)
                )
                ''')
                
                # Таблица поступлений
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS receipts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    supplier TEXT NOT NULL,
                    total REAL NOT NULL DEFAULT 0,
                    notes TEXT
                )
                ''')
                
                # Таблица позиций поступлений
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS receipt_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    receipt_id INTEGER NOT NULL,
                    part_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    buy_price REAL NOT NULL,
                    FOREIGN KEY (receipt_id) REFERENCES receipts (id),
                    FOREIGN KEY (part_id) REFERENCES parts (id)
                )
                ''')
                
                conn.commit()
                print(f"✅ База данных инициализирована: {self.db_path}")
                
        except Exception as e:
            print(f"❌ Ошибка инициализации БД: {e}")
    
    def add_part(self, article: str, name: str, brand: str, car_model: str, 
                 category: str, quantity: int, buy_price: float, 
                 sell_price: float, description: str = "") -> bool:
        """Добавить запчасть"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                
                cursor.execute('''
                INSERT INTO parts (article, name, brand, car_model, category, 
                                 quantity, buy_price, sell_price, description, 
                                 created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (article, name, brand, car_model, category, quantity, 
                      buy_price, sell_price, description, now, now))
                
                conn.commit()
                return True
                
        except sqlite3.IntegrityError:
            print(f"❌ Запчасть с артикулом {article} уже существует")
            return False
        except Exception as e:
            print(f"❌ Ошибка добавления запчасти: {e}")
            return False
    
    def get_all_parts(self) -> List[Dict]:
        """Получить все запчасти"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM parts ORDER BY article')
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"❌ Ошибка получения запчастей: {e}")
            return []
    
    def search_parts(self, query: str) -> List[Dict]:
        """Поиск запчастей (без учета регистра)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Приводим поисковый запрос к нижнему регистру
                search_query = f"%{query.lower()}%"
                
                cursor.execute('''
                SELECT * FROM parts 
                WHERE LOWER(article) LIKE ? 
                   OR LOWER(name) LIKE ? 
                   OR LOWER(brand) LIKE ? 
                   OR LOWER(car_model) LIKE ?
                   OR LOWER(category) LIKE ?
                ORDER BY article
                ''', (search_query, search_query, search_query, search_query, search_query))
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"❌ Ошибка поиска: {e}")
            return []
    
    def update_part(self, part_id: int, **kwargs) -> bool:
        """Обновить запчасть"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Строим запрос динамически
                set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
                values = list(kwargs.values())
                values.append(datetime.now().isoformat())  # updated_at
                values.append(part_id)
                
                cursor.execute(f'''
                UPDATE parts 
                SET {set_clause}, updated_at = ?
                WHERE id = ?
                ''', values)
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"❌ Ошибка обновления: {e}")
            return False
    
    def delete_part(self, part_id: int) -> bool:
        """Удалить запчасть"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM parts WHERE id = ?', (part_id,))
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"❌ Ошибка удаления: {e}")
            return False
    
    def get_part_by_id(self, part_id: int) -> Optional[Dict]:
        """Получить запчасть по ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM parts WHERE id = ?', (part_id,))
                row = cursor.fetchone()
                
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, row))
                return None
                
        except Exception as e:
            print(f"❌ Ошибка получения запчасти: {e}")
            return None
    
    def create_sale(self, items: List[Dict]) -> bool:
        """
        Создать продажу
        items: [{'part_id': int, 'quantity': int, 'price': float}]
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Начинаем транзакцию
                cursor.execute('BEGIN TRANSACTION')
                
                try:
                    # Проверяем доступность всех товаров
                    for item in items:
                        cursor.execute('SELECT quantity FROM parts WHERE id = ?', (item['part_id'],))
                        result = cursor.fetchone()
                        if not result or result[0] < item['quantity']:
                            raise ValueError(f"Недостаточно товара на складе (ID: {item['part_id']})")
                    
                    # Создаем продажу
                    total = sum(item['quantity'] * item['price'] for item in items)
                    cursor.execute('''
                    INSERT INTO sales (date, total)
                    VALUES (?, ?)
                    ''', (datetime.now().isoformat(), total))
                    
                    sale_id = cursor.lastrowid
                    
                    # Добавляем позиции продажи и списываем со склада
                    for item in items:
                        # Добавляем позицию
                        cursor.execute('''
                        INSERT INTO sale_items (sale_id, part_id, quantity, price)
                        VALUES (?, ?, ?, ?)
                        ''', (sale_id, item['part_id'], item['quantity'], item['price']))
                        
                        # Списываем со склада
                        cursor.execute('''
                        UPDATE parts SET quantity = quantity - ?, updated_at = ?
                        WHERE id = ?
                        ''', (item['quantity'], datetime.now().isoformat(), item['part_id']))
                    
                    cursor.execute('COMMIT')
                    return True
                    
                except Exception as e:
                    cursor.execute('ROLLBACK')
                    print(f"❌ Ошибка транзакции: {e}")
                    return False
                
        except Exception as e:
            print(f"❌ Ошибка создания продажи: {e}")
            return False
    
    def get_all_sales(self) -> List[Dict]:
        """Получить все продажи"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT s.id, s.date, s.total,
                       COUNT(si.id) as items_count
                FROM sales s
                LEFT JOIN sale_items si ON s.id = si.sale_id
                GROUP BY s.id, s.date, s.total
                ORDER BY s.date DESC
                ''')
                
                columns = ['id', 'date', 'total', 'items_count']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"❌ Ошибка получения продаж: {e}")
            return []
    
    def get_sale_items(self, sale_id: int) -> List[Dict]:
        """Получить позиции продажи"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT si.*, p.article, p.name
                FROM sale_items si
                JOIN parts p ON si.part_id = p.id
                WHERE si.sale_id = ?
                ''', (sale_id,))
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"❌ Ошибка получения позиций: {e}")
            return []
    
    def create_receipt(self, supplier: str, items: List[Dict], notes: str = "") -> bool:
        """
        Создать поступление
        items: [{'part_id': int, 'quantity': int, 'buy_price': float}]
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Начинаем транзакцию
                cursor.execute('BEGIN TRANSACTION')
                
                try:
                    # Создаем поступление
                    total = sum(item['quantity'] * item['buy_price'] for item in items)
                    cursor.execute('''
                    INSERT INTO receipts (date, supplier, total, notes)
                    VALUES (?, ?, ?, ?)
                    ''', (datetime.now().isoformat(), supplier, total, notes))
                    
                    receipt_id = cursor.lastrowid
                    
                    # Добавляем позиции поступления и увеличиваем остатки на складе
                    for item in items:
                        # Добавляем позицию
                        cursor.execute('''
                        INSERT INTO receipt_items (receipt_id, part_id, quantity, buy_price)
                        VALUES (?, ?, ?, ?)
                        ''', (receipt_id, item['part_id'], item['quantity'], item['buy_price']))
                        
                        # Увеличиваем остаток на складе
                        cursor.execute('''
                        UPDATE parts SET quantity = quantity + ?, updated_at = ?
                        WHERE id = ?
                        ''', (item['quantity'], datetime.now().isoformat(), item['part_id']))
                    
                    cursor.execute('COMMIT')
                    return True
                    
                except Exception as e:
                    cursor.execute('ROLLBACK')
                    print(f"❌ Ошибка транзакции: {e}")
                    return False
                
        except Exception as e:
            print(f"❌ Ошибка создания поступления: {e}")
            return False
    
    def get_all_receipts(self) -> List[Dict]:
        """Получить все поступления"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT r.id, r.date, r.supplier, r.total, r.notes,
                       COUNT(ri.id) as items_count
                FROM receipts r
                LEFT JOIN receipt_items ri ON r.id = ri.receipt_id
                GROUP BY r.id, r.date, r.supplier, r.total, r.notes
                ORDER BY r.date DESC
                ''')
                
                columns = ['id', 'date', 'supplier', 'total', 'notes', 'items_count']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"❌ Ошибка получения поступлений: {e}")
            return []
    
    def get_receipt_items(self, receipt_id: int) -> List[Dict]:
        """Получить позиции поступления"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT ri.*, p.article, p.name
                FROM receipt_items ri
                JOIN parts p ON ri.part_id = p.id
                WHERE ri.receipt_id = ?
                ''', (receipt_id,))
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"❌ Ошибка получения позиций поступления: {e}")
            return []

# Глобальный экземпляр базы данных
db = SimpleDatabase() 
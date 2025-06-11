"""
Тесты для database_simple.py
"""

import pytest
import tempfile
import os
import sqlite3
from unittest.mock import patch

# Импортируем модуль для тестирования
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database_simple import SimpleDatabase

@pytest.fixture
def temp_simple_db():
    """Создает временную тестовую базу данных для SimpleDatabase"""
    # Временная директория для БД
    temp_dir = tempfile.mkdtemp()
    
    # Мокаем get_data_dir чтобы использовать временную директорию
    with patch('database_simple.get_data_dir', return_value=temp_dir):
        db = SimpleDatabase()
        yield db
    
    # Очистка
    db_path = os.path.join(temp_dir, 'autoparts.db')
    if os.path.exists(db_path):
        os.unlink(db_path)
    os.rmdir(temp_dir)

class TestSimpleDatabase:
    """Тесты для SimpleDatabase"""
    
    def test_database_initialization(self, temp_simple_db):
        """Тест инициализации базы данных"""
        # База должна создаться и содержать нужные таблицы
        with sqlite3.connect(temp_simple_db.db_path) as conn:
            cursor = conn.cursor()
            
            # Проверяем существование таблиц
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['parts', 'sales', 'sale_items', 'receipts', 'receipt_items']
            for table in expected_tables:
                assert table in tables
    
    def test_add_part_success(self, temp_simple_db):
        """Тест успешного добавления запчасти"""
        result = temp_simple_db.add_part(
            article="TEST001",
            name="Тестовая запчасть",
            brand="TestBrand",
            car_model="TestModel",
            category="Тест",
            quantity=10,
            buy_price=100.0,
            sell_price=150.0,
            description="Описание"
        )
        
        assert result is True
        
        # Проверяем, что запчасть добавилась в БД
        parts = temp_simple_db.get_all_parts()
        assert len(parts) == 1
        assert parts[0]['article'] == "TEST001"
        assert parts[0]['name'] == "Тестовая запчасть"
        assert parts[0]['car_model'] == "TestModel"  # проверяем новое поле
    
    def test_add_part_duplicate_article(self, temp_simple_db):
        """Тест добавления запчасти с дублирующимся артикулом"""
        # Добавляем первую запчасть
        temp_simple_db.add_part(
            article="DUP001",
            name="Первая запчасть",
            brand="Brand1",
            car_model="Model1",
            category="Категория1",
            quantity=5,
            buy_price=50.0,
            sell_price=75.0
        )
        
        # Пытаемся добавить вторую с тем же артикулом
        result = temp_simple_db.add_part(
            article="DUP001",  # тот же артикул
            name="Вторая запчасть",
            brand="Brand2",
            car_model="Model2",
            category="Категория2",
            quantity=3,
            buy_price=30.0,
            sell_price=45.0
        )
        
        assert result is False
        
        # В БД должна остаться только первая запчасть
        parts = temp_simple_db.get_all_parts()
        assert len(parts) == 1
        assert parts[0]['name'] == "Первая запчасть"
    
    def test_get_all_parts_empty(self, temp_simple_db):
        """Тест получения всех запчастей из пустой БД"""
        parts = temp_simple_db.get_all_parts()
        assert parts == []
    
    def test_search_parts(self, temp_simple_db):
        """Тест поиска запчастей"""
        # Добавляем несколько запчастей
        temp_simple_db.add_part("FILT001", "Масляный фильтр", "Toyota", "Camry", "Двигатель", 5, 100, 150)
        temp_simple_db.add_part("FILT002", "Воздушный фильтр", "Honda", "Civic", "Двигатель", 3, 80, 120)
        temp_simple_db.add_part("BRAKE001", "Тормозные колодки", "BMW", "3 Series", "Тормоза", 2, 200, 300)
        
        # Поиск по артикулу
        results = temp_simple_db.search_parts("FILT001")
        assert len(results) == 1
        assert results[0]['article'] == "FILT001"
        
        # Поиск по названию (регистронезависимый)
        results = temp_simple_db.search_parts("фильтр")
        assert len(results) == 2
        
        # Поиск по марке
        results = temp_simple_db.search_parts("toyota")
        assert len(results) == 1
        assert results[0]['brand'] == "Toyota"
        
        # Поиск по модели автомобиля
        results = temp_simple_db.search_parts("camry")
        assert len(results) == 1
        assert results[0]['car_model'] == "Camry"
        
        # Поиск по категории
        results = temp_simple_db.search_parts("двигатель")
        assert len(results) == 2
    
    def test_update_part(self, temp_simple_db):
        """Тест обновления запчасти"""
        # Добавляем запчасть
        temp_simple_db.add_part("UPD001", "Старое название", "OldBrand", "OldModel", "Категория", 5, 100, 150)
        
        # Получаем ID добавленной запчасти
        parts = temp_simple_db.get_all_parts()
        part_id = parts[0]['id']
        
        # Обновляем
        result = temp_simple_db.update_part(
            part_id,
            name="Новое название",
            quantity=10,
            sell_price=200.0
        )
        
        assert result is True
        
        # Проверяем изменения
        updated_part = temp_simple_db.get_part_by_id(part_id)
        assert updated_part['name'] == "Новое название"
        assert updated_part['quantity'] == 10
        assert updated_part['sell_price'] == 200.0
        # Неизмененные поля должны остаться
        assert updated_part['article'] == "UPD001"
        assert updated_part['brand'] == "OldBrand"
    
    def test_delete_part(self, temp_simple_db):
        """Тест удаления запчасти"""
        # Добавляем запчасть
        temp_simple_db.add_part("DEL001", "Запчасть для удаления", "Brand", "Model", "Категория", 1, 50, 75)
        
        # Получаем ID
        parts = temp_simple_db.get_all_parts()
        part_id = parts[0]['id']
        
        # Удаляем
        result = temp_simple_db.delete_part(part_id)
        assert result is True
        
        # Проверяем, что запчасть удалена
        assert temp_simple_db.get_part_by_id(part_id) is None
        assert len(temp_simple_db.get_all_parts()) == 0
    
    def test_get_part_by_id(self, temp_simple_db):
        """Тест получения запчасти по ID"""
        # Добавляем запчасть
        temp_simple_db.add_part("GET001", "Тестовая запчасть", "Brand", "Model", "Категория", 1, 50, 75)
        
        # Получаем ID
        parts = temp_simple_db.get_all_parts()
        part_id = parts[0]['id']
        
        # Получаем по ID
        part = temp_simple_db.get_part_by_id(part_id)
        assert part is not None
        assert part['article'] == "GET001"
        assert part['name'] == "Тестовая запчасть"
        
        # Тест с несуществующим ID
        assert temp_simple_db.get_part_by_id(99999) is None
    
    def test_create_sale(self, temp_simple_db):
        """Тест создания продажи"""
        # Добавляем запчасти
        temp_simple_db.add_part("SALE001", "Запчасть 1", "Brand", "Model", "Категория", 10, 100, 150)
        temp_simple_db.add_part("SALE002", "Запчасть 2", "Brand", "Model", "Категория", 5, 200, 300)
        
        parts = temp_simple_db.get_all_parts()
        part1_id = parts[0]['id']
        part2_id = parts[1]['id']
        
        # Создаем продажу
        items = [
            {'part_id': part1_id, 'quantity': 2, 'price': 150.0},
            {'part_id': part2_id, 'quantity': 1, 'price': 300.0}
        ]
        
        result = temp_simple_db.create_sale(items)
        assert result is True
        
        # Проверяем, что продажа создалась
        sales = temp_simple_db.get_all_sales()
        assert len(sales) == 1
        assert sales[0]['total'] == 600.0  # 2*150 + 1*300
        
        # Проверяем, что количество запчастей уменьшилось
        updated_parts = temp_simple_db.get_all_parts()
        part1 = next(p for p in updated_parts if p['id'] == part1_id)
        part2 = next(p for p in updated_parts if p['id'] == part2_id)
        
        assert part1['quantity'] == 8  # было 10, продали 2
        assert part2['quantity'] == 4  # было 5, продали 1
    
    def test_create_sale_insufficient_stock(self, temp_simple_db):
        """Тест создания продажи с недостаточным остатком"""
        # Добавляем запчасть с малым количеством
        temp_simple_db.add_part("LOW001", "Запчасть с малым остатком", "Brand", "Model", "Категория", 1, 100, 150)
        
        parts = temp_simple_db.get_all_parts()
        part_id = parts[0]['id']
        
        # Пытаемся продать больше чем есть
        items = [
            {'part_id': part_id, 'quantity': 5, 'price': 150.0}  # больше чем есть
        ]
        
        result = temp_simple_db.create_sale(items)
        assert result is False
        
        # Количество не должно измениться
        updated_part = temp_simple_db.get_part_by_id(part_id)
        assert updated_part['quantity'] == 1
    
    def test_get_all_sales(self, temp_simple_db):
        """Тест получения всех продаж"""
        # Сначала пустая база
        sales = temp_simple_db.get_all_sales()
        assert sales == []
        
        # Добавляем запчасть и создаем продажу
        temp_simple_db.add_part("SALES001", "Запчасть", "Brand", "Model", "Категория", 10, 100, 150)
        part_id = temp_simple_db.get_all_parts()[0]['id']
        
        items = [{'part_id': part_id, 'quantity': 1, 'price': 150.0}]
        temp_simple_db.create_sale(items)
        
        # Проверяем
        sales = temp_simple_db.get_all_sales()
        assert len(sales) == 1
        assert 'items_count' in sales[0]
        assert sales[0]['items_count'] == 1
    
    def test_get_sale_items(self, temp_simple_db):
        """Тест получения позиций продажи"""
        # Создаем запчасть и продажу
        temp_simple_db.add_part("ITEMS001", "Тестовая запчасть", "Brand", "Model", "Категория", 10, 100, 150)
        part_id = temp_simple_db.get_all_parts()[0]['id']
        
        items = [{'part_id': part_id, 'quantity': 2, 'price': 150.0}]
        temp_simple_db.create_sale(items)
        
        # Получаем ID продажи
        sale_id = temp_simple_db.get_all_sales()[0]['id']
        
        # Получаем позиции
        sale_items = temp_simple_db.get_sale_items(sale_id)
        assert len(sale_items) == 1
        assert sale_items[0]['quantity'] == 2
        assert sale_items[0]['price'] == 150.0
        assert sale_items[0]['article'] == "ITEMS001"  # должен подтягиваться через JOIN
    
    def test_create_receipt(self, temp_simple_db):
        """Тест создания поступления"""
        # Добавляем запчасть
        temp_simple_db.add_part("REC001", "Запчасть для поступления", "Brand", "Model", "Категория", 5, 100, 150)
        part_id = temp_simple_db.get_all_parts()[0]['id']
        
        # Создаем поступление
        items = [
            {'part_id': part_id, 'quantity': 10, 'buy_price': 90.0}
        ]
        
        result = temp_simple_db.create_receipt("Тестовый поставщик", items, "Тестовые заметки")
        assert result is True
        
        # Проверяем, что поступление создалось
        receipts = temp_simple_db.get_all_receipts()
        assert len(receipts) == 1
        assert receipts[0]['supplier'] == "Тестовый поставщик"
        assert receipts[0]['total'] == 900.0  # 10 * 90
        assert receipts[0]['notes'] == "Тестовые заметки"
        
        # Проверяем, что количество запчасти увеличилось
        updated_part = temp_simple_db.get_part_by_id(part_id)
        assert updated_part['quantity'] == 15  # было 5, пришло 10
    
    def test_get_all_receipts(self, temp_simple_db):
        """Тест получения всех поступлений"""
        receipts = temp_simple_db.get_all_receipts()
        assert receipts == []
        
        # Создаем поступление и проверяем
        temp_simple_db.add_part("RECEIPTS001", "Запчасть", "Brand", "Model", "Категория", 0, 100, 150)
        part_id = temp_simple_db.get_all_parts()[0]['id']
        
        items = [{'part_id': part_id, 'quantity': 5, 'buy_price': 100.0}]
        temp_simple_db.create_receipt("Поставщик", items)
        
        receipts = temp_simple_db.get_all_receipts()
        assert len(receipts) == 1
        assert 'items_count' in receipts[0]
        assert receipts[0]['items_count'] == 1
    
    def test_get_receipt_items(self, temp_simple_db):
        """Тест получения позиций поступления"""
        # Создаем запчасть и поступление
        temp_simple_db.add_part("RECITEMS001", "Запчасть", "Brand", "Model", "Категория", 0, 100, 150)
        part_id = temp_simple_db.get_all_parts()[0]['id']
        
        items = [{'part_id': part_id, 'quantity': 7, 'buy_price': 95.0}]
        temp_simple_db.create_receipt("Поставщик", items)
        
        # Получаем ID поступления
        receipt_id = temp_simple_db.get_all_receipts()[0]['id']
        
        # Получаем позиции
        receipt_items = temp_simple_db.get_receipt_items(receipt_id)
        assert len(receipt_items) == 1
        assert receipt_items[0]['quantity'] == 7
        assert receipt_items[0]['buy_price'] == 95.0
        assert receipt_items[0]['article'] == "RECITEMS001"  # через JOIN 
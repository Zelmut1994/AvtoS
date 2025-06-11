"""
Упрощённые тесты для database_simple.py
"""

import pytest
import tempfile
import os
import shutil
import sys

# Добавляем путь к src для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database_simple import SimpleDatabase

@pytest.fixture
def temp_db():
    """Создает временную тестовую базу данных"""
    # Создаём временную директорию
    temp_dir = tempfile.mkdtemp()
    
    # Создаём экземпляр SimpleDatabase с временным путём
    db = SimpleDatabase()
    
    # Подменяем путь к БД на временный
    original_path = db.db_path
    db.db_path = os.path.join(temp_dir, 'test_autoparts.db')
    
    # Пересоздаём БД в новом месте
    db.init_database()
    
    yield db
    
    # Очистка
    if os.path.exists(db.db_path):
        os.unlink(db.db_path)
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)

class TestSimpleDatabaseBasic:
    """Базовые тесты для SimpleDatabase"""
    
    def test_add_and_get_part(self, temp_db):
        """Тест добавления и получения запчасти"""
        # Добавляем запчасть
        result = temp_db.add_part(
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
        
        # Получаем все запчасти
        parts = temp_db.get_all_parts()
        assert len(parts) == 1
        
        part = parts[0]
        assert part['article'] == "TEST001"
        assert part['name'] == "Тестовая запчасть"
        assert part['car_model'] == "TestModel"  # проверяем новое поле
        assert part['quantity'] == 10
        assert part['buy_price'] == 100.0
        assert part['sell_price'] == 150.0
    
    def test_duplicate_article(self, temp_db):
        """Тест защиты от дублирующихся артикулов"""
        # Добавляем первую запчасть
        result1 = temp_db.add_part("DUP001", "Первая", "Brand1", "Model1", "Cat1", 5, 50.0, 75.0)
        assert result1 is True
        
        # Пытаемся добавить с тем же артикулом
        result2 = temp_db.add_part("DUP001", "Вторая", "Brand2", "Model2", "Cat2", 3, 30.0, 45.0)
        assert result2 is False
        
        # Должна остаться только первая
        parts = temp_db.get_all_parts()
        assert len(parts) == 1
        assert parts[0]['name'] == "Первая"
    
    def test_search_parts(self, temp_db):
        """Тест поиска запчастей"""
        # Добавляем несколько запчастей
        temp_db.add_part("FILT001", "Масляный фильтр", "Toyota", "Camry", "Двигатель", 5, 100, 150)
        temp_db.add_part("FILT002", "Воздушный фильтр", "Honda", "Civic", "Двигатель", 3, 80, 120)
        temp_db.add_part("BRAKE001", "Тормозные колодки", "BMW", "3 Series", "Тормоза", 2, 200, 300)
        
        # Поиск по артикулу
        results = temp_db.search_parts("FILT001")
        assert len(results) == 1
        assert results[0]['article'] == "FILT001"
        
        # Поиск по названию
        results = temp_db.search_parts("фильтр")
        assert len(results) == 2
        
        # Поиск по марке
        results = temp_db.search_parts("toyota")
        assert len(results) == 1
        
        # Поиск по модели
        results = temp_db.search_parts("camry")
        assert len(results) == 1
    
    def test_update_part(self, temp_db):
        """Тест обновления запчасти"""
        # Добавляем запчасть
        temp_db.add_part("UPD001", "Старое название", "OldBrand", "OldModel", "Категория", 5, 100, 150)
        
        # Получаем ID
        parts = temp_db.get_all_parts()
        part_id = parts[0]['id']
        
        # Обновляем
        result = temp_db.update_part(
            part_id,
            name="Новое название",
            quantity=10,
            sell_price=200.0
        )
        
        assert result is True
        
        # Проверяем изменения
        updated_part = temp_db.get_part_by_id(part_id)
        assert updated_part['name'] == "Новое название"
        assert updated_part['quantity'] == 10
        assert updated_part['sell_price'] == 200.0
        assert updated_part['article'] == "UPD001"  # неизменяемое поле
    
    def test_create_sale(self, temp_db):
        """Тест создания продажи"""
        # Добавляем запчасти
        temp_db.add_part("SALE001", "Запчасть 1", "Brand", "Model", "Категория", 10, 100, 150)
        temp_db.add_part("SALE002", "Запчасть 2", "Brand", "Model", "Категория", 5, 200, 300)
        
        parts = temp_db.get_all_parts()
        part1_id = parts[0]['id']
        part2_id = parts[1]['id']
        
        # Создаем продажу
        items = [
            {'part_id': part1_id, 'quantity': 2, 'price': 150.0},
            {'part_id': part2_id, 'quantity': 1, 'price': 300.0}
        ]
        
        result = temp_db.create_sale(items)
        assert result is True
        
        # Проверяем продажу
        sales = temp_db.get_all_sales()
        assert len(sales) == 1
        assert sales[0]['total'] == 600.0  # 2*150 + 1*300
        
        # Проверяем остатки
        updated_parts = temp_db.get_all_parts()
        part1 = next(p for p in updated_parts if p['id'] == part1_id)
        part2 = next(p for p in updated_parts if p['id'] == part2_id)
        
        assert part1['quantity'] == 8  # было 10, продали 2
        assert part2['quantity'] == 4  # было 5, продали 1
    
    def test_create_receipt(self, temp_db):
        """Тест создания поступления"""
        # Добавляем запчасть
        temp_db.add_part("REC001", "Запчасть", "Brand", "Model", "Категория", 5, 100, 150)
        part_id = temp_db.get_all_parts()[0]['id']
        
        # Создаем поступление
        items = [{'part_id': part_id, 'quantity': 10, 'buy_price': 90.0}]
        
        result = temp_db.create_receipt("Тестовый поставщик", items, "Заметки")
        assert result is True
        
        # Проверяем поступление
        receipts = temp_db.get_all_receipts()
        assert len(receipts) == 1
        assert receipts[0]['supplier'] == "Тестовый поставщик"
        assert receipts[0]['total'] == 900.0  # 10 * 90
        
        # Проверяем, что остаток увеличился
        updated_part = temp_db.get_part_by_id(part_id)
        assert updated_part['quantity'] == 15  # было 5, пришло 10 
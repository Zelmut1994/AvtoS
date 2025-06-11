"""
Тесты для моделей данных
"""

import pytest
import sys
import os
from decimal import Decimal
from datetime import datetime

# Добавляем путь к src для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.part import Part
from models.sale import Sale, SaleItem

class TestPartModel:
    """Тесты для модели Part"""
    
    def test_part_creation(self, temp_db):
        """Тест создания запчасти"""
        part = Part.create(
            article="ABC123",
            name="Тестовая запчасть",
            brand="TestBrand",
            car_model="TestModel",
            category="Тест",
            quantity=5,
            buy_price=100.0,
            sell_price=150.0,
            description="Описание"
        )
        
        assert part.article == "ABC123"
        assert part.name == "Тестовая запчасть"
        assert part.brand == "TestBrand"
        assert part.car_model == "TestModel"
        assert part.category == "Тест"
        assert part.quantity == 5
        assert part.buy_price == 100.0
        assert part.sell_price == 150.0
        assert part.description == "Описание"
        assert part.created_at is not None
        assert part.updated_at is not None
    
    def test_part_str_representation(self, sample_part):
        """Тест строкового представления запчасти"""
        expected = "TEST001 - Тестовая запчасть"
        assert str(sample_part) == expected
    
    def test_part_profit_margin(self, sample_part):
        """Тест расчета маржи прибыли"""
        # buy_price = 100, sell_price = 150
        # Маржа = ((150 - 100) / 100) * 100 = 50%
        assert sample_part.profit_margin == 50.0
    
    def test_part_profit_margin_zero_buy_price(self, temp_db):
        """Тест расчета маржи при нулевой закупочной цене"""
        part = Part.create(
            article="FREE001",
            name="Бесплатная запчасть",
            brand="Test",
            car_model="Test",
            category="Тест",
            quantity=1,
            buy_price=0.0,
            sell_price=100.0
        )
        
        assert part.profit_margin == 0
    
    def test_part_reduce_quantity_success(self, sample_part):
        """Тест успешного уменьшения количества"""
        initial_qty = sample_part.quantity
        result = sample_part.reduce_quantity(3)
        
        assert result is True
        assert sample_part.quantity == initial_qty - 3
    
    def test_part_reduce_quantity_insufficient(self, sample_part):
        """Тест неудачного уменьшения количества (недостаточно на складе)"""
        initial_qty = sample_part.quantity
        result = sample_part.reduce_quantity(15)  # больше чем есть
        
        assert result is False
        assert sample_part.quantity == initial_qty  # количество не изменилось
    
    def test_part_reduce_quantity_exact(self, sample_part):
        """Тест уменьшения количества до нуля"""
        initial_qty = sample_part.quantity
        result = sample_part.reduce_quantity(initial_qty)
        
        assert result is True
        assert sample_part.quantity == 0
    
    def test_part_search(self, sample_parts):
        """Тест поиска запчастей"""
        # Поиск по артикулу
        results = list(Part.search("PART001"))
        assert len(results) == 1
        assert results[0].article == "PART001"
        
        # Поиск по названию
        results = list(Part.search("фильтр"))
        assert len(results) == 2  # масляный и воздушный фильтр
        
        # Поиск по марке
        results = list(Part.search("Toyota"))
        assert len(results) == 1
        assert results[0].brand == "Toyota"
        
        # Поиск по модели автомобиля
        results = list(Part.search("Camry"))
        assert len(results) == 1
        assert results[0].car_model == "Camry"
    
    def test_part_get_by_article_exists(self, sample_part):
        """Тест получения запчасти по артикулу (существует)"""
        part = Part.get_by_article("TEST001")
        
        assert part is not None
        assert part.article == "TEST001"
        assert part.name == "Тестовая запчасть"
    
    def test_part_get_by_article_not_exists(self, temp_db):
        """Тест получения запчасти по артикулу (не существует)"""
        part = Part.get_by_article("NONEXISTENT")
        
        assert part is None
    
    def test_part_unique_article_constraint(self, temp_db, sample_part):
        """Тест уникальности артикула"""
        with pytest.raises(Exception):  # IntegrityError или подобная
            Part.create(
                article="TEST001",  # тот же артикул
                name="Другая запчасть",
                brand="Other",
                car_model="Other",
                category="Другая",
                quantity=1,
                buy_price=50.0,
                sell_price=75.0
            )

class TestSaleModel:
    """Тесты для модели Sale"""
    
    def test_sale_creation(self, temp_db):
        """Тест создания продажи"""
        sale = Sale.create(total=250.50)
        
        assert sale.total == 250.50
        assert sale.date is not None
        assert isinstance(sale.date, datetime)
    
    def test_sale_str_representation(self, sample_sale):
        """Тест строкового представления продажи"""
        result = str(sample_sale)
        
        assert result.startswith("Продажа #")
        assert "от" in result
        assert result.endswith(sample_sale.date.strftime('%d.%m.%Y %H:%M'))
    
    def test_sale_items_count(self, sample_sale):
        """Тест подсчета позиций в продаже"""
        assert sample_sale.items_count == 1
        
        # Добавим еще одну позицию
        SaleItem.create(
            sale=sample_sale,
            part=999,  # фиктивный ID
            quantity=2,
            price=75.0
        )
        
        assert sample_sale.items_count == 2
    
    def test_sale_calculate_total(self, temp_db, sample_part):
        """Тест пересчета общей суммы"""
        sale = Sale.create(total=0.0)
        
        # Добавляем позиции
        SaleItem.create(sale=sale, part=sample_part.id, quantity=2, price=100.0)
        SaleItem.create(sale=sale, part=sample_part.id, quantity=1, price=50.0)
        
        total = sale.calculate_total()
        
        assert total == 250.0  # 2*100 + 1*50
        assert sale.total == 250.0

class TestSaleItemModel:
    """Тесты для модели SaleItem"""
    
    def test_sale_item_creation(self, temp_db, sample_sale, sample_part):
        """Тест создания позиции продажи"""
        item = SaleItem.create(
            sale=sample_sale,
            part=sample_part.id,
            quantity=3,
            price=120.0
        )
        
        assert item.sale == sample_sale
        assert item.part == sample_part.id
        assert item.quantity == 3
        assert item.price == 120.0
    
    def test_sale_item_total_price(self, temp_db, sample_sale):
        """Тест расчета общей стоимости позиции"""
        item = SaleItem.create(
            sale=sample_sale,
            part=999,
            quantity=4,
            price=25.0
        )
        
        assert item.total_price == 100.0  # 4 * 25
    
    def test_sale_item_str_representation(self, temp_db, sample_sale):
        """Тест строкового представления позиции"""
        item = SaleItem.create(
            sale=sample_sale,
            part=123,
            quantity=2,
            price=150.0
        )
        
        expected = "Товар ID:123 x2 = 300.0 руб."
        assert str(item) == expected 
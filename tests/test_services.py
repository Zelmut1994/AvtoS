"""
Тесты для сервисных классов
"""

import pytest
import sys
import os
from decimal import Decimal

# Добавляем путь к src для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.part_service import PartService
from services.sale_service import SaleService
from models.part import Part
from models.sale import Sale, SaleItem

class TestPartService:
    """Тесты для PartService"""
    
    def test_create_part(self, temp_db):
        """Тест создания запчасти через сервис"""
        part = PartService.create_part(
            article="SRV001",
            name="Сервисная запчасть",
            brand="ServiceBrand",
            car_model="ServiceModel",
            category="Сервис",
            quantity=5,
            buy_price=Decimal("100.00"),
            sell_price=Decimal("150.00"),
            description="Тест через сервис"
        )
        
        assert part.article == "SRV001"
        assert part.name == "Сервисная запчасть"
        assert part.brand == "ServiceBrand"
        assert part.car_model == "ServiceModel"
        assert part.category == "Сервис"
        assert part.quantity == 5
        assert part.buy_price == Decimal("100.00")
        assert part.sell_price == Decimal("150.00")
        assert part.description == "Тест через сервис"
    
    def test_get_all_parts(self, sample_parts):
        """Тест получения всех запчастей"""
        parts = PartService.get_all_parts()
        
        assert len(parts) == 3
        # Проверяем сортировку по артикулу
        assert parts[0].article == "PART001"
        assert parts[1].article == "PART002"
        assert parts[2].article == "PART003"
    
    def test_get_parts_in_stock(self, sample_parts):
        """Тест получения запчастей с ненулевыми остатками"""
        parts = PartService.get_parts_in_stock()
        
        assert len(parts) == 2  # PART001 (15 шт.) и PART002 (2 шт.)
        for part in parts:
            assert part.quantity > 0
    
    def test_search_parts_by_article(self, sample_parts):
        """Тест поиска запчастей по артикулу"""
        results = PartService.search_parts("PART001")
        
        assert len(results) == 1
        assert results[0].article == "PART001"
    
    def test_search_parts_by_name(self, sample_parts):
        """Тест поиска запчастей по названию"""
        results = PartService.search_parts("фильтр")
        
        assert len(results) == 2  # масляный и воздушный фильтр
    
    def test_search_parts_empty_query(self, sample_parts):
        """Тест поиска с пустым запросом возвращает все запчасти"""
        results = PartService.search_parts("")
        
        assert len(results) == 3
        
        results = PartService.search_parts("   ")  # только пробелы
        assert len(results) == 3
    
    def test_get_part_by_id_exists(self, sample_part):
        """Тест получения запчасти по ID (существует)"""
        part = PartService.get_part_by_id(sample_part.id)
        
        assert part is not None
        assert part.id == sample_part.id
        assert part.article == sample_part.article
    
    def test_get_part_by_id_not_exists(self, temp_db):
        """Тест получения запчасти по ID (не существует)"""
        part = PartService.get_part_by_id(99999)
        
        assert part is None
    
    def test_get_part_by_article(self, sample_part):
        """Тест получения запчасти по артикулу"""
        part = PartService.get_part_by_article("TEST001")
        
        assert part is not None
        assert part.article == "TEST001"
    
    def test_update_part(self, sample_part):
        """Тест обновления запчасти"""
        original_updated_at = sample_part.updated_at
        
        updated_part = PartService.update_part(
            sample_part,
            name="Обновленное название",
            quantity=20,
            sell_price=Decimal("200.00")
        )
        
        assert updated_part.name == "Обновленное название"
        assert updated_part.quantity == 20
        assert updated_part.sell_price == Decimal("200.00")
        assert updated_part.updated_at > original_updated_at
        
        # Остальные поля должны остаться без изменений
        assert updated_part.article == sample_part.article
        assert updated_part.brand == sample_part.brand
    
    def test_delete_part(self, temp_db, sample_part):
        """Тест удаления запчасти"""
        part_id = sample_part.id
        
        result = PartService.delete_part(sample_part)
        
        assert result is True
        assert PartService.get_part_by_id(part_id) is None
    
    def test_check_availability_sufficient(self, sample_part):
        """Тест проверки доступности (достаточно)"""
        result = PartService.check_availability(sample_part, 5)
        
        assert result is True
    
    def test_check_availability_insufficient(self, sample_part):
        """Тест проверки доступности (недостаточно)"""
        result = PartService.check_availability(sample_part, 15)
        
        assert result is False
    
    def test_check_availability_exact(self, sample_part):
        """Тест проверки доступности (точно)"""
        result = PartService.check_availability(sample_part, sample_part.quantity)
        
        assert result is True
    
    def test_reduce_quantity(self, sample_part):
        """Тест уменьшения количества на складе"""
        initial_qty = sample_part.quantity
        
        result = PartService.reduce_quantity(sample_part, 3)
        
        assert result is True
        # Перезагружаем объект из БД
        sample_part.refresh()
        assert sample_part.quantity == initial_qty - 3
    
    def test_get_categories(self, sample_parts):
        """Тест получения списка категорий"""
        categories = PartService.get_categories()
        
        expected_categories = ["Двигатель", "Тормозная система"]
        assert sorted(categories) == sorted(expected_categories)
    
    def test_get_brands(self, sample_parts):
        """Тест получения списка марок"""
        brands = PartService.get_brands()
        
        expected_brands = ["BMW", "Honda", "Toyota"]
        assert sorted(brands) == sorted(expected_brands)
    
    def test_get_low_stock_parts_default_threshold(self, sample_parts):
        """Тест получения запчастей с низким остатком (порог по умолчанию)"""
        low_stock_parts = PartService.get_low_stock_parts()
        
        assert len(low_stock_parts) == 1  # только PART002 (2 шт.)
        assert low_stock_parts[0].article == "PART002"
    
    def test_get_low_stock_parts_custom_threshold(self, sample_parts):
        """Тест получения запчастей с низким остатком (кастомный порог)"""
        low_stock_parts = PartService.get_low_stock_parts(threshold=10)
        
        assert len(low_stock_parts) == 1  # только PART002 (2 шт.)
        
        low_stock_parts = PartService.get_low_stock_parts(threshold=20)
        assert len(low_stock_parts) == 2  # PART001 (15 шт.) и PART002 (2 шт.)
    
    def test_validate_article_unique(self, temp_db, sample_part):
        """Тест валидации уникальности артикула"""
        # Новый артикул должен быть валидным
        assert PartService.validate_article("NEW001") is True
        
        # Существующий артикул должен быть невалидным
        assert PartService.validate_article("TEST001") is False
    
    def test_validate_article_exclude_id(self, sample_part):
        """Тест валидации артикула с исключением ID"""
        # При редактировании той же записи, артикул должен быть валидным
        assert PartService.validate_article("TEST001", exclude_id=sample_part.id) is True
        
        # Но для другой записи - невалидным
        assert PartService.validate_article("TEST001", exclude_id=99999) is False

class TestSaleService:
    """Тесты для SaleService"""
    
    def test_create_sale_success(self, temp_db, sample_parts):
        """Тест успешного создания продажи"""
        # Используем запчасти с достаточным количеством
        items = [
            {'part_id': sample_parts[0].id, 'quantity': 2, 'price': Decimal("180.00")},
            {'part_id': sample_parts[1].id, 'quantity': 1, 'price': Decimal("120.00")}
        ]
        
        sale, success = SaleService.create_sale(items)
        
        assert success is True
        assert sale is not None
        assert sale.total == Decimal("480.00")  # 2*180 + 1*120
        
        # Проверяем, что количество уменьшилось
        sample_parts[0].refresh()
        sample_parts[1].refresh()
        assert sample_parts[0].quantity == 13  # было 15, продали 2
        assert sample_parts[1].quantity == 1   # было 2, продали 1
    
    def test_create_sale_insufficient_stock(self, temp_db, sample_parts):
        """Тест создания продажи с недостаточным остатком"""
        items = [
            {'part_id': sample_parts[0].id, 'quantity': 20, 'price': Decimal("180.00")}  # больше чем есть
        ]
        
        sale, success = SaleService.create_sale(items)
        
        assert success is False
        assert sale is None
        
        # Количество не должно измениться
        sample_parts[0].refresh()
        assert sample_parts[0].quantity == 15
    
    def test_get_all_sales(self, temp_db, sample_sale):
        """Тест получения всех продаж"""
        sales = SaleService.get_all_sales()
        
        assert len(sales) >= 1
        # Проверяем сортировку по дате (новые первыми)
        assert sales[0].id == sample_sale.id
    
    def test_get_sale_by_id_exists(self, sample_sale):
        """Тест получения продажи по ID (существует)"""
        sale = SaleService.get_sale_by_id(sample_sale.id)
        
        assert sale is not None
        assert sale.id == sample_sale.id
    
    def test_get_sale_by_id_not_exists(self, temp_db):
        """Тест получения продажи по ID (не существует)"""
        sale = SaleService.get_sale_by_id(99999)
        
        assert sale is None
    
    def test_validate_sale_items_valid(self, sample_parts):
        """Тест валидации валидных позиций продажи"""
        items = [
            {'part_id': sample_parts[0].id, 'quantity': 2, 'price': Decimal("180.00")},
            {'part_id': sample_parts[1].id, 'quantity': 1, 'price': Decimal("120.00")}
        ]
        
        is_valid, errors = SaleService.validate_sale_items(items)
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_sale_items_empty(self, temp_db):
        """Тест валидации пустого списка позиций"""
        is_valid, errors = SaleService.validate_sale_items([])
        
        assert is_valid is False
        assert "Не выбраны товары для продажи" in errors[0]
    
    def test_validate_sale_items_insufficient_stock(self, sample_parts):
        """Тест валидации позиций с недостаточным остатком"""
        items = [
            {'part_id': sample_parts[0].id, 'quantity': 20, 'price': Decimal("180.00")}  # больше чем есть
        ]
        
        is_valid, errors = SaleService.validate_sale_items(items)
        
        assert is_valid is False
        assert "недостаточно товара на складе" in errors[0]
    
    def test_validate_sale_items_zero_quantity(self, sample_parts):
        """Тест валидации позиций с нулевым количеством"""
        items = [
            {'part_id': sample_parts[0].id, 'quantity': 0, 'price': Decimal("180.00")}
        ]
        
        is_valid, errors = SaleService.validate_sale_items(items)
        
        assert is_valid is False
        assert "количество должно быть больше 0" in errors[0]
    
    def test_validate_sale_items_nonexistent_part(self, temp_db):
        """Тест валидации позиций с несуществующим товаром"""
        items = [
            {'part_id': 99999, 'quantity': 1, 'price': Decimal("100.00")}
        ]
        
        is_valid, errors = SaleService.validate_sale_items(items)
        
        assert is_valid is False
        assert "товар не найден" in errors[0]
    
    def test_calculate_change_sufficient(self, temp_db):
        """Тест расчета сдачи (достаточно денег)"""
        total = Decimal("150.00")
        paid = Decimal("200.00")
        
        change = SaleService.calculate_change(total, paid)
        
        assert change == Decimal("50.00")
    
    def test_calculate_change_exact(self, temp_db):
        """Тест расчета сдачи (точная сумма)"""
        total = Decimal("150.00")
        paid = Decimal("150.00")
        
        change = SaleService.calculate_change(total, paid)
        
        assert change == Decimal("0.00")
    
    def test_calculate_change_insufficient(self, temp_db):
        """Тест расчета сдачи (недостаточно денег)"""
        total = Decimal("200.00")
        paid = Decimal("150.00")
        
        change = SaleService.calculate_change(total, paid)
        
        assert change == Decimal("0.00") 
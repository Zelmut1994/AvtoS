"""
Конфигурация pytest и общие фикстуры
"""

import pytest
import tempfile
import os
from peewee import SqliteDatabase
from datetime import datetime

# Импортируем модели
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.part import Part
from models.sale import Sale, SaleItem
from models.database import database

@pytest.fixture
def temp_db():
    """Создает временную тестовую базу данных"""
    # Создаём временный файл для БД
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_file.close()
    
    # Настраиваем тестовую БД
    test_db = SqliteDatabase(temp_file.name)
    
    # Подключаем модели к тестовой БД
    database.initialize(test_db)
    
    # Создаём таблицы
    with test_db.bind_ctx([Part, Sale, SaleItem]):
        test_db.create_tables([Part, Sale, SaleItem])
        yield test_db
        
    # Очищаем после тестов
    test_db.close()
    os.unlink(temp_file.name)

@pytest.fixture
def sample_part(temp_db):
    """Создает тестовую запчасть"""
    return Part.create(
        article="TEST001",
        name="Тестовая запчасть",
        brand="TestBrand",
        car_model="TestModel",
        category="Тест",
        quantity=10,
        buy_price=100.0,
        sell_price=150.0,
        description="Тестовое описание"
    )

@pytest.fixture
def sample_parts(temp_db):
    """Создает несколько тестовых запчастей"""
    parts = []
    
    # Запчасть с хорошим остатком
    parts.append(Part.create(
        article="PART001",
        name="Масляный фильтр",
        brand="Toyota",
        car_model="Camry",
        category="Двигатель",
        quantity=15,
        buy_price=120.0,
        sell_price=180.0,
        description="Оригинальный масляный фильтр"
    ))
    
    # Запчасть с низким остатком
    parts.append(Part.create(
        article="PART002", 
        name="Воздушный фильтр",
        brand="Honda",
        car_model="Civic",
        category="Двигатель",
        quantity=2,
        buy_price=80.0,
        sell_price=120.0,
        description="Воздушный фильтр двигателя"
    ))
    
    # Запчасть без остатка
    parts.append(Part.create(
        article="PART003",
        name="Тормозные колодки",
        brand="BMW",
        car_model="3 Series", 
        category="Тормозная система",
        quantity=0,
        buy_price=200.0,
        sell_price=300.0,
        description="Передние тормозные колодки"
    ))
    
    return parts

@pytest.fixture
def sample_sale(temp_db, sample_part):
    """Создает тестовую продажу"""
    sale = Sale.create(total=150.0)
    
    SaleItem.create(
        sale=sale,
        part=sample_part.id,
        quantity=1,
        price=150.0
    )
    
    return sale 
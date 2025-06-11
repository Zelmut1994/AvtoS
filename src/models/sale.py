from peewee import (
    Model, DateTimeField, DecimalField, ForeignKeyField, IntegerField
)
from .database import database
from datetime import datetime

class Sale(Model):
    """Модель для хранения информации о продажах"""
    
    date = DateTimeField(default=datetime.now, verbose_name="Дата продажи")
    total = DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    
    class Meta:
        database = database
        table_name = 'sales'
    
    def __str__(self):
        return f"Продажа #{self.id} от {self.date.strftime('%d.%m.%Y %H:%M')}"
    
    @property
    def items_count(self):
        """Количество позиций в продаже"""
        return self.items.count()
    
    def calculate_total(self):
        """Пересчитать общую сумму на основе позиций"""
        total = sum(item.total_price for item in self.items)
        self.total = total
        self.save()
        return total

class SaleItem(Model):
    """Модель для хранения позиций продажи"""
    
    sale = ForeignKeyField(Sale, backref='items', verbose_name="Продажа")
    part = IntegerField(verbose_name="ID запчасти")  # Временно упростим
    quantity = IntegerField(verbose_name="Количество")
    price = DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    
    class Meta:
        database = database
        table_name = 'sale_items'
    
    @property
    def total_price(self):
        """Общая стоимость позиции"""
        return self.quantity * self.price
    
    def __str__(self):
        return f"Товар ID:{self.part} x{self.quantity} = {self.total_price} руб." 
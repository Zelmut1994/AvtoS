from peewee import (
    Model, CharField, IntegerField, DecimalField, TextField, 
    DateTimeField
)
from .database import database
from datetime import datetime

class Part(Model):
    """Модель для хранения информации о запчастях"""
    
    article = CharField(max_length=100, unique=True, verbose_name="Артикул")
    name = CharField(max_length=255, verbose_name="Наименование")
    brand = CharField(max_length=100, verbose_name="Марка")
    car_model = CharField(max_length=100, verbose_name="Модель")
    category = CharField(max_length=100, verbose_name="Категория")
    quantity = IntegerField(default=0, verbose_name="Количество")
    buy_price = DecimalField(max_digits=10, decimal_places=2, verbose_name="Закупочная цена")
    sell_price = DecimalField(max_digits=10, decimal_places=2, verbose_name="Розничная цена")
    description = TextField(null=True, verbose_name="Описание")
    created_at = DateTimeField(default=datetime.now, verbose_name="Дата создания")
    updated_at = DateTimeField(default=datetime.now, verbose_name="Дата обновления")
    
    class Meta:
        database = database
        table_name = 'parts'
        
    def save(self, *args, **kwargs):
        """Переопределяем save для обновления времени изменения"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.article} - {self.name}"
    
    @classmethod
    def search(cls, query):
        """Поиск запчастей по артикулу, названию, марке или модели"""
        return cls.select().where(
            (cls.article.contains(query)) |
            (cls.name.contains(query)) |
            (cls.brand.contains(query)) |
            (cls.car_model.contains(query))
        )
    
    @classmethod
    def get_by_article(cls, article):
        """Получить запчасть по артикулу"""
        try:
            return cls.get(cls.article == article)
        except cls.DoesNotExist:
            return None
    
    def reduce_quantity(self, amount):
        """Уменьшить количество на складе"""
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
            return True
        return False
    
    @property
    def profit_margin(self):
        """Расчет маржи прибыли"""
        if self.buy_price > 0:
            return ((self.sell_price - self.buy_price) / self.buy_price) * 100
        return 0 
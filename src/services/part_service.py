from typing import List, Optional
from decimal import Decimal

try:
from ..models import Part
except ImportError:
    # Для работы в тестах
    from models.part import Part

class PartService:
    """Сервис для работы с запчастями"""
    
    @staticmethod
    def create_part(article: str, name: str, brand: str, model: str, 
                   category: str, quantity: int, buy_price: Decimal, 
                   sell_price: Decimal, description: str = None) -> Part:
        """Создать новую запчасть"""
        part = Part.create(
            article=article,
            name=name,
            brand=brand,
            model=model,
            category=category,
            quantity=quantity,
            buy_price=buy_price,
            sell_price=sell_price,
            description=description
        )
        return part
    
    @staticmethod
    def get_all_parts() -> List[Part]:
        """Получить все запчасти"""
        return list(Part.select().order_by(Part.article))
    
    @staticmethod
    def get_parts_in_stock() -> List[Part]:
        """Получить запчасти с ненулевыми остатками"""
        return list(Part.select().where(Part.quantity > 0).order_by(Part.article))
    
    @staticmethod
    def search_parts(query: str) -> List[Part]:
        """Поиск запчастей по запросу"""
        if not query.strip():
            return PartService.get_all_parts()
        return list(Part.search(query.strip()))
    
    @staticmethod
    def get_part_by_id(part_id: int) -> Optional[Part]:
        """Получить запчасть по ID"""
        try:
            return Part.get_by_id(part_id)
        except Part.DoesNotExist:
            return None
    
    @staticmethod
    def get_part_by_article(article: str) -> Optional[Part]:
        """Получить запчасть по артикулу"""
        return Part.get_by_article(article)
    
    @staticmethod
    def update_part(part: Part, **kwargs) -> Part:
        """Обновить данные запчасти"""
        for key, value in kwargs.items():
            if hasattr(part, key):
                setattr(part, key, value)
        part.save()
        return part
    
    @staticmethod
    def delete_part(part: Part) -> bool:
        """Удалить запчасть"""
        try:
            part.delete_instance()
            return True
        except Exception:
            return False
    
    @staticmethod
    def check_availability(part: Part, quantity: int) -> bool:
        """Проверить доступность количества запчасти"""
        return part.quantity >= quantity
    
    @staticmethod
    def reduce_quantity(part: Part, quantity: int) -> bool:
        """Уменьшить количество запчасти на складе"""
        return part.reduce_quantity(quantity)
    
    @staticmethod
    def get_categories() -> List[str]:
        """Получить список всех категорий"""
        categories = Part.select(Part.category).distinct()
        return sorted([cat.category for cat in categories if cat.category])
    
    @staticmethod
    def get_brands() -> List[str]:
        """Получить список всех марок"""
        brands = Part.select(Part.brand).distinct()
        return sorted([brand.brand for brand in brands if brand.brand])
    
    @staticmethod
    def get_low_stock_parts(threshold: int = 5) -> List[Part]:
        """Получить запчасти с низким остатком"""
        return list(Part.select().where(
            (Part.quantity <= threshold) & (Part.quantity > 0)
        ).order_by(Part.quantity))
    
    @staticmethod
    def validate_article(article: str, exclude_id: int = None) -> bool:
        """Проверить уникальность артикула"""
        query = Part.select().where(Part.article == article)
        if exclude_id:
            query = query.where(Part.id != exclude_id)
        return not query.exists() 
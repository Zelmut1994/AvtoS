from typing import List, Dict, Tuple
from decimal import Decimal
from datetime import datetime, date

try:
from ..models import Sale, SaleItem, Part
except ImportError:
    # Для работы в тестах
    from models.sale import Sale, SaleItem
    from models.part import Part

class SaleService:
    """Сервис для работы с продажами"""
    
    @staticmethod
    def create_sale(items: List[Dict]) -> Tuple[Sale, bool]:
        """
        Создать новую продажу
        items: [{'part_id': int, 'quantity': int, 'price': Decimal}]
        Возвращает (Sale, success)
        """
        try:
            sale = Sale.create(total=0)
            total = Decimal('0')
            
            for item_data in items:
                part = Part.get_by_id(item_data['part_id'])
                quantity = item_data['quantity']
                price = item_data['price']
                
                # Проверяем доступность
                if not part.reduce_quantity(quantity):
                    # Откатываем транзакцию
                    sale.delete_instance()
                    return None, False
                
                # Создаем позицию продажи
                SaleItem.create(
                    sale=sale,
                    part=part,
                    quantity=quantity,
                    price=price
                )
                
                total += quantity * price
            
            # Обновляем общую сумму
            sale.total = total
            sale.save()
            
            return sale, True
            
        except Exception as e:
            print(f"Ошибка создания продажи: {e}")
            return None, False
    
    @staticmethod
    def get_all_sales() -> List[Sale]:
        """Получить все продажи"""
        return list(Sale.select().order_by(Sale.date.desc()))
    
    @staticmethod
    def get_sales_by_date(start_date: date, end_date: date) -> List[Sale]:
        """Получить продажи за период"""
        return list(Sale.select().where(
            Sale.date.between(start_date, end_date)
        ).order_by(Sale.date.desc()))
    
    @staticmethod
    def get_sale_by_id(sale_id: int) -> Sale:
        """Получить продажу по ID"""
        try:
            return Sale.get_by_id(sale_id)
        except Sale.DoesNotExist:
            return None
    
    @staticmethod
    def validate_sale_items(items: List[Dict]) -> Tuple[bool, List[str]]:
        """Валидация позиций продажи"""
        errors = []
        
        if not items:
            errors.append("Не выбраны товары для продажи")
            return False, errors
        
        for i, item in enumerate(items):
            try:
                part = Part.get_by_id(item['part_id'])
                quantity = item['quantity']
                
                if quantity <= 0:
                    errors.append(f"Позиция {i+1}: количество должно быть больше 0")
                
                if part.quantity < quantity:
                    errors.append(f"Позиция {i+1}: недостаточно товара на складе "
                                f"(доступно: {part.quantity}, требуется: {quantity})")
                
            except Part.DoesNotExist:
                errors.append(f"Позиция {i+1}: товар не найден")
            except (KeyError, TypeError, ValueError):
                errors.append(f"Позиция {i+1}: некорректные данные")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def calculate_change(total: Decimal, paid: Decimal) -> Decimal:
        """Рассчитать сдачу"""
        return paid - total if paid >= total else Decimal('0') 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class SalesWidget(QWidget):
    """Виджет для проведения продаж"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        
        # Временная заглушка
        label = QLabel("Раздел продаж")
        label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 20px;")
        layout.addWidget(label)
        
        # Кнопка для новой продажи
        self.new_sale_button = QPushButton("Новая продажа")
        layout.addWidget(self.new_sale_button)
        
        layout.addStretch()
    
    def new_sale(self):
        """Создать новую продажу"""
        print("Создание новой продажи...") 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class ReportsWidget(QWidget):
    """Виджет для отчётов"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        
        # Временная заглушка
        label = QLabel("Раздел отчётов")
        label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 20px;")
        layout.addWidget(label)
        
        # Кнопки отчётов
        stock_report_btn = QPushButton("Остатки на складе")
        layout.addWidget(stock_report_btn)
        
        sales_report_btn = QPushButton("История продаж")
        layout.addWidget(sales_report_btn)
        
        layout.addStretch() 
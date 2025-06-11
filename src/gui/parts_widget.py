from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class PartsWidget(QWidget):
    """Виджет для управления запчастями"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        
        # Временная заглушка
        label = QLabel("Раздел управления запчастями")
        label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 20px;")
        layout.addWidget(label)
        
        # Кнопка для добавления запчасти
        self.add_button = QPushButton("Добавить запчасть")
        layout.addWidget(self.add_button)
        
        layout.addStretch()
    
    def add_part(self):
        """Добавить новую запчасть"""
        print("Добавление новой запчасти...") 
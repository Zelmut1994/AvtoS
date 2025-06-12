 # --- ВАЖНО: Импортируем скомпилированные ресурсы ---
 try:
     import resources_rc
 except ImportError:
     print("⚠️ Файл ресурсов (resources_rc.py) не найден.")
     print("   Пожалуйста, запустите скрипт scripts/compile_resources.py")
 # --------------------------------------------------
 
 from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QTabWidget, QPushButton, QLabel, 
                              QMessageBox, QDialog, QFormLayout, QLineEdit,
                              QSpinBox, QDoubleSpinBox, QTextEdit, QTableWidget,
                              QTableWidgetItem, QHeaderView, QComboBox,
                              QAbstractItemView, QSplitter, QDateEdit, QGroupBox,
                              QScrollArea, QFrame, QGridLayout, QCheckBox,
                              QTreeView)
 from PySide6.QtCore import Qt, QTimer, QDate
 from PySide6.QtGui import (QFont, QAction, QColor, QStandardItemModel,
                            QStandardItem)
 from datetime import datetime, timedelta
 
 from database_simple import db
 from styles_enhanced import get_enhanced_complete_style, ENHANCED_COLORS, ICONS, ENHANCED_DIALOG_STYLES
 from settings_manager import get_settings
 from settings_dialog import show_settings_dialog
+from parts_dialogs import AddPartDialog, EditPartDialog
 
 # --- Глобальные переменные ---
 APP_NAME = "Система учёта автозапчастей"
 # ... existing code ...
-
-class AddPartDialog(QDialog):
-    """Диалог добавления запчасти"""
-    
-    def __init__(self, parent=None):
-        super().__init__(parent)
-        self.setWindowTitle("➕ Добавить новую запчасть")
-        self.setModal(True)
-        self.setMinimumSize(450, 600)
-        self._is_updating = False
-        
-        self.setup_ui()
-        self._connect_signals()
-    
-    def setup_ui(self):
-        layout = QFormLayout(self)
-        
-        # Поля ввода
-        self.article_input = QLineEdit()
-        self.article_input.setPlaceholderText("Например: ART001")
-        layout.addRow("Артикул*:", self.article_input)
-        
-        self.name_input = QLineEdit()
-        self.name_input.setPlaceholderText("Название запчасти")
-        layout.addRow("Наименование*:", self.name_input)
-        
-        self.brand_input = QLineEdit()
-        self.brand_input.setPlaceholderText("Например: Toyota (или 'Универсальная')")
-        layout.addRow("Марка:", self.brand_input)
-        
-        self.model_input = QLineEdit()
-        self.model_input.setPlaceholderText("Например: Camry (или 'Универсальная')")
-        layout.addRow("Модель:", self.model_input)
-        
-        self.category_input = QComboBox()
-        self.category_input.setEditable(True)
-        self.category_input.addItems([
-            "Двигатель", "Трансмиссия", "Тормозная система", 
-            "Подвеска", "Электрика", "Кузов", "Салон", 
-            "Универсальные", "Аксессуары", "Прочее"
-        ])
-        layout.addRow("Категория*:", self.category_input)
-        
-        self.quantity_input = QSpinBox()
-        self.quantity_input.setRange(0, 9999)
-        self.quantity_input.setValue(1)
-        layout.addRow("Количество*:", self.quantity_input)
-        
-        self.buy_price_input = QDoubleSpinBox()
-        self.buy_price_input.setRange(0.01, 999999.99)
-        self.buy_price_input.setDecimals(2)
-        self.buy_price_input.setSuffix(" ₽")
-        layout.addRow("Закупочная цена*:", self.buy_price_input)
-        
-        self.markup_input = QDoubleSpinBox()
-        self.markup_input.setRange(0, 9999)
-        self.markup_input.setDecimals(2)
-        self.markup_input.setSuffix(" %")
-        layout.addRow("Наценка:", self.markup_input)
-        
-        self.sell_price_input = QDoubleSpinBox()
-        self.sell_price_input.setRange(0.01, 999999.99)
-        self.sell_price_input.setDecimals(2)
-        self.sell_price_input.setSuffix(" ₽")
-        layout.addRow("Розничная цена*:", self.sell_price_input)
-        
-        self.description_input = QTextEdit()
-        self.description_input.setMaximumHeight(80)
-        self.description_input.setPlaceholderText("Дополнительная информация...")
-        layout.addRow("Описание:", self.description_input)
-        
-        # Кнопки
-        buttons_layout = QHBoxLayout()
-        
-        save_btn = QPushButton("💾 Сохранить")
-        save_btn.setProperty("class", "success")
-        save_btn.setProperty("class", "large")
-        save_btn.clicked.connect(self.save_part)
-        buttons_layout.addWidget(save_btn)
-        
-        cancel_btn = QPushButton("❌ Отмена")
-        cancel_btn.setProperty("class", "warning")
-        cancel_btn.clicked.connect(self.reject)
-        buttons_layout.addWidget(cancel_btn)
-        
-        layout.addRow(buttons_layout)
-    
-    def _connect_signals(self):
-        """Подключить сигналы для авто-расчета цен."""
-        self.buy_price_input.valueChanged.connect(self._update_sell_price)
-        self.markup_input.valueChanged.connect(self._update_sell_price)
-        self.sell_price_input.valueChanged.connect(self._update_markup)
-
-    def _update_sell_price(self):
-        """Обновить розничную цену на основе закупки и наценки."""
-        if self._is_updating:
-            return
-        self._is_updating = True
-        
-        buy_price = self.buy_price_input.value()
-        markup = self.markup_input.value()
-        
-        sell_price = buy_price * (1 + markup / 100)
-        self.sell_price_input.setValue(sell_price)
-        
-        self._is_updating = False
-
-    def _update_markup(self):
-        """Обновить наценку на основе закупочной и розничной цены."""
-        if self._is_updating:
-            return
-        self._is_updating = True
-        
-        buy_price = self.buy_price_input.value()
-        sell_price = self.sell_price_input.value()
-        
-        if buy_price > 0:
-            markup = ((sell_price / buy_price) - 1) * 100
-            self.markup_input.setValue(markup)
-        
-        self._is_updating = False
-    
-    def save_part(self):
-        """Сохранить запчасть"""
-        # Валидация
-        if not all([
-            self.article_input.text().strip(),
-            self.name_input.text().strip(),
-            self.category_input.currentText().strip()
-        ]):
-            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля (отмечены *)")
-            return
-        
-        # Добавление в базу
-        brand = self.brand_input.text().strip() or "Универсальная"
-        model = self.model_input.text().strip() or "Универсальная"
-        
-        success = db.add_part(
-            article=self.article_input.text().strip(),
-            name=self.name_input.text().strip(),
-            brand=brand,
-            car_model=model,
-            category=self.category_input.currentText().strip(),
-            quantity=self.quantity_input.value(),
-            buy_price=self.buy_price_input.value(),
-            sell_price=self.sell_price_input.value(),
-            description=self.description_input.toPlainText().strip()
-        )
-        
-        if success:
-            QMessageBox.information(self, "Успех", "Запчасть успешно добавлена!")
-            self.accept()
-        else:
-            QMessageBox.warning(self, "Ошибка", "Не удалось добавить запчасть.\nВозможно, артикул уже существует.")
-
-class EditPartDialog(QDialog):
-    """Диалог редактирования запчасти"""
-    
-    def __init__(self, part_data, parent=None):
-        super().__init__(parent)
-        self.part_data = part_data
-        self.setWindowTitle(f"✏️ Редактировать запчасть: {part_data['article']}")
-        self.setModal(True)
-        self.setMinimumSize(450, 600)
-        self._is_updating = False
-        
-        self.setup_ui()
-        self._connect_signals()
-        self.fill_data()
-    
-    def setup_ui(self):
-        layout = QFormLayout(self)
-        
-        # Поля ввода
-        self.article_input = QLineEdit()
-        self.article_input.setPlaceholderText("Например: ART001")
-        layout.addRow("Артикул*:", self.article_input)
-        
-        self.name_input = QLineEdit()
-        self.name_input.setPlaceholderText("Название запчасти")
-        layout.addRow("Наименование*:", self.name_input)
-        
-        self.brand_input = QLineEdit()
-        self.brand_input.setPlaceholderText("Например: Toyota (или 'Универсальная')")
-        layout.addRow("Марка:", self.brand_input)
-        
-        self.model_input = QLineEdit()
-        self.model_input.setPlaceholderText("Например: Camry (или 'Универсальная')")
-        layout.addRow("Модель:", self.model_input)
-        
-        self.category_input = QComboBox()
-        self.category_input.setEditable(True)
-        self.category_input.addItems([
-            "Двигатель", "Трансмиссия", "Тормозная система", 
-            "Подвеска", "Электрика", "Кузов", "Салон", 
-            "Универсальные", "Аксессуары", "Прочее"
-        ])
-        layout.addRow("Категория*:", self.category_input)
-        
-        self.quantity_input = QSpinBox()
-        self.quantity_input.setRange(0, 9999)
-        layout.addRow("Количество*:", self.quantity_input)
-        
-        self.buy_price_input = QDoubleSpinBox()
-        self.buy_price_input.setRange(0.01, 999999.99)
-        self.buy_price_input.setDecimals(2)
-        self.buy_price_input.setSuffix(" ₽")
-        layout.addRow("Закупочная цена*:", self.buy_price_input)
-        
-        self.markup_input = QDoubleSpinBox()
-        self.markup_input.setRange(0, 9999)
-        self.markup_input.setDecimals(2)
-        self.markup_input.setSuffix(" %")
-        layout.addRow("Наценка:", self.markup_input)
-        
-        self.sell_price_input = QDoubleSpinBox()
-        self.sell_price_input.setRange(0.01, 999999.99)
-        self.sell_price_input.setDecimals(2)
-        self.sell_price_input.setSuffix(" ₽")
-        layout.addRow("Розничная цена*:", self.sell_price_input)
-        
-        self.description_input = QTextEdit()
-        self.description_input.setMaximumHeight(80)
-        self.description_input.setPlaceholderText("Дополнительная информация...")
-        layout.addRow("Описание:", self.description_input)
-        
-        # Кнопки
-        buttons_layout = QHBoxLayout()
-        
-        save_btn = QPushButton("💾 Сохранить изменения")
-        save_btn.setProperty("class", "warning")
-        save_btn.setProperty("class", "large")
-        save_btn.clicked.connect(self.save_changes)
-        buttons_layout.addWidget(save_btn)
-        
-        cancel_btn = QPushButton("❌ Отмена")
-        cancel_btn.setProperty("class", "danger")
-        cancel_btn.clicked.connect(self.reject)
-        buttons_layout.addWidget(cancel_btn)
-        
-        layout.addRow(buttons_layout)
-    
-    def _connect_signals(self):
-        """Подключить сигналы для авто-расчета цен."""
-        self.buy_price_input.valueChanged.connect(self._update_sell_price)
-        self.markup_input.valueChanged.connect(self._update_sell_price)
-        self.sell_price_input.valueChanged.connect(self._update_markup)
-
-    def _update_sell_price(self):
-        """Обновить розничную цену на основе закупки и наценки."""
-        if self._is_updating:
-            return
-        self._is_updating = True
-        
-        buy_price = self.buy_price_input.value()
-        markup = self.markup_input.value()
-        
-        sell_price = buy_price * (1 + markup / 100)
-        self.sell_price_input.setValue(sell_price)
-        
-        self._is_updating = False
-
-    def _update_markup(self):
-        """Обновить наценку на основе закупочной и розничной цены."""
-        if self._is_updating:
-            return
-        self._is_updating = True
-        
-        buy_price = self.buy_price_input.value()
-        sell_price = self.sell_price_input.value()
-        
-        if buy_price > 0:
-            markup = ((sell_price / buy_price) - 1) * 100
-            self.markup_input.setValue(markup)
-        
-        self._is_updating = False
-    
-    def fill_data(self):
-        """Заполнить поля данными запчасти"""
-        self.article_input.setText(self.part_data['article'])
-        self.name_input.setText(self.part_data['name'])
-        self.brand_input.setText(self.part_data['brand'])
-        self.model_input.setText(self.part_data['car_model'])
-        
-        # Установить категорию
-        category_index = self.category_input.findText(self.part_data['category'])
-        if category_index >= 0:
-            self.category_input.setCurrentIndex(category_index)
-        else:
-            self.category_input.setEditText(self.part_data['category'])
-        
-        self.quantity_input.setValue(self.part_data['quantity'])
-        self.buy_price_input.setValue(float(self.part_data['buy_price']))
-        self.sell_price_input.setValue(float(self.part_data['sell_price']))
-        self._update_markup() # Рассчитываем наценку при загрузке
-        
-        if self.part_data['description']:
-            self.description_input.setPlainText(self.part_data['description'])
-    
-    def save_changes(self):
-        """Сохранить изменения"""
-        # Валидация
-        if not all([
-            self.article_input.text().strip(),
-            self.name_input.text().strip(),
-            self.category_input.currentText().strip()
-        ]):
-            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля (отмечены *)")
-            return
-        
-        # Подготовка данных
-        brand = self.brand_input.text().strip() or "Универсальная"
-        model = self.model_input.text().strip() or "Универсальная"
-        
-        # Обновление в базе
-        success = db.update_part(
-            part_id=self.part_data['id'],
-            article=self.article_input.text().strip(),
-            name=self.name_input.text().strip(),
-            brand=brand,
-            car_model=model,
-            category=self.category_input.currentText().strip(),
-            quantity=self.quantity_input.value(),
-            buy_price=self.buy_price_input.value(),
-            sell_price=self.sell_price_input.value(),
-            description=self.description_input.toPlainText().strip()
-        )
-        
-        if success:
-            QMessageBox.information(self, "Успех", "Запчасть успешно обновлена!")
-            self.accept()
-        else:
-            QMessageBox.warning(self, "Ошибка", "Не удалось обновить запчасть.\nВозможно, артикул уже используется.")
-
 class PartsWidget(QWidget):
     """Виджет для управления запчастями с базой данных"""
     
     def __init__(self, main_window=None):
         super().__init__()
         self.main_window = main_window
         self.setup_ui()
         self.load_parts()
     
     def setup_ui(self):
         layout = QVBoxLayout(self)
         
         # Заголовок и поиск
         header_layout = QHBoxLayout()
         
         title = QLabel("🔧 Управление запчастями")
         title.setProperty("class", "section-title")
         header_layout.addWidget(title)
         
         header_layout.addStretch()
         
         # Поле поиска
         self.search_input = QLineEdit()
         self.search_input.setPlaceholderText("🔍 Поиск по артикулу, названию, марке...")
         self.search_input.setMaximumWidth(300)

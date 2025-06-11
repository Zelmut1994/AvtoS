import sys
from datetime import datetime

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
from parts_dialogs import AddPartDialog, EditPartDialog

# --- Глобальные переменные ---
APP_NAME = "Система учёта автозапчастей"
# ... existing code ...
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
        self.search_input.textChanged.connect(self.search_parts)
        header_layout.addWidget(self.search_input)
        
        layout.addLayout(header_layout)
        
        # Кнопки действий
        actions_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Добавить запчасть")
        add_btn.setProperty("class", "success")
        add_btn.clicked.connect(self.add_part)
        actions_layout.addWidget(add_btn)
        
        self.edit_btn = QPushButton("✏️ Редактировать")
        self.edit_btn.setProperty("class", "warning")
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.edit_part)
        actions_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("🗑️ Удалить")
        self.delete_btn.setProperty("class", "danger")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_part)
        actions_layout.addWidget(self.delete_btn)
        
        actions_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.clicked.connect(self.load_parts)
        actions_layout.addWidget(refresh_btn)
        
        layout.addLayout(actions_layout)
        
        # Дерево запчастей
        self.tree = QTreeView()
        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.model = QStandardItemModel()
        self.tree.setModel(self.model)
        
        # Подключаем сигнал после установки модели
        self.tree.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        layout.addWidget(self.tree)
        
        # Статистика
        self.stats_label = QLabel("Загрузка...")
        self.stats_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.stats_label)
    
    def load_parts(self):
        """Загрузить запчасти из базы и сгруппировать по категориям"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels([
            "Наименование", "Артикул", "Марка", "Модель", 
            "Кол-во", "Закуп. цена", "Розн. цена"
        ])
        
        parts = db.get_all_parts()
        
        # Группировка по категориям
        categories = {}
        for part in parts:
            category = part.get('category', 'Без категории')
            if category not in categories:
                categories[category] = []
            categories[category].append(part)
            
        # Заполнение модели
        for category_name, parts_in_category in sorted(categories.items()):
            category_item = QStandardItem(f"📁 {category_name} ({len(parts_in_category)})")
            category_item.setEditable(False)
            category_item.setData(-1, Qt.UserRole) # ID для категории
            self.model.appendRow(category_item)
            
            for part in sorted(parts_in_category, key=lambda x: x['name']):
                name_item = QStandardItem(part['name'])
                name_item.setData(part['id'], Qt.UserRole) # Сохраняем ID запчасти
                
                article_item = QStandardItem(part['article'])
                brand_item = QStandardItem(part['brand'])
                model_item = QStandardItem(part['car_model'])
                
                qty_item = QStandardItem(str(part['quantity']))
                if part['quantity'] == 0:
                    qty_item.setBackground(QColor("#FF5252"))
                    qty_item.setForeground(QColor("white"))
                elif part['quantity'] <= 2:
                    qty_item.setBackground(QColor("#FFC107"))
                
                buy_price_item = QStandardItem(f"{part['buy_price']:.2f} ₽")
                sell_price_item = QStandardItem(f"{part['sell_price']:.2f} ₽")
                
                category_item.appendRow([
                    name_item, article_item, brand_item, model_item, 
                    qty_item, buy_price_item, sell_price_item
                ])

        # Растягиваем колонку с наименованием
        self.tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, self.model.columnCount()):
            self.tree.header().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        # Обновляем статистику
        total_parts = len(parts)
        total_quantity = sum(part['quantity'] for part in parts)
        in_stock = len([p for p in parts if p['quantity'] > 0])
        
        self.stats_label.setText(
            f"📊 Всего позиций: {total_parts} | "
            f"В наличии: {in_stock} | "
            f"Общее количество: {total_quantity} шт."
        )
    
    def search_parts(self):
        """Поиск запчастей по всем основным полям, регистронезависимый."""
        query = self.search_input.text().strip().lower()

        # Поиск работает по-старому, просто перезагружая отфильтрованный список
        # Для древовидного представления лучше фильтровать на месте, но это сложнее
        # Пока оставим так: поиск очищает дерево и показывает плоский список
        if not query:
            self.load_parts()
            return

        try:
            all_parts = db.get_all_parts()
            
            filtered_parts = []
            for part in all_parts:
                if (query in str(part['article']).lower() or 
                    query in str(part['name']).lower() or
                    query in str(part.get('brand', '')).lower() or
                    query in str(part.get('car_model', '')).lower() or
                    query in str(part.get('category', '')).lower()):
                    filtered_parts.append(part)
            
            self.model.clear()
            self.model.setHorizontalHeaderLabels([
                "Наименование", "Артикул", "Марка", "Модель", 
                "Кол-во", "Закуп. цена", "Розн. цена", "ID"
            ])
            
            if not filtered_parts:
                return
            
            self.model.setRowCount(len(filtered_parts))
            for i, part in enumerate(filtered_parts):
                self.model.setItem(i, 0, QStandardItem(part['name']))
                self.model.setItem(i, 1, QStandardItem(part['article']))
                self.model.setItem(i, 2, QStandardItem(part.get('brand', '')))
                self.model.setItem(i, 3, QStandardItem(part.get('car_model', '')))
                
                qty_item = QStandardItem(str(part['quantity']))
                if part['quantity'] == 0:
                    qty_item.setBackground(QColor("#FF5252"))
                    qty_item.setForeground(QColor("white"))
                elif part['quantity'] <= 2:
                    qty_item.setBackground(QColor("#FFC107"))
                self.model.setItem(i, 4, qty_item)
                
                self.model.setItem(i, 5, QStandardItem(f"{float(part['buy_price']):.2f} ₽"))
                self.model.setItem(i, 6, QStandardItem(f"{float(part['sell_price']):.2f} ₽"))
                
                id_item = QStandardItem(str(part['id']))
                id_item.setData(part['id'], Qt.UserRole)
                self.model.setItem(i, 7, id_item)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка поиска", f"Произошла ошибка: {str(e)}")
        
    def on_selection_changed(self, selected, deselected):
        """Изменение выделения в дереве"""
        indexes = self.tree.selectionModel().selectedIndexes()
        has_selection = len(indexes) > 0
        
        # Разрешаем редактирование/удаление только если выбрана запчасть (не категория)
        if has_selection:
            part_id = self.model.itemFromIndex(indexes[0]).data(Qt.UserRole)
            is_part = part_id is not None and part_id > 0
            self.edit_btn.setEnabled(is_part)
            self.delete_btn.setEnabled(is_part)
        else:
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
    
    def add_part(self):
        """Добавить запчасть"""
        dialog = AddPartDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_parts()
            # Обновляем все модули через главное окно
            if self.main_window:
                self.main_window.refresh_all_data()
    
    def edit_part(self):
        """Редактировать запчасть"""
        indexes = self.tree.selectionModel().selectedIndexes()
        if not indexes:
            return
            
        item = self.model.itemFromIndex(indexes[0])
        part_id = item.data(Qt.UserRole)
        
        if part_id and part_id > 0:
            part_data = db.get_part_by_id(part_id)
            
            if part_data:
                dialog = EditPartDialog(part_data, self)
                if dialog.exec() == QDialog.Accepted:
                    self.load_parts()
                    if self.main_window:
                        self.main_window.refresh_all_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные запчасти")
    
    def delete_part(self):
        """Удалить запчасть"""
        indexes = self.tree.selectionModel().selectedIndexes()
        if not indexes:
            return
            
        item = self.model.itemFromIndex(indexes[0])
        part_id = item.data(Qt.UserRole)
        
        # Получаем артикул из второго столбца
        # Для дочерних элементов item.row() вернет индекс относительно родителя,
        # нужно получить доступ к модели через index.row() и index.parent()
        index = indexes[0]
        parent = index.parent()
        row = index.row()
        
        # Артикул находится во втором столбце (индекс 1)
        article_item = self.model.itemFromIndex(parent.child(row, 1))
        article = article_item.text() if article_item else ""
        
        if part_id and part_id > 0:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Подтверждение")
            msg_box.setText(f"Удалить запчасть {article}?")
            msg_box.setIcon(QMessageBox.Question)
            
            yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
            no_button = msg_box.addButton("Нет", QMessageBox.NoRole)
            
            msg_box.exec()

            if msg_box.clickedButton() == yes_button:
                if db.delete_part(part_id):
                    QMessageBox.information(self, "Успех", "Запчасть удалена!")
                    self.load_parts()
                    if self.main_window:
                        self.main_window.refresh_all_data()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить запчасть")

class SalesWidget(QWidget):
    """Виджет для проведения продаж"""
    
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.cart_items = []  # Корзина товаров
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        # Левая панель - выбор товаров
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Заголовок и поиск товаров
        title_label = QLabel("💰 Продажи")
        title_label.setProperty("class", "section-title")
        left_layout.addWidget(title_label)
        
        search_layout = QHBoxLayout()
        search_label = QLabel("Поиск товара:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите артикул или название...")
        self.search_input.textChanged.connect(self.search_products)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        
        # Кнопка обновления
        refresh_btn = QPushButton("🔄")
        refresh_btn.setToolTip("Обновить список товаров")
        refresh_btn.setMaximumWidth(40)
        refresh_btn.setProperty("class", "small")
        refresh_btn.clicked.connect(self.load_products)
        search_layout.addWidget(refresh_btn)
        
        left_layout.addLayout(search_layout)
        
        # Таблица товаров
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Артикул", "Наименование", "Остаток", "Цена"
        ])
        
        # Настройка таблицы товаров
        products_header = self.products_table.horizontalHeader()
        products_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        products_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Артикул
        products_header.setSectionResizeMode(2, QHeaderView.Stretch)           # Название
        products_header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Остаток
        products_header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Цена
        
        self.products_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.itemDoubleClicked.connect(self.add_to_cart)
        
        # Применяем стили для исправления зачеркивания (копируем стиль из корзины)
        self.products_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
                text-decoration: none;
            }
            QTableWidget::item:hover {
                background-color: #F5F5F5;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #2196F3;
                font-weight: bold;
            }
        """)
        
        left_layout.addWidget(self.products_table)
        
        # Кнопка добавления в корзину
        add_to_cart_btn = QPushButton("🛒 Добавить в корзину")
        add_to_cart_btn.setProperty("class", "large")
        add_to_cart_btn.clicked.connect(self.add_to_cart)
        left_layout.addWidget(add_to_cart_btn)
        
        # Правая панель - корзина
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        cart_title = QLabel("🛒 Корзина")
        cart_title.setProperty("class", "subsection-title")
        right_layout.addWidget(cart_title)
        
        # Таблица корзины
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(6)
        self.cart_table.setHorizontalHeaderLabels([
            "Артикул", "Наименование", "Кол-во", "Цена за ед.", "Сумма", "Действия"
        ])
        
        cart_header = self.cart_table.horizontalHeader()
        cart_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Артикул
        cart_header.setSectionResizeMode(1, QHeaderView.Stretch)           # Наименование - растягивается
        cart_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Количество
        cart_header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Цена
        cart_header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Сумма
        cart_header.setSectionResizeMode(5, QHeaderView.Fixed)             # Кнопки - фиксированная ширина
        
        # Устанавливаем фиксированную ширину для колонки с кнопкой
        self.cart_table.setColumnWidth(5, 70)  # Ширина для одной кнопки
        
        self.cart_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.cart_table.setAlternatingRowColors(True)
        self.cart_table.verticalHeader().setVisible(False)
        self.cart_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Исправляем стили для предотвращения зачеркивания
        self.cart_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
                text-decoration: none;
            }
            QTableWidget::item:hover {
                background-color: #F5F5F5;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #2196F3;
                font-weight: bold;
            }
        """)
        
        right_layout.addWidget(self.cart_table)
        
        # Кнопки управления корзиной
        cart_buttons_layout = QHBoxLayout()
        
        remove_btn = QPushButton("❌ Удалить")
        remove_btn.setProperty("class", "danger")
        remove_btn.clicked.connect(self.remove_from_cart)
        cart_buttons_layout.addWidget(remove_btn)
        
        clear_btn = QPushButton("🗑️ Очистить всё")
        clear_btn.setProperty("class", "warning")
        clear_btn.clicked.connect(self.clear_cart)
        cart_buttons_layout.addWidget(clear_btn)
        
        cart_buttons_layout.addStretch()
        right_layout.addLayout(cart_buttons_layout)
        
        # Итоговая сумма
        self.total_label = QLabel("Итого: 0.00 ₽")
        self.total_label.setProperty("class", "total")
        right_layout.addWidget(self.total_label)
        
        # Кнопка оформления продажи
        checkout_btn = QPushButton("💳 Оформить продажу")
        checkout_btn.setProperty("class", "success")
        checkout_btn.setProperty("class", "large")
        checkout_btn.clicked.connect(self.checkout)
        right_layout.addWidget(checkout_btn)
        
        # Добавляем панели в основной layout
        layout.addWidget(left_panel, 3)  # 3/5 ширины
        layout.addWidget(right_panel, 2)  # 2/5 ширины
        
        # Загружаем товары
        self.load_products()
    
    def load_products(self):
        """Загрузить товары из базы"""
        parts = db.get_all_parts()
        # Показываем только товары с остатком > 0
        in_stock_parts = [p for p in parts if p['quantity'] > 0]
        
        self.products_table.setRowCount(len(in_stock_parts))
        
        for row, part in enumerate(in_stock_parts):
            self.products_table.setItem(row, 0, QTableWidgetItem(str(part['id'])))
            self.products_table.setItem(row, 1, QTableWidgetItem(part['article']))
            self.products_table.setItem(row, 2, QTableWidgetItem(part['name']))
            self.products_table.setItem(row, 3, QTableWidgetItem(str(part['quantity'])))
            self.products_table.setItem(row, 4, QTableWidgetItem(f"{part['sell_price']:.2f} ₽"))
    
    def search_products(self):
        """Поиск товаров"""
        query = self.search_input.text().strip()
        
        if not query:
            self.load_products()
            return
        
        try:
            # Используем Python-side фильтрацию как в модуле поступлений
            all_parts = db.get_all_parts()
            query_lower = query.lower()
            
            filtered_parts = []
            for part in all_parts:
                if (query_lower in part['article'].lower() or 
                    query_lower in part['name'].lower() or
                    query_lower in part['brand'].lower() or
                    query_lower in part['car_model'].lower() or
                    query_lower in part['category'].lower()):
                    filtered_parts.append(part)
            
            # Показываем только товары с остатком > 0
            in_stock_parts = [p for p in filtered_parts if p['quantity'] > 0]
            
            self.products_table.setRowCount(len(in_stock_parts))
            
            for row, part in enumerate(in_stock_parts):
                self.products_table.setItem(row, 0, QTableWidgetItem(str(part['id'])))
                self.products_table.setItem(row, 1, QTableWidgetItem(part['article']))
                self.products_table.setItem(row, 2, QTableWidgetItem(part['name']))
                self.products_table.setItem(row, 3, QTableWidgetItem(str(part['quantity'])))
                self.products_table.setItem(row, 4, QTableWidgetItem(f"{part['sell_price']:.2f} ₽"))
            
        except Exception as e:
            print(f"❌ Ошибка поиска товаров: {e}")
    
    def add_to_cart(self):
        """Добавить товар в корзину"""
        current_row = self.products_table.currentRow()
        if current_row >= 0:
            part_id = int(self.products_table.item(current_row, 0).text())
            article = self.products_table.item(current_row, 1).text()
            name = self.products_table.item(current_row, 2).text()
            available = int(self.products_table.item(current_row, 3).text())
            price = float(self.products_table.item(current_row, 4).text().replace(' ₽', ''))
            
            # Запрашиваем количество
            from PySide6.QtWidgets import QInputDialog
            quantity, ok = QInputDialog.getInt(
                self, "Количество", 
                f"Введите количество для {article} (доступно: {available}):",
                1  # значение по умолчанию
            )
            
            if ok:
                if quantity <= 0:
                    QMessageBox.warning(self, "Ошибка", "Количество должно быть больше 0")
                    return
                # Дополнительная валидация количества
                if quantity > available:
                    QMessageBox.warning(self, "Ошибка", f"Недостаточно товара на складе!\nДоступно: {available}, запрошено: {quantity}")
                    return
                
                # Проверяем, есть ли товар уже в корзине
                existing_item = None
                for item in self.cart_items:
                    if item['part_id'] == part_id:
                        existing_item = item
                        break
                
                if existing_item:
                    # Увеличиваем количество
                    new_quantity = existing_item['quantity'] + quantity
                    if new_quantity <= available:
                        existing_item['quantity'] = new_quantity
                    else:
                        QMessageBox.warning(self, "Ошибка", f"Недостаточно товара на складе!\nДоступно: {available}")
                        return
                else:
                    # Добавляем новый товар
                    self.cart_items.append({
                        'part_id': part_id,
                        'article': article,
                        'name': name,
                        'quantity': quantity,
                        'price': price
                    })
                
                self.update_cart_display()
    
    def update_cart_display(self):
        """Обновить отображение корзины"""
        self.cart_table.setRowCount(len(self.cart_items))
        
        total = 0
        for row, item in enumerate(self.cart_items):
            item_total = item['quantity'] * item['price']
            total += item_total
            
            # Артикул
            article_item = QTableWidgetItem(item['article'])
            article_item.setTextAlignment(Qt.AlignCenter)
            self.cart_table.setItem(row, 0, article_item)
            
            # Наименование
            self.cart_table.setItem(row, 1, QTableWidgetItem(item['name']))
            
            # Количество
            qty_item = QTableWidgetItem(f"{item['quantity']} шт.")
            qty_item.setTextAlignment(Qt.AlignCenter)
            self.cart_table.setItem(row, 2, qty_item)
            
            # Цена
            price_item = QTableWidgetItem(f"{item['price']:.2f} ₽")
            price_item.setTextAlignment(Qt.AlignRight)
            self.cart_table.setItem(row, 3, price_item)
            
            # Сумма
            total_item = QTableWidgetItem(f"{item_total:.2f} ₽")
            total_item.setTextAlignment(Qt.AlignRight)
            total_item.setFont(QFont("Arial", 10, QFont.Bold))
            self.cart_table.setItem(row, 4, total_item)
            
            # Кнопка действий максимально слева
            button_container = QWidget()
            button_layout = QHBoxLayout(button_container)
            button_layout.setContentsMargins(2, 2, 10, 2)  # Минимальный отступ слева, больше справа
            
            edit_btn = QPushButton("⚙️")
            edit_btn.setToolTip("Изменить количество или применить скидку")
            edit_btn.setFixedSize(45, 26)  # Еще меньше размер
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """)
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_item(r))
            
            button_layout.addWidget(edit_btn)
            button_layout.addStretch()  # Растяжка справа
            self.cart_table.setCellWidget(row, 5, button_container)
            
            # Высота строки
            self.cart_table.setRowHeight(row, 45)
        
        self.total_label.setText(f"Итого: {total:.2f} ₽")
    
    def edit_item(self, row):
        """Универсальное редактирование товара в корзине (стабильная версия v3)"""
        if not (0 <= row < len(self.cart_items)):
            return
            
        item = self.cart_items[row]
        current_price = item['price']
        current_qty = item['quantity']
        
        part = db.get_part_by_id(item['part_id'])
        if not part:
            QMessageBox.warning(self, "Ошибка", "Товар не найден в базе данных")
            return
        
        available = part['quantity'] + current_qty
        
        try:
            dialog = QDialog(self)
            dialog.setModal(True)
            dialog.setWindowTitle("Редактировать товар")
            dialog.setFixedSize(500, 450)
            
            # Упрощенные стили без градиентов
            dialog.setStyleSheet("""
                QDialog { 
                    background-color: #f5f5f5; 
                }
                QLabel {
                    color: #333;
                }
                QLineEdit, QSpinBox {
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background: white;
                }
                QPushButton {
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
            """)

            # Главный layout с фиксированными отступами
            main_layout = QVBoxLayout(dialog)
            main_layout.setContentsMargins(20, 20, 20, 20)
            main_layout.setSpacing(20)

            # Заголовок
            title = QLabel("⚙️ Редактирование товара")
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
            main_layout.addWidget(title)
            
            # Информация о товаре (используем QWidget вместо QFrame)
            info_widget = QWidget()
            info_widget.setStyleSheet("""
                QWidget {
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }
            """)
            info_layout = QFormLayout(info_widget)
            info_layout.setContentsMargins(15, 15, 15, 15)
            info_layout.setSpacing(10)
            
            # Поля только для чтения
            name_label = QLabel(item.get('name', 'N/A'))
            name_label.setWordWrap(True)
            article_label = QLabel(item.get('article', 'N/A'))
            price_label = QLabel(f"{current_price:.2f} ₽")
            
            info_layout.addRow("Название:", name_label)
            info_layout.addRow("Артикул:", article_label)
            info_layout.addRow("Текущая цена:", price_label)
            
            main_layout.addWidget(info_widget)
            
            # Количество
            qty_widget = QWidget()
            qty_widget.setStyleSheet("""
                QWidget {
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }
            """)
            qty_layout = QHBoxLayout(qty_widget)
            qty_layout.setContentsMargins(15, 15, 15, 15)
            
            qty_layout.addWidget(QLabel(f"В наличии: {available} шт."))
            qty_layout.addStretch()
            qty_layout.addWidget(QLabel("Количество:"))
            
            qty_input = QSpinBox()
            qty_input.setMinimum(1)
            qty_input.setMaximum(available)
            qty_input.setValue(current_qty)
            qty_input.setSuffix(" шт.")
            qty_layout.addWidget(qty_input)
            
            main_layout.addWidget(qty_widget)
            
            # Скидка
            discount_widget = QWidget()
            discount_widget.setStyleSheet("""
                QWidget {
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }
            """)
            discount_layout = QVBoxLayout(discount_widget)
            discount_layout.setContentsMargins(15, 15, 15, 15)
            
            discount_layout.addWidget(QLabel("Скидка (сумма):"))
            
            discount_input = QLineEdit("0")
            discount_input.setPlaceholderText("Введите сумму скидки")
            discount_layout.addWidget(discount_input)
            
            preview_label = QLabel(f"Новая цена: {current_price:.2f} ₽")
            preview_label.setAlignment(Qt.AlignCenter)
            preview_label.setStyleSheet("""
                padding: 8px;
                background: #e8f5e9;
                border: 1px solid #4caf50;
                border-radius: 4px;
                color: #2e7d32;
                font-weight: bold;
            """)
            discount_layout.addWidget(preview_label)
            
            def update_preview():
                try:
                    discount_value = float(discount_input.text().replace(",", ".")) if discount_input.text() else 0
                    if 0 <= discount_value < current_price:
                        new_price = current_price - discount_value
                        preview_label.setText(f"Новая цена: {new_price:.2f} ₽")
                        preview_label.setStyleSheet("""
                            padding: 8px;
                            background: #e8f5e9;
                            border: 1px solid #4caf50;
                            border-radius: 4px;
                            color: #2e7d32;
                            font-weight: bold;
                        """)
                    else:
                        preview_label.setText("Некорректная скидка!")
                        preview_label.setStyleSheet("""
                            padding: 8px;
                            background: #ffebee;
                            border: 1px solid #f44336;
                            border-radius: 4px;
                            color: #d32f2f;
                            font-weight: bold;
                        """)
                except ValueError:
                    preview_label.setText("Некорректная скидка!")
                    preview_label.setStyleSheet("""
                        padding: 8px;
                        background: #ffebee;
                        border: 1px solid #f44336;
                        border-radius: 4px;
                        color: #d32f2f;
                        font-weight: bold;
                    """)
            
            discount_input.textChanged.connect(update_preview)
            main_layout.addWidget(discount_widget)
            
            # Разделитель
            main_layout.addStretch()
            
            # Кнопки
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(10)
            
            ok_btn = QPushButton("✅ Применить")
            ok_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4caf50;
                    color: white;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            
            cancel_btn = QPushButton("❌ Отмена")
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            
            buttons_layout.addStretch()
            buttons_layout.addWidget(ok_btn)
            buttons_layout.addWidget(cancel_btn)
            buttons_layout.addStretch()
            
            main_layout.addLayout(buttons_layout)
            
            # Подключение сигналов
            ok_btn.clicked.connect(dialog.accept)
            cancel_btn.clicked.connect(dialog.reject)
            
            # Показываем диалог
            if dialog.exec() == QDialog.Accepted:
                new_qty = qty_input.value()
                try:
                    discount_value = float(discount_input.text().replace(",", ".")) if discount_input.text() else 0
                    if not (0 <= discount_value < item['price']):
                        raise ValueError("Invalid discount")
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Некорректная сумма скидки.")
                    return
                
                item['quantity'] = new_qty
                item['price'] = current_price - discount_value
                self.update_cart_display()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть диалог: {str(e)}")
    
    def remove_from_cart(self):
        """Удалить товар из корзины"""
        current_row = self.cart_table.currentRow()
        if current_row >= 0:
            del self.cart_items[current_row]
            self.update_cart_display()
    
    def clear_cart(self):
        """Очистить корзину"""
        if self.cart_items:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Подтверждение")
            msg_box.setText("Очистить корзину?")
            msg_box.setIcon(QMessageBox.Question)
            
            yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
            no_button = msg_box.addButton("Нет", QMessageBox.NoRole)
            
            msg_box.exec()

            if msg_box.clickedButton() == yes_button:
                self.cart_items.clear()
                self.update_cart_display()
    
    def checkout(self):
        """Оформить продажу"""
        if not self.cart_items:
            QMessageBox.warning(self, "Ошибка", "Корзина пуста!")
            return
        
        # Подтверждение продажи
        total = sum(item['quantity'] * item['price'] for item in self.cart_items)
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение продажи")
        msg_box.setText(f"Оформить продажу на сумму {total:.2f} ₽?")
        msg_box.setIcon(QMessageBox.Question)
        
        yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
        no_button = msg_box.addButton("Нет", QMessageBox.NoRole)
        
        msg_box.exec()
        
        if msg_box.clickedButton() == yes_button:
            # Создаем продажу
            sale_items = [
                {
                    'part_id': item['part_id'],
                    'quantity': item['quantity'],
                    'price': item['price']
                }
                for item in self.cart_items
            ]
            
            if db.create_sale(sale_items):
                QMessageBox.information(self, "Успех", 
                    f"Продажа оформлена!\n"
                    f"Сумма: {total:.2f} ₽\n"
                    f"Товары списаны со склада.")
                
                # Очищаем корзину и обновляем список товаров
                self.cart_items.clear()
                self.update_cart_display()
                self.load_products()
                
                # Обновляем все модули через главное окно
                if self.main_window:
                    self.main_window.refresh_all_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось оформить продажу!\nВозможно, недостаточно товара на складе.")


class ReceiptsWidget(QWidget):
    """Виджет поступлений товара"""
    
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.receipt_items = []  # Позиции текущего поступления
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Полный набор стилей для таблиц, который гарантированно убирает зачеркивание
        table_stylesheet = """
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
                text-decoration: none; /* Убираем зачеркивание */
            }
            QTableWidget::item:hover {
                background-color: #F5F5F5;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #2196F3;
                font-weight: bold;
            }
        """

        # Заголовок
        title = QLabel("📦 Поступление товаров")
        title.setProperty("class", "section-title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Основной контейнер с разделителем
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # === ЛЕВАЯ ПАНЕЛЬ - КОМПАКТНАЯ ИСТОРИЯ ===
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(5, 0, 5, 0)
        
        history_label = QLabel("📋 История")
        history_label.setProperty("class", "subsection-title")
        left_layout.addWidget(history_label)
        
        # Компактная таблица поступлений
        self.receipts_table = QTableWidget()
        self.receipts_table.setColumnCount(3)
        self.receipts_table.setHorizontalHeaderLabels([
            "Дата", "Поставщик", "Сумма"
        ])
        
        # Настройка колонок для компактности
        header = self.receipts_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Дата
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # Поставщик  
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Сумма
        
        self.receipts_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.receipts_table.doubleClicked.connect(self.show_receipt_details_from_history)
        self.receipts_table.setStyleSheet(table_stylesheet)
        left_layout.addWidget(self.receipts_table)
        
        splitter.addWidget(left_widget)
        
        # === ПРАВАЯ ПАНЕЛЬ - РАБОЧАЯ ОБЛАСТЬ ===
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 0, 5, 0)
        right_layout.setSpacing(10)
        
        # === 1. ФОРМА ПОСТАВЩИКА (КОМПАКТНАЯ) ===
        supplier_layout = QHBoxLayout()
        
        supplier_label = QLabel("Поставщик:")
        supplier_label.setMinimumWidth(80)
        supplier_layout.addWidget(supplier_label)
        
        self.supplier_input = QLineEdit()
        self.supplier_input.setPlaceholderText("Введите название поставщика...")
        supplier_layout.addWidget(self.supplier_input)
        
        add_new_btn = QPushButton("➕ Новый товар")
        add_new_btn.setProperty("class", "success")
        add_new_btn.clicked.connect(self.add_new_part)
        supplier_layout.addWidget(add_new_btn)
        
        right_layout.addLayout(supplier_layout)
        
        # Примечания (одной строкой)
        notes_layout = QHBoxLayout()
        notes_label = QLabel("Примечания:")
        notes_label.setMinimumWidth(80)
        notes_layout.addWidget(notes_label)
        
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Дополнительная информация...")
        notes_layout.addWidget(self.notes_input)
        
        right_layout.addLayout(notes_layout)
        
        # === 2. ПОИСК ТОВАРОВ ===
        search_layout = QHBoxLayout()
        search_label = QLabel("Поиск:")
        search_label.setMinimumWidth(80)
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Поиск товара по артикулу или названию...")
        self.search_input.textChanged.connect(self.search_parts)
        search_layout.addWidget(self.search_input)
        
        right_layout.addLayout(search_layout)
        
        # === 3. ТАБЛИЦА ПОИСКА (УВЕЛИЧЕННАЯ) ===
        search_label = QLabel("Найденные товары (двойной клик для добавления):")
        search_label.setProperty("class", "stat-label")
        right_layout.addWidget(search_label)
        
        self.parts_table = QTableWidget()
        self.parts_table.setColumnCount(3)
        self.parts_table.setHorizontalHeaderLabels([
            "Артикул", "Наименование", "Остаток"
        ])
        
        parts_header = self.parts_table.horizontalHeader()
        parts_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        parts_header.setSectionResizeMode(1, QHeaderView.Stretch)
        parts_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.parts_table.setMaximumHeight(200)
        self.parts_table.setMinimumHeight(200)
        self.parts_table.setAlternatingRowColors(True)
        self.parts_table.doubleClicked.connect(self.add_part_from_table)
        self.parts_table.setStyleSheet(table_stylesheet)
        right_layout.addWidget(self.parts_table)
        
        # === 4. ТОВАРЫ В ПОСТУПЛЕНИИ (УВЕЛИЧЕННАЯ) ===
        items_label = QLabel("Товары в поступлении:")
        items_label.setProperty("class", "stat-label")
        right_layout.addWidget(items_label)
        
        self.receipt_items_table = QTableWidget()
        self.receipt_items_table.setColumnCount(6)
        self.receipt_items_table.setHorizontalHeaderLabels([
            "Артикул", "Наименование", "Кол-во", "Цена", "Сумма", ""
        ])
        
        items_header = self.receipt_items_table.horizontalHeader()
        items_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        items_header.setSectionResizeMode(1, QHeaderView.Stretch)
        items_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        items_header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        items_header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        items_header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        self.receipt_items_table.setAlternatingRowColors(True)
        self.receipt_items_table.setMinimumHeight(200)
        self.receipt_items_table.setStyleSheet(table_stylesheet)
        right_layout.addWidget(self.receipt_items_table)
        
        # === 5. ИТОГИ И КНОПКИ ===
        bottom_layout = QHBoxLayout()
        
        # Итоговая сумма
        self.total_label = QLabel("Итого: 0.00 ₽")
        self.total_label.setProperty("class", "total")
        bottom_layout.addWidget(self.total_label)
        
        bottom_layout.addStretch()
        
        # Кнопки
        clear_btn = QPushButton("🗑️ Очистить")
        clear_btn.setProperty("class", "warning")
        clear_btn.clicked.connect(self.clear_receipt)
        bottom_layout.addWidget(clear_btn)
        
        save_btn = QPushButton("💾 Оформить поступление")
        save_btn.setProperty("class", "success")
        save_btn.setProperty("class", "large")
        save_btn.clicked.connect(self.save_receipt)
        bottom_layout.addWidget(save_btn)
        
        right_layout.addLayout(bottom_layout)
        
        splitter.addWidget(right_widget)
        
        # Настройка пропорций: история компактная, рабочая область большая
        splitter.setSizes([300, 700])
        
        # Инициализация данных
        self.receipt_items = []
        
        # Загружаем данные
        self.load_receipts()
        self.load_parts()
    
    def load_receipts(self):
        """Загрузить историю поступлений"""
        try:
            receipts = db.get_all_receipts()
            self.receipts_table.setRowCount(len(receipts))
            
            for row, receipt in enumerate(receipts):
                # Дата (компактный формат)
                receipt_date = datetime.fromisoformat(receipt['date']).strftime("%d.%m.%Y")
                date_item = QTableWidgetItem(receipt_date)
                date_item.setData(Qt.UserRole, receipt['id'])  # Сохраняем ID для двойного клика
                self.receipts_table.setItem(row, 0, date_item)
                
                # Поставщик
                self.receipts_table.setItem(row, 1, QTableWidgetItem(receipt['supplier']))
                
                # Сумма
                self.receipts_table.setItem(row, 2, QTableWidgetItem(f"{receipt['total']:,.2f} ₽"))
            
        except Exception as e:
            print(f"❌ Ошибка загрузки поступлений: {e}")
    
    def load_parts(self):
        """Загрузить список товаров для поиска"""
        try:
            parts = db.get_all_parts()
            self.parts_table.setRowCount(len(parts))
            
            for row, part in enumerate(parts):
                article_item = QTableWidgetItem(part['article'])
                article_item.setData(Qt.UserRole, part)  # Сохраняем данные товара
                # Принудительно устанавливаем обычный шрифт
                font = article_item.font()
                font.setStrikeOut(False)
                article_item.setFont(font)
                self.parts_table.setItem(row, 0, article_item)
                
                name_item = QTableWidgetItem(part['name'])
                font = name_item.font()
                font.setStrikeOut(False)
                name_item.setFont(font)
                self.parts_table.setItem(row, 1, name_item)
                
                qty_item = QTableWidgetItem(str(part['quantity']))
                font = qty_item.font()
                font.setStrikeOut(False)
                qty_item.setFont(font)
                self.parts_table.setItem(row, 2, qty_item)
            
        except Exception as e:
            print(f"❌ Ошибка загрузки товаров: {e}")
    
    def search_parts(self):
        """Поиск товаров"""
        query = self.search_input.text().strip()
        if not query:
            self.load_parts()
            return
        
        try:
            # Используем функцию поиска из базы (работает для Python-side фильтрации)
            all_parts = db.get_all_parts()
            query_lower = query.lower()
            
            filtered_parts = []
            for part in all_parts:
                if (query_lower in part['article'].lower() or 
                    query_lower in part['name'].lower() or
                    query_lower in part['brand'].lower() or
                    query_lower in part['car_model'].lower() or
                    query_lower in part['category'].lower()):
                    filtered_parts.append(part)
            
            self.parts_table.setRowCount(len(filtered_parts))
            
            for row, part in enumerate(filtered_parts):
                article_item = QTableWidgetItem(part['article'])
                article_item.setData(Qt.UserRole, part)  # Сохраняем данные товара
                # Принудительно устанавливаем обычный шрифт
                font = article_item.font()
                font.setStrikeOut(False)
                article_item.setFont(font)
                self.parts_table.setItem(row, 0, article_item)
                
                name_item = QTableWidgetItem(part['name'])
                font = name_item.font()
                font.setStrikeOut(False)
                name_item.setFont(font)
                self.parts_table.setItem(row, 1, name_item)
                
                qty_item = QTableWidgetItem(str(part['quantity']))
                font = qty_item.font()
                font.setStrikeOut(False)
                qty_item.setFont(font)
                self.parts_table.setItem(row, 2, qty_item)
            
        except Exception as e:
            print(f"❌ Ошибка поиска: {e}")
    
    def add_part_to_receipt(self, part):
        """Добавить товар в поступление"""
        try:
            # Запрашиваем количество и закупочную цену
            from PySide6.QtWidgets import QInputDialog
            
            quantity, ok = QInputDialog.getInt(
                self, "Количество", 
                f"Введите количество для {part['article']}:",
                1  # значение по умолчанию
            )
            
            if not ok or quantity <= 0:
                return
            
            buy_price, ok = QInputDialog.getDouble(
                self, "Закупочная цена", 
                f"Введите закупочную цену за единицу {part['article']}:",
                part['buy_price'], 0.01, 999999.99, 2
            )
            
            if not ok or buy_price <= 0:
                return
            
            # Проверяем, есть ли товар уже в поступлении
            existing_item = None
            for item in self.receipt_items:
                if item['part_id'] == part['id']:
                    existing_item = item
                    break
            
            if existing_item:
                # Увеличиваем количество
                existing_item['quantity'] += quantity
                existing_item['buy_price'] = buy_price  # Обновляем цену
            else:
                # Добавляем новый товар
                self.receipt_items.append({
                    'part_id': part['id'],
                    'article': part['article'],
                    'name': part['name'],
                    'quantity': quantity,
                    'buy_price': buy_price
                })
            
            self.update_receipt_display()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить товар: {e}")
    
    def update_receipt_display(self):
        """Обновить отображение товаров в поступлении"""
        self.receipt_items_table.setRowCount(len(self.receipt_items))
        
        total = 0
        for row, item in enumerate(self.receipt_items):
            item_total = item['quantity'] * item['buy_price']
            total += item_total
            
            self.receipt_items_table.setItem(row, 0, QTableWidgetItem(item['article']))
            self.receipt_items_table.setItem(row, 1, QTableWidgetItem(item['name']))
            self.receipt_items_table.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
            self.receipt_items_table.setItem(row, 3, QTableWidgetItem(f"{item['buy_price']:.2f} ₽"))
            self.receipt_items_table.setItem(row, 4, QTableWidgetItem(f"{item_total:.2f} ₽"))
            
            # Кнопка удаления
            remove_btn = QPushButton("❌")
            remove_btn.setProperty("class", "danger")
            remove_btn.setProperty("class", "small")
            remove_btn.setMaximumWidth(35)
            remove_btn.clicked.connect(lambda checked, idx=row: self.remove_from_receipt(idx))
            self.receipt_items_table.setCellWidget(row, 5, remove_btn)
        
        self.total_label.setText(f"Итого: {total:.2f} ₽")
    
    def remove_from_receipt(self, index):
        """Удалить товар из поступления"""
        if 0 <= index < len(self.receipt_items):
            del self.receipt_items[index]
            self.update_receipt_display()
    
    def clear_receipt(self):
        """Очистить поступление"""
        if self.receipt_items:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Подтверждение")
            msg_box.setText("Очистить текущее поступление?")
            msg_box.setIcon(QMessageBox.Question)
            
            yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
            no_button = msg_box.addButton("Нет", QMessageBox.NoRole)
            
            msg_box.exec()

            if msg_box.clickedButton() == yes_button:
                self.receipt_items.clear()
                self.supplier_input.clear()
                self.notes_input.clear()
                self.update_receipt_display()
    
    def show_receipt_details_from_history(self, index):
        """Показать детали поступления из истории при двойном клике"""
        if index.isValid():
            receipt_id = self.receipts_table.item(index.row(), 0).data(Qt.UserRole)
            if receipt_id:
                self.show_receipt_details(receipt_id)
    
    def add_part_from_table(self, index):
        """Добавить товар в поступление при двойном клике"""
        if index.isValid():
            part = self.parts_table.item(index.row(), 0).data(Qt.UserRole)
            if part:
                self.add_part_to_receipt(part)
    
    def save_receipt(self):
        """Сохранить поступление"""
        if not self.receipt_items:
            QMessageBox.warning(self, "Ошибка", "Добавьте товары в поступление!")
            return
        
        supplier = self.supplier_input.text().strip()
        if not supplier:
            QMessageBox.warning(self, "Ошибка", "Укажите поставщика!")
            return
        
        # Подтверждение поступления
        total = sum(item['quantity'] * item['buy_price'] for item in self.receipt_items)
        reply = QMessageBox.question(
            self, "Подтверждение поступления",
            f"Оформить поступление от '{supplier}' на сумму {total:.2f} ₽?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Создаем поступление
            receipt_items = [
                {
                    'part_id': item['part_id'],
                    'quantity': item['quantity'],
                    'buy_price': item['buy_price']
                }
                for item in self.receipt_items
            ]
            
            notes = self.notes_input.text().strip()
            
            if db.create_receipt(supplier, receipt_items, notes):
                QMessageBox.information(self, "Успех", 
                    f"Поступление оформлено!\n"
                    f"Поставщик: {supplier}\n"
                    f"Сумма: {total:.2f} ₽\n"
                    f"Товары добавлены на склад.")
                
                # Очищаем форму и обновляем данные
                self.receipt_items.clear()
                self.supplier_input.clear()
                self.notes_input.clear()
                self.update_receipt_display()
                self.load_receipts()
                self.load_parts()  # Обновляем остатки
                
                # Обновляем все модули через главное окно
                if self.main_window:
                    self.main_window.refresh_all_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось оформить поступление!")
    
    def add_new_part(self):
        """Добавить новый товар"""
        # Открываем диалог добавления товара (повторно используем существующий)
        dialog = AddPartDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_parts()  # Обновляем список товаров
    
    def show_receipt_details(self, receipt_id):
        """Показать детали поступления"""
        try:
            items = db.get_receipt_items(receipt_id)
            
            # Создаем диалог с деталями
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Детали поступления #{receipt_id}")
            dialog.setModal(True)
            dialog.resize(600, 400)
            
            layout = QVBoxLayout(dialog)
            
            # Таблица с товарами
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Артикул", "Наименование", "Количество", "Цена"])
            table.setRowCount(len(items))
            
            total = 0
            for row, item in enumerate(items):
                table.setItem(row, 0, QTableWidgetItem(item['article']))
                table.setItem(row, 1, QTableWidgetItem(item['name']))
                table.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
                table.setItem(row, 3, QTableWidgetItem(f"{item['buy_price']:,.2f} ₽"))
                total += item['quantity'] * item['buy_price']
            
            layout.addWidget(table)
            
            # Итого
            total_label = QLabel(f"Итого: {total:,.2f} ₽")
            total_label.setFont(QFont("Arial", 12, QFont.Bold))
            total_label.setAlignment(Qt.AlignRight)
            layout.addWidget(total_label)
            
            # Кнопка закрыть
            close_btn = QPushButton("Закрыть")
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)
            
            dialog.exec()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить детали поступления: {e}")


class ReportsWidget(QWidget):
    """Виджет отчетов"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel("📊 Отчеты и аналитика")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2E7D32; margin: 10px;")
        layout.addWidget(title)
        
        # Scroll area для отчетов
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Блок: Статистика
        stats_group = QGroupBox("📈 Общая статистика")
        stats_layout = QGridLayout(stats_group)
        
        self.stats_labels = {}
        stats_items = [
            ("total_parts", "Всего товаров:", "0"),
            ("total_value", "Общая стоимость склада:", "0 ₽"),
            ("low_stock", "Товаров с низким остатком:", "0"),
            ("total_receipts", "Общее количество поступлений:", "0"),
            ("total_sales", "Общее количество продаж:", "0"),
            ("total_revenue", "Общая выручка:", "0 ₽"),
            ("total_profit", "Общая прибыль:", "0 ₽"),
            ("profit_margin", "Средняя прибыльность:", "0%")
        ]
        
        for i, (key, label, default) in enumerate(stats_items):
            row, col = i // 2, (i % 2) * 2
            stats_layout.addWidget(QLabel(label), row, col)
            value_label = QLabel(default)
            value_label.setStyleSheet("font-weight: bold; color: #1976D2;")
            stats_layout.addWidget(value_label, row, col + 1)
            self.stats_labels[key] = value_label
        
        scroll_layout.addWidget(stats_group)
        
        # Блок: История продаж
        sales_group = QGroupBox("🛒 История продаж")
        sales_layout = QVBoxLayout(sales_group)
        
        # Фильтры для дат
        filters_layout = QHBoxLayout()
        
        filters_layout.addWidget(QLabel("Период:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        filters_layout.addWidget(self.date_from)
        
        filters_layout.addWidget(QLabel("по"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        filters_layout.addWidget(self.date_to)
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.clicked.connect(self.load_sales_report)
        filters_layout.addWidget(refresh_btn)
        
        filters_layout.addStretch()
        sales_layout.addLayout(filters_layout)
        
        # Таблица продаж
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(4)
        self.sales_table.setHorizontalHeaderLabels(["Дата", "Количество позиций", "Сумма", "Детали"])
        
        # Улучшаем отображение таблицы
        self.sales_table.horizontalHeader().setStretchLastSection(True)
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sales_table.verticalHeader().setVisible(False)
        self.sales_table.setMinimumHeight(200)
        self.sales_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрещаем редактирование
        
        # Исправляем стили для предотвращения зачеркивания
        self.sales_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
            }
            QTableWidget::item:hover {
                background-color: #F5F5F5;
            }
        """)
        
        # Настраиваем размеры колонок
        self.sales_table.setColumnWidth(0, 130)  # Дата
        self.sales_table.setColumnWidth(1, 140)  # Количество
        self.sales_table.setColumnWidth(2, 120)  # Сумма
        self.sales_table.setColumnWidth(3, 120)  # Детали
        
        # Устанавливаем минимальную высоту строк
        self.sales_table.verticalHeader().setDefaultSectionSize(40)
        
        sales_layout.addWidget(self.sales_table)
        
        scroll_layout.addWidget(sales_group)
        
        # Блок: Остатки на складе
        inventory_group = QGroupBox("📦 Остатки на складе")
        inventory_layout = QVBoxLayout(inventory_group)
        
        # Фильтры для остатков
        inventory_filters = QHBoxLayout()
        
        self.low_stock_check = QCheckBox("Только товары с низким остатком (≤ 2 шт.)")
        self.low_stock_check.stateChanged.connect(self.load_inventory_report)
        inventory_filters.addWidget(self.low_stock_check)
        
        inventory_filters.addStretch()
        inventory_layout.addLayout(inventory_filters)
        
        # Таблица остатков
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels([
            "Артикул", "Наименование", "Категория", "Количество", "Цена", "Общая стоимость"
        ])
        
        # Улучшаем отображение таблицы
        self.inventory_table.horizontalHeader().setStretchLastSection(True)
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.setMinimumHeight(200)
        self.inventory_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрещаем редактирование
        
        # Исправляем стили для предотвращения зачеркивания
        self.inventory_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
            }
            QTableWidget::item:hover {
                background-color: #F5F5F5;
            }
        """)
        
        # Настраиваем размеры колонок
        self.inventory_table.setColumnWidth(0, 120)  # Артикул
        self.inventory_table.setColumnWidth(1, 280)  # Наименование
        self.inventory_table.setColumnWidth(2, 140)  # Категория
        self.inventory_table.setColumnWidth(3, 100)  # Количество
        self.inventory_table.setColumnWidth(4, 120)  # Цена
        self.inventory_table.setColumnWidth(5, 140)  # Общая стоимость
        
        # Устанавливаем минимальную высоту строк
        self.inventory_table.verticalHeader().setDefaultSectionSize(40)
        
        inventory_layout.addWidget(self.inventory_table)
        
        scroll_layout.addWidget(inventory_group)
        
        # Блок: Популярные товары
        popular_group = QGroupBox("🔥 Популярные товары")
        popular_layout = QVBoxLayout(popular_group)
        
        self.popular_table = QTableWidget()
        self.popular_table.setColumnCount(5)
        self.popular_table.setHorizontalHeaderLabels([
            "Артикул", "Наименование", "Продано (шт.)", "Выручка", "Прибыль"
        ])
        
        # Улучшаем отображение таблицы
        self.popular_table.horizontalHeader().setStretchLastSection(True)
        self.popular_table.setAlternatingRowColors(True)
        self.popular_table.verticalHeader().setVisible(False)
        self.popular_table.setMinimumHeight(200)
        self.popular_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрещаем редактирование
        
        # Исправляем стили для предотвращения зачеркивания
        self.popular_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
            }
            QTableWidget::item:hover {
                background-color: #F5F5F5;
            }
        """)
        
        # Настраиваем размеры колонок
        self.popular_table.setColumnWidth(0, 100)  # Артикул
        self.popular_table.setColumnWidth(1, 280)  # Наименование
        self.popular_table.setColumnWidth(2, 120)  # Продано
        self.popular_table.setColumnWidth(3, 120)  # Выручка
        self.popular_table.setColumnWidth(4, 120)  # Прибыль
        
        # Устанавливаем минимальную высоту строк
        self.popular_table.verticalHeader().setDefaultSectionSize(40)
        
        popular_layout.addWidget(self.popular_table)
        
        scroll_layout.addWidget(popular_group)
        
        # Кнопки экспорта
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        
        export_btn = QPushButton("📄 Экспорт отчета")
        export_btn.setMinimumSize(150, 40)
        export_btn.setMaximumSize(200, 40)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
        """)
        export_btn.clicked.connect(self.export_report)
        export_layout.addWidget(export_btn)
        
        scroll_layout.addLayout(export_layout)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Загружаем данные
        self.load_all_reports()
    
    def load_all_reports(self):
        """Загрузить все отчеты"""
        self.load_statistics()
        self.load_sales_report()
        self.load_inventory_report()
        self.load_popular_items()
    
    def load_statistics(self):
        """Загрузить общую статистику"""
        try:
            # Статистика по товарам
            parts = db.get_all_parts()
            total_parts = len(parts)
            
            # Безопасное вычисление общей стоимости склада
            total_value = 0
            low_stock = 0
            for part in parts:
                try:
                    quantity = int(part.get('quantity', 0))
                    sell_price = float(part.get('sell_price', 0))
                    total_value += quantity * sell_price
                    
                    if quantity <= 2:
                        low_stock += 1
                except (ValueError, TypeError):
                    continue
            
            # Статистика по поступлениям
            receipts = db.get_all_receipts()
            total_receipts = len(receipts)
            
            # Статистика по продажам
            sales = db.get_all_sales()
            total_sales = len(sales)
            
            # Безопасное вычисление общей выручки и прибыли
            total_revenue = 0
            total_profit = 0
            
            for sale in sales:
                try:
                    sale_revenue = float(sale.get('total', 0))
                    total_revenue += sale_revenue
                    
                    # Рассчитываем прибыль для этой продажи
                    sale_items = db.get_sale_items(sale['id'])
                    sale_cost = 0
                    
                    for item in sale_items:
                        # Получаем закупочную цену товара
                        part = db.get_part_by_id(item.get('part_id'))
                        if part:
                            buy_price = float(part.get('buy_price', 0))
                            quantity = int(item.get('quantity', 0))
                            sale_cost += buy_price * quantity
                    
                    sale_profit = sale_revenue - sale_cost
                    total_profit += sale_profit
                    
                except (ValueError, TypeError):
                    continue
            
            # Обновляем метки
            self.stats_labels['total_parts'].setText(str(total_parts))
            self.stats_labels['total_value'].setText(f"{total_value:,.2f} ₽")
            self.stats_labels['low_stock'].setText(str(low_stock))
            self.stats_labels['total_receipts'].setText(str(total_receipts))
            # Рассчитываем среднюю прибыльность
            profit_margin = 0
            if total_revenue > 0:
                profit_margin = (total_profit / total_revenue) * 100
            
            self.stats_labels['total_sales'].setText(str(total_sales))
            self.stats_labels['total_revenue'].setText(f"{total_revenue:,.2f} ₽")
            self.stats_labels['total_profit'].setText(f"{total_profit:,.2f} ₽")
            self.stats_labels['profit_margin'].setText(f"{profit_margin:.1f}%")
            
            print(f"📊 Статистика обновлена: товаров={total_parts}, продаж={total_sales}, выручка={total_revenue:.2f}, прибыль={total_profit:.2f}, маржа={profit_margin:.1f}%")
            
        except Exception as e:
            print(f"❌ Ошибка загрузки статистики: {e}")
            # Показываем нули в случае ошибки
            for key in self.stats_labels:
                if 'total_' in key and key.endswith(('_value', '_revenue', '_profit')):
                    self.stats_labels[key].setText("0.00 ₽")
                elif key == 'profit_margin':
                    self.stats_labels[key].setText("0%")
                else:
                    self.stats_labels[key].setText("0")
    
    def load_sales_report(self):
        """Загрузить отчет по продажам"""
        try:
            sales = db.get_all_sales()
            print(f"🔍 Загружено продаж: {len(sales)}")
            
            # Фильтрация по датам
            date_from = self.date_from.date().toPython()
            date_to = self.date_to.date().toPython()
            
            filtered_sales = []
            for sale in sales:
                try:
                    sale_date = datetime.fromisoformat(sale['date']).date()
                    if date_from <= sale_date <= date_to:
                        filtered_sales.append(sale)
                except (ValueError, KeyError) as e:
                    print(f"⚠️ Ошибка парсинга даты продажи {sale.get('id', 'неизвестно')}: {e}")
                    continue
            
            print(f"🔍 Отфильтровано продаж: {len(filtered_sales)}")
            self.sales_table.setRowCount(len(filtered_sales))
            
            if not filtered_sales:
                # Если нет данных, показываем пустую таблицу с информационным сообщением
                self.sales_table.setRowCount(1)
                no_data_item = QTableWidgetItem("Нет данных за выбранный период")
                no_data_item.setTextAlignment(Qt.AlignCenter)
                no_data_item.setFlags(Qt.ItemIsEnabled)  # Делаем нередактируемым
                # Устанавливаем фоновый цвет
                no_data_item.setBackground(QColor("#F5F5F5"))
                self.sales_table.setItem(0, 0, no_data_item)
                self.sales_table.setSpan(0, 0, 1, 4)  # Объединяем все столбцы
                # Устанавливаем высоту строки
                self.sales_table.setRowHeight(0, 40)
                return
            
            for row, sale in enumerate(filtered_sales):
                try:
                    # Дата
                    sale_date = datetime.fromisoformat(sale['date']).strftime("%d.%m.%Y %H:%M")
                    self.sales_table.setItem(row, 0, QTableWidgetItem(sale_date))
                    
                    # Количество позиций
                    self.sales_table.setItem(row, 1, QTableWidgetItem(str(sale.get('items_count', 0))))
                    
                    # Сумма
                    total = float(sale.get('total', 0))
                    self.sales_table.setItem(row, 2, QTableWidgetItem(f"{total:,.2f} ₽"))
                    
                    # Кнопка деталей
                    details_btn = QPushButton("Подробнее")
                    details_btn.setFixedSize(100, 28)
                    details_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #2196F3;
                            color: white;
                            border: none;
                            padding: 4px 8px;
                            border-radius: 4px;
                            font-size: 11px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #1976D2;
                        }
                        QPushButton:pressed {
                            background-color: #0D47A1;
                        }
                    """)
                    details_btn.clicked.connect(lambda checked, s_id=sale['id']: self.show_sale_details(s_id))
                    self.sales_table.setCellWidget(row, 3, details_btn)
                    
                    # Устанавливаем высоту строки
                    self.sales_table.setRowHeight(row, 40)
                    
                except Exception as e:
                    print(f"⚠️ Ошибка обработки продажи {sale.get('id', 'неизвестно')}: {e}")
                    continue
            
            # Размеры колонок уже настроены в setup_ui
            
        except Exception as e:
            print(f"❌ Ошибка загрузки продаж: {e}")
            # Показываем сообщение об ошибке в таблице
            self.sales_table.setRowCount(1)
            error_item = QTableWidgetItem(f"Ошибка загрузки данных: {str(e)}")
            error_item.setTextAlignment(Qt.AlignCenter)
            self.sales_table.setItem(0, 0, error_item)
            self.sales_table.setSpan(0, 0, 1, 4)
    
    def load_inventory_report(self):
        """Загрузить отчет по остаткам"""
        try:
            parts = db.get_all_parts()
            print(f"🔍 Загружено запчастей: {len(parts)}")
            
            # Фильтрация по низкому остатку
            if self.low_stock_check.isChecked():
                parts = [p for p in parts if p.get('quantity', 0) <= 2]
                print(f"🔍 Отфильтровано по низкому остатку: {len(parts)}")
            
            self.inventory_table.setRowCount(len(parts))
            
            if not parts:
                # Если нет данных, показываем сообщение
                self.inventory_table.setRowCount(1)
                no_data_item = QTableWidgetItem("Нет данных для отображения")
                no_data_item.setTextAlignment(Qt.AlignCenter)
                self.inventory_table.setItem(0, 0, no_data_item)
                self.inventory_table.setSpan(0, 0, 1, 6)  # Объединяем все столбцы
                return
            
            for row, part in enumerate(parts):
                try:
                    # Артикул
                    self.inventory_table.setItem(row, 0, QTableWidgetItem(str(part.get('article', ''))))
                    
                    # Наименование
                    self.inventory_table.setItem(row, 1, QTableWidgetItem(str(part.get('name', ''))))
                    
                    # Категория
                    self.inventory_table.setItem(row, 2, QTableWidgetItem(str(part.get('category', ''))))
                    
                    # Количество с выделением низкого остатка
                    quantity = int(part.get('quantity', 0))
                    qty_item = QTableWidgetItem(str(quantity))
                    qty_item.setTextAlignment(Qt.AlignCenter)
                    
                    if quantity <= 2:
                        # Выделяем низкий остаток красным цветом
                        qty_item.setData(Qt.ForegroundRole, QColor("#F44336"))
                        font = QFont()
                        font.setBold(True)
                        qty_item.setData(Qt.FontRole, font)
                    elif quantity <= 5:
                        # Средний остаток - желтым
                        qty_item.setData(Qt.ForegroundRole, QColor("#FF9800"))
                    else:
                        # Нормальный остаток - зеленым
                        qty_item.setData(Qt.ForegroundRole, QColor("#4CAF50"))
                    
                    self.inventory_table.setItem(row, 3, qty_item)
                    
                    # Цена продажи
                    sell_price = float(part.get('sell_price', 0))
                    price_item = QTableWidgetItem(f"{sell_price:,.2f} ₽")
                    price_item.setTextAlignment(Qt.AlignRight)
                    self.inventory_table.setItem(row, 4, price_item)
                    
                    # Общая стоимость
                    total_value = quantity * sell_price
                    total_item = QTableWidgetItem(f"{total_value:,.2f} ₽")
                    total_item.setTextAlignment(Qt.AlignRight)
                    # Выделяем крупные суммы
                    if total_value > 10000:
                        font = QFont()
                        font.setBold(True)
                        total_item.setData(Qt.FontRole, font)
                    self.inventory_table.setItem(row, 5, total_item)
                    
                    # Устанавливаем высоту строки
                    self.inventory_table.setRowHeight(row, 40)
                    
                except Exception as e:
                    print(f"⚠️ Ошибка обработки запчасти {part.get('id', 'неизвестно')}: {e}")
                    continue
            
            # Размеры колонок уже настроены в setup_ui
            
        except Exception as e:
            print(f"❌ Ошибка загрузки остатков: {e}")
            # Показываем сообщение об ошибке в таблице
            self.inventory_table.setRowCount(1)
            error_item = QTableWidgetItem(f"Ошибка загрузки данных: {str(e)}")
            error_item.setTextAlignment(Qt.AlignCenter)
            self.inventory_table.setItem(0, 0, error_item)
            self.inventory_table.setSpan(0, 0, 1, 6)
    
    def load_popular_items(self):
        """Загрузить популярные товары"""
        try:
            # Получаем все продажи и группируем по товарам
            sales = db.get_all_sales()
            print(f"🔍 Обрабатываем продажи для популярных товаров: {len(sales)}")
            
            item_stats = {}
            
            for sale in sales:
                try:
                    items = db.get_sale_items(sale['id'])
                    for item in items:
                        part_id = item.get('part_id')
                        if part_id is None:
                            continue
                            
                        if part_id not in item_stats:
                            item_stats[part_id] = {
                                'article': item.get('article', 'Неизвестно'),
                                'name': item.get('name', 'Неизвестно'),
                                'total_qty': 0,
                                'total_revenue': 0,
                                'total_profit': 0
                            }
                        
                        quantity = int(item.get('quantity', 0))
                        price = float(item.get('price', 0))
                        revenue = quantity * price
                        
                        # Получаем закупочную цену для расчета прибыли
                        part = db.get_part_by_id(part_id)
                        buy_price = 0
                        if part:
                            buy_price = float(part.get('buy_price', 0))
                        
                        cost = quantity * buy_price
                        profit = revenue - cost
                        
                        item_stats[part_id]['total_qty'] += quantity
                        item_stats[part_id]['total_revenue'] += revenue
                        item_stats[part_id]['total_profit'] += profit
                        
                except Exception as e:
                    print(f"⚠️ Ошибка обработки продажи {sale.get('id', 'неизвестно')}: {e}")
                    continue
            
            print(f"🔍 Найдено уникальных товаров: {len(item_stats)}")
            
            # Сортируем по количеству продаж
            sorted_items = sorted(item_stats.values(), key=lambda x: x['total_qty'], reverse=True)[:10]
            
            self.popular_table.setRowCount(len(sorted_items))
            
            if not sorted_items:
                # Если нет данных, показываем сообщение
                self.popular_table.setRowCount(1)
                no_data_item = QTableWidgetItem("Нет данных о продажах")
                no_data_item.setTextAlignment(Qt.AlignCenter)
                self.popular_table.setItem(0, 0, no_data_item)
                self.popular_table.setSpan(0, 0, 1, 5)  # Объединяем все столбцы
                return
            
            for row, item in enumerate(sorted_items):
                try:
                    # Артикул
                    self.popular_table.setItem(row, 0, QTableWidgetItem(str(item['article'])))
                    
                    # Наименование
                    self.popular_table.setItem(row, 1, QTableWidgetItem(str(item['name'])))
                    
                    # Количество продаж
                    qty_item = QTableWidgetItem(str(item['total_qty']))
                    qty_item.setTextAlignment(Qt.AlignCenter)
                    # Выделяем топ-3 товара
                    if row < 3:
                        font = QFont()
                        font.setBold(True)
                        qty_item.setData(Qt.FontRole, font)
                        if row == 0:
                            qty_item.setData(Qt.ForegroundRole, QColor("#FFD700"))  # Золотой
                        elif row == 1:
                            qty_item.setData(Qt.ForegroundRole, QColor("#C0C0C0"))  # Серебро
                        else:
                            qty_item.setData(Qt.ForegroundRole, QColor("#CD7F32"))  # Бронза
                    self.popular_table.setItem(row, 2, qty_item)
                    
                    # Выручка
                    revenue_item = QTableWidgetItem(f"{item['total_revenue']:,.2f} ₽")
                    revenue_item.setTextAlignment(Qt.AlignRight)
                    if row < 3:
                        font = QFont()
                        font.setBold(True)
                        revenue_item.setData(Qt.FontRole, font)
                    self.popular_table.setItem(row, 3, revenue_item)
                    
                    # Прибыль
                    profit_item = QTableWidgetItem(f"{item['total_profit']:,.2f} ₽")
                    profit_item.setTextAlignment(Qt.AlignRight)
                    if row < 3:
                        font = QFont()
                        font.setBold(True)
                        profit_item.setData(Qt.FontRole, font)
                    # Цветовая индикация прибыли
                    if item['total_profit'] > 0:
                        profit_item.setData(Qt.ForegroundRole, QColor("#4CAF50"))  # Зеленый для прибыли
                    elif item['total_profit'] < 0:
                        profit_item.setData(Qt.ForegroundRole, QColor("#F44336"))  # Красный для убытка
                    self.popular_table.setItem(row, 4, profit_item)
                    
                    # Устанавливаем высоту строки
                    self.popular_table.setRowHeight(row, 40)
                    
                except Exception as e:
                    print(f"⚠️ Ошибка отображения популярного товара {row + 1}: {e}")
                    continue
            
            # Размеры колонок уже настроены в setup_ui
            
        except Exception as e:
            print(f"❌ Ошибка загрузки популярных товаров: {e}")
            # Показываем сообщение об ошибке в таблице
            self.popular_table.setRowCount(1)
            error_item = QTableWidgetItem(f"Ошибка загрузки данных: {str(e)}")
            error_item.setTextAlignment(Qt.AlignCenter)
            self.popular_table.setItem(0, 0, error_item)
            self.popular_table.setSpan(0, 0, 1, 5)
    
    def show_sale_details(self, sale_id):
        """Показать детали продажи"""
        try:
            items = db.get_sale_items(sale_id)
            
            # Создаем диалог с деталями
            dialog = QDialog(self)
            dialog.setWindowTitle(f"📋 Детали продажи #{sale_id}")
            dialog.setModal(True)
            dialog.resize(700, 500)
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #f8f9fa;
                }
            """)
            
            layout = QVBoxLayout(dialog)
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Заголовок
            header_label = QLabel(f"🛒 Продажа #{sale_id}")
            header_label.setFont(QFont("Arial", 16, QFont.Bold))
            header_label.setStyleSheet("""
                QLabel {
                    color: #2E7D32;
                    padding: 10px;
                    background-color: white;
                    border-radius: 8px;
                    border: 1px solid #e0e0e0;
                }
            """)
            header_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(header_label)
            
            # Таблица с товарами
            table = QTableWidget()
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["Артикул", "Наименование", "Количество", "Цена за ед.", "Сумма"])
            table.setRowCount(len(items))
            
            # Стилизуем таблицу
            table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    gridline-color: #e0e0e0;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }
                QTableWidget::item {
                    padding: 10px;
                    border: none;
                }
                QTableWidget::item:selected {
                    background-color: #E3F2FD;
                    color: black;
                }
                QHeaderView::section {
                    background-color: #f5f5f5;
                    padding: 8px;
                    border: none;
                    border-bottom: 2px solid #2196F3;
                    font-weight: bold;
                }
            """)
            
            # Настраиваем таблицу
            table.horizontalHeader().setStretchLastSection(True)
            table.verticalHeader().setVisible(False)
            table.setAlternatingRowColors(True)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрещаем редактирование
            
            # Размеры колонок
            table.setColumnWidth(0, 120)  # Артикул
            table.setColumnWidth(1, 250)  # Наименование
            table.setColumnWidth(2, 100)  # Количество
            table.setColumnWidth(3, 120)  # Цена за ед.
            table.setColumnWidth(4, 120)  # Сумма
            
            total = 0
            for row, item in enumerate(items):
                # Артикул
                article_item = QTableWidgetItem(str(item.get('article', '')))
                article_item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 0, article_item)
                
                # Наименование
                name_item = QTableWidgetItem(str(item.get('name', '')))
                table.setItem(row, 1, name_item)
                
                # Количество
                quantity = int(item.get('quantity', 0))
                qty_item = QTableWidgetItem(f"{quantity} шт.")
                qty_item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 2, qty_item)
                
                # Цена за единицу
                price = float(item.get('price', 0))
                price_item = QTableWidgetItem(f"{price:,.2f} ₽")
                price_item.setTextAlignment(Qt.AlignRight)
                table.setItem(row, 3, price_item)
                
                # Сумма за позицию
                item_total = quantity * price
                total_item = QTableWidgetItem(f"{item_total:,.2f} ₽")
                total_item.setTextAlignment(Qt.AlignRight)
                total_item.setFont(QFont("Arial", 10, QFont.Bold))
                table.setItem(row, 4, total_item)
                
                total += item_total
                
                # Высота строки
                table.setRowHeight(row, 40)
            
            layout.addWidget(table)
            
            # Блок с итогами
            summary_widget = QWidget()
            summary_layout = QHBoxLayout(summary_widget)
            summary_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border-radius: 8px;
                    border: 1px solid #e0e0e0;
                }
            """)
            
            # Статистика
            stats_layout = QVBoxLayout()
            
            items_count_label = QLabel(f"📦 Количество позиций: {len(items)}")
            items_count_label.setFont(QFont("Arial", 11))
            stats_layout.addWidget(items_count_label)
            
            total_qty = sum(int(item.get('quantity', 0)) for item in items)
            total_qty_label = QLabel(f"📊 Общее количество товаров: {total_qty} шт.")
            total_qty_label.setFont(QFont("Arial", 11))
            stats_layout.addWidget(total_qty_label)
            
            summary_layout.addLayout(stats_layout)
            summary_layout.addStretch()
            
            # Итоговая сумма
            total_label = QLabel(f"💰 Итого: {total:,.2f} ₽")
            total_label.setFont(QFont("Arial", 14, QFont.Bold))
            total_label.setStyleSheet("""
                QLabel {
                    color: #2E7D32;
                    padding: 10px;
                    background-color: #E8F5E8;
                    border-radius: 6px;
                    border: 1px solid #4CAF50;
                }
            """)
            total_label.setAlignment(Qt.AlignCenter)
            summary_layout.addWidget(total_label)
            
            layout.addWidget(summary_widget)
            
            # Кнопки
            buttons_layout = QHBoxLayout()
            buttons_layout.addStretch()
            
            close_btn = QPushButton("✖ Закрыть")
            close_btn.setFixedSize(120, 35)
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
                QPushButton:pressed {
                    background-color: #b71c1c;
                }
            """)
            close_btn.clicked.connect(dialog.accept)
            buttons_layout.addWidget(close_btn)
            
            layout.addLayout(buttons_layout)
            
            dialog.exec()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить детали продажи: {e}")
    
    def export_report(self):
        """Экспорт отчета"""
        # Пока просто показываем сообщение, позже добавим реальный экспорт
        QMessageBox.information(self, "Экспорт", "Функция экспорта будет добавлена в следующей версии")


class FullMainWindow(QMainWindow):
    """Полноценное главное окно с базой данных"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚗 Система учёта автозапчастей v2.0 - Профессиональная версия")
        self.setMinimumSize(1200, 800)
        
        # Инициализируем настройки
        self.settings = get_settings()
        
        # Применяем расширенные современные стили
        self.setStyleSheet(get_enhanced_complete_style())
        
        self.setup_menu_bar()
        self.setup_ui()
        self.setup_status_bar()
        self.load_window_settings()
        
        # Запускаем проверку низких остатков с небольшой задержкой
        QTimer.singleShot(1000, self.show_startup_notifications)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Заголовок
        title_label = QLabel("🚗 Система учёта автозапчастей")
        title_label.setObjectName("main_title")  # Для применения стилей из CSS
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Панель уведомлений
        self.notification_widget = self.create_notification_widget()
        layout.addWidget(self.notification_widget)
        
        # Вкладки
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Вкладка "Запчасти" с полным функционалом
        self.parts_widget = PartsWidget(self)
        self.tab_widget.addTab(self.parts_widget, "📦 Запчасти")
        
        # Вкладка "Продажи" с полным функционалом
        self.sales_widget = SalesWidget(self)
        self.tab_widget.addTab(self.sales_widget, "💰 Продажи")
        
        # Вкладка "Поступления" с полным функционалом
        self.receipts_widget = ReceiptsWidget(self)
        self.tab_widget.addTab(self.receipts_widget, "📦 Поступления")
        
        # Вкладка "Отчеты" с полным функционалом
        self.reports_widget = ReportsWidget()
        self.tab_widget.addTab(self.reports_widget, "📊 Отчёты")
    
    def setup_menu_bar(self):
        """Настройка панели меню"""
        menubar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menubar.addMenu("📁 Файл")
        
        # Экспорт данных
        export_action = QAction("📤 Экспорт данных", self)
        export_action.setStatusTip("Экспортировать данные в файл")
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        # Резервная копия
        backup_action = QAction("💾 Создать резервную копию", self)
        backup_action.setStatusTip("Создать резервную копию базы данных")
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)
        
        file_menu.addSeparator()
        
        # Выход
        exit_action = QAction("🚪 Выход", self)
        exit_action.setStatusTip("Выход из приложения")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню "Данные"
        data_menu = menubar.addMenu("🗃️ Данные")
        
        # Обновить все
        refresh_action = QAction("🔄 Обновить всё", self)
        refresh_action.setStatusTip("Обновить данные во всех разделах")
        refresh_action.triggered.connect(self.refresh_all_data)
        data_menu.addAction(refresh_action)
        
        # Меню "Настройки"
        settings_menu = menubar.addMenu("⚙️ Настройки")
        
        # Настройки приложения
        app_settings_action = QAction("⚙️ Настройки приложения", self)
        app_settings_action.setStatusTip("Открыть настройки приложения")
        app_settings_action.triggered.connect(self.show_settings)
        settings_menu.addAction(app_settings_action)
        
        # Меню "Справка"
        help_menu = menubar.addMenu("❓ Справка")
        
        # О программе
        about_action = QAction("ℹ️ О программе", self)
        about_action.setStatusTip("Информация о программе")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def load_window_settings(self):
        """Загрузить настройки окна"""
        try:
            # Загружаем геометрию окна
            geometry = self.settings.load_window_geometry("main")
            if geometry:
                self.restoreGeometry(geometry)
            
            # Загружаем состояние окна
            state = self.settings.load_window_state("main")
            if state:
                self.restoreState(state)
                
        except Exception as e:
            print(f"❌ Ошибка загрузки настроек окна: {e}")
    
    def save_window_settings(self):
        """Сохранить настройки окна"""
        try:
            self.settings.save_window_geometry("main", self.saveGeometry())
            self.settings.save_window_state("main", self.saveState())
        except Exception as e:
            print(f"❌ Ошибка сохранения настроек окна: {e}")
    
    def show_settings(self):
        """Показать диалог настроек"""
        try:
            result = show_settings_dialog(self)
            if result:
                # Настройки были изменены, можно обновить интерфейс
                self.refresh_all_data()
                print("✅ Настройки применены")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть настройки:\n{e}")
    
    def export_data(self):
        """Экспорт данных"""
        QMessageBox.information(self, "Экспорт", "Функция экспорта будет добавлена в следующей версии")
    
    def create_backup(self):
        """Создать резервную копию"""
        try:
            from datetime import datetime
            import shutil
            import os
            
            backup_dir = os.path.join(self.settings.app_data_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"autoparts_backup_{timestamp}.db")
            
            shutil.copy2(self.settings.database_path, backup_file)
            
            QMessageBox.information(
                self, "Резервная копия", 
                f"Резервная копия создана:\n{backup_file}"
            )
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать резервную копию:\n{e}")
    
    def show_about(self):
        """Показать информацию о программе"""
        QMessageBox.about(
            self, "О программе",
            """
            <h2>🚗 AutoParts v1.0</h2>
            <p><b>Система управления автозапчастями</b></p>
            <p>Современное приложение для учёта запчастей и продаж</p>
            <br>
            <p>Разработано с использованием PySide6 и SQLite</p>
            <p>© 2024 AutoParts Team</p>
            """
        )
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.save_window_settings()
        event.accept()
    
    def setup_status_bar(self):
        """Настройка строки состояния"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("✅ База данных подключена. Приложение готово к работе.")
        
        # Таймер для обновления времени
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(60000)  # Обновляем каждую минуту
    
    def update_status(self):
        """Обновление строки состояния"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        self.status_bar.showMessage(f"⏰ {current_time} | ✅ База данных: Подключена")
    
    def refresh_all_data(self):
        """Обновить данные во всех модулях"""
        try:
            # Обновляем запчасти
            if hasattr(self, 'parts_widget'):
                self.parts_widget.load_parts()
            
            # Обновляем продажи
            if hasattr(self, 'sales_widget'):
                self.sales_widget.load_products()
            
            # Обновляем поступления
            if hasattr(self, 'receipts_widget'):
                self.receipts_widget.load_receipts()
                self.receipts_widget.load_parts()
            
            # Обновляем отчеты
            if hasattr(self, 'reports_widget'):
                self.reports_widget.load_all_reports()
            
            # Проверяем низкие остатки
            self.check_low_stock()
                
        except Exception as e:
            print(f"❌ Ошибка обновления данных: {e}")
    
    def create_notification_widget(self):
        """Создать панель уведомлений"""
        notification_frame = QFrame()
        notification_frame.setStyleSheet("""
            QFrame {
                background-color: #FFF3CD;
                border: 2px solid #FFC107;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        notification_frame.setVisible(False)  # Скрыто по умолчанию
        
        layout = QHBoxLayout(notification_frame)
        
        # Иконка предупреждения
        warning_icon = QLabel("⚠️")
        warning_icon.setStyleSheet("font-size: 20px; margin: 5px;")
        layout.addWidget(warning_icon)
        
        # Текст уведомления
        self.notification_text = QLabel("")
        self.notification_text.setStyleSheet("color: #856404; font-weight: bold; margin: 5px;")
        layout.addWidget(self.notification_text)
        
        layout.addStretch()
        
        # Кнопка "Показать детали"
        details_btn = QPushButton("📋 Показать детали")
        details_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: #212529;
                font-weight: bold;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #FFB300;
            }
        """)
        details_btn.clicked.connect(self.show_low_stock_details)
        layout.addWidget(details_btn)
        
        # Кнопка закрытия
        close_btn = QPushButton("❌")
        close_btn.setMaximumWidth(30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #856404;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #F0D9A0;
                border-radius: 3px;
            }
        """)
        close_btn.clicked.connect(lambda: notification_frame.setVisible(False))
        layout.addWidget(close_btn)
        
        return notification_frame
    
    def check_low_stock(self):
        """Проверить низкие остатки"""
        try:
            parts = db.get_all_parts()
            low_stock_parts = [p for p in parts if p['quantity'] <= 2 and p['quantity'] >= 0]
            
            if low_stock_parts:
                count = len(low_stock_parts)
                if count == 1:
                    text = f"1 товар заканчивается на складе!"
                elif count < 5:
                    text = f"{count} товара заканчиваются на складе!"
                else:
                    text = f"{count} товаров заканчиваются на складе!"
                
                self.notification_text.setText(text)
                self.notification_widget.setVisible(True)
                
                # Обновляем строку состояния
                self.status_bar.showMessage(f"⚠️ Предупреждение: {text}")
                
                return low_stock_parts
            else:
                self.notification_widget.setVisible(False)
                return []
                
        except Exception as e:
            print(f"❌ Ошибка проверки остатков: {e}")
            return []
    
    def show_low_stock_details(self):
        """Показать детали товаров с низким остатком"""
        low_stock_parts = [p for p in db.get_all_parts() if p['quantity'] <= 2 and p['quantity'] >= 0]
        
        if not low_stock_parts:
            QMessageBox.information(self, "Информация", "Нет товаров с низким остатком")
            return
        
        # Создаем диалог с деталями
        dialog = QDialog(self)
        dialog.setWindowTitle("⚠️ Товары с низким остатком")
        dialog.setModal(True)
        dialog.resize(800, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Заголовок
        header = QLabel(f"Обнаружено {len(low_stock_parts)} товаров с низким остатком (≤ 2 шт.):")
        header.setStyleSheet("font-weight: bold; color: #856404; margin: 10px;")
        layout.addWidget(header)
        
        # Таблица с товарами
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Артикул", "Наименование", "Категория", "Остаток", "Цена", "Статус"
        ])
        table.setRowCount(len(low_stock_parts))
        
        for row, part in enumerate(low_stock_parts):
            table.setItem(row, 0, QTableWidgetItem(part['article']))
            table.setItem(row, 1, QTableWidgetItem(part['name']))
            table.setItem(row, 2, QTableWidgetItem(part['category']))
            
            # Количество с цветовым выделением
            qty_item = QTableWidgetItem(str(part['quantity']))
            if part['quantity'] == 0:
                qty_item.setBackground(QColor("#FF5252"))
                qty_item.setForeground(QColor("white"))
                status = "НЕТ В НАЛИЧИИ"
            elif part['quantity'] == 1:
                qty_item.setBackground(QColor("#FF9800"))
                qty_item.setForeground(QColor("white"))
                status = "КРИТИЧЕСКИ МАЛО"
            else:
                qty_item.setBackground(QColor("#FFC107"))
                qty_item.setForeground(QColor("black"))
                status = "МАЛО"
            
            table.setItem(row, 3, qty_item)
            table.setItem(row, 4, QTableWidgetItem(f"{part['sell_price']:.2f} ₽"))
            
            status_item = QTableWidgetItem(status)
            # Убираем setStyleSheet, так как QTableWidgetItem не поддерживает это
            table.setItem(row, 5, status_item)
        
        # Настройка таблицы
        table.horizontalHeader().setStretchLastSection(True)
        table.setAlternatingRowColors(True)
        layout.addWidget(table)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        
        # Кнопка "Перейти к поступлениям"
        receipts_btn = QPushButton("📦 Оформить поступление")
        receipts_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        receipts_btn.clicked.connect(lambda: (dialog.accept(), self.tab_widget.setCurrentIndex(2)))
        buttons_layout.addWidget(receipts_btn)
        
        buttons_layout.addStretch()
        
        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dialog.accept)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        dialog.exec()
    
    def show_startup_notifications(self):
        """Показать уведомления при запуске"""
        low_stock_parts = self.check_low_stock()
        
        if low_stock_parts:
            # Создаем диалог предупреждения при запуске
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("⚠️ Предупреждение о низких остатках")
            
            count = len(low_stock_parts)
            if count == 1:
                text = "Обнаружен 1 товар с низким остатком!"
            elif count < 5:
                text = f"Обнаружено {count} товара с низким остатком!"
            else:
                text = f"Обнаружено {count} товаров с низким остатком!"
            
            msg.setText(text)
            msg.setInformativeText("Рекомендуется пополнить запасы для обеспечения бесперебойной работы.")
            
            # Кнопки
            details_btn = msg.addButton("📋 Детали", QMessageBox.ActionRole)
            receipts_btn = msg.addButton("📦 Пополнить", QMessageBox.ActionRole)
            later_btn = msg.addButton("⏰ Позже", QMessageBox.RejectRole)
            
            msg.exec()
            
            if msg.clickedButton() == details_btn:
                self.show_low_stock_details()
            elif msg.clickedButton() == receipts_btn:
                self.tab_widget.setCurrentIndex(2)  # Переключаемся на вкладку поступлений

def main():
    """Главная функция приложения"""
    app = QApplication(sys.argv)
    app.setApplicationName("AutoParts Full")
    app.setApplicationDisplayName("Система учёта автозапчастей - Полная версия")
    
    try:
        window = FullMainWindow()
        window.show()
        
        print("🚀 Полная версия приложения запущена!")
        print(f"📁 База данных: {db.db_path}")
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        QMessageBox.critical(None, "Ошибка", f"Не удалось запустить приложение:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
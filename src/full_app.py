"""Главное приложение системы учёта автозапчастей"""
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
        self.search_input.textChanged.connect(self.filter_parts)
        header_layout.addWidget(self.search_input)
        
        layout.addLayout(header_layout)
        
        # Панель кнопок
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Добавить запчасть")
        add_btn.setProperty("class", "success")
        add_btn.clicked.connect(self.add_part)
        buttons_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Редактировать")
        edit_btn.setProperty("class", "warning")
        edit_btn.clicked.connect(self.edit_part)
        buttons_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Удалить")
        delete_btn.setProperty("class", "danger")
        delete_btn.clicked.connect(self.delete_part)
        buttons_layout.addWidget(delete_btn)
        
        buttons_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.clicked.connect(self.load_parts)
        buttons_layout.addWidget(refresh_btn)
        
        layout.addLayout(buttons_layout)
        
        # Таблица запчастей
        self.parts_table = QTableWidget()
        self.parts_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.parts_table.setAlternatingRowColors(True)
        self.parts_table.setSortingEnabled(True)
        self.parts_table.doubleClicked.connect(self.edit_part)
        
        # Настройка колонок
        headers = ["ID", "Артикул", "Наименование", "Марка", "Модель", 
                  "Категория", "Кол-во", "Закуп. цена", "Розн. цена", "Описание"]
        self.parts_table.setColumnCount(len(headers))
        self.parts_table.setHorizontalHeaderLabels(headers)
        
        # Скрываем колонку ID
        self.parts_table.setColumnHidden(0, True)
        
        # Растягиваем колонки
        header = self.parts_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Наименование
        
        layout.addWidget(self.parts_table)
        
        # Статистика
        self.stats_label = QLabel()
        self.stats_label.setProperty("class", "info-text")
        layout.addWidget(self.stats_label)
    
    def load_parts(self):
        """Загрузить запчасти из базы данных"""
        parts = db.get_all_parts()
        
        self.parts_table.setRowCount(len(parts))
        
        for row, part in enumerate(parts):
            # Создаем элементы таблицы
            items = [
                QTableWidgetItem(str(part['id'])),
                QTableWidgetItem(part['article']),
                QTableWidgetItem(part['name']),
                QTableWidgetItem(part['brand']),
                QTableWidgetItem(part['car_model']),
                QTableWidgetItem(part['category']),
                QTableWidgetItem(str(part['quantity'])),
                QTableWidgetItem(f"{float(part['buy_price']):.2f} ₽"),
                QTableWidgetItem(f"{float(part['sell_price']):.2f} ₽"),
                QTableWidgetItem(part['description'] or "")
            ]
            
            # Добавляем в таблицу
            for col, item in enumerate(items):
                self.parts_table.setItem(row, col, item)
            
            # Выделяем строки с низким остатком
            if part['quantity'] <= 5:
                for col in range(len(items)):
                    self.parts_table.item(row, col).setBackground(QColor("#fff3cd"))
        
        # Обновляем статистику
        self.update_stats(parts)
    
    def update_stats(self, parts):
        """Обновить статистику"""
        total_parts = len(parts)
        total_value = sum(float(part['sell_price']) * part['quantity'] for part in parts)
        low_stock = sum(1 for part in parts if part['quantity'] <= 5)
        
        stats_text = (f"📊 Всего запчастей: {total_parts} | "
                     f"💰 Общая стоимость: {total_value:.2f} ₽ | "
                     f"⚠️ Низкий остаток: {low_stock}")
        
        self.stats_label.setText(stats_text)
    
    def filter_parts(self):
        """Фильтровать запчасти по поисковому запросу"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.parts_table.rowCount()):
            show_row = False
            
            # Проверяем каждую колонку (кроме ID)
            for col in range(1, self.parts_table.columnCount()):
                item = self.parts_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            
            self.parts_table.setRowHidden(row, not show_row)
    
    def add_part(self):
        """Добавить новую запчасть"""
        dialog = AddPartDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_parts()
    
    def edit_part(self):
        """Редактировать выбранную запчасть"""
        current_row = self.parts_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите запчасть для редактирования")
            return
        
        # Получаем ID запчасти
        part_id = int(self.parts_table.item(current_row, 0).text())
        part_data = db.get_part_by_id(part_id)
        
        if part_data:
            dialog = EditPartDialog(part_data, self)
            if dialog.exec() == QDialog.Accepted:
                self.load_parts()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные запчасти")
    
    def delete_part(self):
        """Удалить выбранную запчасть"""
        current_row = self.parts_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите запчасть для удаления")
            return
        
        # Получаем данные запчасти
        article = self.parts_table.item(current_row, 1).text()
        name = self.parts_table.item(current_row, 2).text()
        
        # Подтверждение удаления
        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Вы действительно хотите удалить запчасть:\n{article} - {name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            part_id = int(self.parts_table.item(current_row, 0).text())
            
            if db.delete_part(part_id):
                QMessageBox.information(self, "Успех", "Запчасть успешно удалена!")
                self.load_parts()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить запчасть")


class StatisticsWidget(QWidget):
    """Виджет статистики и аналитики"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_statistics()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel("📊 Статистика и аналитика")
        title.setProperty("class", "section-title")
        layout.addWidget(title)
        
        # Создаем области для статистики
        stats_scroll = QScrollArea()
        stats_scroll.setWidgetResizable(True)
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        
        # Общая статистика
        self.general_stats = self.create_stats_group("📈 Общая статистика")
        stats_layout.addWidget(self.general_stats)
        
        # Статистика по категориям
        self.category_stats = self.create_stats_group("🏷️ По категориям")
        stats_layout.addWidget(self.category_stats)
        
        # Статистика по маркам
        self.brand_stats = self.create_stats_group("🚗 По маркам")
        stats_layout.addWidget(self.brand_stats)
        
        # Низкие остатки
        self.low_stock_stats = self.create_stats_group("⚠️ Низкие остатки")
        stats_layout.addWidget(self.low_stock_stats)
        
        stats_scroll.setWidget(stats_widget)
        layout.addWidget(stats_scroll)
        
        # Кнопка обновления
        refresh_btn = QPushButton("🔄 Обновить статистику")
        refresh_btn.clicked.connect(self.load_statistics)
        layout.addWidget(refresh_btn)
    
    def create_stats_group(self, title):
        """Создать группу статистики"""
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        
        content_label = QLabel("Загрузка...")
        content_label.setWordWrap(True)
        layout.addWidget(content_label)
        
        return group
    
    def load_statistics(self):
        """Загрузить статистику"""
        parts = db.get_all_parts()
        
        # Общая статистика
        self.update_general_stats(parts)
        
        # Статистика по категориям
        self.update_category_stats(parts)
        
        # Статистика по маркам
        self.update_brand_stats(parts)
        
        # Низкие остатки
        self.update_low_stock_stats(parts)
    
    def update_general_stats(self, parts):
        """Обновить общую статистику"""
        total_parts = len(parts)
        total_quantity = sum(part['quantity'] for part in parts)
        total_buy_value = sum(float(part['buy_price']) * part['quantity'] for part in parts)
        total_sell_value = sum(float(part['sell_price']) * part['quantity'] for part in parts)
        potential_profit = total_sell_value - total_buy_value
        
        stats_text = f"""
        🔢 Всего наименований: {total_parts}
        📦 Общее количество: {total_quantity} шт.
        💸 Закупочная стоимость: {total_buy_value:.2f} ₽
        💰 Розничная стоимость: {total_sell_value:.2f} ₽
        📈 Потенциальная прибыль: {potential_profit:.2f} ₽
        """
        
        layout = self.general_stats.layout()
        label = layout.itemAt(0).widget()
        label.setText(stats_text.strip())
    
    def update_category_stats(self, parts):
        """Обновить статистику по категориям"""
        categories = {}
        
        for part in parts:
            category = part['category']
            if category not in categories:
                categories[category] = {'count': 0, 'quantity': 0, 'value': 0}
            
            categories[category]['count'] += 1
            categories[category]['quantity'] += part['quantity']
            categories[category]['value'] += float(part['sell_price']) * part['quantity']
        
        stats_lines = []
        for category, stats in sorted(categories.items()):
            stats_lines.append(
                f"• {category}: {stats['count']} наим., "
                f"{stats['quantity']} шт., {stats['value']:.2f} ₽"
            )
        
        layout = self.category_stats.layout()
        label = layout.itemAt(0).widget()
        label.setText('\n'.join(stats_lines) if stats_lines else "Нет данных")
    
    def update_brand_stats(self, parts):
        """Обновить статистику по маркам"""
        brands = {}
        
        for part in parts:
            brand = part['brand']
            if brand not in brands:
                brands[brand] = {'count': 0, 'quantity': 0, 'value': 0}
            
            brands[brand]['count'] += 1
            brands[brand]['quantity'] += part['quantity']
            brands[brand]['value'] += float(part['sell_price']) * part['quantity']
        
        # Сортируем по стоимости (убывание)
        sorted_brands = sorted(brands.items(), key=lambda x: x[1]['value'], reverse=True)
        
        stats_lines = []
        for brand, stats in sorted_brands[:10]:  # Топ 10
            stats_lines.append(
                f"• {brand}: {stats['count']} наим., "
                f"{stats['quantity']} шт., {stats['value']:.2f} ₽"
            )
        
        layout = self.brand_stats.layout()
        label = layout.itemAt(0).widget()
        label.setText('\n'.join(stats_lines) if stats_lines else "Нет данных")
    
    def update_low_stock_stats(self, parts):
        """Обновить статистику низких остатков"""
        low_stock_parts = [part for part in parts if part['quantity'] <= 5]
        low_stock_parts.sort(key=lambda x: x['quantity'])
        
        if low_stock_parts:
            stats_lines = []
            for part in low_stock_parts[:20]:  # Показываем до 20 позиций
                stats_lines.append(
                    f"• {part['article']} ({part['name']}): {part['quantity']} шт."
                )
            
            stats_text = f"⚠️ Найдено {len(low_stock_parts)} позиций с низким остатком:\n\n" + '\n'.join(stats_lines)
        else:
            stats_text = "✅ Все запчасти в достаточном количестве!"
        
        layout = self.low_stock_stats.layout()
        label = layout.itemAt(0).widget()
        label.setText(stats_text)


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1200, 800)
        
        # Инициализация базы данных
        db.init_database()
        
        self.setup_ui()
        self.setup_menu()
        
        # Применяем стили
        self.setStyleSheet(get_enhanced_complete_style())
        
        # Статусная строка
        self.statusBar().showMessage("Готов к работе")
    
    def setup_ui(self):
        """Настройка интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Заголовок приложения
        header = QLabel(f"🚗 {APP_NAME}")
        header.setProperty("class", "main-title")
        layout.addWidget(header)
        
        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "main-tabs")
        
        # Вкладка управления запчастями
        self.parts_widget = PartsWidget(self)
        self.tabs.addTab(self.parts_widget, "🔧 Запчасти")
        
        # Вкладка статистики
        self.stats_widget = StatisticsWidget()
        self.tabs.addTab(self.stats_widget, "📊 Статистика")
        
        layout.addWidget(self.tabs)
    
    def setup_menu(self):
        """Настройка меню"""
        menubar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menubar.addMenu("📁 Файл")
        
        # Настройки
        settings_action = QAction("⚙️ Настройки", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        # Выход
        exit_action = QAction("🚪 Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню "Справка"
        help_menu = menubar.addMenu("❓ Справка")
        
        about_action = QAction("ℹ️ О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_settings(self):
        """Показать настройки"""
        show_settings_dialog(self)
    
    def show_about(self):
        """Показать информацию о программе"""
        QMessageBox.about(
            self, 
            "О программе",
            f"""
            <h3>{APP_NAME}</h3>
            <p>Версия: 1.0.0</p>
            <p>Простая и удобная система для учёта автозапчастей</p>
            <p><b>Возможности:</b></p>
            <ul>
                <li>Добавление и редактирование запчастей</li>
                <li>Поиск и фильтрация</li>
                <li>Статистика и аналитика</li>
                <li>Контроль остатков</li>
            </ul>
            """
        )


def main():
    """Главная функция приложения"""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion("1.0.0")
    
    # Создание и показ главного окна
    window = MainWindow()
    window.show()
    
    # Запуск приложения
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

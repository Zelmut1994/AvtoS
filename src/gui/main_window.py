from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QPushButton, QMenuBar, QStatusBar, 
                             QMessageBox, QLabel)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QFont

from .parts_widget import PartsWidget
from .sales_widget import SalesWidget
from .reports_widget import ReportsWidget
from ..services import BackupService

class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система учёта автозапчастей v1.0")
        self.setMinimumSize(1200, 800)
        
        # Устанавливаем иконку окна (если есть файл)
        # self.setWindowIcon(QIcon("resources/icon.ico"))
        
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout(central_widget)
        
        # Заголовок
        title_label = QLabel("Система учёта автозапчастей")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Создаем виджет с вкладками
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Вкладка "Запчасти"
        self.parts_widget = PartsWidget()
        self.tab_widget.addTab(self.parts_widget, "📦 Запчасти")
        
        # Вкладка "Продажи"
        self.sales_widget = SalesWidget()
        self.tab_widget.addTab(self.sales_widget, "💰 Продажи")
        
        # Вкладка "Отчёты"
        self.reports_widget = ReportsWidget()
        self.tab_widget.addTab(self.reports_widget, "📊 Отчёты")
        
        # Панель быстрых действий
        self.setup_quick_actions(layout)
        
    def setup_quick_actions(self, layout):
        """Панель быстрых действий"""
        quick_layout = QHBoxLayout()
        
        # Кнопка "Новая продажа"
        new_sale_btn = QPushButton("🛒 Новая продажа")
        new_sale_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        new_sale_btn.clicked.connect(self.new_sale)
        quick_layout.addWidget(new_sale_btn)
        
        # Кнопка "Добавить запчасть"
        new_part_btn = QPushButton("➕ Добавить запчасть")
        new_part_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        new_part_btn.clicked.connect(self.new_part)
        quick_layout.addWidget(new_part_btn)
        
        quick_layout.addStretch()
        
        # Кнопка резервного копирования
        backup_btn = QPushButton("💾 Резервная копия")
        backup_btn.clicked.connect(self.create_backup)
        quick_layout.addWidget(backup_btn)
        
        layout.addLayout(quick_layout)
    
    def setup_menu(self):
        """Настройка меню"""
        menubar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menubar.addMenu("Файл")
        
        backup_action = QAction("Создать резервную копию", self)
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)
        
        restore_action = QAction("Восстановить из копии", self)
        restore_action.triggered.connect(self.restore_backup)
        file_menu.addAction(restore_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню "Справка"
        help_menu = menubar.addMenu("Справка")
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Настройка строки состояния"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_bar.showMessage("Готов к работе")
        
        # Таймер для обновления времени
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(60000)  # Обновляем каждую минуту
    
    def update_status(self):
        """Обновление строки состояния"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        self.status_bar.showMessage(f"Время: {current_time}")
    
    def new_sale(self):
        """Переключиться на вкладку продаж и создать новую продажу"""
        self.tab_widget.setCurrentIndex(1)  # Индекс вкладки "Продажи"
        self.sales_widget.new_sale()
    
    def new_part(self):
        """Переключиться на вкладку запчастей и добавить новую"""
        self.tab_widget.setCurrentIndex(0)  # Индекс вкладки "Запчасти"
        self.parts_widget.add_part()
    
    def create_backup(self):
        """Создать резервную копию"""
        success, message = BackupService.create_backup()
        
        if success:
            QMessageBox.information(self, "Резервное копирование", message)
        else:
            QMessageBox.warning(self, "Ошибка", message)
    
    def restore_backup(self):
        """Восстановить из резервной копии"""
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите файл резервной копии",
            BackupService.get_backup_dir(),
            "Database files (*.db)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self, 
                "Подтверждение",
                "Вы уверены, что хотите восстановить базу данных?\n"
                "Текущие данные будут заменены!",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success, message = BackupService.restore_backup(file_path)
                
                if success:
                    QMessageBox.information(self, "Восстановление", 
                                          message + "\n\nПерезапустите приложение.")
                else:
                    QMessageBox.warning(self, "Ошибка", message)
    
    def show_about(self):
        """Показать информацию о программе"""
        QMessageBox.about(self, "О программе", 
                         "Система учёта автозапчастей v1.0\n\n"
                         "Приложение для учёта и продажи автозапчастей\n"
                         "в небольших магазинах.\n\n"
                         "Разработано на Python + PySide6")
    
    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        reply = QMessageBox.question(self, "Выход", 
                                   "Вы действительно хотите выйти?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Создаем автоматическую резервную копию при выходе
            BackupService.auto_backup()
            event.accept()
        else:
            event.ignore() 
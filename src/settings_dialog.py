"""
Диалог настроек приложения
"""

import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QFormLayout, QGroupBox, QCheckBox, QSpinBox, QLineEdit,
    QPushButton, QFileDialog, QLabel, QComboBox, 
    QSlider, QDialogButtonBox, QMessageBox, QTextEdit, QSplitter
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap

from settings_manager import get_settings
from modern_widgets import ModernButton, ModernGroupBox
from ui_utils import apply_modern_styling
from simple_icon_loader import SimpleIconLoader


class SettingsDialog(QDialog):
    """Диалог настроек приложения"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = get_settings()
        self.icon_loader = SimpleIconLoader()
        self.init_ui()
        self.load_settings()
        self.setModal(True)
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("Настройки AutoParts")
        self.setMinimumSize(600, 500)
        self.resize(800, 600)
        
        # Основной layout
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Заголовок
        title_label = QLabel("⚙️ Настройки приложения")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Вкладки настроек
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Создаём вкладки
        self.create_interface_tab()
        self.create_database_tab()
        self.create_export_tab()
        self.create_advanced_tab()
        self.create_about_tab()
        
        # Кнопки
        self.create_button_box()
        layout.addWidget(self.button_box)
        
        # Применяем стили
        apply_modern_styling(self)
    
    def create_interface_tab(self):
        """Создать вкладку интерфейса"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Группа: Внешний вид
        appearance_group = ModernGroupBox("🎨 Внешний вид")
        appearance_layout = QFormLayout(appearance_group)
        
        # Показывать диалог приветствия
        self.show_welcome_check = QCheckBox("Показывать диалог приветствия при запуске")
        appearance_layout.addRow(self.show_welcome_check)
        
        # Подтверждать удаления
        self.confirm_deletions_check = QCheckBox("Подтверждать удаления")
        appearance_layout.addRow(self.confirm_deletions_check)
        
        layout.addWidget(appearance_group)
        
        # Группа: Производительность
        performance_group = ModernGroupBox("⚡ Производительность")
        performance_layout = QFormLayout(performance_group)
        
        # Элементов на странице
        self.items_per_page_spin = QSpinBox()
        self.items_per_page_spin.setRange(10, 1000)
        self.items_per_page_spin.setSuffix(" элементов")
        performance_layout.addRow("Элементов на странице:", self.items_per_page_spin)
        
        # Интервал автообновления
        self.auto_refresh_spin = QSpinBox()
        self.auto_refresh_spin.setRange(5, 300)
        self.auto_refresh_spin.setSuffix(" сек")
        performance_layout.addRow("Автообновление каждые:", self.auto_refresh_spin)
        
        layout.addWidget(performance_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "🖥️ Интерфейс")
    
    def create_database_tab(self):
        """Создать вкладку базы данных"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Группа: Файл базы данных
        db_file_group = ModernGroupBox("💾 Файл базы данных")
        db_file_layout = QVBoxLayout(db_file_group)
        
        # Путь к БД
        db_path_layout = QHBoxLayout()
        self.db_path_edit = QLineEdit()
        self.db_path_edit.setReadOnly(True)
        self.db_browse_btn = ModernButton("📁 Обзор...")
        self.db_browse_btn.clicked.connect(self.browse_database_path)
        
        db_path_layout.addWidget(QLabel("Путь к файлу:"))
        db_path_layout.addWidget(self.db_path_edit)
        db_path_layout.addWidget(self.db_browse_btn)
        db_file_layout.addLayout(db_path_layout)
        
        layout.addWidget(db_file_group)
        
        # Группа: Резервное копирование
        backup_group = ModernGroupBox("💿 Резервное копирование")
        backup_layout = QFormLayout(backup_group)
        
        # Автоматическое резервное копирование
        self.auto_backup_check = QCheckBox("Включить автоматическое резервное копирование")
        backup_layout.addRow(self.auto_backup_check)
        
        # Интервал резервного копирования
        self.backup_interval_spin = QSpinBox()
        self.backup_interval_spin.setRange(1, 30)
        self.backup_interval_spin.setSuffix(" дней")
        backup_layout.addRow("Создавать резервную копию каждые:", self.backup_interval_spin)
        
        # Максимум файлов резервных копий
        self.max_backup_spin = QSpinBox()
        self.max_backup_spin.setRange(1, 100)
        self.max_backup_spin.setSuffix(" файлов")
        backup_layout.addRow("Максимум резервных копий:", self.max_backup_spin)
        
        layout.addWidget(backup_group)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.backup_now_btn = ModernButton("💿 Создать резервную копию сейчас")
        self.backup_now_btn.clicked.connect(self.create_backup_now)
        
        self.open_backup_folder_btn = ModernButton("📁 Открыть папку резервных копий")
        self.open_backup_folder_btn.clicked.connect(self.open_backup_folder)
        
        buttons_layout.addWidget(self.backup_now_btn)
        buttons_layout.addWidget(self.open_backup_folder_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        self.tab_widget.addTab(tab, "💾 База данных")
    
    def create_export_tab(self):
        """Создать вкладку экспорта"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Группа: Настройки экспорта
        export_group = ModernGroupBox("📤 Настройки экспорта")
        export_layout = QFormLayout(export_group)
        
        # Формат по умолчанию
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["csv", "xlsx", "json", "txt"])
        export_layout.addRow("Формат по умолчанию:", self.export_format_combo)
        
        # Папка экспорта
        export_dir_layout = QHBoxLayout()
        self.export_dir_edit = QLineEdit()
        self.export_dir_edit.setReadOnly(True)
        self.export_browse_btn = ModernButton("📁 Обзор...")
        self.export_browse_btn.clicked.connect(self.browse_export_directory)
        
        export_dir_layout.addWidget(self.export_dir_edit)
        export_dir_layout.addWidget(self.export_browse_btn)
        export_layout.addRow("Папка для экспорта:", export_dir_layout)
        
        layout.addWidget(export_group)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.open_export_folder_btn = ModernButton("📁 Открыть папку экспорта")
        self.open_export_folder_btn.clicked.connect(self.open_export_folder)
        
        buttons_layout.addWidget(self.open_export_folder_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        self.tab_widget.addTab(tab, "📤 Экспорт")
    
    def create_advanced_tab(self):
        """Создать вкладку дополнительных настроек"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Группа: Управление настройками
        settings_group = ModernGroupBox("⚙️ Управление настройками")
        settings_layout = QVBoxLayout(settings_group)
        
        # Информация о настройках
        info_layout = QFormLayout()
        
        self.settings_file_label = QLabel()
        self.settings_file_label.setWordWrap(True)
        info_layout.addRow("Файл настроек:", self.settings_file_label)
        
        self.app_data_label = QLabel()
        self.app_data_label.setWordWrap(True)
        info_layout.addRow("Папка данных:", self.app_data_label)
        
        settings_layout.addLayout(info_layout)
        
        # Кнопки управления настройками
        settings_buttons_layout = QHBoxLayout()
        
        self.export_settings_btn = ModernButton("📤 Экспортировать настройки")
        self.export_settings_btn.clicked.connect(self.export_settings)
        
        self.import_settings_btn = ModernButton("📥 Импортировать настройки")
        self.import_settings_btn.clicked.connect(self.import_settings)
        
        self.reset_settings_btn = ModernButton("🔄 Сбросить к умолчанию")
        self.reset_settings_btn.clicked.connect(self.reset_settings)
        self.reset_settings_btn.setStyleSheet("QPushButton { background-color: #ff6b6b; }")
        
        settings_buttons_layout.addWidget(self.export_settings_btn)
        settings_buttons_layout.addWidget(self.import_settings_btn)
        settings_buttons_layout.addWidget(self.reset_settings_btn)
        settings_buttons_layout.addStretch()
        
        settings_layout.addLayout(settings_buttons_layout)
        layout.addWidget(settings_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "🔧 Дополнительно")
    
    def create_about_tab(self):
        """Создать вкладку информации"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Информация о приложении
        info_group = ModernGroupBox("ℹ️ О программе")
        info_layout = QVBoxLayout(info_group)
        
        # Заголовок
        title_label = QLabel("🚗 AutoParts v1.0")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(title_label)
        
        # Описание
        desc_label = QLabel("""
        <p align="center">
        <b>Система управления автозапчастями</b><br>
        Современное приложение для учёта запчастей и продаж
        </p>
        """)
        desc_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(desc_label)
        
        # Технические детали
        tech_info = QTextEdit()
        tech_info.setMaximumHeight(200)
        tech_info.setReadOnly(True)
        
        settings_info = self.settings.get_settings_info()
        tech_text = f"""
Техническая информация:

📁 Файл настроек: {settings_info['settings_file']}
📂 Папка данных: {settings_info['app_data_dir']}
💾 База данных: {settings_info['database_path']}
📤 Папка экспорта: {settings_info['export_directory']}

Настройки:
• Автобэкап: {'Включён' if settings_info['auto_backup_enabled'] else 'Выключен'}
• Интервал бэкапа: {settings_info['backup_interval_days']} дней 
• Элементов на страницу: {settings_info['items_per_page']}
• Автообновление: {settings_info['auto_refresh_interval']} сек
        """
        tech_info.setPlainText(tech_text.strip())
        info_layout.addWidget(tech_info)
        
        layout.addWidget(info_group)
        layout.addStretch()
        self.tab_widget.addTab(tab, "ℹ️ О программе")
    
    def create_button_box(self):
        """Создать панель кнопок"""
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )
        
        # Переименовываем кнопки
        self.button_box.button(QDialogButtonBox.Ok).setText("✅ ОК")
        self.button_box.button(QDialogButtonBox.Cancel).setText("❌ Отмена")
        self.button_box.button(QDialogButtonBox.Apply).setText("💾 Применить")
        
        self.button_box.accepted.connect(self.accept_settings)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply_settings)
    
    def load_settings(self):
        """Загрузить настройки в UI"""
        # Интерфейс
        self.show_welcome_check.setChecked(self.settings.show_welcome_dialog)
        self.confirm_deletions_check.setChecked(self.settings.confirm_deletions)
        self.items_per_page_spin.setValue(self.settings.items_per_page)
        self.auto_refresh_spin.setValue(self.settings.auto_refresh_interval)
        
        # База данных
        self.db_path_edit.setText(self.settings.database_path)
        self.auto_backup_check.setChecked(self.settings.auto_backup_enabled)
        self.backup_interval_spin.setValue(self.settings.backup_interval_days)
        self.max_backup_spin.setValue(self.settings.max_backup_files)
        
        # Экспорт
        self.export_format_combo.setCurrentText(self.settings.default_export_format)
        self.export_dir_edit.setText(self.settings.export_directory)
        
        # Дополнительно
        info = self.settings.get_settings_info()
        self.settings_file_label.setText(info['settings_file'])
        self.app_data_label.setText(info['app_data_dir'])
    
    def apply_settings(self):
        """Применить настройки"""
        try:
            # Интерфейс
            self.settings.show_welcome_dialog = self.show_welcome_check.isChecked()
            self.settings.confirm_deletions = self.confirm_deletions_check.isChecked()
            self.settings.items_per_page = self.items_per_page_spin.value()
            self.settings.auto_refresh_interval = self.auto_refresh_spin.value()
            
            # База данных
            self.settings.database_path = self.db_path_edit.text()
            self.settings.auto_backup_enabled = self.auto_backup_check.isChecked()
            self.settings.backup_interval_days = self.backup_interval_spin.value()
            self.settings.max_backup_files = self.max_backup_spin.value()
            
            # Экспорт
            self.settings.default_export_format = self.export_format_combo.currentText()
            self.settings.export_directory = self.export_dir_edit.text()
            
            print("✅ Настройки применены")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось применить настройки:\n{e}")
    
    def accept_settings(self):
        """Принять и закрыть диалог"""
        self.apply_settings()
        self.accept()
    
    def browse_database_path(self):
        """Выбрать путь к базе данных"""
        current_path = self.db_path_edit.text()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Выберите файл базы данных", 
            current_path, "База данных (*.db);;Все файлы (*)"
        )
        if file_path:
            self.db_path_edit.setText(file_path)
    
    def browse_export_directory(self):
        """Выбрать папку экспорта"""
        current_dir = self.export_dir_edit.text()
        dir_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку для экспорта", current_dir
        )
        if dir_path:
            self.export_dir_edit.setText(dir_path)
    
    def create_backup_now(self):
        """Создать резервную копию сейчас"""
        try:
            from datetime import datetime
            backup_dir = os.path.join(self.settings.app_data_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"autoparts_backup_{timestamp}.db")
            
            import shutil
            shutil.copy2(self.settings.database_path, backup_file)
            
            QMessageBox.information(
                self, "Успешно", 
                f"Резервная копия создана:\n{backup_file}"
            )
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать резервную копию:\n{e}")
    
    def open_backup_folder(self):
        """Открыть папку резервных копий"""
        backup_dir = os.path.join(self.settings.app_data_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        import subprocess
        subprocess.run(["explorer", backup_dir], shell=True)
    
    def open_export_folder(self):
        """Открыть папку экспорта"""
        export_dir = self.settings.export_directory
        os.makedirs(export_dir, exist_ok=True)
        
        import subprocess
        subprocess.run(["explorer", export_dir], shell=True)
    
    def export_settings(self):
        """Экспортировать настройки"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт настроек", 
            "autoparts_settings.ini", 
            "Файлы настроек (*.ini);;Все файлы (*)"
        )
        if file_path:
            if self.settings.export_settings(file_path):
                QMessageBox.information(self, "Успешно", "Настройки экспортированы")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось экспортировать настройки")
    
    def import_settings(self):
        """Импортировать настройки"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Импорт настроек", "", 
            "Файлы настроек (*.ini);;Все файлы (*)"
        )
        if file_path:
            reply = QMessageBox.question(
                self, "Подтверждение",
                "Импорт настроек заменит текущие настройки.\nПродолжить?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                if self.settings.import_settings(file_path):
                    QMessageBox.information(
                        self, "Успешно", 
                        "Настройки импортированы.\nПерезапустите приложение для применения изменений."
                    )
                    self.load_settings()  # Перезагружаем UI
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось импортировать настройки")
    
    def reset_settings(self):
        """Сбросить настройки к значениям по умолчанию"""
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Сброс настроек удалит все пользовательские настройки.\nПродолжить?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.settings.reset_to_defaults()
            self.load_settings()
            QMessageBox.information(self, "Успешно", "Настройки сброшены к значениям по умолчанию")


def show_settings_dialog(parent=None):
    """Показать диалог настроек"""
    dialog = SettingsDialog(parent)
    return dialog.exec()

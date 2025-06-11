#!/usr/bin/env python3
"""
Скрипт для компиляции ресурсов Qt
"""

import os
import subprocess
import sys
from pathlib import Path

def find_pyside_rcc():
    """Найти исполняемый файл pyside6-rcc"""
    # Возможные имена команды
    possible_names = ['pyside6-rcc', 'pyside6-rcc.exe']
    
    # Поиск в PATH
    for name in possible_names:
        try:
            result = subprocess.run(['which', name] if os.name != 'nt' else ['where', name], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                return name
        except:
            pass
    
    # Поиск в стандартных местах Python
    python_path = Path(sys.executable).parent
    for name in possible_names:
        rcc_path = python_path / name
        if rcc_path.exists():
            return str(rcc_path)
        
        # Также проверяем Scripts (Windows)
        scripts_path = python_path / 'Scripts' / name
        if scripts_path.exists():
            return str(scripts_path)
    
    return None

def compile_resources():
    """Компилировать ресурсы Qt в Python модуль"""
    print("🔨 Компиляция ресурсов Qt...")
    
    # Пути
    project_root = Path(__file__).parent.parent
    qrc_file = project_root / "resources" / "styles.qrc"
    output_file = project_root / "src" / "resources_rc.py"
    
    # Проверяем существование QRC файла
    if not qrc_file.exists():
        print(f"❌ Файл ресурсов не найден: {qrc_file}")
        return False
    
    # Находим pyside6-rcc
    rcc_cmd = find_pyside_rcc()
    if not rcc_cmd:
        print("❌ Команда pyside6-rcc не найдена")
        print("💡 Установите PySide6: pip install PySide6")
        return False
    
    # Компилируем ресурсы
    try:
        cmd = [rcc_cmd, str(qrc_file), '-o', str(output_file)]
        print(f"🚀 Выполняем: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Ресурсы скомпилированы: {output_file}")
            return True
        else:
            print(f"❌ Ошибка компиляции: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение при компиляции: {e}")
        return False

def check_qss_files():
    """Проверить существование QSS файлов"""
    print("🔍 Проверка QSS файлов...")
    
    project_root = Path(__file__).parent.parent
    styles_dir = project_root / "resources" / "styles"
    
    qss_files = [
        "main.qss",
        "tabs.qss", 
        "buttons.qss",
        "tables.qss",
        "forms.qss"
    ]
    
    all_exist = True
    for filename in qss_files:
        filepath = styles_dir / filename
        if filepath.exists():
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} - не найден")
            all_exist = False
    
    return all_exist

def main():
    """Основная функция"""
    print("🎨 Компиляция стилей AutoParts")
    print("=" * 40)
    
    # Проверяем QSS файлы
    if not check_qss_files():
        print("\n❌ Не все QSS файлы найдены. Прервано.")
        return 1
    
    # Компилируем ресурсы
    if compile_resources():
        print("\n🎉 Компиляция завершена успешно!")
        print("💡 Теперь можно использовать ресурсы в приложении")
        return 0
    else:
        print("\n❌ Компиляция не удалась")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
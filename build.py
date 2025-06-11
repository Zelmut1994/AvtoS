#!/usr/bin/env python3
"""
Скрипт для сборки приложения AutoParts в исполняемый файл
"""
import os
import subprocess
import sys
import shutil
import zipfile
from datetime import datetime
import glob
import platform

def check_requirements():
    """Проверка всех требований перед сборкой"""
    print("🔍 Проверка требований...")
    
    errors = []
    
    # Проверяем Python версию
    if sys.version_info < (3, 8):
        errors.append(f"❌ Требуется Python 3.8+, текущая версия: {sys.version}")
    else:
        print(f"✅ Python {sys.version.split()[0]}")
    
    # Проверяем PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("⚠️ PyInstaller не найден. Устанавливаем...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])
    
    # Проверяем PySide6
    try:
        import PySide6
        print(f"✅ PySide6 найден в: {os.path.dirname(PySide6.__file__)}")
        
        # Проверяем критически важные Qt плагины
        qt_dir = os.path.dirname(PySide6.__file__)
        platforms_path = os.path.join(qt_dir, "plugins", "platforms", "qwindows.dll")
        if not os.path.exists(platforms_path):
            errors.append(f"❌ Не найден qwindows.dll в {platforms_path}")
        else:
            print(f"✅ qwindows.dll найден")
            
    except ImportError:
        errors.append("❌ PySide6 не установлен")
    
    # Проверяем spec файл
    if not os.path.exists("build.spec"):
        errors.append("❌ Файл build.spec не найден")
    else:
        print("✅ build.spec найден")
    
    # Проверяем исходный файл
    if not os.path.exists("src/full_app.py"):
        errors.append("❌ Файл src/full_app.py не найден")
    else:
        print("✅ Исходный файл найден")
    
    if errors:
        print("\n⛔ Обнаружены проблемы:")
        for error in errors:
            print(error)
        return False
    
    return True

def clean_build_artifacts():
    """Очистка артефактов предыдущих сборок"""
    print("\n🧹 Очистка артефактов предыдущих сборок...")
    
    # Удаляем временные файлы PyInstaller
    for pattern in ["*.pyc", "__pycache__", "*.pyo"]:
        for path in glob.glob(f"**/{pattern}", recursive=True):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except:
                pass
    
    # Удаляем старые runtime hooks
    for hook in glob.glob("qt_*.py"):
        try:
            os.remove(hook)
            print(f"  Удален: {hook}")
        except:
            pass
    
    # Удаляем старые директории сборки
    for dir_name in ["build", "dist", "build_new"]:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  Удалена папка: {dir_name}")
            except Exception as e:
                print(f"  ⚠️ Не удалось удалить {dir_name}: {e}")

def build_executable():
    """Собрать исполняемый файл"""
    print("\n🔨 Начинаем сборку AutoParts...")
    
    # Создаем новую директорию для сборки
    build_dir = "build_new"
    os.makedirs(build_dir, exist_ok=True)
    
    # Запускаем PyInstaller с spec-файлом
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--distpath", f"{build_dir}/dist",
        "--workpath", f"{build_dir}/work",
        "--log-level", "INFO",
        "build.spec"
    ]
    
    print("⚙️ Запускаем PyInstaller...")
    print(f"📝 Команда: {' '.join(cmd)}")
    
    try:
        # Запускаем с выводом в реальном времени
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                 text=True, bufsize=1, universal_newlines=True)
        
        # Читаем вывод построчно
        for line in process.stdout:
            line = line.strip()
            if line:
                # Фильтруем важные сообщения
                if "ERROR" in line or "WARNING" in line:
                    print(f"⚠️ {line}")
                elif "INFO: Building" in line:
                    print(f"🔧 {line}")
                elif "completed successfully" in line:
                    print(f"✅ {line}")
        
        process.wait()
        
        if process.returncode == 0:
            print("\n✅ Сборка завершена успешно!")
            return True
        else:
            print(f"\n❌ Сборка завершилась с кодом ошибки: {process.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при сборке: {e}")
        return False

def verify_qt_plugins(app_dir):
    """Проверка и исправление Qt плагинов"""
    print("\n🔍 Проверка Qt плагинов...")
    
    # Проверяем наличие qwindows.dll
    platforms_paths = [
        os.path.join(app_dir, "_internal", "platforms"),
        os.path.join(app_dir, "platforms"),
    ]
    
    qwindows_found = False
    for path in platforms_paths:
        qwindows_path = os.path.join(path, "qwindows.dll")
        if os.path.exists(qwindows_path):
            print(f"✅ qwindows.dll найден: {qwindows_path}")
            qwindows_found = True
            break
    
    if not qwindows_found:
        print("❌ qwindows.dll не найден! Пытаемся скопировать...")
        try:
            import PySide6
            qt_dir = os.path.dirname(PySide6.__file__)
            source_qwindows = os.path.join(qt_dir, "plugins", "platforms", "qwindows.dll")
            
            if os.path.exists(source_qwindows):
                # Создаем директорию platforms в _internal
                target_dir = os.path.join(app_dir, "_internal", "platforms")
                os.makedirs(target_dir, exist_ok=True)
                
                shutil.copy2(source_qwindows, target_dir)
                print(f"✅ qwindows.dll скопирован в {target_dir}")
            else:
                print(f"❌ Исходный qwindows.dll не найден: {source_qwindows}")
                return False
        except Exception as e:
            print(f"❌ Ошибка при копировании qwindows.dll: {e}")
            return False
    
    # Проверяем другие важные DLL
    required_dlls = ["Qt6Core.dll", "Qt6Gui.dll", "Qt6Widgets.dll"]
    missing_dlls = []
    
    for dll in required_dlls:
        dll_path = os.path.join(app_dir, "_internal", dll)
        if not os.path.exists(dll_path):
            dll_path = os.path.join(app_dir, dll)
            if not os.path.exists(dll_path):
                missing_dlls.append(dll)
    
    if missing_dlls:
        print(f"⚠️ Отсутствуют DLL: {', '.join(missing_dlls)}")
    else:
        print("✅ Все основные Qt DLL на месте")
    
    return True

def create_launcher_batch(app_dir):
    """Создать batch файл для запуска с правильными переменными окружения"""
    batch_content = """@echo off
echo Starting AutoParts...
echo.

REM Устанавливаем текущую директорию
cd /d "%~dp0"

REM Устанавливаем переменные окружения Qt
set QT_PLUGIN_PATH=%~dp0_internal
set QT_QPA_PLATFORM_PLUGIN_PATH=%~dp0_internal\\platforms

REM Проверяем наличие qwindows.dll
if exist "_internal\\platforms\\qwindows.dll" (
    echo [OK] Platform plugin found
) else (
    echo [ERROR] Platform plugin not found!
    echo Please reinstall the application.
    pause
    exit /b 1
)

REM Запускаем приложение
AutoParts.exe %*

REM Если произошла ошибка
if errorlevel 1 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)
"""
    
    batch_path = os.path.join(app_dir, "AutoParts_launcher.bat")
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"✅ Создан launcher: {batch_path}")

def test_build():
    """Тестирование собранного приложения"""
    print("\n🧪 Тестируем собранное приложение...")
    
    exe_path = "build_new/dist/AutoParts/AutoParts.exe"
    app_dir = os.path.dirname(exe_path)
    
    if not os.path.exists(exe_path):
        print("❌ Исполняемый файл не найден")
        return False
    
    # Проверяем размер
    total_size = 0
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(app_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            file_count += 1
    
    size_mb = total_size / (1024 * 1024)
    print(f"📊 Статистика:")
    print(f"   - Размер: {size_mb:.1f} MB")
    print(f"   - Файлов: {file_count}")
    print(f"   - Путь: {os.path.abspath(exe_path)}")
    
    # Проверяем Qt плагины
    verify_qt_plugins(app_dir)
    
    # Создаем launcher
    create_launcher_batch(app_dir)
    
    return True

def create_distribution_package():
    """Создать пакет дистрибутива"""
    print("\n📦 Создаем пакет дистрибутива...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"build_new/AutoParts_{timestamp}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        app_dir = "build_new/dist/AutoParts"
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "build_new/dist")
                zipf.write(file_path, arcname)
    
    # Получаем размер архива
    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"✅ Архив создан: {zip_filename} ({size_mb:.1f} MB)")
    
    return True

def main():
    """Главная функция"""
    print("=" * 60)
    print("🚀 AutoParts Build Script v2.0")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💻 {platform.system()} {platform.release()}")
    print("=" * 60)
    
    # Проверяем требования
    if not check_requirements():
        print("\n💥 Сборка отменена из-за отсутствия требований")
        sys.exit(1)
    
    # Очищаем старые артефакты
    clean_build_artifacts()
    
    # Собираем приложение
    if build_executable():
        if test_build():
            create_distribution_package()
            print("\n" + "=" * 60)
            print("🎉 ГОТОВО! Приложение успешно собрано!")
            print("📁 Результаты в папке: build_new/dist/AutoParts/")
            print("🚀 Запустите AutoParts_launcher.bat для старта")
            print("=" * 60)
        else:
            print("\n💥 Тестирование выявило проблемы")
            sys.exit(1)
    else:
        print("\n💥 Сборка не удалась")
        sys.exit(1)

if __name__ == "__main__":
    main()
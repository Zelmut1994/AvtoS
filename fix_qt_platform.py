#!/usr/bin/env python3
"""
Скрипт для исправления проблемы с Qt platform plugin
"""
import os
import sys
import shutil
import urllib.request
import zipfile

def download_qt_fix():
    """Скачать исправленные Qt библиотеки"""
    print("📥 Загружаем исправления для Qt...")
    
    # URL к исправленным библиотекам (пример)
    # В реальности нужно использовать актуальные ссылки
    fixes = {
        'qwindows.dll': 'https://example.com/qwindows_fixed.dll',
        # Альтернатива - использовать Qt5 версию qwindows.dll
    }
    
    print("⚠️ Автоматическая загрузка недоступна.")
    print("   Используйте одно из решений ниже:")
    
    return False

def solution_1_downgrade_qt(app_dir):
    """Решение 1: Использовать Qt5 вместо Qt6"""
    print("\n🔧 Решение 1: Переход на Qt5")
    print("1. Деинсталлируйте PySide6:")
    print("   pip uninstall PySide6")
    print("2. Установите PySide2 (Qt5):")
    print("   pip install PySide2")
    print("3. Измените импорты в коде с PySide6 на PySide2")
    print("4. Пересоберите приложение")

def solution_2_patch_dll(app_dir):
    """Решение 2: Патч qwindows.dll"""
    print("\n🔧 Решение 2: Патч qwindows.dll")
    
    # Создаем обертку для qwindows.dll
    wrapper_code = """
#include <windows.h>

// Заглушка для отсутствующей функции
extern "C" __declspec(dllexport) 
HRESULT WINAPI UiaRaiseNotificationEvent(void* provider, int notificationKind, 
                                         int notificationProcessing, 
                                         BSTR displayString, BSTR activityId) {
    return S_OK; // Просто возвращаем успех
}
"""
    
    print("Для исправления нужно:")
    print("1. Скомпилировать DLL-обертку с заглушкой для UiaRaiseNotificationEvent")
    print("2. Или использовать hex-редактор для патча импортов в qwindows.dll")
    print("3. Или найти qwindows.dll от Qt 5.15 (обычно совместим)")

def solution_3_windows_update(app_dir):
    """Решение 3: Обновить Windows"""
    print("\n🔧 Решение 3: Обновление Windows")
    print("1. Откройте Параметры → Обновление и безопасность")
    print("2. Установите все доступные обновления Windows")
    print("3. Особенно важно обновление KB4601319 или новее")
    print("4. Перезагрузите компьютер")
    
    # Проверяем версию Windows
    try:
        import platform
        win_ver = platform.win32_ver()
        print(f"\nВаша версия Windows: {win_ver[0]} {win_ver[1]}")
        
        # UiaRaiseNotificationEvent появилась в Windows 10 версии 1709
        if win_ver[1] < '10.0.16299':
            print("⚠️ Ваша версия Windows слишком старая!")
            print("   Требуется Windows 10 версии 1709 или новее")
    except:
        pass

def solution_4_use_alternative_platform(app_dir):
    """Решение 4: Использовать альтернативную платформу"""
    print("\n🔧 Решение 4: Альтернативный платформенный плагин")
    
    # Создаем батник для запуска с minimal platform
    batch_content = """@echo off
cd /d "%~dp0"

REM Используем minimal платформу вместо windows
set QT_QPA_PLATFORM=minimal
set QT_PLUGIN_PATH=%~dp0_internal

echo Запуск с minimal платформой (без GUI)...
AutoParts.exe

if errorlevel 1 (
    echo Попробуем offscreen платформу...
    set QT_QPA_PLATFORM=offscreen
    AutoParts.exe
)
pause
"""
    
    batch_path = os.path.join(app_dir, "AutoParts_minimal.bat")
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    print(f"✅ Создан: {batch_path}")
    print("   Внимание: minimal платформа работает без отображения окон!")

def solution_5_copy_from_working_system(app_dir):
    """Решение 5: Копировать с рабочей системы"""
    print("\n🔧 Решение 5: Копирование с другой системы")
    print("Если у вас есть доступ к компьютеру где приложение работает:")
    print("1. Скопируйте qwindows.dll с рабочего компьютера")
    print("2. Желательно с Windows 10 версии 1909 или новее")
    print("3. Путь: C:\\Python3X\\Lib\\site-packages\\PySide6\\plugins\\platforms\\")
    print("4. Замените файл в вашей сборке")

def apply_quick_fix(app_dir):
    """Быстрое временное решение"""
    print("\n⚡ Применяем быстрое решение...")
    
    # Создаем манифест приложения для совместимости
    manifest_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <!-- Windows 10 -->
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
      <!-- Windows 8.1 -->
      <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"/>
      <!-- Windows 8 -->
      <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>
      <!-- Windows 7 -->
      <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>
    </application>
  </compatibility>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity type="win32" name="Microsoft.Windows.Common-Controls" 
                        version="6.0.0.0" processorArchitecture="*" 
                        publicKeyToken="6595b64144ccf1df" language="*"/>
    </dependentAssembly>
  </dependency>
</assembly>"""
    
    manifest_path = os.path.join(app_dir, "AutoParts.exe.manifest")
    with open(manifest_path, 'w') as f:
        f.write(manifest_content)
    
    print(f"✅ Создан манифест: {manifest_path}")
    
    # Создаем батник с обходом проблемы
    workaround_batch = """@echo off
cd /d "%~dp0"

REM Отключаем UI Automation
set QT_DISABLE_WINDOWSCONTEXT=1
set QT_QPA_PLATFORM=windows:fontengine=freetype

REM Устанавливаем пути
set QT_PLUGIN_PATH=%~dp0_internal
set QT_QPA_PLATFORM_PLUGIN_PATH=%~dp0_internal\\platforms

REM Запускаем с обходом
echo Запуск с обходом UI Automation...
AutoParts.exe

if errorlevel 1 (
    echo.
    echo Если не помогло, попробуйте:
    echo 1. Обновить Windows до последней версии
    echo 2. Установить Windows 10 версии 1909 или новее
    echo 3. Использовать PySide2 вместо PySide6
    pause
)
"""
    
    workaround_path = os.path.join(app_dir, "AutoParts_workaround.bat")
    with open(workaround_path, 'w') as f:
        f.write(workaround_batch)
    
    print(f"✅ Создан обходной запуск: {workaround_path}")

def main():
    print("=" * 60)
    print("🔧 Qt Platform Plugin Fix Tool")
    print("=" * 60)
    print("\n❌ Проблема: qwindows.dll требует UiaRaiseNotificationEvent")
    print("   которая отсутствует в вашей версии Windows")
    
    if len(sys.argv) > 1:
        app_dir = sys.argv[1]
    else:
        app_dir = "build_new/dist/AutoParts"
    
    if not os.path.exists(app_dir):
        print(f"❌ Папка не найдена: {app_dir}")
        return
    
    # Применяем быстрое решение
    apply_quick_fix(app_dir)
    
    # Показываем все варианты решения
    print("\n📋 Доступные решения:")
    solution_3_windows_update(app_dir)
    solution_2_patch_dll(app_dir)
    solution_1_downgrade_qt(app_dir)
    solution_4_use_alternative_platform(app_dir)
    solution_5_copy_from_working_system(app_dir)
    
    print("\n" + "=" * 60)
    print("💡 Рекомендации:")
    print("1. Сначала попробуйте AutoParts_workaround.bat")
    print("2. Если не поможет - обновите Windows")
    print("3. Крайний случай - пересоберите с PySide2")
    print("=" * 60)

if __name__ == "__main__":
    main()
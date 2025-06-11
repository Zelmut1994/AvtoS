#!/usr/bin/env python3
"""
Скрипт для запуска всех проверок качества кода
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd: list[str], description: str) -> bool:
    """Запустить команду и вернуть результат"""
    print(f"\n🔍 {description}...")
    print(f"Команда: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} - успешно")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ошибка")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Основная функция"""
    print("🚀 Запуск проверок качества кода для AutoParts")
    
    # Переходим в корень проекта
    root_dir = Path(__file__).parent.parent
    print(f"📁 Рабочая директория: {root_dir}")
    
    all_passed = True
    
    # 1. Форматирование с ruff
    if not run_command(
        ["ruff", "format", "src/"],
        "Форматирование кода с ruff"
    ):
        all_passed = False
    
    # 2. Линтинг с ruff
    if not run_command(
        ["ruff", "check", "src/", "--fix"],
        "Линтинг с ruff (с автоисправлениями)"
    ):
        all_passed = False
    
    # 3. Проверка типов с mypy
    if not run_command(
        ["mypy", "src/"],
        "Проверка типов с mypy"
    ):
        all_passed = False
    
    # 4. Проверка синтаксиса
    syntax_files = ["src/main.py", "src/full_app.py"]
    for file_path in syntax_files:
        if not run_command(
            ["python", "-m", "py_compile", file_path],
            f"Проверка синтаксиса {file_path}"
        ):
            all_passed = False
    
    # 5. Запуск тестов (если есть)
    tests_dir = root_dir / "tests"
    if tests_dir.exists():
        if not run_command(
            ["pytest", "tests/", "-v"],
            "Запуск тестов"
        ):
            all_passed = False
    else:
        print("\n⚠️ Директория tests/ не найдена, тесты пропущены")
    
    # Итоговый результат
    print("\n" + "="*50)
    if all_passed:
        print("🎉 Все проверки прошли успешно!")
        sys.exit(0)
    else:
        print("💥 Некоторые проверки не прошли!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
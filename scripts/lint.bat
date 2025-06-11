@echo off
echo 🚀 Запуск проверок качества кода для AutoParts
cd /d "%~dp0\.."

echo.
echo 🔍 Установка dev зависимостей...
pip install -e ".[dev]"

echo.
echo 🔍 Запуск проверок...
python scripts/lint.py

pause 
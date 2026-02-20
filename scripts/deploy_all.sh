#!/usr/bin/env bash
set -e

echo "🚀 Установка LightweightClaw..."

# Создаем директории для хранения данных и памяти
mkdir -p memory/long_term_summaries data logs models/piper

# Настраиваем виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# Обновляем pip и ставим зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Создаем базовый .env если его нет
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️ Файл .env создан. Отредактируйте его для настройки Telegram/Deepseek!"
fi

echo "✅ Установка завершена!"
echo "▶️ Для запуска используй:"
echo "source .venv/bin/activate && python main.py"

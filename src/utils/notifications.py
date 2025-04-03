import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from src.api.openrouter import OpenRouterAPI

# Загрузка переменных окружения из .env файла
load_dotenv()

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
BALANCE_THRESHOLD = float(os.getenv('BALANCE_THRESHOLD', 100))

async def send_telegram_notification(message):
    bot = Bot(token=TELEGRAM_API_KEY)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def check_balance_and_notify():
    api = OpenRouterAPI()
    balance_str = api.get_balance()
    if balance_str == "Ошибка":
        print("Ошибка проверки баланса")
        return

    balance = float(balance_str.replace('$', ''))
    if balance < BALANCE_THRESHOLD:
        message = f"Внгимание! Низкий баланс. Текущий баланс: {balance_str}"
        await send_telegram_notification(message)
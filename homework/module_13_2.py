import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

# Вставьте ваш токен бота ниже
API_TOKEN = 'токен'

# Настроим логирование
logging.basicConfig(level=logging.INFO)

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для обработки команды /start
@dp.message(Command("start"))
async def start(message: Message):
    print('Привет! Я бот помогающий твоему здоровью.')

# Функция для обработки всех остальных сообщений
@dp.message()
async def all_messages(message: Message):
    print('Введите команду /start, чтобы начать общение.')

# Запуск бота
async def main():
    print("Бот запущен и готов к работе...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
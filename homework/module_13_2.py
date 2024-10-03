import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio


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
    # Запускаем основной цикл через asyncio
    asyncio.run(main())

# INFO:aiogram.dispatcher:Start polling
# Бот запущен и готов к работе...
# INFO:aiogram.dispatcher:Run polling for bot @taggo12_belyaevanya_bot id=XXXXXXXXXX - 'ItemsBot'
# Введите команду /start, чтобы начать общение.
# INFO:aiogram.event:Update id=XXXXXXXXXX is handled. Duration 500 ms by bot id=XXXXXXXXXX
# Привет! Я бот помогающий твоему здоровью.
# INFO:aiogram.event:Update id=XXXXXXXXXX is handled. Duration 186 ms by bot id=XXXXXXXXXX
>>>>>>> 247cdb473f6ce7d13ec04d9db67bf8d1d08e9914

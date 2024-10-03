import logging
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

# Вставьте ваш токен бота ниже
API_TOKEN = 'token'

# Настроим логирование
logging.basicConfig(level=logging.INFO)

# Создаем объект бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()


@router.message(F.text == 'Печеньки')
async def cookies_messages(message):
    print(message.text.upper())
    await message.answer(message.text.upper())


# Функция для обработки команды /start
@router.message(Command("start"))
async def start(message: Message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer("Привет! Я бот, помогающий твоему здоровью.")


# Функция для обработки всех остальных сообщений
@router.message(F.text)
async def all_messages(message: Message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer("Введите команду /start, чтобы начать общение.")


# Привязываем роутер к диспетчеру
dp.include_router(router)


# Запуск бота
async def main():
    print("Бот запущен и готов к работе...")
    # Запуск polling (долгий опрос серверов Telegram)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Запускаем основной цикл через asyncio
    asyncio.run(main())

# INFO:aiogram.dispatcher:Start polling
# Бот запущен и готов к работе...
# INFO:aiogram.dispatcher:Run polling for bot @_bot id=XXXXXXXXXX - 'ItemsBot'
# Введите команду /start, чтобы начать общение.
# INFO:aiogram.event:Update id=XXXXXXXXXX is handled. Duration 500 ms by bot id=XXXXXXXXXX
# Привет! Я бот помогающий твоему здоровью.
# INFO:aiogram.event:Update id=XXXXXXXXXX is handled. Duration 186 ms by bot id=XXXXXXXXXX

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import Router

# Инициализация бота и диспетчера
API_TOKEN = ''
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создаем рутер для регистраций хэндлеров
router = Router()
dp.include_router(router)


# 1. Создание класса состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# 2. Создание клавиатуры с кнопками
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ]
    ],
    resize_keyboard=True
)


# 3. Добавляем обработчик для команды /start
@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я бот для расчета нормы калорий. Чтобы начать, нажмите 'Рассчитать'.",
        reply_markup=start_keyboard
    )


# 4. Обработчик для кнопки 'Рассчитать'
@router.message(lambda message: message.text == 'Рассчитать')
async def set_age(message: Message, state: FSMContext):
    await message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)  # Установка состояния на ожидание возраста


# 5. Обработчик для ввода возраста (состояние age)
@router.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    try:
        age = int(message.text)  # Проверка на корректность ввода
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число для возраста.')
        return

    await state.update_data(age=age)  # Обновление данных состояния
    await message.answer('Введите свой рост (в см):')
    await state.set_state(UserState.growth)  # Установка состояния на ожидание роста


# 6. Обработчик для ввода роста (состояние growth)
@router.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    try:
        growth = int(message.text)  # Проверка на корректность ввода
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число для роста.')
        return

    await state.update_data(growth=growth)  # Обновление данных состояния
    await message.answer('Введите свой вес (в кг):')
    await state.set_state(UserState.weight)  # Установка состояния на ожидание веса


# 7. Обработчик для подсчета калорий и отправки результата (состояние weight)
@router.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    try:
        weight = int(message.text)  # Проверка на корректность ввода
    except ValueError:
        await message.answer('Пожалуйста, введите корректное число для веса.')
        return

    await state.update_data(weight=weight)  # Обновление данных состояния

    # Получаем все введенные данные
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    # Формула Миффлина - Сан Жеора для женщин
    # BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161
    bmr = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {bmr:.2f} ккал в день.", reply_markup=ReplyKeyboardRemove())

    # Завершаем машину состояний
    await state.clear()  # Очистка состояния


# Асинхронная функция запуска бота
async def main():
    # Запуск диспетчера
    await dp.start_polling(bot)


# Запуск программы
if __name__ == '__main__':
    # Запускаем main() через asyncio
    asyncio.run(main())

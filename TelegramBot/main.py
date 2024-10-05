import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
import asyncio

API_TOKEN = '7779824271:AAHJ01L3be-L55ymfBc4STqtMB0d27q-U1U'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Пример каталога настольных игр
games_catalog = {
    "Catan": {"price": 1500, "description": "Настольная игра о заселении острова Катан."},
    "Monopoly": {"price": 1200, "description": "Классическая игра про управление финансами."},
    "Carcassonne": {"price": 1800, "description": "Средневековая игра о строительстве городов и дорог."}
}

# Корзина для пользователей
cart = {}


# Главное меню с инлайн-кнопками для игр и кнопкой "Информация"
def get_main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=game, callback_data=f"select_{game}") for game in games_catalog.keys()],
            [InlineKeyboardButton(text="Информация о магазине", callback_data="store_info")]
        ]
    )
    return keyboard


# Функция для старта бота
@dp.message(F.text == "/start")
async def send_welcome(message: types.Message):
    await message.answer("Добро пожаловать в магазин настольных игр!\nВыберите игру:",
                         reply_markup=get_main_menu_keyboard())


# Функция для отображения инлайн-кнопки "Добавить в корзину"
def get_add_to_cart_button(game_name):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{game_name}")]
        ]
    )
    return keyboard


# Обработка нажатия на инлайн-кнопки и вывод информации об игре
@dp.callback_query(lambda callback: callback.data.startswith("select_"))
async def handle_game_selection(callback_query: types.CallbackQuery):
    game_name = callback_query.data.split("_")[1]  # Получаем название игры из callback_data
    game_info = games_catalog.get(game_name)

    if game_info:
        # Формируем текст с информацией об игре
        game_details = (f"🕹 <b>{game_name}</b>\n"
                        f"💵 Цена: {game_info['price']} руб.\n"
                        f"📜 Описание: {game_info['description']}\n")

        # Отправляем информацию об игре пользователю
        await callback_query.message.answer(game_details, parse_mode="HTML",
                                            reply_markup=get_add_to_cart_button(game_name))

        await callback_query.answer()  # Закрываем alert
    else:
        await callback_query.answer(f"Игра {game_name} не найдена.", show_alert=True)


# Обработка нажатия на кнопку "Добавить в корзину"
@dp.callback_query(lambda callback: callback.data.startswith("add_"))
async def handle_add_to_cart(callback_query: types.CallbackQuery):
    game_name = callback_query.data.split("_")[1]  # Получаем название игры из callback_data

    # Добавляем игру в корзину
    if callback_query.from_user.id not in cart:
        cart[callback_query.from_user.id] = []
    cart[callback_query.from_user.id].append(game_name)

    # Отправляем уведомление о добавлении в корзину
    await callback_query.answer(f"Игра {game_name} добавлена в корзину", show_alert=True)


# Обработка инлайн-кнопки "Информация о магазине"
@dp.callback_query(lambda callback: callback.data == "store_info")
async def handle_store_info(callback_query: types.CallbackQuery):
    # Текст с информацией о магазине и доставке
    store_info = (
        "🏬 <b>Магазин настольных игр</b>\n"
        "Мы предлагаем широкий выбор популярных настольных игр.\n\n"
        "📦 <b>Способы доставки:</b>\n"
        "1. Курьерская доставка по Москве - 300 руб.\n"
        "2. Самовывоз из нашего офиса (бесплатно)\n"
        "3. Почтовая доставка по России - 500 руб.\n\n"
        "💳 <b>Способы оплаты:</b>\n"
        "- Наличные при получении\n"
        "- Банковская карта\n"
        "- Онлайн-оплата через сайт"
    )

    # Отправляем информацию пользователю
    await callback_query.message.answer(store_info, parse_mode="HTML")
    await callback_query.answer()  # Закрываем alert


# Просмотр корзины
@dp.message(F.text == "Корзина")
async def show_cart(message: types.Message):
    user_cart = cart.get(message.from_user.id, [])
    if not user_cart:
        await message.answer("Ваша корзина пуста.")
    else:
        cart_text = "Ваши игры в корзине:\n\n"
        total_price = 0
        for game in user_cart:
            game_info = games_catalog[game]
            cart_text += f"🕹 {game} - {game_info['price']} руб.\n"
            total_price += game_info['price']
        cart_text += f"\nОбщая сумма: {total_price} руб."
        await message.answer(cart_text)


# Оформление заказа
@dp.message(F.text == "/checkout")
async def checkout(message: types.Message):
    user_cart = cart.get(message.from_user.id, [])
    if not user_cart:
        await message.answer("Ваша корзина пуста.")
    else:
        total_price = sum(games_catalog[game]['price'] for game in user_cart)
        await message.answer(
            f"Вы оформили заказ на сумму {total_price} руб.\nНаш менеджер свяжется с вами для подтверждения заказа.")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

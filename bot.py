
import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Отримуємо токен з змінної середовища
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

try:
    with open('data.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        users[user_id] = {"clicks": 0, "referrals": 0}
        save_data()
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Клік!", callback_data="click")
    )
    await message.answer("Ласкаво просимо до гри Tapalka!\nНатискай на кнопку нижче, щоб заробити токени!", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "click")
async def click_handler(callback_query: types.CallbackQuery):
    user_id = str(callback_query.from_user.id)
    users[user_id]["clicks"] += 1
    save_data()
    await callback_query.answer(f"Ти натиснув! Твій баланс: {users[user_id]['clicks']} токенів.")

def save_data():
    with open('data.json', 'w') as f:
        json.dump(users, f, indent=4)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

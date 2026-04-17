import logging
import random
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- ТВІЙ ТОКЕН ТУТ ---
API_TOKEN = '6554854731:AAHtmSZGdTf1Ig7ZZ8QJTPOaGaO8s69HfL8'

# Налаштування логів
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- ЕКОНОМІКА ---
RATE = 1000  # 1000 Clean = 1 LumisCoin

# База гравців (в пам'яті)
users = {}

def get_user(uid, name):
    if uid not in users:
        users[uid] = {
            "name": name,
            "clean": 0, 
            "lumis": 0, 
            "level": 1, 
            "holders": 0
        }
    return users[uid]

# --- КНОПКИ ГОЛОВНОГО МЕНЮ ---
def main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🕹️ ГРАТИ", callback_data="play"),
        InlineKeyboardButton("🏙️ МОЄ СІТІ", callback_data="city"),
        InlineKeyboardButton("💰 ЗАРОБІТОК (TASKS)", callback_data="tasks"),
        InlineKeyboardButton("👛 ГАМАНЕЦЬ", callback_data="wallet"),
        InlineKeyboardButton("🏆 ЛІДЕРБОРД", callback_data="leaderboard")
    )
    return kb

# --- КОМАНДА СТАРТ ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    get_user(message.from_user.id, message.from_user.first_name)
    await message.answer(
        f"🦾 Вітаю, {message.from_user.first_name}! Це світ Люміса.\n\n"
        f"Твоя мета — відбудувати СІТІ. Збирай брухт ($CLEAN), міняй його на чисті $LUMIS за курсом 1000 до 1.\n"
        f"Або виконуй завдання для швидкого заробітку!",
        reply_markup=main_kb()
    )

# --- ЛОГІКА ГРИ (КЛІКЕР) ---
@dp.callback_query_handler(text="play")
async def play(call: types.CallbackQuery):
    u = get_user(call.from_user.id, call.from_user.first_name)
    loot = random.randint(50, 150)
    u["clean"] += loot
    
    # Кожні 5000 clean підвищуємо рівень
    new_level = (u["clean"] // 5000) + 1
    u["level"] = new_level

    await call.message.edit_text(
        f"🏭 ЛОКАЦІЯ: ЗАВОД (Рівень {u['level']})\n"
        f"Ти знайшов: +{loot} $CLEAN брухту.\n\n"
        f"💰 Всього брухту в мішку: {u['clean']}\n"
        f"🏙️ Твоє місто чекає на інвестиції!",
        reply_markup=main_kb()
    )

# --- ЛОГІКА ГАМАНЦЯ ТА ОБМІНУ ---
@dp.callback_query_handler(text="wallet")
async def wallet(call: types.CallbackQuery):
    u = get_user(call.from_user.id, call.from_user.first_name)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("🔄 ОБМІНЯТИ 1000 $CLEAN ➡️ 1 $LUMIS", callback_data="convert"))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    
    await call.message.edit_text(
        f"👛 Твій баланс:\n\n"
        f"🪙 Брухт ($CLEAN): {u['clean']}\n"
        f"💎 Чисті ($LUMIS): {u['lumis']}\n\n"
        f"Курс: {RATE} до 1",
        reply_markup=kb
    )

@dp.callback_query_handler(text="convert")
async def convert(call: types.CallbackQuery):
    u = get_user(call.from_user.id, call.from_user.first_name)
    if u["clean"] >= RATE:
        gained = u["clean"] // RATE
        u["lumis"] += gained
        u["clean"] %= RATE
        await call.answer(f"✅ Обмін виконано! +{gained} $LUMIS", show_alert=True)
        await wallet(call)
    else:
        await call.answer("❌ Тобі треба мінімум 1000 $CLEAN для обміну!", show_alert=True)

# --- ЗАВДАННЯ (8 ТАСКІВ) ---
@dp.callback_query_handler(text="tasks")
async def tasks(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1)
    # Сюди вставляй свої 8 посилань
    kb.add(
        InlineKeyboardButton("📢 Канал AI Community", url="https://t.me/your_link"),
        InlineKeyboardButton("✅ ПЕРЕВІРИТИ ПІДПИСКУ (Таск 1)", callback_data="check_1"),
        InlineKeyboardButton("📊 Binance Square Аналітика", url="https://binance.com/..."),
        InlineKeyboardButton("✅ ПЕРЕВІРИТИ (Таск 2)", callback_data="check_2"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back")
    )
    await call.message.edit_text("💰 Швидкий заробіток чистих $LUMIS:\nВиконуй таски і тисни 'Перевірити'.", reply_markup=kb)

# --- ЛІДЕРБОРД ---
@dp.callback_query_handler(text="leaderboard")
async def leaderboard(call: types.CallbackQuery):
    u = get_user(call.from_user.id, call.from_user.first_name)
    # В реальній БД тут буде сортування всіх юзерів
    msg = "🏆 ТОП ГРАВЦІВ:\n\n"
    msg += f"🥇 {u['name']} — {u['level']} Рівень | {u['lumis']} $LUMIS\n"
    msg += "\nСтань першим у списку!"
    
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    await call.message.edit_text(msg, reply_markup=kb)

# --- СІТІ ---
@dp.callback_query_handler(text="city")
async def city(call: types.CallbackQuery):
    u = get_user(call.from_user.id, call.from_user.first_name)
    await call.message.edit_text(
        f"🏙️ ТВОЄ МІСТО\n\n"
        f"👤 Холдерів: {u['holders']}\n"
        f"🏗️ Рівень розвитку: {u['level']}\n\n"
        f"Чим більше у тебе $LUMIS, тим швидше росте твоє Сіті!",
        reply_markup=main_kb()
    )

@dp.callback_query_handler(text="back")
async def back(call: types.CallbackQuery):
    await start(call.message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
  

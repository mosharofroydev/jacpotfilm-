import asyncio, random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from ads import ad_links
from database import init_db, search_movies

API_TOKEN = "8210471056:AAEc76RNEX1w32M7WfyY3R8uKzEBy4aOb8s"
CHANNEL_ID = -1002912984408  # চ্যানেল ID (number)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

init_db()

RESULTS_PER_PAGE = 5

def build_keyboard(results, page):
    start = page * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    keyboard = []

    for r in results[start:end]:
        keyboard.append([InlineKeyboardButton(text=r[1], callback_data=f"video_{r[2]}")])

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{page-1}"))
    if end < len(results):
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("👋 Welcome! মুভির নাম লিখে সার্চ করুন।")

user_search = {}  # store user's last search results

@dp.message()
async def search_handler(message: types.Message):
    query = message.text.strip()
    results = search_movies(query)
    if not results:
        await message.answer("❌ কোনো ভিডিও পাওয়া যায়নি।")
        return

    user_search[message.from_user.id] = results
    keyboard = build_keyboard(results, 0)
    msg = await message.answer("🔎 Search Result:", reply_markup=keyboard)

    # 2 মিনিট পরে delete
    await asyncio.sleep(120)
    try: await msg.delete()
    except: pass

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    data = callback.data
    uid = callback.from_user.id

    # Pagination
    if data.startswith("page_"):
        page = int(data.split("_")[1])
        results = user_search.get(uid, [])
        keyboard = build_keyboard(results, page)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer()
        return

    # Video copy
    if data.startswith("video_"):
        channel_message_id = int(data.split("_", 1)[1])

        ad = random.choice(ad_links)
        await bot.send_message(chat_id=uid, text=f"📢 {ad}")
        await asyncio.sleep(5)

        sent = await bot.copy_message(
            chat_id=uid,
            from_chat_id=CHANNEL_ID,
            message_id=channel_message_id,
            protect_content=True
        )

        # 6 দিন পরে auto delete
        await asyncio.sleep(518400)
        try: await bot.delete_message(uid, sent.message_id)
        except: pass

        await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

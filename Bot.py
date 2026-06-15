import asyncio
import random
import sqlite3
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions
import os

TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = "PRIME"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ========== БАЗА ДАННЫХ ==========
def init_db():
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, chat_id INTEGER, user_id INTEGER, 
                  username TEXT, text TEXT, date TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS warns
                 (user_id INTEGER, chat_id INTEGER, count INTEGER, 
                  reason TEXT, date TEXT, warned_by INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS rp_roles
                 (user_id INTEGER, chat_id INTEGER, level INTEGER DEFAULT 1,
                  PRIMARY KEY (user_id, chat_id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS user_join_date
                 (user_id INTEGER, chat_id INTEGER, join_date TEXT,
                  PRIMARY KEY (user_id, chat_id))""")
    conn.commit()
    conn.close()

async def save_message(chat_id, user_id, username, text):
    if not text or len(text) > 1000:
        return
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (chat_id, user_id, username, text, date) VALUES (?,?,?,?,?)",
              (chat_id, user_id, username, text[:500], datetime.now().isoformat()))
    conn.commit()
    conn.close()

async def save_join_date(user_id, chat_id):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO user_join_date (user_id, chat_id, join_date) VALUES (?,?,?)",
              (user_id, chat_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()

async def get_join_date(user_id, chat_id):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT join_date FROM user_join_date WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

async def get_role(user_id, chat_id):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT level FROM rp_roles WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 1

async def set_role(user_id, chat_id, level):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO rp_roles (user_id, chat_id, level) VALUES (?,?,?)", (user_id, chat_id, level))
    conn.commit()
    conn.close()

async def add_warn(user_id, chat_id, reason, warned_by):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM warns WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    count = c.fetchone()[0] + 1
    c.execute("INSERT INTO warns (user_id, chat_id, count, reason, date, warned_by) VALUES (?,?,?,?,?,?)",
              (user_id, chat_id, count, reason, datetime.now().isoformat(), warned_by))
    conn.commit()
    conn.close()
    
    if count >= 5:
        await bot.ban_chat_member(chat_id, user_id)
        return f"⚠️ {count}/5 варнов. Пользователь исключён."
    return f"⚠️ Предупреждение {count}/5: {reason}"

async def remove_warn(user_id, chat_id):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT count FROM warns WHERE user_id = ? AND chat_id = ? ORDER BY date DESC LIMIT 1", (user_id, chat_id))
    row = c.fetchone()
    if row:
        c.execute("DELETE FROM warns WHERE user_id = ? AND chat_id = ? AND count = ?", (user_id, chat_id, row[0]))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

async def get_user_message_count(chat_id, user_id):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages WHERE chat_id = ? AND user_id = ?", (chat_id, user_id))
    count = c.fetchone()[0]
    conn.close()
    return count

async def get_random_message(chat_id):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT text, username FROM messages WHERE chat_id = ? AND text != '' ORDER BY RANDOM() LIMIT 1", (chat_id,))
    row = c.fetchone()
    conn.close()
    if row and row[0]:
        return f"📖 {row[0]}\n— {row[1] or 'кто-то'}"
    return None

# ========== НОВЫЙ ПОЛЬЗОВАТЕЛЬ ==========
@dp.message(lambda message: message.new_chat_members)
async def on_user_join(message: types.Message):
    for user in message.new_chat_members:
        if user.id != bot.id:
            await save_join_date(user.id, message.chat.id)

# ========== АВТО-СООБЩЕНИЯ (РАНДОМНЫЕ ФРАЗЫ) ==========
active_chats = set()

async def auto_random_message(chat_id: int):
    while True:
        wait_time = random.choice([300, 600, 900])  # 5, 10 или 15 минут
        await asyncio.sleep(wait_time)
        phrase = await get_random_message(chat_id)
        if phrase:
            await bot.send_message(chat_id, phrase)

# ========== ОБРАБОТЧИК СООБЩЕНИЙ ==========
@dp.message()
async def catch_all(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        await save_message(message.chat.id, message.from_user.id, 
                          message.from_user.username, message.text)
        
        if message.chat.id not in active_chats:
            active_chats.add(message.chat.id)
            asyncio.create_task(auto_random_message(message.chat.id))

# ========== КОМАНДЫ ==========
@dp.message(Command("dice"))
async def cmd_dice(message: types.Message):
    value = random.randint(1, 6)
    await message.reply(f"🎲 Вам выпало: **{value}**")

@dp.message(Command("guess"))
async def cmd_guess(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.reply("ℹ️ /guess число (1-10)")
        return
    try:
        guess = int(args[1])
        if not 1 <= guess <= 10:
            raise ValueError
    except:
        await message.reply("⚠️ Введите число от 1 до 10.")
        return
    secret = random.randint(1, 10)
    if guess == secret:
        await message.reply(f"🎉 Угадали! Было число {secret}.")
    else:
        await message.reply(f"❌ Не угадали. Было число {secret}.")

@dp.message(Command("myrole"))
async def cmd_myrole(message: types.Message):
    level = await get_role(message.from_user.id, message.chat.id)
    await message.reply(f"🎭 Ваш РП-уровень в {BOT_NAME}: **{level}** из 10")

@dp.message(Command("rp_admins"))
async def cmd_rp_admins(message: types.Message):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT user_id, level FROM rp_roles WHERE chat_id = ? AND level >= 1 ORDER BY level DESC", (message.chat.id,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        await message.answer("🎭 РП-админов пока нет.")
        return
    text = f"👑 **РП-админы {BOT_NAME}:**\n"
    for uid, lvl in rows:
        try:
            member = await bot.get_chat_member(message.chat.id, uid)
            name = f"@{member.user.username}" if member.user.username else member.user.full_name
            text += f"⭐ Lv{lvl}: {name}\n"
        except:
            pass
    await message.answer(text)

@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    level = await get_role(message.from_user.id, message.chat.id)
    msg_count = await get_user_message_count(message.chat.id, message.from_user.id)
    join_date = await get_join_date(message.from_user.id, message.chat.id)
    
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM warns WHERE user_id = ? AND chat_id = ?", (message.from_user.id, message.chat.id))
    warn_count = c.fetchone()[0]
    conn.close()
    
    text = f"📊 **Профиль @{message.from_user.username or message.from_user.first_name}**\n"
    text += f"🎭 Уровень: {level}/10\n"
    text += f"💬 Сообщений: {msg_count}\n"
    text += f"⚠️ Варнов: {warn_count}/5\n"
    if join_date:
        text += f"📅 В чате с: {join_date[:10]}"
    await message.reply(text)

@dp.message(Command("top"))
async def cmd_top(message: types.Message):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT user_id, COUNT(*) as cnt FROM messages WHERE chat_id = ? GROUP BY user_id ORDER BY cnt DESC LIMIT 5", (message.chat.id,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        await message.reply("📭 Нет сообщений.")
        return
    text = f"🏆 **Топ активных в {BOT_NAME}:**\n"
    for i, (uid, cnt) in enumerate(rows, 1):
        try:
            member = await bot.get_chat_member(message.chat.id, uid)
            name = f"@{member.user.username}" if member.user.username else f"id{uid}"
            text += f"{i}. {name} — {cnt} сообщений\n"
        except:
            pass
    await message.answer(text)

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages WHERE chat_id = ?", (message.chat.id,))
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT user_id) FROM messages WHERE chat_id = ?", (message.chat.id,))
    users = c.fetchone()[0]
    conn.close()
    await message.reply(f"📊 **Статистика чата {BOT_NAME}:**\n💬 Сообщений: {total}\n👥 Участников писало: {users}")

@dp.message(Command("warns"))
async def cmd_warns(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 2:
        await message.reply("❌ Нужен 2+ уровень.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("ℹ️ /warns @username")
        return
    target = args[1].replace("@", "")
    try:
        member = await message.chat.get_member((await bot.get_chat_member(message.chat.id, target)).user.id)
        conn = sqlite3.connect("prime_bot.db")
        c = conn.cursor()
        c.execute("SELECT count, reason, date FROM warns WHERE user_id = ? AND chat_id = ? ORDER BY date DESC", (member.user.id, message.chat.id))
        warns = c.fetchall()
        conn.close()
        if not warns:
            await message.reply(f"✅ У @{target} нет варнов.")
            return
        text = f"⚠️ **Варны @{target}:**\n"
        for count, reason, date in warns[:5]:
            text += f"#{count}: {reason} ({date[:10]})\n"
        await message.answer(text)
    except:
        await message.reply("❌ Пользователь не найден.")

@dp.message(Command("slowmode"))
async def cmd_slowmode(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 3:
        await message.reply("❌ Нужен 3+ уровень.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("ℹ️ /slowmode <секунды>\n/slowmode 0 — выключить")
        return
    try:
        seconds = int(args[1])
        if seconds < 0:
            await message.reply("⚠️ Секунды не могут быть отрицательными.")
            return
        await bot.set_chat_slow_mode_delay(message.chat.id, seconds)
        if seconds == 0:
            await message.reply(f"✅ Медленный режим выключен.")
        else:
            await message.reply(f"🐢 Медленный режим: 1 сообщение в {seconds} секунд.")
    except:
        await message.reply("⚠️ /slowmode 5")

@dp.message(Command("warn"))
async def cmd_warn(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 4:
        await message.reply("❌ Нужен 4+ уровень.")
        return
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        await message.reply("ℹ️ /warn @username причина")
        return
    target = args[1].replace("@", "")
    reason = args[2] if len(args) > 2 else "Без причины"
    try:
        member = await message.chat.get_member((await bot.get_chat_member(message.chat.id, target)).user.id)
        if member.user.id == message.from_user.id:
            await message.reply("❌ Нельзя выдать варн самому себе.")
            return
        result = await add_warn(member.user.id, message.chat.id, reason, message.from_user.id)
        await message.reply(result)
    except:
        await message.reply("❌ Пользователь не найден.")

@dp.message(Command("unwarn"))
async def cmd_unwarn(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 5:
        await message.reply("❌ Нужен 5+ уровень.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("ℹ️ /unwarn @username")
        return
    target = args[1].replace("@", "")
    try:
        member = await message.chat.get_member((await bot.get_chat_member(message.chat.id, target)).user.id)
        if await remove_warn(member.user.id, message.chat.id):
            await message.reply(f"✅ Снят последний варн у @{target}.")
        else:
            await message.reply(f"✅ У @{target} нет варнов.")
    except:
        await message.reply("❌ Пользователь не найден.")

@dp.message(Command("mute"))
async def cmd_mute(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 6:
        await message.reply("❌ Нужен 6+ уровень.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("ℹ️ /mute @username")
        return
    target = args[1].replace("@", "")
    try:
        member = await message.chat.get_member((await bot.get_chat_member(message.chat.id, target)).user.id)
        await bot.restrict_chat_member(message.chat.id, member.user.id, 
                                       ChatPermissions(can_send_messages=False),
                                       until_date=datetime.now() + timedelta(minutes=5))
        await message.reply(f"🔇 @{target} замьючен на 5 минут.")
    except:
        await message.reply("❌ Ошибка.")

@dp.message(Command("unmute"))
async def cmd_unmute(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 6:
        await message.reply("❌ Нужен 6+ уровень.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("ℹ️ /unmute @username")
        return
    target = args[1].replace("@", "")
    try:
        member = await message.chat.get_member((await bot.get_chat_member(message.chat.id, target)).user.id)
        await bot.restrict_chat_member(message.chat.id, member.user.id, 
                                       ChatPermissions(can_send_messages=True, can_send_media_messages=True,
                                                      can_send_other_messages=True, can_add_web_page_previews=True))
        await message.reply(f"🔊 @{target} размьючен.")
    except:
        await message.reply("❌ Ошибка.")

@dp.message(Command("kick"))
async def cmd_kick(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 7:
        await message.reply("❌ Нужен 7+ уровень.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("ℹ️ /kick @username")
        return
    target = args[1].replace("@", "")
    try:
        member = await message.chat.get_member((await bot.get_chat_member(message.chat.id, target)).user.id)
        await bot.ban_chat_member(message.chat.id, member.user.id)
        await bot.unban_chat_member(message.chat.id, member.user.id)
        await message.reply(f"👢 @{target} кикнут.")
    except:
        await message.reply("❌ Ошибка.")

@dp.message(Command("ban"))
async def cmd_ban(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 8:
        await message.reply("❌ Нужен 8+ уровень.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("ℹ️ /ban @username")
        return
    target = args[1].replace("@", "")
    try:
        member = await message.chat.get_member((await bot.get_chat_member(message.chat.id, target)).user.id)
        await bot.ban_chat_member(message.chat.id, member.user.id)
        await message.reply(f"🚫 @{target} забанен.")
    except:
        await message.reply("❌ Ошибка.")

@dp.message(Command("unban"))
async def cmd_unban(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 8:
        await message.reply("❌ Нужен 8+ уровень.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("ℹ️ /unban @username")
        return
    target = args[1].replace("@", "")
    try:
        await bot.unban_chat_member(message.chat.id, target)
        await message.reply(f"✅ @{target} разбанен.")
    except:
        await message.reply("❌ Ошибка.")

@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 9:
        await message.reply("❌ Нужен 9+ уровень.")
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("ℹ️ /clear <количество>")
        return
    try:
        count = int(args[1])
        if count < 1 or count > 100:
            await message.reply("⚠️ От 1 до 100 сообщений.")
            return
        async for msg in message.chat.history(limit=count):
            await msg.delete()
        await message.reply(f"🗑️ Удалено {count} сообщений.")
    except:
        await message.reply("❌ Ошибка.")

@dp.message(Command("set_rp"))
async def cmd_set_rp(message: types.Message):
    if await get_role(message.from_user.id, message.chat.id) < 10:
        await message.reply("❌ Только 10 уровень назначает роли.")
        return
    args = message.text.split()
    if len(args) != 3:
        await message.reply("ℹ️ /set_rp @username уровень(1-10)")
        return
    target = args[1].replace("@", "")
    try:
        level = int(args[2])
        if not 1 <= level <= 10:
            raise ValueError
    except:
        await message.reply("⚠️ Уровень от 1 до 10.")
        return
    try:
        member = await message.chat.get_member((await bot.get_chat_member(message.chat.id, target)).user.id)
        await set_role(member.user.id, message.chat.id, level)
        await message.reply(f"✅ @{target} получил {level} уровень.")
    except:
        await message.reply("❌ Пользователь не найден.")

# ========== ЗАПУСК ==========
async def main():
    init_db()
    print(f"✅ {BOT_NAME} запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
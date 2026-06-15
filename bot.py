import asyncio
import random
import sqlite3
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
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
    c.execute("""CREATE TABLE IF NOT EXISTS duels
                 (chat_id INTEGER, challenger INTEGER, opponent INTEGER, turn INTEGER, aim_bonus INTEGER, message_id INTEGER)""")
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

async def get_name(user_id):
    try:
        user = await bot.get_chat(user_id)
        return f"@{user.username}" if user.username else f"id{user_id}"
    except:
        return f"id{user_id}"

# ========== ДУЭЛЬ ==========
active_duels = set()

async def duel_loop(chat_id, challenger, opponent, message_id):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO duels (chat_id, challenger, opponent, turn, aim_bonus, message_id) VALUES (?,?,?,?,?,?)",
              (chat_id, challenger, opponent, challenger, 0, message_id))
    conn.commit()
    conn.close()
    
    active_duels.add((chat_id, challenger, opponent))
    
    await update_duel_message(chat_id, message_id, challenger, opponent, 0, challenger)

async def update_duel_message(chat_id, message_id, challenger, opponent, aim_bonus, turn):
    turn_name = "Игрок 1" if turn == challenger else "Игрок 2"
    aim_text = f"🎯 Бонус прицела: +{aim_bonus*10}% к шансу" if aim_bonus > 0 else ""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔫 СТРЕЛЯТЬ", callback_data=f"duel_shoot_{chat_id}_{message_id}_{turn}"),
            InlineKeyboardButton(text="🎯 ПРИЦЕЛИТЬСЯ", callback_data=f"duel_aim_{chat_id}_{message_id}_{turn}")
        ],
        [
            InlineKeyboardButton(text="⏭️ ПРОПУСТИТЬ", callback_data=f"duel_skip_{chat_id}_{message_id}_{turn}")
        ]
    ])
    
    await bot.edit_message_text(
        text=f"🔫 **ДУЭЛЬ!**\n\n"
             f"⚔️ {await get_name(challenger)} против {await get_name(opponent)}\n"
             f"🎲 Ход: **{turn_name}**\n"
             f"{aim_text}\n\n"
             f"👇 Выбери действие:",
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def end_duel(chat_id, message_id, winner, loser, reason):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("DELETE FROM duels WHERE chat_id = ? AND message_id = ?", (chat_id, message_id))
    conn.commit()
    conn.close()
    
    active_duels.discard((chat_id, winner, loser))
    active_duels.discard((chat_id, loser, winner))
    
    await bot.edit_message_text(
        text=f"🔫 **ДУЭЛЬ ЗАВЕРШЕНА!**\n\n"
             f"🏆 Победитель: {await get_name(winner)}!\n"
             f"💀 {reason}\n\n"
             f"🎉 {await get_name(winner)} выиграл дуэль!",
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=None,
        parse_mode=ParseMode.MARKDOWN
    )

# ========== НОВЫЙ ПОЛЬЗОВАТЕЛЬ ==========
@dp.message(lambda message: message.new_chat_members)
async def on_user_join(message: types.Message):
    for user in message.new_chat_members:
        if user.id != bot.id:
            await save_join_date(user.id, message.chat.id)

# ========== АВТО-СООБЩЕНИЯ ==========
active_chats = set()

async def auto_random_message(chat_id: int):
    while True:
        wait_time = random.choice([300, 600, 900])
        await asyncio.sleep(wait_time)
        phrase = await get_random_message(chat_id)
        if phrase:
            await bot.send_message(chat_id, phrase)

# ========== ОСНОВНОЙ ОБРАБОТЧИК ==========
@dp.message()
async def catch_all(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        await save_message(message.chat.id, message.from_user.id, 
                          message.from_user.username, message.text)
        
        if message.chat.id not in active_chats:
            active_chats.add(message.chat.id)
            asyncio.create_task(auto_random_message(message.chat.id))

# ========== КОМАНДЫ БЕЗ СЛЕША ==========
@dp.message()
async def handle_text_commands(message: types.Message):
    if not message.text:
        return
    
    text = message.text.lower().strip()
    
    # ===== КУБЫ =====
    if text == "кубы":
        if message.reply_to_message:
            opponent_id = message.reply_to_message.from_user.id
            challenger_id = message.from_user.id
            
            if challenger_id == opponent_id:
                await message.reply("❌ Нельзя играть с самим собой!")
                return
            
            cube1 = random.randint(1, 6)
            cube2 = random.randint(1, 6)
            total1 = cube1 + cube2
            
            cube3 = random.randint(1, 6)
            cube4 = random.randint(1, 6)
            total2 = cube3 + cube4
            
            if total1 > total2:
                result_text = f"🏆 Победил {await get_name(challenger_id)}!"
            elif total2 > total1:
                result_text = f"🏆 Победил {await get_name(opponent_id)}!"
            else:
                result_text = "🤝 Ничья!"
            
            await message.reply(
                f"🎲 **Кубы-дуэль!**\n\n"
                f"{await get_name(challenger_id)}: {cube1} + {cube2} = **{total1}**\n"
                f"{await get_name(opponent_id)}: {cube3} + {cube4} = **{total2}**\n\n"
                f"{result_text}",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            cube1 = random.randint(1, 6)
            cube2 = random.randint(1, 6)
            total = cube1 + cube2
            await message.reply(f"🎲 {message.from_user.first_name} кидает кости...\nВыпало: **{cube1}** и **{cube2}** = **{total}**", parse_mode=ParseMode.MARKDOWN)
        return
    
    # ===== ОРЁЛ/РЕШКА =====
    if text in ["орёл", "орел", "решка"]:
        if message.reply_to_message:
            opponent_id = message.reply_to_message.from_user.id
            challenger_id = message.from_user.id
            
            if challenger_id == opponent_id:
                await message.reply("❌ Нельзя играть с самим собой!")
                return
            
            user_choice = "орёл" if text in ["орёл", "орел"] else "решка"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🪙 КИНУТЬ МОНЕТКУ", callback_data=f"coinflip_{message.chat.id}_{challenger_id}_{opponent_id}_{user_choice}")]
            ])
            
            await message.reply(f"🪙 **{await get_name(challenger_id)}** вызывает **{await get_name(opponent_id)}** на **Орёл/Решку**!\n\n"
                               f"🎲 {await get_name(challenger_id)} выбрал: **{user_choice}**\n\n"
                               f"👇 Нажми на кнопку, чтобы кинуть монетку:",
                               parse_mode=ParseMode.MARKDOWN,
                               reply_markup=keyboard)
        else:
            result = random.choice(["орёл", "решка"])
            user_choice = "орёл" if text in ["орёл", "орел"] else "решка"
            
            if user_choice == result:
                await message.reply(f"🪙 Монетка упала **{result}**!\n🎉 Ты угадал!")
            else:
                await message.reply(f"🪙 Монетка упала **{result}**!\n😭 Ты не угадал...")
        return
    
    # ===== КАМЕНЬ/НОЖНИЦЫ/БУМАГА =====
    if text == "кнб":
        if not message.reply_to_message:
            await message.reply("ℹ️ Чтобы сыграть в КНБ, ответь на сообщение противника и напиши **кнб**")
            return
        
        challenger_id = message.from_user.id
        opponent_id = message.reply_to_message.from_user.id
        
        if challenger_id == opponent_id:
            await message.reply("❌ Нельзя играть с самим собой!")
            return
        
        if (message.chat.id, challenger_id, opponent_id) in active_knb:
            await message.reply("⚠️ Игра с этим участником уже идёт!")
            return
        
        active_knb.add((message.chat.id, challenger_id, opponent_id))
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✊ КАМЕНЬ", callback_data=f"knb_{message.chat.id}_{challenger_id}_{opponent_id}_камень"),
                InlineKeyboardButton(text="✌️ НОЖНИЦЫ", callback_data=f"knb_{message.chat.id}_{challenger_id}_{opponent_id}_ножницы"),
                InlineKeyboardButton(text="✋ БУМАГА", callback_data=f"knb_{message.chat.id}_{challenger_id}_{opponent_id}_бумага")
            ]
        ])
        
        await message.reply(f"✊✌️✋ **{await get_name(challenger_id)}** вызывает **{await get_name(opponent_id)}** на **Камень/Ножницы/Бумага**!\n\n"
                           f"🎲 **{await get_name(challenger_id)}**, сделай свой выбор:",
                           parse_mode=ParseMode.MARKDOWN,
                           reply_markup=keyboard)
        return
    
    # ===== ДУЭЛЬ =====
    if text == "дуэль":
        if not message.reply_to_message:
            await message.reply("ℹ️ Чтобы вызвать на дуэль, ответь на сообщение противника и напиши **Дуэль**", parse_mode=ParseMode.MARKDOWN)
            return
        
        challenger_id = message.from_user.id
        opponent_id = message.reply_to_message.from_user.id
        
        if challenger_id == opponent_id:
            await message.reply("❌ Нельзя вызвать на дуэль самого себя!")
            return
        
        if (message.chat.id, challenger_id, opponent_id) in active_duels or (message.chat.id, opponent_id, challenger_id) in active_duels:
            await message.reply("⚠️ Дуэль с этим участником уже идёт!")
            return
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ НАЧАТЬ ДУЭЛЬ", callback_data=f"duel_accept_{message.chat.id}_{challenger_id}_{opponent_id}")]
        ])
        
        await message.reply(f"🔫 **{await get_name(challenger_id)}** вызывает на дуэль **{await get_name(opponent_id)}**!\n\n"
                           f"⚡ Для начала дуэли {await get_name(opponent_id)} нажми **✅ Начать дуэль**",
                           parse_mode=ParseMode.MARKDOWN,
                           reply_markup=keyboard)
        return

# ========== КОЛБЭКИ ==========
@dp.callback_query(lambda c: c.data.startswith("duel_accept_"))
async def duel_accept(callback: types.CallbackQuery):
    _, _, chat_id, challenger_id, opponent_id = callback.data.split("_")
    chat_id = int(chat_id)
    challenger_id = int(challenger_id)
    opponent_id = int(opponent_id)
    
    if callback.from_user.id != opponent_id:
        await callback.answer("❌ Только вызванный игрок может начать дуэль!", show_alert=True)
        return
    
    await callback.message.delete()
    
    duel_msg = await bot.send_message(chat_id, "🔫 **Дуэль начинается!**\n⏳ Подготовка...")
    await duel_loop(chat_id, challenger_id, opponent_id, duel_msg.message_id)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("duel_shoot_"))
async def duel_shoot(callback: types.CallbackQuery):
    _, _, chat_id, message_id, turn_id = callback.data.split("_")
    chat_id = int(chat_id)
    message_id = int(message_id)
    turn_id = int(turn_id)
    
    if callback.from_user.id != turn_id:
        await callback.answer("❌ Сейчас не твой ход!", show_alert=True)
        return
    
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT challenger, opponent, aim_bonus FROM duels WHERE chat_id = ? AND message_id = ?", (chat_id, message_id))
    row = c.fetchone()
    conn.close()
    
    if not row:
        await callback.answer("❌ Дуэль уже завершена!", show_alert=True)
        return
    
    challenger, opponent, aim_bonus = row
    
    chance = 50 + (aim_bonus * 10)
    shot = random.randint(1, 100)
    hit = shot <= chance
    
    if hit:
        winner = callback.from_user.id
        loser = challenger if winner == opponent else opponent
        await end_duel(chat_id, message_id, winner, loser, f"💥 Точный выстрел! Попадание! ({shot}% vs {chance}%)")
    else:
        await callback.answer(f"💨 Промах! Шанс попадания был {chance}%, выпало {shot}%", show_alert=True)
        
        new_turn = challenger if callback.from_user.id == opponent else opponent
        conn = sqlite3.connect("prime_bot.db")
        c = conn.cursor()
        c.execute("UPDATE duels SET turn = ?, aim_bonus = 0 WHERE chat_id = ? AND message_id = ?", (new_turn, chat_id, message_id))
        conn.commit()
        conn.close()
        
        await update_duel_message(chat_id, message_id, challenger, opponent, 0, new_turn)
    
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("duel_aim_"))
async def duel_aim(callback: types.CallbackQuery):
    _, _, chat_id, message_id, turn_id = callback.data.split("_")
    chat_id = int(chat_id)
    message_id = int(message_id)
    turn_id = int(turn_id)
    
    if callback.from_user.id != turn_id:
        await callback.answer("❌ Сейчас не твой ход!", show_alert=True)
        return
    
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT challenger, opponent, aim_bonus FROM duels WHERE chat_id = ? AND message_id = ?", (chat_id, message_id))
    row = c.fetchone()
    conn.close()
    
    if not row:
        await callback.answer("❌ Дуэль уже завершена!", show_alert=True)
        return
    
    challenger, opponent, aim_bonus = row
    
    if aim_bonus >= 2:
        await callback.answer("❌ Нельзя прицеливаться больше 2 раз подряд!", show_alert=True)
        return
    
    new_aim_bonus = aim_bonus + 1
    new_turn = challenger if callback.from_user.id == opponent else opponent
    
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("UPDATE duels SET turn = ?, aim_bonus = ? WHERE chat_id = ? AND message_id = ?", (new_turn, new_aim_bonus, chat_id, message_id))
    conn.commit()
    conn.close()
    
    await callback.answer(f"🎯 Ты прицелился! Шанс следующего выстрела +{new_aim_bonus*10}%", show_alert=True)
    await update_duel_message(chat_id, message_id, challenger, opponent, new_aim_bonus, new_turn)

@dp.callback_query(lambda c: c.data.startswith("duel_skip_"))
async def duel_skip(callback: types.CallbackQuery):
    _, _, chat_id, message_id, turn_id = callback.data.split("_")
    chat_id = int(chat_id)
    message_id = int(message_id)
    turn_id = int(turn_id)
    
    if callback.from_user.id != turn_id:
        await callback.answer("❌ Сейчас не твой ход!", show_alert=True)
        return
    
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT challenger, opponent FROM duels WHERE chat_id = ? AND message_id = ?", (chat_id, message_id))
    row = c.fetchone()
    conn.close()
    
    if not row:
        await callback.answer("❌ Дуэль уже завершена!", show_alert=True)
        return
    
    challenger, opponent = row
    
    new_turn = challenger if callback.from_user.id == opponent else opponent
    
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("UPDATE duels SET turn = ?, aim_bonus = 0 WHERE chat_id = ? AND message_id = ?", (new_turn, chat_id, message_id))
    conn.commit()
    conn.close()
    
    await callback.answer("⏭️ Ты пропустил ход!", show_alert=True)
    await update_duel_message(chat_id, message_id, challenger, opponent, 0, new_turn)

@dp.callback_query(lambda c: c.data.startswith("coinflip_"))
async def coinflip_result(callback: types.CallbackQuery):
    _, _, chat_id, challenger_id, opponent_id, user_choice = callback.data.split("_")
    chat_id = int(chat_id)
    challenger_id = int(challenger_id)
    opponent_id = int(opponent_id)
    
    if callback.from_user.id != opponent_id:
        await callback.answer("❌ Кинуть монетку может только вызванный игрок!", show_alert=True)
        return
    
    result = random.choice(["орёл", "решка"])
    
    if result == user_choice:
        winner = challenger_id
        text = f"🏆 Победил: {await get_name(winner)}!\n🪙 Монетка упала **{result}**, {await get_name(winner)} угадал!"
    else:
        winner = opponent_id
        text = f"🏆 Победил: {await get_name(winner)}!\n🪙 Монетка упала **{result}**, {await get_name(winner)} не угадал (и выиграл)!"
    
    await callback.message.edit_text(
        text=f"🪙 **Результат игры в Орёл/Решку:**\n\n"
             f"📌 {await get_name(challenger_id)} выбрал: **{user_choice}**\n\n"
             f"{text}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=None
    )
    
    await callback.answer()

# ========== КНБ ==========
active_knb = set()
knb_choices = {}

def get_knb_result(choice1, choice2):
    if choice1 == choice2:
        return "Ничья!"
    
    wins = {
        "камень": "ножницы",
        "ножницы": "бумага",
        "бумага": "камень"
    }
    
    if wins[choice1] == choice2:
        return "🎉 Победил игрок 1!"
    else:
        return "🎉 Победил игрок 2!"

@dp.callback_query(lambda c: c.data.startswith("knb_"))
async def knb_choice(callback: types.CallbackQuery):
    _, chat_id, player1, player2, choice = callback.data.split("_")
    chat_id = int(chat_id)
    player1 = int(player1)
    player2 = int(player2)
    
    user_id = callback.from_user.id
    
    if user_id != player1 and user_id != player2:
        await callback.answer("❌ Это не твоя игра!", show_alert=True)
        return
    
    game_key = (chat_id, player1, player2)
    
    if game_key not in active_knb:
        await callback.answer("❌ Игра уже завершена!", show_alert=True)
        return
    
    if user_id == player1:
        knb_choices[(chat_id, player1)] = choice
        await callback.answer(f"✅ Ты выбрал: {choice}")
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✊ КАМЕНЬ", callback_data=f"knb_{chat_id}_{player1}_{player2}_камень"),
                InlineKeyboardButton(text="✌️ НОЖНИЦЫ", callback_data=f"knb_{chat_id}_{player1}_{player2}_ножницы"),
                InlineKeyboardButton(text="✋ БУМАГА", callback_data=f"knb_{chat_id}_{player1}_{player2}_бумага")
            ]
        ])
        
        await callback.message.edit_text(
            text=f"✊✌️✋ **{await get_name(player1)}** вызывает **{await get_name(player2)}** на **Камень/Ножницы/Бумага**!\n\n"
                 f"🎲 **{await get_name(player2)}**, теперь твой выбор:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard
        )
    else:
        knb_choices[(chat_id, player2)] = choice
        await callback.answer(f"✅ Ты выбрал: {choice}")
        
        choice1 = knb_choices.get((chat_id, player1))
        choice2 = choice
        
        result = get_knb_result(choice1, choice2)
        
        if "Победил игрок 1" in result:
            winner = player1
            result_text = f"🏆 Победил: {await get_name(winner)}!\n{result}"
        elif "Победил игрок 2" in result:
            winner = player2
            result_text = f"🏆 Победил: {await get_name(winner)}!\n{result}"
        else:
            result_text = f"🤝 {result}"
        
        await callback.message.edit_text(
            text=f"✊✌️✋ **Результат игры:**\n\n"
                 f"📌 {await get_name(player1)} выбрал: **{choice1}**\n"
                 f"📌 {await get_name(player2)} выбрал: **{choice2}**\n\n"
                 f"{result_text}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=None
        )
        
        active_knb.discard(game_key)
        knb_choices.pop((chat_id, player1), None)
        knb_choices.pop((chat_id, player2), None)

# ========== КОМАНДЫ СО СЛЕШЕМ ==========
@dp.message(Command("кубы"))
async def cmd_cubes(message: types.Message):
    if message.reply_to_message:
        opponent_id = message.reply_to_message.from_user.id
        challenger_id = message.from_user.id
        
        if challenger_id == opponent_id:
            await message.reply("❌ Нельзя играть с самим собой!")
            return
        
        cube1 = random.randint(1, 6)
        cube2 = random.randint(1, 6)
        total1 = cube1 + cube2
        
        cube3 = random.randint(1, 6)
        cube4 = random.randint(1, 6)
        total2 = cube3 + cube4
        
        if total1 > total2:
            result_text = f"🏆 Победил {await get_name(challenger_id)}!"
        elif total2 > total1:
            result_text = f"🏆 Победил {await get_name(opponent_id)}!"
        else:
            result_text = "🤝 Ничья!"
        
        await message.reply(
            f"🎲 **Кубы-дуэль!**\n\n"
            f"{await get_name(challenger_id)}: {cube1} + {cube2} = **{total1}**\n"
            f"{await get_name(opponent_id)}: {cube3} + {cube4} = **{total2}**\n\n"
            f"{result_text}",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        cube1 = random.randint(1, 6)
        cube2 = random.randint(1, 6)
        total = cube1 + cube2
        await message.reply(f"🎲 {message.from_user.first_name} кидает кости...\nВыпало: **{cube1}** и **{cube2}** = **{total}**", parse_mode=ParseMode.MARKDOWN)

@dp.message(Command("myrole"))
async def cmd_myrole(message: types.Message):
    level = await get_role(message.from_user.id, message.chat.id)
    await message.reply(f"🎭 Ваш РП-уровень в {BOT_NAME}: **{level}** из 10", parse_mode=ParseMode.MARKDOWN)

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
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

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
    await message.reply(text, parse_mode=ParseMode.MARKDOWN)

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
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    conn = sqlite3.connect("prime_bot.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages WHERE chat_id = ?", (message.chat.id,))
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT user_id) FROM messages WHERE chat_id = ?", (message.chat.id,))
    users = c.fetchone()[0]
    conn.close()
    await message.reply(f"📊 **Статистика чата {BOT_NAME}:**\n💬 Сообщений: {total}\n👥 Участников писало: {users}", parse_mode=ParseMode.MARKDOWN)

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
        await message.answer(text, parse_mode=ParseMode.MARKDOWN)
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
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = "PRIME"

bot = Bot(token=TOKEN)
dp = Dispatcher()

print(f"🚀 Бот {BOT_NAME} запускается...")

@dp.message(Command("start"))
async def start(message: types.Message):
    print(f"📩 Получена команда /start от {message.from_user.id}")
    await message.reply(f"✅ Бот {BOT_NAME} работает!")

@dp.message()
async def echo(message: types.Message):
    print(f"📩 Сообщение: {message.text}")
    if message.text.lower() == "кубы":
        await message.reply("🎲 Кубы работают! 4 и 3 = 7")

async def main():
    print("🔄 Удаляю вебхук...")
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Вебхук удалён")
    print("🏁 Запускаю поллинг...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("🌟 Точка входа")
    asyncio.run(main())
# ===== ОРЁЛ/РЕШКА =====
@dp.message()
async def handle_coinflip(message: types.Message):
    if not message.text:
        return
    
    text = message.text.lower().strip()
    
    if text in ["орёл", "орел", "решка"]:
        result = random.choice(["орёл", "решка"])
        user_choice = "орёл" if text in ["орёл", "орел"] else "решка"
        
        if user_choice == result:
            await message.reply(f"🪙 Монетка упала **{result}**!\n🎉 Ты угадал! +1 к удаче")
        else:
            await message.reply(f"🪙 Монетка упала **{result}**!\n😭 Ты не угадал...")
        return
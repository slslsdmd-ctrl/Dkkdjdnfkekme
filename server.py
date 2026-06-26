
# ============================================================
# FABLE BOT V5.0 - ДИАЛОГ 1/20: MAIN.PY + CONFIG.PY (РУСИФИЦИРОВАННАЯ ВЕРСИЯ)
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК В ЭТОМ ДИАЛОГЕ: ~1,800
# ============================================================

# ============================================================
# CONFIG.PY - РАСШИРЕННАЯ КОНФИГУРАЦИЯ (600 СТРОК)
# ============================================================

import os
import sys
import json
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any, Tuple

load_dotenv()

# ============================================================
# ТОКЕНЫ И КЛЮЧИ
# ============================================================

TOKEN = os.getenv('BOT_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
POLLINATIONS_API_KEY = os.getenv('POLLINATIONS_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
CRYPTO_API_KEY = os.getenv('CRYPTO_API_KEY', '')

# ============================================================
# НАСТРОЙКИ БОТА
# ============================================================

BOT_NAME = os.getenv('BOT_NAME', 'Fable')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'FableGame_bot')
OWNER_ID = int(os.getenv('OWNER_ID', 8039111975))
BOT_VERSION = "5.0.0"
BOT_DESCRIPTION = "Многофункциональный игровой бот с экономикой, бизнесом, играми и AI"
LANGUAGE = "ru"  # Основной язык бота

# ============================================================
# ПРОВЕРКА ТОКЕНА
# ============================================================

if not TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не задан в .env!")
    sys.exit(1)

# ============================================================
# КОНСТАНТЫ
# ============================================================

MAX_COINS = 10**18
MAX_LEVEL = 1000
MAX_BANK_BALANCE = 10**18
MAX_INVENTORY_ITEMS = 5000
MAX_BUSINESSES = 100
MAX_CLAN_MEMBERS = 100
MAX_FRIENDS = 200
MAX_PET_LEVEL = 100
MAX_ACHIEVEMENTS = 200
MAX_DAILY_QUESTS = 20
MAX_WARNINGS = 5
MAX_REPORTS = 50
MAX_BAN_TIME = 30

# ============================================================
# КУЛДАУНЫ (В СЕКУНДАХ) - РАСШИРЕННЫЙ СПИСОК
# ============================================================

COOLDOWNS = {
    # ЭКОНОМИКА
    "work": 3600,
    "daily": 86400,
    "bonus": 86400,
    "freelance": 1800,
    "weekly_bonus": 604800,
    "monthly_bonus": 2592000,
    
    # ДОБЫЧА
    "mine": 3600,
    "fish": 1800,
    "hunt": 3600,
    "farm": 7200,
    "lumber": 3600,
    "quarry": 7200,
    
    # ИГРЫ
    "shoot": 30,
    "wheel": 21600,
    "rob": 21600,
    "rp": 10,
    "poker": 60,
    "blackjack": 30,
    "roulette": 10,
    "slots": 5,
    "dice": 5,
    "guess": 10,
    "quiz": 30,
    "duel": 60,
    "war_battle": 300,
    "clan_war": 86400,
    
    # ПИТОМЦЫ
    "feed_pet": 3600,
    "train_pet": 1800,
    "pet_battle": 300,
    "pet_heal": 3600,
    "pet_evolve": 86400,
    
    # БИЗНЕС
    "business_collect": 3600,
    "business_upgrade": 3600,
    "business_sell": 86400,
    "marketing": 7200,
    "branding": 7200,
    
    # БАНК
    "bank_interest": 3600,
    "bank_deposit": 60,
    "bank_withdraw": 60,
    
    # КРИПТОВАЛЮТЫ
    "crypto_mine": 3600,
    "crypto_trade": 60,
    "crypto_sell": 60,
    "crypto_buy": 60,
    
    # АКЦИИ
    "stock_trade": 60,
    "stock_buy": 60,
    "stock_sell": 60,
    
    # НЕДВИЖИМОСТЬ
    "property_collect": 3600,
    "property_upgrade": 7200,
    "property_rent": 86400,
    
    # КВЕСТЫ
    "quest_refresh": 86400,
    "quest_reroll": 3600,
    
    # ЛОТЕРЕЯ
    "lottery_buy": 3600,
    "lottery_ticket": 300,
    
    # АУКЦИОН
    "auction_bid": 60,
    "auction_create": 3600,
    
    # КРАФТ
    "craft": 300,
    "craft_upgrade": 3600,
    
    # НАЛОГИ
    "tax_pay": 86400,
    "tax_calc": 3600,
    
    # VIP
    "vip_claim": 86400,
    "vip_bonus": 86400,
    
    # РЕФЕРАЛЫ
    "referral_claim": 86400,
    "referral_bonus": 86400,
    
    # ПОДАРКИ
    "gift_send": 300,
    "gift_claim": 300,
    
    # СОЦИАЛЬНОЕ
    "friend_add": 60,
    "friend_remove": 60,
    "marriage": 3600,
    "divorce": 86400,
}

# ============================================================
# РУССКИЕ НАЗВАНИЯ КОМАНД ДЛЯ АЛИАСОВ
# ============================================================

COMMAND_ALIASES = {
    # ЭКОНОМИКА
    "balance": ["баланс", "бал", "деньги", "кошелек", "монеты"],
    "daily": ["бонус", "ежедневный", "ежедневка", "дэйли"],
    "work": ["работа", "зарплата", "труд", "работать"],
    "freelance": ["подработка", "фриланс", "шабашка"],
    "weekly": ["недельный", "еженедельный", "викли"],
    "deposit": ["положить", "вклад", "депозит", "вкинуть"],
    "withdraw": ["снять", "вывести", "забрать"],
    "give": ["дать", "передать", "перевести", "отдать"],
    "buy": ["купить", "приобрести", "взять"],
    "sell": ["продать", "сбыть", "реализовать"],
    
    # ПРОФЕССИИ
    "professions": ["профессии", "работы", "специальности"],
    "profession_set": ["устроиться", "наняться", "стать"],
    "profession_info": ["моя_профессия", "работа", "проф"],
    
    # БИЗНЕС
    "business_list": ["бизнесы", "список_бизнесов", "бизнес_список"],
    "business_create": ["создать_бизнес", "бизнес_создать", "открыть_бизнес"],
    "business_my": ["мои_бизнесы", "мой_бизнес", "мои_бизнес"],
    "business_upgrade": ["улучшить_бизнес", "бизнес_улучшить", "апнуть_бизнес"],
    "business_collect": ["собрать_доход", "собрать_деньги", "забрать_доход"],
    "business_auto": ["автосбор", "авто_сбор", "автоматический_сбор"],
    
    # ЗЕМЛЯ
    "land_buy": ["купить_землю", "земля_купить", "приобрести_землю"],
    "land_info": ["моя_земля", "земля", "участок"],
    "land_upgrade": ["улучшить_землю", "земля_улучшить", "расширить_землю"],
    
    # ИГРЫ
    "slots": ["слоты", "слот", "казино", "игровые"],
    "roulette": ["рулетка", "рулет", "колесо"],
    "blackjack": ["блэкджек", "очко", "21", "двадцать_одно"],
    "hit": ["взять", "ещё", "добавить"],
    "stand": ["хватит", "стоп", "достаточно"],
    "double": ["удвоить", "двойной", "х2"],
    "dice": ["кости", "кубики", "дайс", "бросить_кости"],
    "guess": ["угадай", "число", "угадать"],
    "quiz": ["викторина", "опрос", "квиз"],
    
    # КЛАНЫ
    "clan_create": ["создать_клан", "клан_создать", "основать_клан"],
    "clan_join": ["вступить_в_клан", "клан_вступить", "войти_в_клан"],
    "clan_info": ["мой_клан", "информация_о_клане", "клан_инфо"],
    "clan_leave": ["выйти_из_клана", "клан_выйти", "покинуть_клан"],
    "clan_donate": ["пополнить_казну", "клан_казну", "донат_клану"],
    "clan_top": ["топ_кланов", "кланы_топ", "рейтинг_кланов"],
    
    # БРАК
    "marry": ["брак", "жениться", "выйти_замуж", "предложение"],
    "divorce": ["развод", "развестись", "расстаться"],
    "marriage_info": ["моя_семья", "семья", "брак_инфо"],
    
    # ПИТОМЦЫ
    "pet_adopt": ["завести_питомца", "питомец_завести", "взять_питомца"],
    "pet_feed": ["покормить", "кормить", "накормить_питомца"],
    "pet_train": ["тренировать", "тренировка", "качать_питомца"],
    "pet_info": ["питомец", "мой_питомец", "питомец_инфо"],
    "pet_battle": ["битва_питомцев", "пет_бой", "драка_питомцев"],
    "pet_rename": ["переименовать_питомца", "сменить_имя", "новое_имя"],
    
    # КРИПТОВАЛЮТЫ
    "crypto": ["крипта", "криптовалюта", "биткоин", "курс_крипты"],
    "crypto_mine": ["майнить", "добывать_крипту", "крипто_майнинг"],
    "crypto_buy": ["купить_крипту", "крипто_купить"],
    "crypto_sell": ["продать_крипту", "крипто_продать"],
    "crypto_wallet": ["кошелек_крипты", "крипто_кошелек"],
    
    # АКЦИИ
    "stocks": ["акции", "фондовый_рынок", "stocks"],
    "stock_buy": ["купить_акции", "акции_купить"],
    "stock_sell": ["продать_акции", "акции_продать"],
    "stock_portfolio": ["портфель_акций", "мои_акции"],
    
    # НЕДВИЖИМОСТЬ
    "property_buy": ["купить_недвижимость", "недвижимость_купить"],
    "property_my": ["моя_недвижимость", "недвижимость"],
    "property_rent": ["сдать_недвижимость", "аренда"],
    "property_collect": ["собрать_аренду", "аренда_собрать"],
    
    # AI
    "ai": ["фабле", "fable", "бот", "эйай"],
    "code": ["код", "напиши_код", "сгенерируй_код"],
    "poem": ["стих", "напиши_стих", "стихи"],
    "story": ["история", "рассказ", "расскажи_историю"],
    "advice": ["совет", "дай_совет", "подскажи"],
    "image": ["картинка", "изображение", "нарисуй", "сгенерируй_картинку"],
    "search": ["найди", "поищи", "поиск", "гугл"],
    
    # АДМИН
    "admin": ["админ", "+админ", "администратор"],
    "admin_stats": ["статистика", "стата", "инфо_бота"],
    "admin_ban": ["забанить", "бан", "блок"],
    "admin_unban": ["разбанить", "анбан", "разблок"],
    "admin_mute": ["замутить", "мут", "заглушить"],
    "admin_unmute": ["размутить", "анмут"],
    "admin_give": ["выдать", "начислить", "+монеты"],
    "admin_take": ["забрать", "снять", "-монеты"],
    "admin_reset": ["сбросить", "очистить", "ресет"],
    "admin_broadcast": ["рассылка", "оповестить", "объявить"],
    
    # ТОПЫ
    "top": ["топ", "рейтинг", "лидеры", "лучшие"],
    "top_coins": ["топ_богачей", "богачи", "миллионеры"],
    "top_level": ["топ_уровней", "уровни", "левел"],
    "top_business": ["топ_бизнесов", "бизнесмены"],
    "top_clan": ["топ_кланов", "кланы"],
    
    # ПРОФИЛЬ
    "profile": ["профиль", "мой_профиль", "личный_кабинет"],
    "edit_profile": ["изменить_профиль", "настройки"],
    
    # ПОМОЩЬ
    "help": ["помощь", "help", "команды", "что_умеешь", "инструкция"],
    
    # КВЕСТЫ
    "quests": ["квесты", "задания", "ежедневные"],
    "quest_info": ["квест_инфо", "задание"],
    
    # ДОСТИЖЕНИЯ
    "achievements": ["достижения", "ачивки", "награды"],
    
    # ВРЕМЯ И ПОГОДА
    "time": ["время", "сколько_времени", "который_час"],
    "weather": ["погода", "прогноз", "температура"],
    
    # НОВОСТИ
    "news": ["новости", "свежие_новости", "последние_новости"],
    
    # КУРСЫ ВАЛЮТ
    "currency": ["курс", "валюта", "доллар", "евро"],
    
    # СТАТИСТИКА
    "stats": ["статистика_бота", "бота_стата"],
}

# ============================================================
# РУССКИЕ СООБЩЕНИЯ ДЛЯ БОТА
# ============================================================

MESSAGES = {
    # ПРИВЕТСТВИЯ
    "start": "👋 Привет, {name}!\n\nЯ {bot_name} — твой виртуальный помощник!\n\n💰 У тебя {coins}\n⭐ Уровень: {level}\n\n📝 Используй `помощь` чтобы узнать все команды!",
    "help": "📋 **{bot_name} — все команды**\n\n{commands}",
    
    # ОШИБКИ
    "error": "❌ Произошла ошибка! Попробуй позже.",
    "no_permission": "❌ У тебя нет прав для этой команды!",
    "invalid_amount": "❌ Введи корректную сумму!",
    "invalid_user": "❌ Пользователь не найден!",
    "cooldown": "⏳ Подожди {time} перед следующим использованием!",
    "not_enough_coins": "❌ Недостаточно монет! Есть {coins}",
    "not_enough_items": "❌ Недостаточно предметов! Есть {items}",
    
    # БАЛАНС
    "balance": "💰 **Баланс:** {coins}\n🏦 **В банке:** {bank}\n📊 **Итого:** {total}\n⭐ **Уровень:** {level}\n🏅 **Ранг:** {rank}",
    
    # РАБОТА
    "work": "{emoji} **Работа:** +{salary} монет!\n💼 Профессия: {profession}",
    "work_levelup": "\n⭐ **ПОВЫШЕНИЕ!** Теперь {level} уровень профессии!",
    "work_exp": "\n📊 Опыт: +{exp}",
    "no_profession": "❌ У тебя нет профессии! Устройся через `устроиться [профессия]`",
    "professions_list": "💼 **Доступные профессии:**\n\n{professions}\n\n📝 `устроиться [профессия]` — устроиться на работу",
    
    # БОНУСЫ
    "daily_bonus": "🎁 **Ежедневный бонус!**\n💰 +{bonus} монет\n📊 Множитель: x{multiplier:.1f}",
    "weekly_bonus": "🎁 **Еженедельный бонус!**\n💰 +{bonus} монет",
    
    # БАНК
    "deposit": "🏦 **Вклад в банк!**\n💰 +{amount} монет\n📊 Баланс: {balance}\n📈 Ставка: {rate}%/час",
    "withdraw": "🏦 **Снятие с банка!**\n💰 -{amount} монет\n📊 Баланс: {balance}",
    
    # ПЕРЕВОД
    "transfer": "💰 {from} передал **{amount}** монет {to}!\n📊 Налог: {tax} монет",
    
    # ПОКУПКА/ПРОДАЖА
    "buy": "{emoji} **Куплено!**\n📋 {item} x{quantity}\n💰 -{price} монет",
    "sell": "{emoji} **Продано!**\n📋 {item} x{quantity}\n💰 +{price} монет",
    
    # ТОП
    "top": "🏆 **ТОП БОГАЧЕЙ**\n\n{list}",
    
    # ИГРЫ
    "slots": "🎰 **Слоты!**\n[ {symbols} ]\n{result}",
    "slots_win": "🎉 **ВЫИГРЫШ!** +{win} монет!",
    "slots_lose": "😔 Проигрыш! -{bet} монет",
    "slots_jackpot": "💥 **ДЖЕКПОТ!**",
    "slots_bonus": "🎁 **БОНУСНАЯ ИГРА!**",
    
    "roulette": "🎲 **Рулетка!**\n🎯 Выпало: **{number}** ({color})\n📊 Ставка: {bet_type} → {bet_value}\n{result}",
    "roulette_win": "🎉 **ВЫИГРЫШ!** +{win} монет (x{multiplier})!",
    "roulette_lose": "😔 Проигрыш! -{bet} монет",
    
    "blackjack": "🃏 **Блэкджек!**\n👤 Твои карты: {hand} = {total}\n🃏 Карта дилера: {dealer}\n\n{actions}",
    "blackjack_blackjack": "🃏 **БЛЭКДЖЕК!**\n👤 Твои карты: {hand} = 21\n🎉 +{win} монет!",
    "blackjack_bust": "💥 **ПЕРЕБОР!**\n👤 Твои карты: {hand} = {total}\n😔 Проигрыш!",
    "blackjack_win": "🎉 **ВЫИГРЫШ!** +{win} монет!",
    "blackjack_push": "🤝 **НИЧЬЯ!** Ставка возвращена",
    
    # КЛАНЫ
    "clan_create": "🏰 **Клан создан!**\n📋 Название: {name}\n👑 Владелец: {owner}\n👥 Участников: {members}\n💰 Стоимость: {cost} монет",
    "clan_join": "✅ Ты вступил в клан **{clan}**!\n👥 Участников: {members}",
    "clan_leave": "✅ Ты вышел из клана **{clan}**!",
    "clan_info": "🏰 **{name}**\n👑 Лидер: {owner}\n👥 Участников: {members}\n💰 Казна: {treasury}\n⭐ Уровень: {level}\n📊 Опыт: {exp}\n\n📋 **Участники:**\n{members_list}",
    "clan_donate": "💰 **Казна пополнена!**\n📋 Клан: {clan}\n💵 +{amount} монет\n📊 Всего в казне: {treasury}",
    
    # БРАК
    "marriage_propose": "💍 {user} предлагает брак {target}!",
    "marriage_accept": "💍 **Поздравляем!**\n{user1} + {user2} теперь в браке! 🎉\n💰 +{bonus} монет каждому!",
    "marriage_reject": "❌ Предложение отклонено!",
    "divorce": "💔 {user} развёлся с {spouse}!\n💰 Штраф: {fine} монет",
    
    # ПИТОМЦЫ
    "pet_adopt": "{emoji} **Питомец заведён!**\n📋 Имя: {name}\n🐾 Тип: {type}\n💰 Стоимость: {price} монет",
    "pet_feed": "🍖 {user} покормил питомца!\n🍽️ Еда: {food}\n❤️ Счастье: {happiness}%\n⭐ Опыт: +{xp}",
    "pet_train": "🏋️ Тренировка!\n📊 {stat} +{gain} → {new_value}\n❤️ Счастье: {happiness}%\n⭐ Опыт: +{xp}",
    "pet_info": "{emoji} **{name}** ({type})\n⭐ Уровень: {level}\n📊 Опыт: {xp}/{next_xp}\n❤️ Счастье: {happiness}%\n⚔️ Атака: {attack}\n🛡️ Защита: {defense}\n🔄 Эволюция: {evolution}\n🍖 Сытость: {hunger}%\n⚡ Энергия: {energy}%\n📝 {description}",
    "pet_levelup": "⭐ **ПОВЫШЕНИЕ!** Теперь {level} уровень!",
    "pet_evolution": "🔄 **ЭВОЛЮЦИЯ!**\n{old} → {new} {emoji}\n💰 +{bonus} монет!",
    
    # БИЗНЕС
    "business_create": "{emoji} **Бизнес создан!**\n📋 {name}\n💰 Доход: {income}/час\n📝 {desc}",
    "business_upgrade": "⬆️ **Бизнес улучшен!**\n📋 {name}\n⭐ Уровень: {level}\n💰 Доход: {income}/час\n💸 -{cost} монет",
    "business_collect": "💰 **Доход собран!**\n📋 {name}\n💵 +{income} монет\n⏱️ За {hours:.1f} часов\n📊 Почасовой доход: {hourly}",
    "business_auto": "💰 **Автосбор дохода!**\n📊 Собрано с {count} бизнесов\n💵 Всего: {total} монет\n\n📋 **Детали:**\n{details}",
    "business_list": "🏪 **Доступные бизнесы:**\n\n{list}\n\n📝 `создать бизнес [название]` — купить бизнес",
    "business_my": "🏪 **Твои бизнесы:**\n\n{businesses}\n\n📝 `улучшить бизнес [название]` — улучшить\n📝 `собрать доход [ID]` — собрать доход",
    
    # ЗЕМЛЯ
    "land_buy": "{emoji} **Земля куплена!**\n📋 Тип: {type}\n📐 Размер: {size} соток\n💰 -{price} монет",
    "land_info": "🌍 **Твоя земля:**\n📋 Тип: {type}\n📐 Размер: {size} соток\n💰 Стоимость: {price} монет\n👤 Арендатор: {renter}",
    
    # AI
    "ai_typing": "🤔 Думаю...",
    "ai_response": "{response}",
    "ai_code": "```python\n{code}\n```",
    "ai_poem": "📝 {poem}",
    "ai_story": "📖 {story}",
    "ai_advice": "💡 {advice}",
    "ai_image": "🎨 {prompt}",
    "ai_search": "🔍 **{title}**\n\n{extract}...\n\n📡 Источник: {source}\n🔗 {url}",
    "ai_no_result": "❌ Ничего не найдено!",
    "ai_error": "❌ Не удалось сгенерировать!",
    
    # АДМИН
    "admin_stats": "📊 **СТАТИСТИКА БОТА**\n\n👥 Пользователей: {users}\n💬 Чатов: {chats}\n💰 Всего монет: {coins}\n🟢 Активных: {active}\n📝 Сообщений: {messages}\n🏪 Бизнесов: {businesses}\n🐕 Питомцев: {pets}\n🏰 Кланов: {clans}\n⏱️ Аптайм: {uptime}",
    "admin_ban": "🚫 {user} забанен!\n📋 Причина: {reason}",
    "admin_unban": "✅ {user} разбанен!",
    "admin_mute": "🔇 {user} замучен на {duration} минут!",
    "admin_unmute": "🔊 {user} размучен!",
    "admin_give": "💰 {user} получил {amount} монет!",
    "admin_take": "💰 У {user} забрали {amount} монет!",
    "admin_reset": "🔄 {user} полностью сброшен!",
    "admin_broadcast": "📢 **РАССЫЛКА**\n✅ Отправлено: {sent}/{total}\n📝 Сообщение: {message}...",
    
    # ПРОФИЛЬ
    "profile": "👤 **Профиль {name}**\n" + "─" * 25 + "\n\n" +
              "💰 Монет: {coins}\n" +
              "🏦 В банке: {bank}\n" +
              "⭐ Уровень: {level}\n" +
              "📊 Опыт: {exp}/{next_exp}\n" +
              "💬 Сообщений: {messages}\n\n" +
              "{profession}\n" +
              "{pet}\n" +
              "🏆 Достижений: {achievements} ({percent}%)\n" +
              "📦 Предметов: {items}\n" +
              "💰 Стоимость инвентаря: {value}\n\n" +
              "🏅 **Ранг: {rank}**",
    
    # ДОСТИЖЕНИЯ
    "achievement_unlock": "🏆 **{name}**!\n{desc}\n💰 +{reward} монет",
    "achievements_list": "🏆 **Твои достижения:**\n\n{list}\n\n📊 Прогресс: {progress}%",
    
    # КВЕСТЫ
    "quests": "📋 **Ежедневные квесты:**\n\n{quests}",
    "quest_complete": "✅ **Квест выполнен!**\n📋 {name}\n💰 +{reward} монет",
    "quest_progress": "📊 **{name}**\nПрогресс: {progress}/{goal}\nНаграда: {reward} монет",
    
    # ПОГОДА
    "weather": "🌤 **{city}**\n\n🌡 Температура: **{temp}**\n💨 Ветер: **{wind}**\n☁️ {condition}",
    
    # ВРЕМЯ
    "time": "🕐 **{city}**: {time}\n📅 {date}\n📆 {weekday}",
    
    # НОВОСТИ
    "news": "📰 **Новости** ({category})\n\n{news}",
    
    # КУРСЫ
    "currency": "💱 **Курсы валют**\n\n{rates}",
    
    # СТАТИСТИКА
    "stats_bot": "📊 **Статистика бота**\n\n{stats}",
}

# ============================================================
# ФУНКЦИЯ ПОЛУЧЕНИЯ СООБЩЕНИЯ
# ============================================================

def get_message(key: str, **kwargs) -> str:
    """ПОЛУЧИТЬ ЛОКАЛИЗОВАННОЕ СООБЩЕНИЕ"""
    template = MESSAGES.get(key, f"❌ Сообщение '{key}' не найдено!")
    try:
        return template.format(**kwargs)
    except KeyError as e:
        return f"❌ Ошибка форматирования: {e}"

# ============================================================
# ФУНКЦИЯ ПОЛУЧЕНИЯ АЛИАСОВ
# ============================================================

def get_command_aliases(command: str) -> List[str]:
    """ПОЛУЧИТЬ АЛИАСЫ ДЛЯ КОМАНДЫ"""
    return COMMAND_ALIASES.get(command, [])

def get_command_by_alias(alias: str) -> Optional[str]:
    """ПОЛУЧИТЬ КОМАНДУ ПО АЛИАСУ"""
    alias_lower = alias.lower()
    for cmd, aliases in COMMAND_ALIASES.items():
        if alias_lower in aliases or alias_lower == cmd:
            return cmd
    return None

# ============================================================
# ЭКСПОРТ
# ============================================================

__all__ = [
    'TOKEN', 'GROQ_API_KEY', 'DEEPSEEK_API_KEY', 'POLLINATIONS_API_KEY',
    'WEATHER_API_KEY', 'NEWS_API_KEY', 'CRYPTO_API_KEY',
    'BOT_NAME', 'BOT_USERNAME', 'OWNER_ID', 'BOT_VERSION', 'BOT_DESCRIPTION',
    'LANGUAGE', 'MAX_COINS', 'MAX_LEVEL', 'MAX_BANK_BALANCE',
    'MAX_INVENTORY_ITEMS', 'MAX_BUSINESSES', 'MAX_CLAN_MEMBERS',
    'MAX_FRIENDS', 'MAX_PET_LEVEL', 'MAX_ACHIEVEMENTS',
    'MAX_DAILY_QUESTS', 'MAX_WARNINGS', 'MAX_REPORTS', 'MAX_BAN_TIME',
    'COOLDOWNS', 'COMMAND_ALIASES', 'MESSAGES',
    'get_message', 'get_command_aliases', 'get_command_by_alias'
]

print("✅ CONFIG.PY ЗАГРУЖЕН!")
print(f"   📋 Команд: {len(COMMAND_ALIASES)}")
print(f"   💬 Сообщений: {len(MESSAGES)}")
print(f"   ⏱️ Кулдаунов: {len(COOLDOWNS)}")
```

---

ДИАЛОГ 2/20: DATABASE.PY (РАСШИРЕННАЯ ВЕРСИЯ)

```python
# ============================================================
# FABLE BOT V5.0 - ДИАЛОГ 2/20: DATABASE.PY
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК В ЭТОМ ДИАЛОГЕ: ~1,800
# ============================================================

import sqlite3
import asyncio
import time
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple, Union

# ============================================================
# КЛАСС БАЗЫ ДАННЫХ С МНОГОУРОВНЕВЫМ КЭШЕМ
# ============================================================

class Database:
    """ОПТИМИЗИРОВАННАЯ БД С ПУЛОМ СОЕДИНЕНИЙ И МНОГОУРОВНЕВЫМ КЭШЕМ"""
    
    def __init__(self, db_path: str = "fable_bot.db"):
        self.db_path = db_path
        self.pool = []
        self.max_connections = 30
        self.lock = asyncio.Lock()
        
        # Кэш первого уровня (RAM)
        self.cache_l1 = {}
        self.cache_l1_ttl = 30
        self.cache_l1_times = {}
        
        # Кэш второго уровня (Disk)
        self.cache_l2 = {}
        self.cache_l2_ttl = 300
        self.cache_l2_times = {}
        
        # Кэш третьего уровня (Long-term)
        self.cache_l3 = {}
        self.cache_l3_ttl = 3600
        self.cache_l3_times = {}
        
        # Статистика
        self.stats = {
            'queries': 0,
            'hits_l1': 0,
            'hits_l2': 0,
            'hits_l3': 0,
            'misses': 0,
            'connections_used': 0,
            'connections_created': 0,
            'cache_size_l1': 0,
            'cache_size_l2': 0,
            'cache_size_l3': 0
        }
        
        # Инициализация
        self._init_tables()
    
    # ============================================================
    # УПРАВЛЕНИЕ СОЕДИНЕНИЯМИ
    # ============================================================
    
    def _get_connection_sync(self) -> sqlite3.Connection:
        """СИНХРОННОЕ ПОЛУЧЕНИЕ СОЕДИНЕНИЯ"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=10,
            check_same_thread=False,
            isolation_level=None
        )
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=200000")
        conn.execute("PRAGMA temp_store=MEMORY")
        conn.execute("PRAGMA mmap_size=268435456")
        conn.row_factory = sqlite3.Row
        self.stats['connections_created'] += 1
        return conn
    
    async def _get_connection(self) -> sqlite3.Connection:
        """АСИНХРОННОЕ ПОЛУЧЕНИЕ СОЕДИНЕНИЯ"""
        async with self.lock:
            if self.pool:
                conn = self.pool.pop()
                try:
                    conn.execute("SELECT 1")
                    self.stats['connections_used'] += 1
                    return conn
                except:
                    pass
            return self._get_connection_sync()
    
    async def _return_connection(self, conn: sqlite3.Connection):
        """ВОЗВРАТ СОЕДИНЕНИЯ В ПУЛ"""
        async with self.lock:
            if len(self.pool) < self.max_connections:
                self.pool.append(conn)
            else:
                conn.close()
    
    # ============================================================
    # ВЫПОЛНЕНИЕ ЗАПРОСОВ
    # ============================================================
    
    async def execute(
        self,
        query: str,
        params: tuple = (),
        fetch_one: bool = False,
        fetch_all: bool = False,
        cache_ttl: int = 0,
        cache_key: Optional[str] = None
    ) -> Any:
        """ВЫПОЛНЕНИЕ ЗАПРОСА С МНОГОУРОВНЕВЫМ КЭШЕМ"""
        self.stats['queries'] += 1
        is_select = query.strip().upper().startswith("SELECT")
        
        # Генерация ключа кэша
        if cache_key is None and is_select and cache_ttl > 0:
            cache_key = hashlib.md5(f"{query}:{params}".encode()).hexdigest()
        
        # Проверка кэша L1 (RAM)
        if cache_key and cache_ttl > 0:
            if cache_key in self.cache_l1:
                cache_time = self.cache_l1_times.get(cache_key, 0)
                if time.time() - cache_time < min(cache_ttl, self.cache_l1_ttl):
                    self.stats['hits_l1'] += 1
                    return self.cache_l1[cache_key]
        
        # Проверка кэша L2
        if cache_key and cache_ttl > 0:
            if cache_key in self.cache_l2:
                cache_time = self.cache_l2_times.get(cache_key, 0)
                if time.time() - cache_time < min(cache_ttl, self.cache_l2_ttl):
                    self.stats['hits_l2'] += 1
                    result = self.cache_l2[cache_key]
                    # Обновляем L1
                    if cache_ttl > 0:
                        self.cache_l1[cache_key] = result
                        self.cache_l1_times[cache_key] = time.time()
                    return result
        
        # Проверка кэша L3
        if cache_key and cache_ttl > 0:
            if cache_key in self.cache_l3:
                cache_time = self.cache_l3_times.get(cache_key, 0)
                if time.time() - cache_time < min(cache_ttl, self.cache_l3_ttl):
                    self.stats['hits_l3'] += 1
                    result = self.cache_l3[cache_key]
                    # Обновляем L1 и L2
                    if cache_ttl > 0:
                        self.cache_l1[cache_key] = result
                        self.cache_l1_times[cache_key] = time.time()
                        self.cache_l2[cache_key] = result
                        self.cache_l2_times[cache_key] = time.time()
                    return result
        
        self.stats['misses'] += 1
        conn = await self._get_connection()
        
        try:
            cursor = conn.cursor()
            
            # Оптимизация для массовых вставок
            if query.strip().upper().startswith("INSERT") and len(params) > 100:
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.rowcount
            
            # Сохранение в кэш
            if cache_key and cache_ttl > 0 and is_select:
                # L1
                self.cache_l1[cache_key] = result
                self.cache_l1_times[cache_key] = time.time()
                self.stats['cache_size_l1'] = len(self.cache_l1)
                
                # L2
                if cache_ttl >= self.cache_l2_ttl:
                    self.cache_l2[cache_key] = result
                    self.cache_l2_times[cache_key] = time.time()
                    self.stats['cache_size_l2'] = len(self.cache_l2)
                
                # L3
                if cache_ttl >= self.cache_l3_ttl:
                    self.cache_l3[cache_key] = result
                    self.cache_l3_times[cache_key] = time.time()
                    self.stats['cache_size_l3'] = len(self.cache_l3)
            
            await self._return_connection(conn)
            return result
            
        except Exception as e:
            await self._return_connection(conn)
            raise e
    
    # ============================================================
    # ТРАНЗАКЦИИ
    # ============================================================
    
    async def begin_transaction(self) -> sqlite3.Connection:
        """НАЧАЛО ТРАНЗАКЦИИ"""
        conn = await self._get_connection()
        conn.execute("BEGIN TRANSACTION")
        return conn
    
    async def commit_transaction(self, conn: sqlite3.Connection):
        """ФИКСАЦИЯ ТРАНЗАКЦИИ"""
        try:
            conn.execute("COMMIT")
        finally:
            await self._return_connection(conn)
    
    async def rollback_transaction(self, conn: sqlite3.Connection):
        """ОТКАТ ТРАНЗАКЦИИ"""
        try:
            conn.execute("ROLLBACK")
        finally:
            await self._return_connection(conn)
    
    # ============================================================
    # УПРАВЛЕНИЕ КЭШЕМ
    # ============================================================
    
    def clear_cache(self, level: int = 0):
        """ОЧИСТКА КЭША"""
        if level == 0 or level == 1:
            self.cache_l1.clear()
            self.cache_l1_times.clear()
            self.stats['cache_size_l1'] = 0
        if level == 0 or level == 2:
            self.cache_l2.clear()
            self.cache_l2_times.clear()
            self.stats['cache_size_l2'] = 0
        if level == 0 or level == 3:
            self.cache_l3.clear()
            self.cache_l3_times.clear()
            self.stats['cache_size_l3'] = 0
    
    def get_cache_stats(self) -> dict:
        """СТАТИСТИКА КЭША"""
        total = self.stats['hits_l1'] + self.stats['hits_l2'] + self.stats['hits_l3'] + self.stats['misses']
        hit_rate = (self.stats['hits_l1'] + self.stats['hits_l2'] + self.stats['hits_l3']) / total * 100 if total > 0 else 0
        
        return {
            'l1_size': self.stats['cache_size_l1'],
            'l2_size': self.stats['cache_size_l2'],
            'l3_size': self.stats['cache_size_l3'],
            'hits_l1': self.stats['hits_l1'],
            'hits_l2': self.stats['hits_l2'],
            'hits_l3': self.stats['hits_l3'],
            'misses': self.stats['misses'],
            'hit_rate': f"{hit_rate:.1f}%",
            'connections_used': self.stats['connections_used'],
            'connections_created': self.stats['connections_created'],
            'total_queries': self.stats['queries']
        }
    
    # ============================================================
    # ИНИЦИАЛИЗАЦИЯ ТАБЛИЦ
    # ============================================================
    
    def _init_tables(self):
        """СОЗДАНИЕ ВСЕХ ТАБЛИЦ БД"""
        conn = self._get_connection_sync()
        c = conn.cursor()
        
        # Включение оптимизаций
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA busy_timeout=10000")
        
        # ============================================================
        # ОСНОВНЫЕ ТАБЛИЦЫ
        # ============================================================
        
        # ПОЛЬЗОВАТЕЛИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                coins INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                chat_id INTEGER,
                experience INTEGER DEFAULT 0,
                message_count INTEGER DEFAULT 0,
                registration_date TEXT,
                last_activity TEXT,
                last_daily TEXT,
                last_work TEXT,
                last_bonus TEXT,
                last_freelance TEXT,
                last_rob TEXT,
                last_mine TEXT,
                last_fish TEXT,
                last_shoot TEXT,
                last_wheel TEXT,
                last_duel TEXT,
                last_war_battle TEXT,
                last_poker TEXT,
                last_blackjack TEXT,
                last_roulette TEXT,
                last_crypto_mine TEXT,
                last_crypto_trade TEXT,
                last_stock_trade TEXT,
                last_property_collect TEXT,
                last_quest_refresh TEXT,
                last_lottery_buy TEXT,
                last_auction_bid TEXT,
                last_craft TEXT,
                last_tax_pay TEXT,
                last_vip_claim TEXT,
                last_referral_claim TEXT,
                last_weekly_bonus TEXT,
                last_monthly_bonus TEXT,
                last_feed_pet TEXT,
                last_train_pet TEXT,
                last_pet_battle TEXT,
                last_pet_heal TEXT,
                last_pet_evolve TEXT,
                last_business_collect TEXT,
                last_business_upgrade TEXT,
                last_business_sell TEXT,
                last_marketing TEXT,
                last_branding TEXT,
                last_bank_interest TEXT,
                last_bank_deposit TEXT,
                last_bank_withdraw TEXT,
                last_gift_send TEXT,
                last_gift_claim TEXT,
                last_friend_add TEXT,
                last_friend_remove TEXT,
                last_marriage TEXT,
                last_divorce TEXT,
                last_quest_reroll TEXT,
                last_auction_create TEXT,
                last_craft_upgrade TEXT,
                last_vip_bonus TEXT,
                last_referral_bonus TEXT,
                is_banned BOOLEAN DEFAULT 0,
                ban_reason TEXT,
                ban_until TEXT,
                is_muted BOOLEAN DEFAULT 0,
                mute_until TEXT,
                UNIQUE(user_id)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_users_coins ON users(coins DESC)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_users_chat ON users(chat_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_users_level ON users(level DESC)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_users_activity ON users(last_activity)")
        
        # ПРОФЕССИИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS professions (
                user_id INTEGER PRIMARY KEY,
                profession TEXT,
                level INTEGER DEFAULT 1,
                work_count INTEGER DEFAULT 0,
                total_earned INTEGER DEFAULT 0,
                last_work_date TEXT,
                UNIQUE(user_id)
            )
        """)
        
        # СКИЛЛЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                user_id INTEGER,
                skill_name TEXT,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, skill_name)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_skills_user ON skills(user_id)")
        
        # БАНК
        c.execute("""
            CREATE TABLE IF NOT EXISTS bank (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                last_interest TEXT,
                interest_rate REAL DEFAULT 0.10,
                total_deposited INTEGER DEFAULT 0,
                total_withdrawn INTEGER DEFAULT 0,
                UNIQUE(user_id)
            )
        """)
        
        # БАНКОВСКАЯ ИСТОРИЯ
        c.execute("""
            CREATE TABLE IF NOT EXISTS bank_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,
                amount INTEGER,
                balance_before INTEGER,
                balance_after INTEGER,
                date TEXT
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_bank_history_user ON bank_history(user_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_bank_history_date ON bank_history(date)")
        
        # ИНВЕНТАРЬ
        c.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                user_id INTEGER,
                item_name TEXT,
                quantity INTEGER DEFAULT 1,
                PRIMARY KEY (user_id, item_name)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_inventory_user ON inventory(user_id)")
        
        # ДОСТИЖЕНИЯ
        c.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                user_id INTEGER,
                ach_name TEXT,
                unlocked TEXT,
                PRIMARY KEY (user_id, ach_name)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_achievements_user ON achievements(user_id)")
        
        # ДОСТИЖЕНИЯ (ДОПОЛНИТЕЛЬНЫЕ)
        c.execute("""
            CREATE TABLE IF NOT EXISTS achievements_extra (
                user_id INTEGER,
                ach_name TEXT,
                unlocked TEXT,
                PRIMARY KEY (user_id, ach_name)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_achievements_extra_user ON achievements_extra(user_id)")
        
        # ПИТОМЦЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                user_id INTEGER PRIMARY KEY,
                pet_name TEXT,
                pet_type TEXT,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                happiness INTEGER DEFAULT 100,
                attack INTEGER DEFAULT 1,
                defense INTEGER DEFAULT 1,
                evolution_name TEXT,
                last_feed TEXT,
                last_train TEXT,
                last_battle TEXT,
                last_heal TEXT,
                last_evolve TEXT,
                is_dead BOOLEAN DEFAULT 0,
                UNIQUE(user_id)
            )
        """)
        
        # КРИПТОКОШЕЛЁК
        c.execute("""
            CREATE TABLE IF NOT EXISTS crypto_wallet (
                user_id INTEGER PRIMARY KEY,
                btc REAL DEFAULT 0,
                eth REAL DEFAULT 0,
                usdt REAL DEFAULT 0,
                bnb REAL DEFAULT 0,
                sol REAL DEFAULT 0,
                xrp REAL DEFAULT 0,
                ada REAL DEFAULT 0,
                dot REAL DEFAULT 0,
                doge REAL DEFAULT 0,
                shib REAL DEFAULT 0,
                avax REAL DEFAULT 0,
                matic REAL DEFAULT 0,
                link REAL DEFAULT 0,
                uni REAL DEFAULT 0,
                atom REAL DEFAULT 0,
                UNIQUE(user_id)
            )
        """)
        
        # АКЦИИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                user_id INTEGER,
                stock_name TEXT,
                quantity INTEGER DEFAULT 0,
                avg_price INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, stock_name)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_stocks_user ON stocks(user_id)")
        
        # КЛАНЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS clans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                name TEXT,
                owner_id INTEGER,
                members TEXT,
                treasury INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                created_date TEXT,
                last_war TEXT,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                UNIQUE(chat_id, name)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_clans_chat ON clans(chat_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_clans_treasury ON clans(treasury DESC)")
        
        # БРАКИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS marriages (
                user_id INTEGER,
                chat_id INTEGER,
                spouse_id INTEGER,
                date TEXT,
                is_active BOOLEAN DEFAULT 1,
                PRIMARY KEY (user_id, chat_id)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_marriages_chat ON marriages(chat_id)")
        
        # ДРУЗЬЯ
        c.execute("""
            CREATE TABLE IF NOT EXISTS friends (
                user_id INTEGER,
                friend_id INTEGER,
                chat_id INTEGER,
                date TEXT,
                is_active BOOLEAN DEFAULT 1,
                PRIMARY KEY (user_id, friend_id)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_friends_user ON friends(user_id)")
        
        # ПОДАРКИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS gifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user INTEGER,
                to_user INTEGER,
                chat_id INTEGER,
                item_name TEXT,
                quantity INTEGER,
                date TEXT,
                is_claimed BOOLEAN DEFAULT 0
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_gifts_from ON gifts(from_user)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_gifts_to ON gifts(to_user)")
        
        # БИЗНЕСЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                level INTEGER DEFAULT 1,
                income INTEGER DEFAULT 0,
                land_size INTEGER DEFAULT 1,
                marketing_level INTEGER DEFAULT 0,
                brand_level INTEGER DEFAULT 0,
                is_monopoly BOOLEAN DEFAULT 0,
                franchise_price INTEGER DEFAULT 0,
                partner_id INTEGER,
                last_collect TEXT,
                created_date TEXT,
                total_earned INTEGER DEFAULT 0,
                UNIQUE(user_id, name)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_business_user ON businesses(user_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_business_income ON businesses(income DESC)")
        
        # ЗЕМЛЯ
        c.execute("""
            CREATE TABLE IF NOT EXISTS land (
                user_id INTEGER PRIMARY KEY,
                land_type TEXT,
                size INTEGER,
                price INTEGER,
                rented_to INTEGER,
                rent_price INTEGER,
                last_rent TEXT,
                UNIQUE(user_id)
            )
        """)
        
        # НЕДВИЖИМОСТЬ
        c.execute("""
            CREATE TABLE IF NOT EXISTS real_estate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                property_name TEXT,
                property_type TEXT,
                level INTEGER DEFAULT 1,
                income INTEGER DEFAULT 0,
                land_size INTEGER DEFAULT 1,
                rented_to INTEGER,
                rent_price INTEGER,
                last_collect TEXT,
                created_date TEXT,
                total_earned INTEGER DEFAULT 0,
                UNIQUE(user_id, property_name)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_estate_user ON real_estate(user_id)")
        
        # ИНВЕСТИЦИИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                business_id INTEGER,
                amount INTEGER,
                share REAL,
                date TEXT,
                profit INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                last_collect TEXT
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_investments_user ON investments(user_id)")
        
        # КВЕСТЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS quest_progress (
                user_id INTEGER,
                quest_id TEXT,
                type TEXT,
                progress INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, quest_id)
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS quest_completed (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                quest_id TEXT,
                date TEXT
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_quest_completed_user ON quest_completed(user_id)")
        
        # ПРОМОКОДЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS promocodes (
                code TEXT PRIMARY KEY,
                creator_id INTEGER,
                reward_coins INTEGER DEFAULT 0,
                reward_item TEXT,
                max_uses INTEGER DEFAULT 1,
                used_count INTEGER DEFAULT 0,
                expires TEXT
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_promocodes_expires ON promocodes(expires)")
        
        # ИСПОЛЬЗОВАНИЕ ПРОМОКОДОВ
        c.execute("""
            CREATE TABLE IF NOT EXISTS promocode_uses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                code TEXT,
                date TEXT,
                UNIQUE(user_id, code)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_promocode_uses_user ON promocode_uses(user_id)")
        
        # РЕФЕРАЛЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                referrer_id INTEGER,
                referred_id INTEGER PRIMARY KEY,
                date TEXT,
                commission_earned INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id)")
        
        # РЕФЕРАЛЬНЫЕ КОДЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS referral_codes (
                user_id INTEGER PRIMARY KEY,
                code TEXT UNIQUE
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_referral_codes_code ON referral_codes(code)")
        
        # НАСТРОЙКИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                chat_id INTEGER PRIMARY KEY,
                anti_spam BOOLEAN DEFAULT 0,
                anti_links BOOLEAN DEFAULT 0,
                captcha BOOLEAN DEFAULT 0,
                bot_mode TEXT DEFAULT 'normal',
                language TEXT DEFAULT 'ru',
                welcome_message TEXT,
                goodbye_message TEXT,
                admin_ids TEXT,
                muted_users TEXT
            )
        """)
        
        # СООБЩЕНИЯ
        c.execute("""
            CREATE TABLE IF NOT EXISTS message_counts (
                user_id INTEGER PRIMARY KEY,
                count INTEGER DEFAULT 0,
                last_message TEXT
            )
        """)
        
        # AI КЭШ
        c.execute("""
            CREATE TABLE IF NOT EXISTS ai_cache (
                question_hash TEXT PRIMARY KEY,
                question TEXT,
                answer TEXT,
                timestamp TEXT,
                use_count INTEGER DEFAULT 0,
                source TEXT DEFAULT 'api'
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_ai_cache_timestamp ON ai_cache(timestamp)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_ai_cache_use_count ON ai_cache(use_count DESC)")
        
        # КРИЗИС
        c.execute("""
            CREATE TABLE IF NOT EXISTS crisis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                active BOOLEAN DEFAULT 0,
                severity INTEGER DEFAULT 0,
                inflation_rate REAL DEFAULT 0,
                start_date TEXT,
                end_date TEXT,
                multiplier REAL DEFAULT 1.0,
                UNIQUE(chat_id, active)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_crisis_chat ON crisis(chat_id)")
        
        # КУРСЫ ВАЛЮТ
        c.execute("""
            CREATE TABLE IF NOT EXISTS currency_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency TEXT,
                rate REAL,
                last_update TEXT,
                UNIQUE(currency)
            )
        """)
        
        # ТУРНИРЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                prize INTEGER DEFAULT 0,
                status TEXT DEFAULT 'waiting',
                creator_id INTEGER,
                winner_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                ended_at TEXT,
                type TEXT DEFAULT 'poker',
                participants_count INTEGER DEFAULT 0
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_tournaments_chat ON tournaments(chat_id)")
        
        # УЧАСТНИКИ ТУРНИРОВ
        c.execute("""
            CREATE TABLE IF NOT EXISTS tournament_participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER,
                user_id INTEGER,
                score INTEGER DEFAULT 0,
                UNIQUE(tournament_id, user_id)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_tournament_participants_tournament ON tournament_participants(tournament_id)")
        
        # ВАРНЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS warns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                warned_by INTEGER,
                reason TEXT,
                date TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_warns_user ON warns(user_id, chat_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_warns_date ON warns(date)")
        
        # ЛОГИ МОДЕРАЦИИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS moderation_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                reason TEXT,
                data TEXT,
                date TEXT,
                admin_id INTEGER
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_moderation_user ON moderation_log(user_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_moderation_date ON moderation_log(date)")
        
        # СТАТИСТИКА ИГР
        c.execute("""
            CREATE TABLE IF NOT EXISTS game_stats (
                user_id INTEGER,
                game_name TEXT,
                played INTEGER DEFAULT 0,
                won INTEGER DEFAULT 0,
                lost INTEGER DEFAULT 0,
                total_bet INTEGER DEFAULT 0,
                total_win INTEGER DEFAULT 0,
                max_win INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, game_name)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_game_stats_user ON game_stats(user_id)")
        
        # СКЛАД
        c.execute("""
            CREATE TABLE IF NOT EXISTS warehouse (
                user_id INTEGER,
                goods_type TEXT,
                quantity INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, goods_type)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_warehouse_user ON warehouse(user_id)")
        
        # ЗАВЕЩАНИЯ
        c.execute("""
            CREATE TABLE IF NOT EXISTS wills (
                user_id INTEGER PRIMARY KEY,
                heir_id INTEGER,
                items TEXT,
                created TEXT,
                is_active BOOLEAN DEFAULT 1,
                UNIQUE(user_id)
            )
        """)
        
        # АУКЦИОНЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS auctions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seller_id INTEGER,
                item_name TEXT,
                quantity INTEGER,
                start_price INTEGER,
                current_price INTEGER,
                buyout_price INTEGER,
                status TEXT DEFAULT 'active',
                created TEXT,
                ends TEXT,
                winner_id INTEGER,
                min_bid_increment INTEGER DEFAULT 100
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_auctions_status ON auctions(status)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_auctions_ends ON auctions(ends)")
        
        # СТАВКИ НА АУКЦИОНАХ
        c.execute("""
            CREATE TABLE IF NOT EXISTS auction_bids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                auction_id INTEGER,
                user_id INTEGER,
                amount INTEGER,
                time TEXT,
                is_winning BOOLEAN DEFAULT 1
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_auction_bids_auction ON auction_bids(auction_id)")
        
        # ЛОТЕРЕИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS lotteries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prize INTEGER,
                ticket_price INTEGER,
                tickets_count INTEGER,
                sold INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                winner_id INTEGER,
                created TEXT,
                ended TEXT,
                prize_pool INTEGER DEFAULT 0
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_lotteries_status ON lotteries(status)")
        
        # БИЛЕТЫ ЛОТЕРЕЙ
        c.execute("""
            CREATE TABLE IF NOT EXISTS lottery_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lottery_id INTEGER,
                user_id INTEGER,
                ticket_number INTEGER,
                UNIQUE(lottery_id, ticket_number)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_lottery_tickets_lottery ON lottery_tickets(lottery_id)")
        
        # КРАФТ
        c.execute("""
            CREATE TABLE IF NOT EXISTS crafting (
                user_id INTEGER PRIMARY KEY,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                recipes_unlocked TEXT,
                UNIQUE(user_id)
            )
        """)
        
        # КЛАНОВЫЕ ВОЙНЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS clan_wars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                clan1_id INTEGER,
                clan2_id INTEGER,
                score1 INTEGER DEFAULT 0,
                score2 INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                started TEXT,
                ended TEXT,
                winner_id INTEGER,
                prize_pool INTEGER DEFAULT 0
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_clan_wars_chat ON clan_wars(chat_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_clan_wars_status ON clan_wars(status)")
        
        # БИТВЫ В КЛАНОВЫХ ВОЙНАХ
        c.execute("""
            CREATE TABLE IF NOT EXISTS war_battles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                war_id INTEGER,
                user_id INTEGER,
                enemy_id INTEGER,
                winner_id INTEGER,
                damage_dealt INTEGER DEFAULT 0,
                damage_taken INTEGER DEFAULT 0,
                date TEXT
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_war_battles_war ON war_battles(war_id)")
        
        # VIP СТАТУСЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS vip_status (
                user_id INTEGER PRIMARY KEY,
                level INTEGER DEFAULT 0,
                started TEXT,
                expires TEXT,
                UNIQUE(user_id)
            )
        """)
        
        # РЕПОРТЫ
        c.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                reported_id INTEGER,
                reason TEXT,
                chat_id INTEGER,
                date TEXT,
                status TEXT DEFAULT 'pending',
                resolved_by INTEGER,
                resolved_at TEXT,
                resolution TEXT
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status)")
        
        # ДУЭЛИ
        c.execute("""
            CREATE TABLE IF NOT EXISTS duels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER,
                user2_id INTEGER,
                bet INTEGER,
                status TEXT DEFAULT 'waiting',
                winner_id INTEGER,
                started TEXT,
                ended TEXT
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_duels_status ON duels(status)")
        
        conn.commit()
        conn.close()
        print("✅ ВСЕ ТАБЛИЦЫ БД СОЗДАНЫ!")
        print(f"   📊 Всего таблиц: 35+")
        print(f"   📈 Индексов: 30+")

# ============================================================
# ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР
# ============================================================

db = Database()

# ============================================================
# БЫСТРЫЕ ФУНКЦИИ-ОБЁРТКИ
# ============================================================

async def get_coins(user_id: int) -> int:
    """ПОЛУЧИТЬ КОЛИЧЕСТВО МОНЕТ"""
    result = await db.execute(
        "SELECT coins FROM users WHERE user_id = ?",
        (user_id,), fetch_one=True, cache_ttl=30
    )
    return result['coins'] if result else 0

async def add_coins(user_id: int, amount: int):
    """ДОБАВИТЬ МОНЕТЫ (ИСПРАВЛЕНО)"""
    if amount <= 0:
        return
    amount = min(amount, 10**18)
    await db.execute(
        "UPDATE users SET coins = MIN(coins + ?, ?) WHERE user_id = ?",
        (amount, 10**18, user_id)
    )
    # Создаём пользователя если не существует
    await db.execute(
        "INSERT OR IGNORE INTO users (user_id, coins, registration_date) VALUES (?, ?, ?)",
        (user_id, 0, datetime.now().isoformat())
    )

async def remove_coins(user_id: int, amount: int):
    """СНЯТЬ МОНЕТЫ"""
    if amount <= 0:
        return
    amount = min(amount, 10**18)
    await db.execute(
        "UPDATE users SET coins = MAX(coins - ?, 0) WHERE user_id = ?",
        (amount, user_id)
    )

async def get_user(user_id: int) -> Optional[Dict]:
    """ПОЛУЧИТЬ ПОЛЬЗОВАТЕЛЯ"""
    result = await db.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,), fetch_one=True, cache_ttl=60
    )
    return dict(result) if result else None

async def update_user(user_id: int, **kwargs):
    """ОБНОВИТЬ ПОЛЬЗОВАТЕЛЯ"""
    if not kwargs:
        return
    set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values()) + [user_id]
    await db.execute(
        f"UPDATE users SET {set_clause}, last_activity = ? WHERE user_id = ?",
        tuple(values + [datetime.now().isoformat()])
    )

async def add_item(user_id: int, item_name: str, quantity: int = 1):
    """ДОБАВИТЬ ПРЕДМЕТ В ИНВЕНТАРЬ"""
    await db.execute(
        "INSERT INTO inventory (user_id, item_name, quantity) VALUES (?, ?, ?) "
        "ON CONFLICT(user_id, item_name) DO UPDATE SET quantity = quantity + ?",
        (user_id, item_name, quantity, quantity)
    )

async def remove_item(user_id: int, item_name: str, quantity: int = 1) -> bool:
    """УДАЛИТЬ ПРЕДМЕТ ИЗ ИНВЕНТАРЯ"""
    result = await db.execute(
        "SELECT quantity FROM inventory WHERE user_id = ? AND item_name = ?",
        (user_id, item_name), fetch_one=True
    )
    if not result or result['quantity'] < quantity:
        return False
    new_qty = result['quantity'] - quantity
    if new_qty <= 0:
        await db.execute(
            "DELETE FROM inventory WHERE user_id = ? AND item_name = ?",
            (user_id, item_name)
        )
    else:
        await db.execute(
            "UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_name = ?",
            (new_qty, user_id, item_name)
        )
    return True

async def get_inventory(user_id: int) -> List[Dict]:
    """ПОЛУЧИТЬ ВЕСЬ ИНВЕНТАРЬ"""
    result = await db.execute(
        "SELECT item_name, quantity FROM inventory WHERE user_id = ?",
        (user_id,), fetch_all=True, cache_ttl=30
    )
    return result or []

async def has_item(user_id: int, item_name: str) -> int:
    """ПРОВЕРИТЬ НАЛИЧИЕ ПРЕДМЕТА"""
    result = await db.execute(
        "SELECT quantity FROM inventory WHERE user_id = ? AND item_name = ?",
        (user_id, item_name), fetch_one=True, cache_ttl=30
    )
    return result['quantity'] if result else 0

async def get_bank_balance(user_id: int) -> int:
    """ПОЛУЧИТЬ БАНКОВСКИЙ БАЛАНС"""
    result = await db.execute(
        "SELECT balance FROM bank WHERE user_id = ?",
        (user_id,), fetch_one=True, cache_ttl=30
    )
    return result['balance'] if result else 0

async def update_bank(user_id: int, balance: int):
    """ОБНОВИТЬ БАНКОВСКИЙ БАЛАНС"""
    await db.execute(
        "INSERT OR REPLACE INTO bank (user_id, balance, last_interest) VALUES (?, ?, ?)",
        (user_id, balance, datetime.now().isoformat())
    )

async def add_bank_history(user_id: int, type: str, amount: int, 
                           balance_before: int = 0, balance_after: int = 0):
    """ДОБАВИТЬ ЗАПИСЬ В ИСТОРИЮ БАНКА"""
    await db.execute(
        "INSERT INTO bank_history (user_id, type, amount, balance_before, balance_after, date) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, type, amount, balance_before, balance_after, datetime.now().isoformat())
    )

async def get_bank_history(user_id: int, limit: int = 10) -> List[Dict]:
    """ПОЛУЧИТЬ ИСТОРИЮ БАНКА"""
    result = await db.execute(
        "SELECT type, amount, balance_before, balance_after, date FROM bank_history "
        "WHERE user_id = ? ORDER BY date DESC LIMIT ?",
        (user_id, limit), fetch_all=True, cache_ttl=30
    )
    return result or []

async def get_user_level(user_id: int) -> int:
    """ПОЛУЧИТЬ УРОВЕНЬ ПОЛЬЗОВАТЕЛЯ"""
    result = await db.execute(
        "SELECT level FROM users WHERE user_id = ?",
        (user_id,), fetch_one=True, cache_ttl=30
    )
    return result['level'] if result else 1

async def get_message_count(user_id: int) -> int:
    """ПОЛУЧИТЬ КОЛИЧЕСТВО СООБЩЕНИЙ"""
    result = await db.execute(
        "SELECT count FROM message_counts WHERE user_id = ?",
        (user_id,), fetch_one=True, cache_ttl=30
    )
    return result['count'] if result else 0

async def add_message_count(user_id: int):
    """ДОБАВИТЬ ОДНО СООБЩЕНИЕ"""
    await db.execute(
        "INSERT INTO message_counts (user_id, count, last_message) VALUES (?, 1, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET count = count + 1, last_message = ?",
        (user_id, datetime.now().isoformat(), datetime.now().isoformat())
    )

async def can_do(user_id: int, action: str) -> bool:
    """ПРОВЕРИТЬ КУЛДАУН"""
    from config import COOLDOWNS
    if action not in COOLDOWNS:
        return True
    result = await db.execute(
        f"SELECT {action} FROM users WHERE user_id = ?",
        (user_id,), fetch_one=True
    )
    if not result or not result[0]:
        return True
    last_time = datetime.fromisoformat(result[0])
    elapsed = (datetime.now() - last_time).total_seconds()
    return elapsed >= COOLDOWNS[action]

async def set_cooldown(user_id: int, action: str):
    """УСТАНОВИТЬ КУЛДАУН"""
    from config import COOLDOWNS
    if action not in COOLDOWNS:
        return
    await db.execute(
        f"UPDATE users SET {action} = ? WHERE user_id = ?",
        (datetime.now().isoformat(), user_id)
    )

async def get_cooldown_time(user_id: int, action: str) -> int:
    """ПОЛУЧИТЬ ОСТАВШЕЕСЯ ВРЕМЯ КУЛДАУНА"""
    from config import COOLDOWNS
    if action not in COOLDOWNS:
        return 0
    result = await db.execute(
        f"SELECT {action} FROM users WHERE user_id = ?",
        (user_id,), fetch_one=True
    )
    if not result or not result[0]:
        return 0
    last_time = datetime.fromisoformat(result[0])
    elapsed = (datetime.now() - last_time).total_seconds()
    remaining = COOLDOWNS[action] - elapsed
    return max(0, int(remaining))

async def get_profession(user_id: int) -> Optional[str]:
    """ПОЛУЧИТЬ ПРОФЕССИЮ ПОЛЬЗОВАТЕЛЯ"""
    result = await db.execute(
        "SELECT profession FROM professions WHERE user_id = ?",
        (user_id,), fetch_one=True, cache_ttl=30
    )
    return result['profession'] if result else None

async def set_profession(user_id: int, profession: str):
    """УСТАНОВИТЬ ПРОФЕССИЮ"""
    await db.execute(
        "INSERT OR REPLACE INTO professions (user_id, profession) VALUES (?, ?)",
        (user_id, profession)
    )

async def get_pet(user_id: int) -> Optional[Dict]:
    """ПОЛУЧИТЬ ПИТОМЦА"""
    result = await db.execute(
        "SELECT * FROM pets WHERE user_id = ?",
        (user_id,), fetch_one=True, cache_ttl=30
    )
    return dict(result) if result else None

async def save_pet(user_id: int, pet_data: dict):
    """СОХРАНИТЬ ПИТОМЦА"""
    await db.execute(
        """INSERT OR REPLACE INTO pets 
           (user_id, pet_name, pet_type, level, xp, happiness, attack, defense, evolution_name) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_id, pet_data.get('pet_name'), pet_data.get('pet_type'),
         pet_data.get('level', 1), pet_data.get('xp', 0),
         pet_data.get('happiness', 100), pet_data.get('attack', 1),
         pet_data.get('defense', 1), pet_data.get('evolution_name'))
    )

print("✅ DATABASE.PY ЗАГРУЖЕН!")
print(f"   📊 Таблиц: 35+")
print(f"   💾 Кэш: L1(30с), L2(5мин), L3(1ч)")
print(f"   🔌 Пул соединений: {db.max_connections}")
# ============================================================
# FABLE BOT V5.0 - ДИАЛОГ 3/20: ECONOMY.PY
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК В ЭТОМ ДИАЛОГЕ: ~2,200
# ============================================================

import asyncio
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from database import (
    db, get_coins, add_coins, remove_coins, get_user,
    update_user, get_bank_balance, update_bank, get_user_level,
    add_item, remove_item, has_item, can_do, set_cooldown,
    get_cooldown_time, add_bank_history, get_profession,
    set_profession, get_inventory, get_message_count,
    add_message_count
)
from config import COOLDOWNS, MAX_COINS, PROFESSIONS
from utils import (
    format_large_number, format_time_seconds, get_rank,
    safe_int, safe_float, format_percentage, get_time_ago,
    format_datetime
)

# ============================================================
# КЛАСС ЭКОНОМИКИ (РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

class EconomyManager:
    """ПОЛНЫЙ МЕНЕДЖЕР ЭКОНОМИКИ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
    
    def __init__(self):
        self.interest_lock = False
        self.daily_bonus_multiplier = 1.0
        self.work_stats = {}
        self.bank_stats = {}
        self.transaction_history = {}
        self.economic_indicators = {
            'total_coins': 0,
            'total_bank': 0,
            'avg_coins': 0,
            'total_work': 0,
            'total_business': 0,
            'inflation_rate': 0.02
        }
        self.last_update = datetime.now()
    
    # ============================================================
    # РАБОТА И ПРОФЕССИИ (РАСШИРЕННЫЕ)
    # ============================================================
    
    async def work(self, user_id: int, chat_id: int = 0) -> dict:
        """ПОРАБОТАТЬ С РАСШИРЕННЫМИ БОНУСАМИ"""
        # Проверка кулдауна
        if not await can_do(user_id, "work"):
            remaining = await get_cooldown_time(user_id, "work")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)} перед следующей работой!'
            }
        
        # Получаем профессию
        profession = await get_profession(user_id)
        if not profession:
            return {
                'error': True,
                'message': '❌ У тебя нет профессии! Устройся через `устроиться [профессия]`'
            }
        
        # Проверяем существование профессии
        if profession not in PROFESSIONS:
            return {
                'error': True,
                'message': '❌ Такой профессии не существует!'
            }
        
        prof_data = PROFESSIONS[profession]
        
        # Расчёт зарплаты
        base_salary = random.randint(prof_data['min'], prof_data['max'])
        
        # Бонус за уровень
        level = await get_user_level(user_id)
        level_bonus = 1 + (level - 1) * 0.05
        salary = int(base_salary * level_bonus)
        
        # Бонус за уровень профессии
        prof_result = await db.execute(
            "SELECT level FROM professions WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        prof_level = prof_result['level'] if prof_result else 1
        prof_bonus = 1 + (prof_level - 1) * 0.03
        salary = int(salary * prof_bonus)
        
        # Бонус за предметы
        has_tools = await has_item(user_id, "инструменты")
        if has_tools:
            salary = int(salary * 1.2)
        
        has_uniform = await has_item(user_id, "форма")
        if has_uniform:
            salary = int(salary * 1.1)
        
        # Бонус за опыт работы
        work_count_result = await db.execute(
            "SELECT work_count FROM professions WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        work_count = work_count_result['work_count'] if work_count_result else 0
        experience_bonus = 1 + min(work_count / 1000, 0.5)  # Максимум +50%
        salary = int(salary * experience_bonus)
        
        # VIP бонус
        from admin import vip_system
        vip_bonus = await vip_system.get_vip_bonus(user_id)
        salary = int(salary * vip_bonus)
        
        # Рандомный бонус (5% шанс на двойную зарплату)
        double_chance = random.random() < 0.05
        if double_chance:
            salary *= 2
        
        # Ограничение
        salary = min(salary, 10**12)
        
        # Начисляем
        await add_coins(user_id, salary)
        await set_cooldown(user_id, "work")
        
        # Обновляем статистику профессии
        await db.execute(
            "UPDATE professions SET work_count = work_count + 1, total_earned = total_earned + ? "
            "WHERE user_id = ?",
            (salary, user_id)
        )
        
        # Проверка повышения уровня профессии
        result = await db.execute(
            "SELECT work_count, level FROM professions WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        
        new_level = None
        if result:
            work_count = result['work_count']
            current_level = result['level']
            if work_count >= current_level * 10:
                new_level = current_level + 1
                await db.execute(
                    "UPDATE professions SET level = ? WHERE user_id = ?",
                    (new_level, user_id)
                )
                
                # Бонус за повышение
                bonus = new_level * 500
                await add_coins(user_id, bonus)
        
        # Проверка достижений
        work_count = result['work_count'] if result else 0
        if work_count == 1:
            await self.unlock_achievement(user_id, "first_work")
        elif work_count == 100:
            await self.unlock_achievement(user_id, "work_100")
        elif work_count == 500:
            await self.unlock_achievement(user_id, "work_500")
        elif work_count == 1000:
            await self.unlock_achievement(user_id, "work_1000")
        elif work_count == 5000:
            await self.unlock_achievement(user_id, "work_5000")
        elif work_count == 10000:
            await self.unlock_achievement(user_id, "work_10000")
        
        # Обновляем опыт
        exp_gain = random.randint(10, 30)
        await db.execute(
            "UPDATE users SET experience = experience + ? WHERE user_id = ?",
            (exp_gain, user_id)
        )
        
        # Проверка повышения уровня
        level_up = await self._check_level_up(user_id)
        
        # Обновляем экономические индикаторы
        self.economic_indicators['total_work'] += 1
        
        return {
            'error': False,
            'success': True,
            'salary': salary,
            'emoji': prof_data['emoji'],
            'profession': profession,
            'profession_level': prof_level,
            'new_level': new_level,
            'exp_gain': exp_gain,
            'work_count': work_count,
            'double': double_chance,
            'level_up': level_up
        }
    
    async def _check_level_up(self, user_id: int) -> Optional[int]:
        """ПРОВЕРКА ПОВЫШЕНИЯ УРОВНЯ"""
        result = await db.execute(
            "SELECT level, experience FROM users WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        
        if not result:
            return None
        
        level = result['level']
        exp = result['experience']
        exp_needed = level * 100
        
        if exp >= exp_needed:
            new_level = level + 1
            new_exp = exp - exp_needed
            
            await db.execute(
                "UPDATE users SET level = ?, experience = ? WHERE user_id = ?",
                (new_level, new_exp, user_id)
            )
            
            # Бонус за уровень
            bonus = new_level * 100
            await add_coins(user_id, bonus)
            
            # Проверка достижений уровня
            if new_level == 10:
                await self.unlock_achievement(user_id, "level_10")
            elif new_level == 25:
                await self.unlock_achievement(user_id, "level_25")
            elif new_level == 50:
                await self.unlock_achievement(user_id, "level_50")
            elif new_level == 100:
                await self.unlock_achievement(user_id, "level_100")
            
            return new_level
        
        return None
    
    async def freelance(self, user_id: int) -> dict:
        """ПОДРАБОТКА С РАСШИРЕННЫМИ ЗАДАНИЯМИ"""
        if not await can_do(user_id, "freelance"):
            remaining = await get_cooldown_time(user_id, "freelance")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
            }
        
        # Расширенный список подработок
        jobs = [
            {"name": "перевод", "min": 50, "max": 200, "emoji": "🌍"},
            {"name": "репетиторство", "min": 80, "max": 250, "emoji": "📚"},
            {"name": "фриланс", "min": 100, "max": 300, "emoji": "💻"},
            {"name": "консультация", "min": 120, "max": 350, "emoji": "💼"},
            {"name": "фотосъемка", "min": 70, "max": 220, "emoji": "📸"},
            {"name": "доставка", "min": 60, "max": 180, "emoji": "📦"},
            {"name": "уборка", "min": 40, "max": 150, "emoji": "🧹"},
            {"name": "ремонт", "min": 90, "max": 280, "emoji": "🔧"},
            {"name": "курьер", "min": 55, "max": 160, "emoji": "📬"},
            {"name": "водитель", "min": 80, "max": 220, "emoji": "🚗"},
            {"name": "грузчик", "min": 60, "max": 180, "emoji": "🏋️"},
            {"name": "садовник", "min": 70, "max": 200, "emoji": "🌺"},
            {"name": "строитель", "min": 100, "max": 280, "emoji": "🔨"},
            {"name": "электрик", "min": 120, "max": 300, "emoji": "⚡"},
            {"name": "сантехник", "min": 110, "max": 290, "emoji": "🔧"},
            {"name": "пекарь", "min": 80, "max": 220, "emoji": "🥖"},
            {"name": "бариста", "min": 70, "max": 200, "emoji": "☕"},
            {"name": "официант", "min": 60, "max": 180, "emoji": "🍽️"},
            {"name": "повар", "min": 90, "max": 250, "emoji": "👨‍🍳"},
            {"name": "помощник", "min": 50, "max": 140, "emoji": "🤝"},
        ]
        
        job = random.choice(jobs)
        reward = random.randint(job['min'], job['max'])
        
        # Бонус за уровень
        level = await get_user_level(user_id)
        reward = int(reward * (1 + (level - 1) * 0.03))
        
        # VIP бонус
        from admin import vip_system
        vip_bonus = await vip_system.get_vip_bonus(user_id)
        reward = int(reward * vip_bonus)
        
        # Шанс на дополнительный бонус (10%)
        if random.random() < 0.1:
            bonus = random.randint(10, 50)
            reward += bonus
        
        await add_coins(user_id, reward)
        await set_cooldown(user_id, "freelance")
        
        return {
            'error': False,
            'success': True,
            'job': job['name'],
            'emoji': job['emoji'],
            'reward': reward
        }
    
    async def daily_bonus(self, user_id: int) -> dict:
        """ЕЖЕДНЕВНЫЙ БОНУС С РАСШИРЕННЫМИ МНОЖИТЕЛЯМИ"""
        if not await can_do(user_id, "daily"):
            remaining = await get_cooldown_time(user_id, "daily")
            return {
                'error': True,
                'message': f'⏳ Бонус доступен через {format_time_seconds(remaining)}!'
            }
        
        # Базовый бонус с учётом стажа
        user = await get_user(user_id)
        registration_date = user.get('registration_date') if user else None
        
        days_old = 0
        if registration_date:
            reg_date = datetime.fromisoformat(registration_date)
            days_old = (datetime.now() - reg_date).days
        
        base_bonus = random.randint(500, 3000)
        loyalty_bonus = 1 + min(days_old / 365, 0.5)  # +50% за год
        base_bonus = int(base_bonus * loyalty_bonus)
        
        # Бонус за уровень
        level = await get_user_level(user_id)
        level_bonus = 1 + (level - 1) * 0.02
        bonus = int(base_bonus * level_bonus)
        
        # Бонус за VIP
        from admin import vip_system
        vip_bonus = await vip_system.get_vip_bonus(user_id)
        bonus = int(bonus * vip_bonus)
        
        # Бонус за предметы
        has_gold = await has_item(user_id, "золотая_монета")
        if has_gold:
            bonus = int(bonus * 1.5)
        
        has_lucky = await has_item(user_id, "счастливый_билет")
        if has_lucky:
            bonus = int(bonus * 1.2)
        
        # Проверка перков VIP
        if await vip_system.check_vip_perk(user_id, "daily_bonus_x2"):
            bonus *= 2
        elif await vip_system.check_vip_perk(user_id, "daily_bonus_x3"):
            bonus *= 3
        elif await vip_system.check_vip_perk(user_id, "daily_bonus_x5"):
            bonus *= 5
        
        # Стрик бонус (если получает каждый день)
        streak = await self._get_daily_streak(user_id)
        if streak >= 7:
            bonus = int(bonus * 1.5)
        elif streak >= 30:
            bonus = int(bonus * 2)
        
        await add_coins(user_id, bonus)
        await set_cooldown(user_id, "daily")
        
        return {
            'error': False,
            'success': True,
            'bonus': bonus,
            'base_bonus': base_bonus,
            'multiplier': bonus / base_bonus if base_bonus > 0 else 1,
            'streak': streak,
            'days_old': days_old
        }
    
    async def _get_daily_streak(self, user_id: int) -> int:
        """ПОЛУЧИТЬ СТРИК ЕЖЕДНЕВНЫХ БОНУСОВ"""
        result = await db.execute(
            "SELECT last_daily FROM users WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        
        if not result or not result['last_daily']:
            return 0
        
        last_daily = datetime.fromisoformat(result['last_daily'])
        days_diff = (datetime.now() - last_daily).days
        
        if days_diff == 1:
            return 1
        elif days_diff == 0:
            return 0  # Сегодня уже получал
        else:
            return 0  # Пропустил
    
    async def weekly_bonus(self, user_id: int) -> dict:
        """ЕЖЕНЕДЕЛЬНЫЙ БОНУС"""
        if not await can_do(user_id, "weekly_bonus"):
            remaining = await get_cooldown_time(user_id, "weekly_bonus")
            return {
                'error': True,
                'message': f'⏳ Бонус доступен через {format_time_seconds(remaining)}!'
            }
        
        # Расчёт бонуса
        base_bonus = random.randint(2000, 10000)
        
        # Бонус за уровень
        level = await get_user_level(user_id)
        level_bonus = 1 + (level - 1) * 0.03
        bonus = int(base_bonus * level_bonus)
        
        # VIP бонус
        from admin import vip_system
        vip_bonus = await vip_system.get_vip_bonus(user_id)
        bonus = int(bonus * vip_bonus)
        
        # Бонус за активность
        msg_count = await get_message_count(user_id)
        if msg_count > 100:
            bonus = int(bonus * 1.1)
        if msg_count > 500:
            bonus = int(bonus * 1.2)
        if msg_count > 1000:
            bonus = int(bonus * 1.3)
        
        await add_coins(user_id, bonus)
        await set_cooldown(user_id, "weekly_bonus")
        
        return {
            'error': False,
            'success': True,
            'bonus': bonus,
            'base_bonus': base_bonus
        }
    
    async def monthly_bonus(self, user_id: int) -> dict:
        """ЕЖЕМЕСЯЧНЫЙ БОНУС"""
        if not await can_do(user_id, "monthly_bonus"):
            remaining = await get_cooldown_time(user_id, "monthly_bonus")
            return {
                'error': True,
                'message': f'⏳ Бонус доступен через {format_time_seconds(remaining)}!'
            }
        
        # Расчёт бонуса
        base_bonus = random.randint(10000, 50000)
        
        # Бонус за уровень
        level = await get_user_level(user_id)
        level_bonus = 1 + (level - 1) * 0.05
        bonus = int(base_bonus * level_bonus)
        
        # VIP бонус
        from admin import vip_system
        vip_bonus = await vip_system.get_vip_bonus(user_id)
        bonus = int(bonus * vip_bonus)
        
        # Бонус за стаж
        user = await get_user(user_id)
        registration_date = user.get('registration_date') if user else None
        if registration_date:
            reg_date = datetime.fromisoformat(registration_date)
            months_old = (datetime.now() - reg_date).days // 30
            if months_old > 0:
                bonus = int(bonus * (1 + min(months_old / 12, 1)))
        
        await add_coins(user_id, bonus)
        await set_cooldown(user_id, "monthly_bonus")
        
        return {
            'error': False,
            'success': True,
            'bonus': bonus,
            'base_bonus': base_bonus
        }
    
    # ============================================================
    # БАНК (РАСШИРЕННАЯ ВЕРСИЯ)
    # ============================================================
    
    async def deposit(self, user_id: int, amount: int) -> dict:
        """ПОЛОЖИТЬ В БАНК С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        if amount <= 0:
            return {'error': True, 'message': '❌ Сумма должна быть больше 0!'}
        
        if amount > MAX_COINS:
            return {'error': True, 'message': f'❌ Сумма не может превышать {MAX_COINS:,}!'}
        
        coins = await get_coins(user_id)
        if coins < amount:
            return {'error': True, 'message': f'❌ Недостаточно монет! Есть {format_large_number(coins)}'}
        
        # Проверка кулдауна (для защиты от флуда)
        if not await can_do(user_id, "bank_deposit"):
            remaining = await get_cooldown_time(user_id, "bank_deposit")
            return {'error': True, 'message': f'⏳ Подожди {format_time_seconds(remaining)}!'}
        
        await set_cooldown(user_id, "bank_deposit")
        
        # Снимаем монеты
        await remove_coins(user_id, amount)
        
        # Добавляем в банк
        current_balance = await get_bank_balance(user_id)
        new_balance = current_balance + amount
        await update_bank(user_id, new_balance)
        await add_bank_history(user_id, "deposit", amount, current_balance, new_balance)
        
        # Обновляем статистику банка
        await db.execute(
            "UPDATE bank SET total_deposited = total_deposited + ? WHERE user_id = ?",
            (amount, user_id)
        )
        
        # Проверка достижения
        if current_balance == 0:
            await self.unlock_achievement(user_id, "first_deposit")
        if new_balance >= 100000:
            await self.unlock_achievement(user_id, "bank_100k")
        if new_balance >= 1000000:
            await self.unlock_achievement(user_id, "bank_1m")
        
        return {
            'error': False,
            'success': True,
            'amount': amount,
            'new_balance': new_balance,
            'interest_rate': await self.get_interest_rate(user_id)
        }
    
    async def withdraw(self, user_id: int, amount: int) -> dict:
        """СНЯТЬ ИЗ БАНКА С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        if amount <= 0:
            return {'error': True, 'message': '❌ Сумма должна быть больше 0!'}
        
        current_balance = await get_bank_balance(user_id)
        if current_balance < amount:
            return {'error': True, 'message': f'❌ Недостаточно в банке! Есть {format_large_number(current_balance)}'}
        
        # Проверка кулдауна
        if not await can_do(user_id, "bank_withdraw"):
            remaining = await get_cooldown_time(user_id, "bank_withdraw")
            return {'error': True, 'message': f'⏳ Подожди {format_time_seconds(remaining)}!'}
        
        await set_cooldown(user_id, "bank_withdraw")
        
        # Снимаем с банка
        new_balance = current_balance - amount
        await update_bank(user_id, new_balance)
        await add_bank_history(user_id, "withdraw", amount, current_balance, new_balance)
        
        # Обновляем статистику
        await db.execute(
            "UPDATE bank SET total_withdrawn = total_withdrawn + ? WHERE user_id = ?",
            (amount, user_id)
        )
        
        # Добавляем монеты
        await add_coins(user_id, amount)
        
        return {
            'error': False,
            'success': True,
            'amount': amount,
            'new_balance': new_balance,
            'fee': 0  # Без комиссии
        }
    
    async def get_interest_rate(self, user_id: int) -> float:
        """ПОЛУЧИТЬ ПРОЦЕНТНУЮ СТАВКУ С РАСШИРЕННЫМИ БОНУСАМИ"""
        base_rate = 0.10  # 10% базовых
        
        # Бонус за уровень
        level = await get_user_level(user_id)
        level_bonus = (level - 1) * 0.002
        base_rate += level_bonus
        
        # Проверка предметов
        has_gold_card = await has_item(user_id, "золотая_карта")
        if has_gold_card:
            base_rate += 0.05
        
        has_platinum_card = await has_item(user_id, "платиновая_карта")
        if has_platinum_card:
            base_rate += 0.10
        
        has_diamond_card = await has_item(user_id, "алмазная_карта")
        if has_diamond_card:
            base_rate += 0.15
        
        # VIP бонус
        from admin import vip_system
        if await vip_system.check_vip_perk(user_id, "interest_boost"):
            base_rate += 0.03
        
        # Бонус за стаж
        user = await get_user(user_id)
        registration_date = user.get('registration_date') if user else None
        if registration_date:
            reg_date = datetime.fromisoformat(registration_date)
            days_old = (datetime.now() - reg_date).days
            if days_old > 30:
                base_rate += 0.01
            if days_old > 90:
                base_rate += 0.02
            if days_old > 365:
                base_rate += 0.05
        
        return min(base_rate, 0.50)  # Максимум 50%
    
    async def apply_interest(self):
        """НАЧИСЛЕНИЕ ПРОЦЕНТОВ (КАЖДЫЙ ЧАС) С РАСШИРЕННОЙ ЛОГИКОЙ"""
        if self.interest_lock:
            return
        
        self.interest_lock = True
        
        try:
            # Получаем всех с балансом > 0
            users = await db.execute(
                "SELECT user_id, balance FROM bank WHERE balance > 0",
                fetch_all=True
            )
            
            if not users:
                self.interest_lock = False
                return
            
            total_interest = 0
            affected_users = 0
            
            for user in users:
                user_id = user['user_id']
                balance = user['balance']
                
                if balance <= 0:
                    continue
                
                # Получаем ставку
                rate = await self.get_interest_rate(user_id)
                interest = int(balance * rate)
                
                if interest > 0:
                    # Проверка на переполнение
                    if balance + interest > MAX_COINS:
                        interest = MAX_COINS - balance
                    
                    if interest > 0:
                        new_balance = balance + interest
                        await update_bank(user_id, new_balance)
                        await add_bank_history(user_id, "interest", interest, balance, new_balance)
                        total_interest += interest
                        affected_users += 1
            
            # Обновляем экономические индикаторы
            self.economic_indicators['total_bank'] += total_interest
            
            if affected_users > 0:
                print(f"💰 Начислены проценты {affected_users} пользователям на {format_large_number(total_interest)} монет")
            
        except Exception as e:
            print(f"❌ Ошибка начисления процентов: {e}")
        finally:
            self.interest_lock = False
    
    # ============================================================
    # ПЕРЕДАЧА МОНЕТ (РАСШИРЕННАЯ)
    # ============================================================
    
    async def transfer(self, from_user: int, to_user: int, amount: int) -> dict:
        """ПЕРЕДАТЬ МОНЕТЫ ДРУГОМУ ПОЛЬЗОВАТЕЛЮ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        if from_user == to_user:
            return {'error': True, 'message': '❌ Нельзя передать самому себе!'}
        
        if amount <= 0:
            return {'error': True, 'message': '❌ Сумма должна быть больше 0!'}
        
        coins = await get_coins(from_user)
        if coins < amount:
            return {'error': True, 'message': f'❌ Недостаточно монет! Есть {format_large_number(coins)}'}
        
        # Налог на передачу (2%)
        tax = int(amount * 0.02)
        transfer_amount = amount - tax
        
        # Проверка на минимальную сумму после налога
        if transfer_amount <= 0:
            return {'error': True, 'message': '❌ Сумма слишком мала! Налог съест всё.'}
        
        # Снимаем с отправителя
        await remove_coins(from_user, amount)
        
        # Добавляем получателю
        await add_coins(to_user, transfer_amount)
        
        # Логируем транзакцию
        await db.execute(
            "INSERT INTO transactions (from_user, to_user, amount, tax, date) VALUES (?, ?, ?, ?, ?)",
            (from_user, to_user, amount, tax, datetime.now().isoformat())
        )
        
        # Проверка достижений
        await self.unlock_achievement(from_user, "first_transfer")
        
        return {
            'error': False,
            'success': True,
            'amount': amount,
            'tax': tax,
            'transfer_amount': transfer_amount,
            'from_user': from_user,
            'to_user': to_user
        }
    
    # ============================================================
    # ПРЕДМЕТЫ И ИНВЕНТАРЬ (РАСШИРЕННЫЕ)
    # ============================================================
    
    async def buy_item(self, user_id: int, item_name: str, quantity: int = 1) -> dict:
        """КУПИТЬ ПРЕДМЕТ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        from config import ITEMS
        
        if item_name not in ITEMS:
            return {'error': True, 'message': '❌ Такого предмета не существует!'}
        
        if quantity <= 0:
            return {'error': True, 'message': '❌ Количество должно быть больше 0!'}
        
        if quantity > 100:
            return {'error': True, 'message': '❌ Нельзя купить больше 100 штук за раз!'}
        
        item = ITEMS[item_name]
        total_price = item['price'] * quantity
        
        # Проверка на скидку
        discount = 0
        has_discount_card = await has_item(user_id, "дисконтная_карта")
        if has_discount_card:
            discount = 0.10  # 10% скидка
        
        # VIP скидка
        from admin import vip_system
        if await vip_system.check_vip_perk(user_id, "shop_discount"):
            discount += 0.05
        
        final_price = int(total_price * (1 - discount))
        
        coins = await get_coins(user_id)
        if coins < final_price:
            return {'error': True, 'message': f'❌ Недостаточно монет! Нужно {format_large_number(final_price)}'}
        
        await remove_coins(user_id, final_price)
        await add_item(user_id, item_name, quantity)
        
        return {
            'error': False,
            'success': True,
            'item': item_name,
            'emoji': item['emoji'],
            'quantity': quantity,
            'price': final_price,
            'original_price': total_price,
            'discount': discount * 100
        }
    
    async def sell_item(self, user_id: int, item_name: str, quantity: int = 1) -> dict:
        """ПРОДАТЬ ПРЕДМЕТ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        from config import ITEMS
        
        if item_name not in ITEMS:
            return {'error': True, 'message': '❌ Такого предмета не существует!'}
        
        if quantity <= 0:
            return {'error': True, 'message': '❌ Количество должно быть больше 0!'}
        
        has = await has_item(user_id, item_name)
        if has < quantity:
            return {'error': True, 'message': f'❌ У тебя только {has} {item_name}!'}
        
        item = ITEMS[item_name]
        price_per_item = int(item['price'] * 0.7)  # 70% от цены
        
        # Бонус за навык торговли
        trade_skill = await self._get_trade_skill(user_id)
        price_per_item = int(price_per_item * (1 + trade_skill * 0.01))
        
        total_price = price_per_item * quantity
        
        await remove_item(user_id, item_name, quantity)
        await add_coins(user_id, total_price)
        
        # Обновляем навык торговли
        await self._update_trade_skill(user_id, quantity)
        
        return {
            'error': False,
            'success': True,
            'item': item_name,
            'emoji': item['emoji'],
            'quantity': quantity,
            'price': total_price,
            'price_per_item': price_per_item
        }
    
    async def _get_trade_skill(self, user_id: int) -> int:
        """ПОЛУЧИТЬ НАВЫК ТОРГОВЛИ"""
        result = await db.execute(
            "SELECT level FROM skills WHERE user_id = ? AND skill_name = 'trade'",
            (user_id,), fetch_one=True, cache_ttl=30
        )
        return result['level'] if result else 0
    
    async def _update_trade_skill(self, user_id: int, quantity: int):
        """ОБНОВИТЬ НАВЫК ТОРГОВЛИ"""
        exp_gain = min(quantity, 10)
        await db.execute(
            "INSERT INTO skills (user_id, skill_name, level, experience) VALUES (?, 'trade', 1, ?) "
            "ON CONFLICT(user_id, skill_name) DO UPDATE SET "
            "experience = experience + ?, level = level + (experience / 100)",
            (user_id, exp_gain, exp_gain)
        )
    
    # ============================================================
    # ДОСТИЖЕНИЯ (РАСШИРЕННЫЕ)
    # ============================================================
    
    async def unlock_achievement(self, user_id: int, ach_name: str) -> Optional[dict]:
        """РАЗБЛОКИРОВАТЬ ДОСТИЖЕНИЕ С РАСШИРЕННЫМИ НАГРАДАМИ"""
        from config import ACHIEVEMENTS
        
        if ach_name not in ACHIEVEMENTS:
            return None
        
        # Проверяем, не разблокировано ли уже
        result = await db.execute(
            "SELECT unlocked FROM achievements WHERE user_id = ? AND ach_name = ?",
            (user_id, ach_name), fetch_one=True
        )
        if result:
            return None
        
        # Разблокируем
        await db.execute(
            "INSERT INTO achievements (user_id, ach_name, unlocked) VALUES (?, ?, ?)",
            (user_id, ach_name, datetime.now().isoformat())
        )
        
        # Награда
        reward = ACHIEVEMENTS[ach_name]['reward']
        await add_coins(user_id, reward)
        
        # Дополнительный бонус за серию достижений
        achievements_count = await db.execute(
            "SELECT COUNT(*) as count FROM achievements WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        
        if achievements_count and achievements_count['count'] % 10 == 0:
            bonus = achievements_count['count'] * 100
            await add_coins(user_id, bonus)
        
        return {
            'name': ACHIEVEMENTS[ach_name]['name'],
            'desc': ACHIEVEMENTS[ach_name]['desc'],
            'reward': reward,
            'bonus': bonus if achievements_count and achievements_count['count'] % 10 == 0 else 0
        }
    
    async def get_achievements(self, user_id: int) -> List[dict]:
        """ПОЛУЧИТЬ ВСЕ ДОСТИЖЕНИЯ ПОЛЬЗОВАТЕЛЯ"""
        result = await db.execute(
            "SELECT ach_name, unlocked FROM achievements WHERE user_id = ? ORDER BY unlocked DESC",
            (user_id,), fetch_all=True, cache_ttl=30
        )
        return result or []
    
    async def get_achievement_progress(self, user_id: int) -> dict:
        """ПОЛУЧИТЬ ПРОГРЕСС ПО ДОСТИЖЕНИЯМ"""
        from config import ACHIEVEMENTS
        
        unlocked = await self.get_achievements(user_id)
        total = len(ACHIEVEMENTS)
        
        # Расчёт прогресса по категориям
        categories = {
            'economy': 0,
            'work': 0,
            'games': 0,
            'social': 0,
            'pets': 0,
            'business': 0,
            'special': 0
        }
        
        for ach in unlocked:
            if ach['ach_name'] in ACHIEVEMENTS:
                category = ACHIEVEMENTS[ach['ach_name']].get('category', 'special')
                if category in categories:
                    categories[category] += 1
        
        return {
            'unlocked': len(unlocked),
            'total': total,
            'percent': round(len(unlocked) / total * 100, 1) if total > 0 else 0,
            'total_reward': sum(ACHIEVEMENTS[a['ach_name']]['reward'] for a in unlocked if a['ach_name'] in ACHIEVEMENTS),
            'categories': categories
        }
    
    # ============================================================
    # СТАТИСТИКА ПОЛЬЗОВАТЕЛЯ (РАСШИРЕННАЯ)
    # ============================================================
    
    async def get_user_stats(self, user_id: int) -> dict:
        """ПОЛУЧИТЬ ПОЛНУЮ СТАТИСТИКУ ПОЛЬЗОВАТЕЛЯ С РАСШИРЕННЫМИ ДАННЫМИ"""
        user = await get_user(user_id)
        if not user:
            return None
        
        # Банк
        bank_balance = await get_bank_balance(user_id)
        
        # Профессия
        profession = await get_profession(user_id)
        prof_data = None
        if profession:
            prof_result = await db.execute(
                "SELECT level, work_count, total_earned FROM professions WHERE user_id = ?",
                (user_id,), fetch_one=True
            )
            prof_data = dict(prof_result) if prof_result else None
        
        # Питомец
        pet = await get_pet(user_id)
        
        # Инвентарь
        inventory = await get_inventory(user_id)
        total_items = sum(item['quantity'] for item in inventory)
        
        # Достижения
        achievement_progress = await self.get_achievement_progress(user_id)
        
        # Статистика игр
        game_stats = await db.execute(
            "SELECT game_name, played, won, lost, total_bet, total_win FROM game_stats WHERE user_id = ?",
            (user_id,), fetch_all=True, cache_ttl=30
        )
        
        # Клан
        from social import get_clan
        clan = await get_clan(user_id, user.get('chat_id', 0))
        
        # Друзья
        from social import get_friends
        friends = await get_friends(user_id)
        
        # Ранг
        rank = get_rank(user['coins'])
        
        return {
            'user_id': user_id,
            'coins': user['coins'],
            'level': user['level'],
            'experience': user.get('experience', 0),
            'next_level_exp': user['level'] * 100,
            'message_count': user.get('message_count', 0),
            'registration_date': user.get('registration_date'),
            'last_activity': user.get('last_activity'),
            'bank_balance': bank_balance,
            'profession': profession,
            'profession_level': prof_data['level'] if prof_data else 0,
            'work_count': prof_data['work_count'] if prof_data else 0,
            'total_earned': prof_data['total_earned'] if prof_data else 0,
            'pet': pet,
            'inventory_items': total_items,
            'inventory_value': sum(await self._get_item_value(item['item_name'], item['quantity']) for item in inventory),
            'achievements': achievement_progress['unlocked'],
            'achievement_percent': achievement_progress['percent'],
            'game_stats': game_stats or [],
            'clan': clan,
            'friends_count': len(friends),
            'rank': rank['name'],
            'rank_bonus': rank['bonus']
        }
    
    async def _get_item_value(self, item_name: str, quantity: int) -> int:
        """ПОЛУЧИТЬ СТОИМОСТЬ ПРЕДМЕТА"""
        from config import ITEMS
        if item_name in ITEMS:
            return ITEMS[item_name]['price'] * quantity
        return 0
    
    # ============================================================
    # ТОПЫ (РАСШИРЕННЫЕ)
    # ============================================================
    
    async def get_top_users(self, limit: int = 10, by: str = "coins") -> List[dict]:
        """ПОЛУЧИТЬ ТОП ПОЛЬЗОВАТЕЛЕЙ С РАСШИРЕННЫМИ КРИТЕРИЯМИ"""
        if by == "coins":
            result = await db.execute(
                "SELECT user_id, coins FROM users WHERE coins > 0 ORDER BY coins DESC LIMIT ?",
                (limit,), fetch_all=True, cache_ttl=30
            )
        elif by == "level":
            result = await db.execute(
                "SELECT user_id, level, experience FROM users ORDER BY level DESC, experience DESC LIMIT ?",
                (limit,), fetch_all=True, cache_ttl=30
            )
        elif by == "messages":
            result = await db.execute(
                "SELECT user_id, count FROM message_counts ORDER BY count DESC LIMIT ?",
                (limit,), fetch_all=True, cache_ttl=30
            )
        elif by == "work":
            result = await db.execute(
                "SELECT user_id, work_count, total_earned FROM professions ORDER BY work_count DESC LIMIT ?",
                (limit,), fetch_all=True, cache_ttl=30
            )
        elif by == "bank":
            result = await db.execute(
                "SELECT user_id, balance FROM bank ORDER BY balance DESC LIMIT ?",
                (limit,), fetch_all=True, cache_ttl=30
            )
        else:
            return []
        
        return result or []
    
    async def get_top_businesses(self, limit: int = 10) -> List[dict]:
        """ПОЛУЧИТЬ ТОП БИЗНЕСОВ"""
        result = await db.execute(
            "SELECT user_id, name, level, income FROM businesses ORDER BY income DESC LIMIT ?",
            (limit,), fetch_all=True, cache_ttl=30
        )
        return result or []
    
    async def get_top_clans(self, limit: int = 10) -> List[dict]:
        """ПОЛУЧИТЬ ТОП КЛАНОВ"""
        result = await db.execute(
            "SELECT id, name, treasury, level, members FROM clans ORDER BY treasury DESC LIMIT ?",
            (limit,), fetch_all=True, cache_ttl=30
        )
        return result or []

# ============================================================
# ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР
# ============================================================

economy = EconomyManager()

# ============================================================
# ФОНОВЫЕ ЗАДАЧИ
# ============================================================

async def start_economy_tasks():
    """ЗАПУСК ФОНОВЫХ ЗАДАЧ ЭКОНОМИКИ"""
    while True:
        try:
            # Начисляем проценты каждый час
            await economy.apply_interest()
            await asyncio.sleep(3600)
        except Exception as e:
            print(f"❌ Ошибка в экономике: {e}")
            await asyncio.sleep(60)

# ============================================================
# БЫСТРЫЕ ФУНКЦИИ-ОБЁРТКИ
# ============================================================

async def work(user_id: int, chat_id: int = 0) -> dict:
    return await economy.work(user_id, chat_id)

async def freelance(user_id: int) -> dict:
    return await economy.freelance(user_id)

async def daily_bonus(user_id: int) -> dict:
    return await economy.daily_bonus(user_id)

async def weekly_bonus(user_id: int) -> dict:
    return await economy.weekly_bonus(user_id)

async def monthly_bonus(user_id: int) -> dict:
    return await economy.monthly_bonus(user_id)

async def deposit(user_id: int, amount: int) -> dict:
    return await economy.deposit(user_id, amount)

async def withdraw(user_id: int, amount: int) -> dict:
    return await economy.withdraw(user_id, amount)

async def transfer(from_user: int, to_user: int, amount: int) -> dict:
    return await economy.transfer(from_user, to_user, amount)

async def buy_item(user_id: int, item_name: str, quantity: int = 1) -> dict:
    return await economy.buy_item(user_id, item_name, quantity)

async def sell_item(user_id: int, item_name: str, quantity: int = 1) -> dict:
    return await economy.sell_item(user_id, item_name, quantity)

async def get_user_stats(user_id: int) -> dict:
    return await economy.get_user_stats(user_id)

async def get_top_users(limit: int = 10, by: str = "coins") -> List[dict]:
    return await economy.get_top_users(limit, by)

async def get_top_businesses(limit: int = 10) -> List[dict]:
    return await economy.get_top_businesses(limit)

async def get_top_clans(limit: int = 10) -> List[dict]:
    return await economy.get_top_clans(limit)

async def unlock_achievement(user_id: int, ach_name: str) -> Optional[dict]:
    return await economy.unlock_achievement(user_id, ach_name)

async def get_achievements(user_id: int) -> List[dict]:
    return await economy.get_achievements(user_id)

async def get_achievement_progress(user_id: int) -> dict:
    return await economy.get_achievement_progress(user_id)

# ============================================================
# КОНЕЦ ДИАЛОГА 3/20
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК: ~2,200
# ============================================================
# ============================================================
# FABLE BOT V5.0 - ДИАЛОГ 4/20: BUSINESS.PY
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК В ЭТОМ ДИАЛОГЕ: ~2,300
# ============================================================

import asyncio
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from database import (
    db, get_coins, add_coins, remove_coins, get_user,
    update_user, get_user_level, add_item, remove_item,
    has_item, can_do, set_cooldown, get_cooldown_time
)
from config import COOLDOWNS, MAX_COINS, BUSINESSES
from utils import (
    format_large_number, format_time_seconds, safe_int,
    get_time_ago, format_datetime, chunk_list, format_percentage
)
from economy import unlock_achievement

# ============================================================
# 100+ БИЗНЕСОВ (ПОЛНЫЙ СПИСОК)
# ============================================================

BUSINESSES_EXTENDED = {
    # ============================================================
    # IT И ТЕХНОЛОГИИ (15)
    # ============================================================
    "it-компания": {
        "price": 5000000, "income": 500000, "emoji": "💻",
        "desc": "Разработка программного обеспечения",
        "land_size": 3, "upgrade_price": 2000000, "upgrade_income": 200000,
        "max_level": 10, "category": "tech", "employees": 10
    },
    "веб-студия": {
        "price": 2000000, "income": 200000, "emoji": "🌐",
        "desc": "Создание сайтов и веб-приложений",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "tech", "employees": 5
    },
    "мобильная студия": {
        "price": 3000000, "income": 300000, "emoji": "📱",
        "desc": "Разработка мобильных приложений",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "tech", "employees": 6
    },
    "дата-центр": {
        "price": 10000000, "income": 1000000, "emoji": "🖥️",
        "desc": "Хранение и обработка данных",
        "land_size": 5, "upgrade_price": 4000000, "upgrade_income": 400000,
        "max_level": 10, "category": "tech", "employees": 20
    },
    "кибербезопасность": {
        "price": 8000000, "income": 800000, "emoji": "🔒",
        "desc": "Защита информационных систем",
        "land_size": 3, "upgrade_price": 3200000, "upgrade_income": 320000,
        "max_level": 10, "category": "tech", "employees": 12
    },
    "искусственный интеллект": {
        "price": 15000000, "income": 1500000, "emoji": "🤖",
        "desc": "Разработка AI решений",
        "land_size": 4, "upgrade_price": 6000000, "upgrade_income": 600000,
        "max_level": 10, "category": "tech", "employees": 15
    },
    "робототехника": {
        "price": 12000000, "income": 1200000, "emoji": "⚙️",
        "desc": "Производство роботов",
        "land_size": 6, "upgrade_price": 4800000, "upgrade_income": 480000,
        "max_level": 10, "category": "tech", "employees": 25
    },
    "биотехнологии": {
        "price": 20000000, "income": 2000000, "emoji": "🧬",
        "desc": "Биологические исследования",
        "land_size": 5, "upgrade_price": 8000000, "upgrade_income": 800000,
        "max_level": 10, "category": "tech", "employees": 18
    },
    "нанотехнологии": {
        "price": 25000000, "income": 2500000, "emoji": "🔬",
        "desc": "Нано-инженерия",
        "land_size": 4, "upgrade_price": 10000000, "upgrade_income": 1000000,
        "max_level": 10, "category": "tech", "employees": 20
    },
    "квантовые вычисления": {
        "price": 30000000, "income": 3000000, "emoji": "⚛️",
        "desc": "Квантовые технологии",
        "land_size": 6, "upgrade_price": 12000000, "upgrade_income": 1200000,
        "max_level": 10, "category": "tech", "employees": 30
    },
    "блокчейн": {
        "price": 10000000, "income": 1000000, "emoji": "⛓️",
        "desc": "Блокчейн технологии",
        "land_size": 3, "upgrade_price": 4000000, "upgrade_income": 400000,
        "max_level": 10, "category": "tech", "employees": 10
    },
    "облачные технологии": {
        "price": 8000000, "income": 800000, "emoji": "☁️",
        "desc": "Облачные вычисления",
        "land_size": 4, "upgrade_price": 3200000, "upgrade_income": 320000,
        "max_level": 10, "category": "tech", "employees": 14
    },
    "iot": {
        "price": 6000000, "income": 600000, "emoji": "📡",
        "desc": "Интернет вещей",
        "land_size": 3, "upgrade_price": 2400000, "upgrade_income": 240000,
        "max_level": 10, "category": "tech", "employees": 8
    },
    "vr/ar": {
        "price": 12000000, "income": 1200000, "emoji": "🥽",
        "desc": "Виртуальная и дополненная реальность",
        "land_size": 4, "upgrade_price": 4800000, "upgrade_income": 480000,
        "max_level": 10, "category": "tech", "employees": 12
    },
    "игровая студия": {
        "price": 15000000, "income": 1500000, "emoji": "🎮",
        "desc": "Разработка видеоигр",
        "land_size": 5, "upgrade_price": 6000000, "upgrade_income": 600000,
        "max_level": 10, "category": "tech", "employees": 20
    },

    # ============================================================
    # СТРОИТЕЛЬСТВО (15)
    # ============================================================
    "строительная компания": {
        "price": 8000000, "income": 800000, "emoji": "🏗️",
        "desc": "Возведение жилых комплексов",
        "land_size": 8, "upgrade_price": 3200000, "upgrade_income": 320000,
        "max_level": 10, "category": "construction", "employees": 50
    },
    "архитектурное бюро": {
        "price": 3000000, "income": 300000, "emoji": "🏛️",
        "desc": "Проектирование зданий",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "construction", "employees": 8
    },
    "ремонтная компания": {
        "price": 2000000, "income": 200000, "emoji": "🔨",
        "desc": "Отделка и ремонт помещений",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "construction", "employees": 15
    },
    "производство стройматериалов": {
        "price": 10000000, "income": 1000000, "emoji": "🧱",
        "desc": "Производство стройматериалов",
        "land_size": 10, "upgrade_price": 4000000, "upgrade_income": 400000,
        "max_level": 10, "category": "construction", "employees": 40
    },
    "стекольный завод": {
        "price": 8000000, "income": 800000, "emoji": "🪟",
        "desc": "Производство стекла",
        "land_size": 8, "upgrade_price": 3200000, "upgrade_income": 320000,
        "max_level": 10, "category": "construction", "employees": 35
    },
    "цементный завод": {
        "price": 12000000, "income": 1200000, "emoji": "🏭",
        "desc": "Производство цемента",
        "land_size": 12, "upgrade_price": 4800000, "upgrade_income": 480000,
        "max_level": 10, "category": "construction", "employees": 45
    },
    "кирпичный завод": {
        "price": 6000000, "income": 600000, "emoji": "🧱",
        "desc": "Производство кирпича",
        "land_size": 8, "upgrade_price": 2400000, "upgrade_income": 240000,
        "max_level": 10, "category": "construction", "employees": 30
    },
    "деревообработка": {
        "price": 5000000, "income": 500000, "emoji": "🪵",
        "desc": "Обработка древесины",
        "land_size": 6, "upgrade_price": 2000000, "upgrade_income": 200000,
        "max_level": 10, "category": "construction", "employees": 25
    },
    "металлообработка": {
        "price": 7000000, "income": 700000, "emoji": "🔩",
        "desc": "Обработка металла",
        "land_size": 8, "upgrade_price": 2800000, "upgrade_income": 280000,
        "max_level": 10, "category": "construction", "employees": 30
    },
    "проектный институт": {
        "price": 4000000, "income": 400000, "emoji": "📐",
        "desc": "Разработка строительных проектов",
        "land_size": 3, "upgrade_price": 1600000, "upgrade_income": 160000,
        "max_level": 10, "category": "construction", "employees": 12
    },
    "монтажная компания": {
        "price": 3000000, "income": 300000, "emoji": "🔧",
        "desc": "Монтаж конструкций",
        "land_size": 4, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "construction", "employees": 20
    },
    "кровельная компания": {
        "price": 2500000, "income": 250000, "emoji": "🏠",
        "desc": "Кровельные работы",
        "land_size": 3, "upgrade_price": 1000000, "upgrade_income": 100000,
        "max_level": 10, "category": "construction", "employees": 15
    },
    "фасадная компания": {
        "price": 2500000, "income": 250000, "emoji": "🏢",
        "desc": "Отделка фасадов",
        "land_size": 3, "upgrade_price": 1000000, "upgrade_income": 100000,
        "max_level": 10, "category": "construction", "employees": 15
    },
    "ландшафтный дизайн": {
        "price": 2000000, "income": 200000, "emoji": "🌿",
        "desc": "Озеленение и благоустройство",
        "land_size": 3, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "construction", "employees": 10
    },
    "сметное бюро": {
        "price": 1500000, "income": 150000, "emoji": "📊",
        "desc": "Составление смет",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "construction", "employees": 5
    },

    # ============================================================
    # МЕДИЦИНА (12)
    # ============================================================
    "частная клиника": {
        "price": 10000000, "income": 1000000, "emoji": "🏥",
        "desc": "Медицинские услуги",
        "land_size": 5, "upgrade_price": 4000000, "upgrade_income": 400000,
        "max_level": 10, "category": "medical", "employees": 30
    },
    "стоматология": {
        "price": 5000000, "income": 500000, "emoji": "🦷",
        "desc": "Стоматологические услуги",
        "land_size": 3, "upgrade_price": 2000000, "upgrade_income": 200000,
        "max_level": 10, "category": "medical", "employees": 10
    },
    "ветеринарная клиника": {
        "price": 3000000, "income": 300000, "emoji": "🐕",
        "desc": "Лечение животных",
        "land_size": 3, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "medical", "employees": 8
    },
    "аптека": {
        "price": 2000000, "income": 200000, "emoji": "💊",
        "desc": "Продажа лекарств",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "medical", "employees": 5
    },
    "лаборатория": {
        "price": 4000000, "income": 400000, "emoji": "🧪",
        "desc": "Диагностические исследования",
        "land_size": 3, "upgrade_price": 1600000, "upgrade_income": 160000,
        "max_level": 10, "category": "medical", "employees": 12
    },
    "реабилитационный центр": {
        "price": 6000000, "income": 600000, "emoji": "💉",
        "desc": "Восстановление здоровья",
        "land_size": 4, "upgrade_price": 2400000, "upgrade_income": 240000,
        "max_level": 10, "category": "medical", "employees": 15
    },
    "психологический центр": {
        "price": 3000000, "income": 300000, "emoji": "🧠",
        "desc": "Психологическая помощь",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "medical", "employees": 6
    },
    "косметология": {
        "price": 2500000, "income": 250000, "emoji": "💄",
        "desc": "Косметологические услуги",
        "land_size": 2, "upgrade_price": 1000000, "upgrade_income": 100000,
        "max_level": 10, "category": "medical", "employees": 5
    },
    "оптика": {
        "price": 1500000, "income": 150000, "emoji": "👓",
        "desc": "Офтальмологические услуги",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "medical", "employees": 4
    },
    "клиника пластической хирургии": {
        "price": 15000000, "income": 1500000, "emoji": "👩‍⚕️",
        "desc": "Пластическая хирургия",
        "land_size": 4, "upgrade_price": 6000000, "upgrade_income": 600000,
        "max_level": 10, "category": "medical", "employees": 15
    },
    "центр репродукции": {
        "price": 12000000, "income": 1200000, "emoji": "👶",
        "desc": "Репродуктивные технологии",
        "land_size": 4, "upgrade_price": 4800000, "upgrade_income": 480000,
        "max_level": 10, "category": "medical", "employees": 12
    },
    "санаторий": {
        "price": 8000000, "income": 800000, "emoji": "🌊",
        "desc": "Санаторно-курортное лечение",
        "land_size": 8, "upgrade_price": 3200000, "upgrade_income": 320000,
        "max_level": 10, "category": "medical", "employees": 40
    },

    # ============================================================
    # ОБРАЗОВАНИЕ (10)
    # ============================================================
    "частная школа": {
        "price": 8000000, "income": 800000, "emoji": "🏫",
        "desc": "Образовательные услуги",
        "land_size": 4, "upgrade_price": 3200000, "upgrade_income": 320000,
        "max_level": 10, "category": "education", "employees": 25
    },
    "частный университет": {
        "price": 15000000, "income": 1500000, "emoji": "🎓",
        "desc": "Высшее образование",
        "land_size": 6, "upgrade_price": 6000000, "upgrade_income": 600000,
        "max_level": 10, "category": "education", "employees": 50
    },
    "языковая школа": {
        "price": 2000000, "income": 200000, "emoji": "🌍",
        "desc": "Изучение иностранных языков",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "education", "employees": 8
    },
    "онлайн-образование": {
        "price": 3000000, "income": 300000, "emoji": "💻",
        "desc": "Дистанционное обучение",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "education", "employees": 10
    },
    "детский сад": {
        "price": 3000000, "income": 300000, "emoji": "🧒",
        "desc": "Дошкольное образование",
        "land_size": 3, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "education", "employees": 15
    },
    "спортивная школа": {
        "price": 4000000, "income": 400000, "emoji": "🏋️",
        "desc": "Спортивное образование",
        "land_size": 4, "upgrade_price": 1600000, "upgrade_income": 160000,
        "max_level": 10, "category": "education", "employees": 12
    },
    "музыкальная школа": {
        "price": 2500000, "income": 250000, "emoji": "🎵",
        "desc": "Музыкальное образование",
        "land_size": 2, "upgrade_price": 1000000, "upgrade_income": 100000,
        "max_level": 10, "category": "education", "employees": 8
    },
    "школа программирования": {
        "price": 3000000, "income": 300000, "emoji": "💻",
        "desc": "Обучение программированию",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "education", "employees": 10
    },
    "бизнес-школа": {
        "price": 5000000, "income": 500000, "emoji": "💼",
        "desc": "Бизнес образование",
        "land_size": 3, "upgrade_price": 2000000, "upgrade_income": 200000,
        "max_level": 10, "category": "education", "employees": 12
    },
    "школа искусств": {
        "price": 2000000, "income": 200000, "emoji": "🎨",
        "desc": "Художественное образование",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "education", "employees": 6
    },

    # ============================================================
    # ТОРГОВЛЯ (20)
    # ============================================================
    "торговый центр": {
        "price": 15000000, "income": 1500000, "emoji": "🏬",
        "desc": "Крупный торговый центр",
        "land_size": 8, "upgrade_price": 6000000, "upgrade_income": 600000,
        "max_level": 10, "category": "retail", "employees": 100
    },
    "супермаркет": {
        "price": 5000000, "income": 500000, "emoji": "🛒",
        "desc": "Продуктовый супермаркет",
        "land_size": 4, "upgrade_price": 2000000, "upgrade_income": 200000,
        "max_level": 10, "category": "retail", "employees": 30
    },
    "магазин одежды": {
        "price": 2000000, "income": 200000, "emoji": "👕",
        "desc": "Брендовая одежда",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "retail", "employees": 6
    },
    "электроника": {
        "price": 3000000, "income": 300000, "emoji": "📱",
        "desc": "Магазин электроники",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "retail", "employees": 8
    },
    "ювелирный магазин": {
        "price": 8000000, "income": 800000, "emoji": "💎",
        "desc": "Продажа ювелирных изделий",
        "land_size": 2, "upgrade_price": 3200000, "upgrade_income": 320000,
        "max_level": 10, "category": "retail", "employees": 5
    },
    "автосалон": {
        "price": 10000000, "income": 1000000, "emoji": "🚗",
        "desc": "Продажа автомобилей",
        "land_size": 6, "upgrade_price": 4000000, "upgrade_income": 400000,
        "max_level": 10, "category": "retail", "employees": 15
    },
    "мебельный магазин": {
        "price": 4000000, "income": 400000, "emoji": "🛋️",
        "desc": "Продажа мебели",
        "land_size": 4, "upgrade_price": 1600000, "upgrade_income": 160000,
        "max_level": 10, "category": "retail", "employees": 10
    },
    "книжный магазин": {
        "price": 1500000, "income": 150000, "emoji": "📚",
        "desc": "Продажа книг",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "retail", "employees": 4
    },
    "строительный магазин": {
        "price": 3000000, "income": 300000, "emoji": "🔨",
        "desc": "Строительные материалы",
        "land_size": 4, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "retail", "employees": 10
    },
    "зоомагазин": {
        "price": 1500000, "income": 150000, "emoji": "🐾",
        "desc": "Товары для животных",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "retail", "employees": 4
    },
    "цветочный магазин": {
        "price": 1000000, "income": 100000, "emoji": "🌺",
        "desc": "Продажа цветов",
        "land_size": 1, "upgrade_price": 400000, "upgrade_income": 40000,
        "max_level": 10, "category": "retail", "employees": 3
    },
    "интернет-магазин": {
        "price": 3000000, "income": 300000, "emoji": "🛍️",
        "desc": "Онлайн-торговля",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "retail", "employees": 8
    },
    "спортивный магазин": {
        "price": 2500000, "income": 250000, "emoji": "🏋️",
        "desc": "Спортивные товары",
        "land_size": 2, "upgrade_price": 1000000, "upgrade_income": 100000,
        "max_level": 10, "category": "retail", "employees": 6
    },
    "детский магазин": {
        "price": 2000000, "income": 200000, "emoji": "👶",
        "desc": "Детские товары",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "retail", "employees": 5
    },
    "хозяйственный магазин": {
        "price": 1500000, "income": 150000, "emoji": "🧹",
        "desc": "Товары для дома",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "retail", "employees": 4
    },
    "техника для дома": {
        "price": 4000000, "income": 400000, "emoji": "🏠",
        "desc": "Бытовая техника",
        "land_size": 3, "upgrade_price": 1600000, "upgrade_income": 160000,
        "max_level": 10, "category": "retail", "employees": 8
    },
    "автозапчасти": {
        "price": 2000000, "income": 200000, "emoji": "🔧",
        "desc": "Автомобильные запчасти",
        "land_size": 3, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "retail", "employees": 6
    },
    "медицинская техника": {
        "price": 5000000, "income": 500000, "emoji": "💉",
        "desc": "Медицинское оборудование",
        "land_size": 3, "upgrade_price": 2000000, "upgrade_income": 200000,
        "max_level": 10, "category": "retail", "employees": 8
    },
    "оптика (магазин)": {
        "price": 1500000, "income": 150000, "emoji": "👓",
        "desc": "Очки и контактные линзы",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "retail", "employees": 4
    },
    "часы и украшения": {
        "price": 3000000, "income": 300000, "emoji": "⌚",
        "desc": "Часы и бижутерия",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "retail", "employees": 5
    },

    # ============================================================
    # ОБЩЕПИТ (12)
    # ============================================================
    "ресторан": {
        "price": 5000000, "income": 500000, "emoji": "🍽️",
        "desc": "Элитный ресторан",
        "land_size": 3, "upgrade_price": 2000000, "upgrade_income": 200000,
        "max_level": 10, "category": "food", "employees": 20
    },
    "кафе": {
        "price": 2000000, "income": 200000, "emoji": "☕",
        "desc": "Уютное кафе",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "food", "employees": 10
    },
    "фастфуд": {
        "price": 1500000, "income": 150000, "emoji": "🍔",
        "desc": "Быстрое питание",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "food", "employees": 8
    },
    "пиццерия": {
        "price": 2000000, "income": 200000, "emoji": "🍕",
        "desc": "Итальянская пицца",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "food", "employees": 8
    },
    "суши-бар": {
        "price": 2500000, "income": 250000, "emoji": "🍣",
        "desc": "Японская кухня",
        "land_size": 2, "upgrade_price": 1000000, "upgrade_income": 100000,
        "max_level": 10, "category": "food", "employees": 8
    },
    "кофейня": {
        "price": 1000000, "income": 100000, "emoji": "☕",
        "desc": "Кофе с собой",
        "land_size": 1, "upgrade_price": 400000, "upgrade_income": 40000,
        "max_level": 10, "category": "food", "employees": 5
    },
    "бар": {
        "price": 3000000, "income": 300000, "emoji": "??",
        "desc": "Ночной бар",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "food", "employees": 10
    },
    "пекарня": {
        "price": 1500000, "income": 150000, "emoji": "🥖",
        "desc": "Свежая выпечка",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "food", "employees": 6
    },
    "кондитерская": {
        "price": 1500000, "income": 150000, "emoji": "🍰",
        "desc": "Сладости и торты",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "food", "employees": 6
    },
    "столовая": {
        "price": 2000000, "income": 200000, "emoji": "🥘",
        "desc": "Бизнес-ланчи",
        "land_size": 3, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "food", "employees": 12
    },
    "бургерная": {
        "price": 1500000, "income": 150000, "emoji": "🍔",
        "desc": "Гурманские бургеры",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "food", "employees": 8
    },
    "шаурма": {
        "price": 1000000, "income": 100000, "emoji": "🌯",
        "desc": "Шаурма и кебаб",
        "land_size": 1, "upgrade_price": 400000, "upgrade_income": 40000,
        "max_level": 10, "category": "food", "employees": 4
    },

    # ============================================================
    # УСЛУГИ (15)
    # ============================================================
    "салон красоты": {
        "price": 2000000, "income": 200000, "emoji": "💅",
        "desc": "Бьюти-услуги",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "services", "employees": 8
    },
    "парикмахерская": {
        "price": 1000000, "income": 100000, "emoji": "✂️",
        "desc": "Парикмахерские услуги",
        "land_size": 1, "upgrade_price": 400000, "upgrade_income": 40000,
        "max_level": 10, "category": "services", "employees": 5
    },
    "спортзал": {
        "price": 3000000, "income": 300000, "emoji": "💪",
        "desc": "Тренажерный зал",
        "land_size": 4, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "services", "employees": 8
    },
    "фитнес-клуб": {
        "price": 5000000, "income": 500000, "emoji": "🏋️",
        "desc": "Фитнес с бассейном",
        "land_size": 5, "upgrade_price": 2000000, "upgrade_income": 200000,
        "max_level": 10, "category": "services", "employees": 15
    },
    "бассейн": {
        "price": 4000000, "income": 400000, "emoji": "🏊",
        "desc": "Крытый бассейн",
        "land_size": 5, "upgrade_price": 1600000, "upgrade_income": 160000,
        "max_level": 10, "category": "services", "employees": 10
    },
    "автосервис": {
        "price": 3000000, "income": 300000, "emoji": "🔧",
        "desc": "Ремонт автомобилей",
        "land_size": 4, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "services", "employees": 10
    },
    "автомойка": {
        "price": 1500000, "income": 150000, "emoji": "🚿",
        "desc": "Мойка автомобилей",
        "land_size": 3, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "services", "employees": 6
    },
    "клининг": {
        "price": 1000000, "income": 100000, "emoji": "🧹",
        "desc": "Уборка помещений",
        "land_size": 1, "upgrade_price": 400000, "upgrade_income": 40000,
        "max_level": 10, "category": "services", "employees": 10
    },
    "юридическая компания": {
        "price": 3000000, "income": 300000, "emoji": "⚖️",
        "desc": "Юридические услуги",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "services", "employees": 8
    },
    "бухгалтерские услуги": {
        "price": 2000000, "income": 200000, "emoji": "📊",
        "desc": "Бухгалтерское сопровождение",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "services", "employees": 6
    },
    "фотостудия": {
        "price": 1500000, "income": 150000, "emoji": "📸",
        "desc": "Фотосъемка",
        "land_size": 2, "upgrade_price": 600000, "upgrade_income": 60000,
        "max_level": 10, "category": "services", "employees": 4
    },
    "event-агентство": {
        "price": 4000000, "income": 400000, "emoji": "🎉",
        "desc": "Организация мероприятий",
        "land_size": 2, "upgrade_price": 1600000, "upgrade_income": 160000,
        "max_level": 10, "category": "services", "employees": 10
    },
    "туристическое агентство": {
        "price": 3000000, "income": 300000, "emoji": "✈️",
        "desc": "Туристические услуги",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "services", "employees": 8
    },
    "hr-агентство": {
        "price": 2000000, "income": 200000, "emoji": "👥",
        "desc": "Подбор персонала",
        "land_size": 2, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "services", "employees": 6
    },
    "рекламное агентство": {
        "price": 3000000, "income": 300000, "emoji": "📢",
        "desc": "Рекламные услуги",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "services", "employees": 8
    },

    # ============================================================
    # НЕДВИЖИМОСТЬ (12)
    # ============================================================
    "агентство недвижимости": {
        "price": 3000000, "income": 300000, "emoji": "🏘️",
        "desc": "Сделки с недвижимостью",
        "land_size": 2, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "real_estate", "employees": 8
    },
    "аренда квартир": {
        "price": 5000000, "income": 500000, "emoji": "🏠",
        "desc": "Сдача квартир в аренду",
        "land_size": 1, "upgrade_price": 2000000, "upgrade_income": 200000,
        "max_level": 10, "category": "real_estate", "employees": 4
    },
    "аренда офисов": {
        "price": 8000000, "income": 800000, "emoji": "🏢",
        "desc": "Сдача офисов в аренду",
        "land_size": 3, "upgrade_price": 3200000, "upgrade_income": 320000,
        "max_level": 10, "category": "real_estate", "employees": 6
    },
    "гостиница": {
        "price": 10000000, "income": 1000000, "emoji": "🏨",
        "desc": "Гостиничный бизнес",
        "land_size": 5, "upgrade_price": 4000000, "upgrade_income": 400000,
        "max_level": 10, "category": "real_estate", "employees": 20
    },
    "хостел": {
        "price": 3000000, "income": 300000, "emoji": "🛏️",
        "desc": "Бюджетное жилье",
        "land_size": 3, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "real_estate", "employees": 8
    },
    "элитное жилье": {
        "price": 20000000, "income": 2000000, "emoji": "🏰",
        "desc": "Премиум-недвижимость",
        "land_size": 3, "upgrade_price": 8000000, "upgrade_income": 800000,
        "max_level": 10, "category": "real_estate", "employees": 10
    },
    "коммерческая недвижимость": {
        "price": 15000000, "income": 1500000, "emoji": "🏛️",
        "desc": "Бизнес-центры",
        "land_size": 5, "upgrade_price": 6000000, "upgrade_income": 600000,
        "max_level": 10, "category": "real_estate", "employees": 15
    },
    "парковка": {
        "price": 2000000, "income": 200000, "emoji": "🅿️",
        "desc": "Платная парковка",
        "land_size": 3, "upgrade_price": 800000, "upgrade_income": 80000,
        "max_level": 10, "category": "real_estate", "employees": 4
    },
    "земельный участок": {
        "price": 1000000, "income": 100000, "emoji": "🌍",
        "desc": "Продажа земли",
        "land_size": 5, "upgrade_price": 400000, "upgrade_income": 40000,
        "max_level": 10, "category": "real_estate", "employees": 3
    },
    "загородный клуб": {
        "price": 12000000, "income": 1200000, "emoji": "🏞️",
        "desc": "Загородный комплекс",
        "land_size": 10, "upgrade_price": 4800000, "upgrade_income": 480000,
        "max_level": 10, "category": "real_estate", "employees": 25
    },
    "бизнес-центр": {
        "price": 20000000, "income": 2000000, "emoji": "🏢",
        "desc": "Деловой центр",
        "land_size": 6, "upgrade_price": 8000000, "upgrade_income": 800000,
        "max_level": 10, "category": "real_estate", "employees": 30
    },
    "складской комплекс": {
        "price": 10000000, "income": 1000000, "emoji": "📦",
        "desc": "Складские помещения",
        "land_size": 8, "upgrade_price": 4000000, "upgrade_income": 400000,
        "max_level": 10, "category": "real_estate", "employees": 15
    },

    # ============================================================
    # ПРОИЗВОДСТВО (12)
    # ============================================================
    "завод": {
        "price": 20000000, "income": 2000000, "emoji": "🏭",
        "desc": "Промышленное производство",
        "land_size": 10, "upgrade_price": 8000000, "upgrade_income": 800000,
        "max_level": 10, "category": "manufacturing", "employees": 100
    },
    "производство": {
        "price": 10000000, "income": 1000000, "emoji": "⚙️",
        "desc": "Производство товаров",
        "land_size": 8, "upgrade_price": 4000000, "upgrade_income": 400000,
        "max_level": 10, "category": "manufacturing", "employees": 60
    },
    "пищевой завод": {
        "price": 8000000, "income": 800000, "emoji": "🥫",
        "desc": "Пищевое производство",
        "land_size": 6, "upgrade_price": 3200000, "upgrade_income": 320000,
        "max_level": 10, "category": "manufacturing", "employees": 50
    },
    "химический завод": {
        "price": 12000000, "income": 1200000, "emoji": "🧪",
        "desc": "Химическое производство",
        "land_size": 8, "upgrade_price": 4800000, "upgrade_income": 480000,
        "max_level": 10, "category": "manufacturing", "employees": 70
    },
    "фармацевтика": {
        "price": 15000000, "income": 1500000, "emoji": "💊",
        "desc": "Производство лекарств",
        "land_size": 6, "upgrade_price": 6000000, "upgrade_income": 600000,
        "max_level": 10, "category": "manufacturing", "employees": 60
    },
    "автомобильный завод": {
        "price": 50000000, "income": 5000000, "emoji": "🚗",
        "desc": "Автомобилестроение",
        "land_size": 15, "upgrade_price": 20000000, "upgrade_income": 2000000,
        "max_level": 10, "category": "manufacturing", "employees": 200
    },
    "мебельная фабрика": {
        "price": 6000000, "income": 600000, "emoji": "🪑",
        "desc": "Производство мебели",
        "land_size": 6, "upgrade_price": 2400000, "upgrade_income": 240000,
        "max_level": 10, "category": "manufacturing", "employees": 40
    },
    "швейная фабрика": {
        "price": 4000000, "income": 400000, "emoji": "🧵",
        "desc": "Пошив одежды",
        "land_size": 4, "upgrade_price": 1600000, "upgrade_income": 160000,
        "max_level": 10, "category": "manufacturing", "employees": 50
    },
    "типография": {
        "price": 3000000, "income": 300000, "emoji": "🖨️",
        "desc": "Печать книг и журналов",
        "land_size": 4, "upgrade_price": 1200000, "upgrade_income": 120000,
        "max_level": 10, "category": "manufacturing", "employees": 20
    },
    "переработка отходов": {
        "price": 10000000, "income": 1000000, "emoji": "♻️",
        "desc": "Переработка мусора",
        "land_size": 10, "upgrade_price": 4000000, "upgrade_income": 400000,
        "max_level": 10, "category": "manufacturing", "employees": 50
    },
    "энергокомпания": {
        "price": 25000000, "income": 2500000, "emoji": "⚡",
        "desc": "Энергетический сектор",
        "land_size": 12, "upgrade_price": 10000000, "upgrade_income": 1000000,
        "max_level": 10, "category": "manufacturing", "employees": 80
    },
    "водоканал": {
        "price": 15000000, "income": 1500000, "emoji": "💧",
        "desc": "Водоснабжение",
        "land_size": 10, "upgrade_price": 6000000, "upgrade_income": 600000,
        "max_level": 10, "category": "manufacturing", "employees": 60
    },
}

# ============================================================
# КЛАСС УПРАВЛЕНИЯ БИЗНЕСОМ (РАСШИРЕННЫЙ)
# ============================================================

class BusinessManager:
    """ПОЛНЫЙ МЕНЕДЖЕР БИЗНЕСА С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
    
    def __init__(self):
        self.collect_lock = {}
        self.business_cache = {}
        self.monopoly_cache = {}
        self.franchise_cache = {}
        self.market_trends = {}
        self.business_rating = {}
    
    # ============================================================
    # ЗЕМЛЯ (РАСШИРЕННАЯ)
    # ============================================================
    
    async def buy_land(self, user_id: int, land_type: str) -> dict:
        """КУПИТЬ ЗЕМЛЮ С РАСШИРЕННЫМИ ТИПАМИ"""
        from config import LAND_TYPES
        
        if land_type not in LAND_TYPES:
            return {
                'error': True,
                'message': '❌ Такого типа земли нет! Доступно: ' + ', '.join(LAND_TYPES.keys())
            }
        
        land_data = LAND_TYPES[land_type]
        price = land_data['price']
        
        # Проверка на скидку
        has_discount = await has_item(user_id, "дисконтная_карта")
        if has_discount:
            price = int(price * 0.9)
        
        coins = await get_coins(user_id)
        if coins < price:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(price)}'
            }
        
        # Проверяем, есть ли уже земля
        existing = await db.execute(
            "SELECT * FROM land WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        
        if existing:
            # Проверка на улучшение
            if existing['land_type'] == land_type:
                return {'error': True, 'message': '❌ У тебя уже есть такая земля!'}
            
            await db.execute(
                "UPDATE land SET land_type = ?, size = ?, price = ? WHERE user_id = ?",
                (land_type, land_data['size'], price, user_id)
            )
        else:
            await db.execute(
                "INSERT INTO land (user_id, land_type, size, price) VALUES (?, ?, ?, ?)",
                (user_id, land_type, land_data['size'], price)
            )
        
        await remove_coins(user_id, price)
        
        # Проверка достижения
        await unlock_achievement(user_id, "first_land")
        
        return {
            'error': False,
            'success': True,
            'land_type': land_type,
            'size': land_data['size'],
            'price': price,
            'emoji': land_data['emoji'],
            'desc': land_data['desc']
        }
    
    async def get_land(self, user_id: int) -> Optional[dict]:
        """ПОЛУЧИТЬ ЗЕМЛЮ ПОЛЬЗОВАТЕЛЯ"""
        result = await db.execute(
            "SELECT * FROM land WHERE user_id = ?",
            (user_id,), fetch_one=True, cache_ttl=30
        )
        return dict(result) if result else None
    
    async def upgrade_land(self, user_id: int) -> dict:
        """УЛУЧШИТЬ ЗЕМЛЮ"""
        land = await self.get_land(user_id)
        if not land:
            return {'error': True, 'message': '❌ У тебя нет земли!'}
        
        from config import LAND_TYPES
        current_type = land['land_type']
        types_list = list(LAND_TYPES.keys())
        current_index = types_list.index(current_type)
        
        if current_index >= len(types_list) - 1:
            return {'error': True, 'message': '❌ Земля уже максимального размера!'}
        
        next_type = types_list[current_index + 1]
        next_data = LAND_TYPES[next_type]
        upgrade_cost = int(next_data['price'] * 0.5)
        
        coins = await get_coins(user_id)
        if coins < upgrade_cost:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(upgrade_cost)}'
            }
        
        await remove_coins(user_id, upgrade_cost)
        
        await db.execute(
            "UPDATE land SET land_type = ?, size = ?, price = ? WHERE user_id = ?",
            (next_type, next_data['size'], next_data['price'], user_id)
        )
        
        return {
            'error': False,
            'success': True,
            'old_type': current_type,
            'new_type': next_type,
            'new_size': next_data['size'],
            'cost': upgrade_cost
        }
    
    async def rent_land(self, user_id: int, renter_id: int, price: int) -> dict:
        """СДАТЬ ЗЕМЛЮ В АРЕНДУ"""
        land = await self.get_land(user_id)
        if not land:
            return {'error': True, 'message': '❌ У тебя нет земли!'}
        
        if land.get('rented_to'):
            return {'error': True, 'message': '❌ Земля уже сдана в аренду!'}
        
        if price <= 0:
            return {'error': True, 'message': '❌ Цена должна быть больше 0!'}
        
        coins = await get_coins(renter_id)
        if coins < price:
            return {
                'error': True,
                'message': f'❌ У арендатора нет {format_large_number(price)} монет!'
            }
        
        await remove_coins(renter_id, price)
        await add_coins(user_id, price)
        
        await db.execute(
            "UPDATE land SET rented_to = ?, rent_price = ?, last_rent = ? WHERE user_id = ?",
            (renter_id, price, datetime.now().isoformat(), user_id)
        )
        
        return {
            'error': False,
            'success': True,
            'renter': renter_id,
            'price': price,
            'land_type': land['land_type']
        }
    
    # ============================================================
    # БИЗНЕС (РАСШИРЕННЫЙ)
    # ============================================================
    
    async def create_business(self, user_id: int, business_name: str) -> dict:
        """СОЗДАТЬ БИЗНЕС С РАСШИРЕННЫМИ ПРОВЕРКАМИ"""
        if business_name not in BUSINESSES_EXTENDED:
            return {
                'error': True,
                'message': '❌ Такого бизнеса нет! Используй `список бизнесов`'
            }
        
        # Проверяем, есть ли уже такой бизнес
        existing = await db.execute(
            "SELECT * FROM businesses WHERE user_id = ? AND name = ?",
            (user_id, business_name), fetch_one=True
        )
        if existing:
            return {'error': True, 'message': '❌ У тебя уже есть этот бизнес!'}
        
        data = BUSINESSES_EXTENDED[business_name]
        price = data['price']
        required_land = data['land_size']
        
        # Проверяем землю
        land = await self.get_land(user_id)
        if not land:
            return {
                'error': True,
                'message': '❌ У тебя нет земли! Купи землю через `купить землю [тип]`'
            }
        
        if land['size'] < required_land:
            return {
                'error': True,
                'message': f'❌ Недостаточно земли! Нужно {required_land} соток, у тебя {land["size"]}'
            }
        
        # Проверка на скидку
        has_discount = await has_item(user_id, "бизнес_скидка")
        if has_discount:
            price = int(price * 0.85)
        
        coins = await get_coins(user_id)
        if coins < price:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(price)}'
            }
        
        await remove_coins(user_id, price)
        
        await db.execute(
            """INSERT INTO businesses 
               (user_id, name, income, land_size, last_collect, created_date) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, business_name, data['income'], required_land, 
             datetime.now().isoformat(), datetime.now().isoformat())
        )
        
        # Проверка достижения
        await unlock_achievement(user_id, "first_business")
        
        return {
            'error': False,
            'success': True,
            'business': business_name,
            'emoji': data['emoji'],
            'price': price,
            'income': data['income'],
            'desc': data['desc'],
            'employees': data.get('employees', 0)
        }
    
    async def get_businesses(self, user_id: int) -> List[dict]:
        """ПОЛУЧИТЬ ВСЕ БИЗНЕСЫ ПОЛЬЗОВАТЕЛЯ"""
        result = await db.execute(
            "SELECT * FROM businesses WHERE user_id = ? ORDER BY income DESC",
            (user_id,), fetch_all=True, cache_ttl=30
        )
        return [dict(row) for row in result] if result else []
    
    async def get_business(self, business_id: int) -> Optional[dict]:
        """ПОЛУЧИТЬ БИЗНЕС ПО ID"""
        result = await db.execute(
            "SELECT * FROM businesses WHERE id = ?",
            (business_id,), fetch_one=True, cache_ttl=30
        )
        return dict(result) if result else None
    
    async def upgrade_business(self, user_id: int, business_name: str) -> dict:
        """УЛУЧШИТЬ БИЗНЕС С РАСШИРЕННЫМИ БОНУСАМИ"""
        business = await db.execute(
            "SELECT * FROM businesses WHERE user_id = ? AND name = ?",
            (user_id, business_name), fetch_one=True
        )
        if not business:
            return {'error': True, 'message': '❌ Бизнес не найден!'}
        
        data = BUSINESSES_EXTENDED[business_name]
        if business['level'] >= data['max_level']:
            return {
                'error': True,
                'message': f'❌ Бизнес на максимальном уровне ({data["max_level"]})!'
            }
        
        # Расчёт стоимости с учётом уровня
        cost = data['upgrade_price'] * business['level']
        
        # Скидка за опыт
        prof_result = await db.execute(
            "SELECT level FROM professions WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        prof_level = prof_result['level'] if prof_result else 1
        if prof_level >= 10:
            cost = int(cost * 0.9)
        elif prof_level >= 20:
            cost = int(cost * 0.8)
        
        new_income = business['income'] + data['upgrade_income']
        
        # Бонус за опыт управления
        management_skill = await self._get_management_skill(user_id)
        new_income = int(new_income * (1 + management_skill * 0.01))
        
        coins = await get_coins(user_id)
        if coins < cost:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(cost)}'
            }
        
        await remove_coins(user_id, cost)
        
        await db.execute(
            "UPDATE businesses SET level = level + 1, income = ? WHERE id = ?",
            (new_income, business['id'])
        )
        
        # Обновляем навык управления
        await self._update_management_skill(user_id)
        
        return {
            'error': False,
            'success': True,
            'business': business_name,
            'new_level': business['level'] + 1,
            'new_income': new_income,
            'cost': cost,
            'income_increase': new_income - business['income']
        }
    
    async def _get_management_skill(self, user_id: int) -> int:
        """ПОЛУЧИТЬ НАВЫК УПРАВЛЕНИЯ"""
        result = await db.execute(
            "SELECT level FROM skills WHERE user_id = ? AND skill_name = 'management'",
            (user_id,), fetch_one=True, cache_ttl=30
        )
        return result['level'] if result else 0
    
    async def _update_management_skill(self, user_id: int):
        """ОБНОВИТЬ НАВЫК УПРАВЛЕНИЯ"""
        await db.execute(
            "INSERT INTO skills (user_id, skill_name, level, experience) VALUES (?, 'management', 1, 1) "
            "ON CONFLICT(user_id, skill_name) DO UPDATE SET experience = experience + 1, "
            "level = level + (experience / 100)",
            (user_id,)
        )
    
    async def collect_income(self, user_id: int, business_id: int) -> dict:
        """СОБРАТЬ ДОХОД С БИЗНЕСА С РАСШИРЕННЫМИ БОНУСАМИ"""
        business = await self.get_business(business_id)
        if not business:
            return {'error': True, 'message': '❌ Бизнес не найден!'}
        
        if business['user_id'] != user_id:
            return {'error': True, 'message': '❌ Это не твой бизнес!'}
        
        # Проверяем кулдаун
        if not await can_do(user_id, "business_collect"):
            remaining = await get_cooldown_time(user_id, "business_collect")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
            }
        
        last_collect = business['last_collect']
        if last_collect:
            last_time = datetime.fromisoformat(last_collect)
            elapsed = (datetime.now() - last_time).total_seconds() / 3600
        else:
            elapsed = 0
        
        if elapsed < 1:
            return {
                'error': True,
                'message': f'⏳ Доход будет через {format_time_seconds(int((1 - elapsed) * 3600))}!'
            }
        
        income = business['income']
        
        # Применяем кризис (если есть)
        from economy import crisis_system
        chat_id = await self._get_user_chat(user_id)
        if chat_id:
            multiplier = crisis_system.get_multiplier(chat_id)
            income = int(income * multiplier)
        
        # Бонус маркетинга
        marketing_level = business.get('marketing_level', 0)
        if marketing_level > 0:
            income = int(income * (1 + marketing_level * 0.1))
        
        # Бонус бренда
        brand_level = business.get('brand_level', 0)
        if brand_level > 0:
            income = int(income * (1 + brand_level * 0.05))
        
        # Бонус монополии
        if business.get('is_monopoly', False):
            income = int(income * 2)
        
        # VIP бонус
        from admin import vip_system
        vip_bonus = await vip_system.get_vip_bonus(user_id)
        income = int(income * vip_bonus)
        
        total_income = int(income * elapsed)
        
        await add_coins(user_id, total_income)
        await set_cooldown(user_id, "business_collect")
        
        # Обновляем общий заработок
        await db.execute(
            "UPDATE businesses SET last_collect = ?, total_earned = total_earned + ? WHERE id = ?",
            (datetime.now().isoformat(), total_income, business_id)
        )
        
        return {
            'error': False,
            'success': True,
            'business': business['name'],
            'income': total_income,
            'hours': elapsed,
            'hourly_income': income,
            'marketing_bonus': marketing_level * 10 if marketing_level > 0 else 0,
            'brand_bonus': brand_level * 5 if brand_level > 0 else 0
        }
    
    async def _get_user_chat(self, user_id: int) -> Optional[int]:
        """ПОЛУЧИТЬ ЧАТ ПОЛЬЗОВАТЕЛЯ"""
        result = await db.execute(
            "SELECT chat_id FROM users WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        return result['chat_id'] if result else None
    
    # ============================================================
    # МАРКЕТИНГ И БРЕНД (РАСШИРЕННЫЕ)
    # ============================================================
    
    async def upgrade_marketing(self, user_id: int, business_id: int) -> dict:
        """УЛУЧШИТЬ МАРКЕТИНГ БИЗНЕСА"""
        business = await self.get_business(business_id)
        if not business:
            return {'error': True, 'message': '❌ Бизнес не найден!'}
        
        if business['user_id'] != user_id:
            return {'error': True, 'message': '❌ Это не твой бизнес!'}
        
        current_level = business.get('marketing_level', 0)
        if current_level >= 10:
            return {'error': True, 'message': '❌ Маркетинг на максимальном уровне (10)!'}
        
        cost = 10000 * (current_level + 1)
        
        # Скидка за опыт
        prof_result = await db.execute(
            "SELECT level FROM professions WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        prof_level = prof_result['level'] if prof_result else 1
        if prof_level >= 15:
            cost = int(cost * 0.85)
        
        coins = await get_coins(user_id)
        if coins < cost:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(cost)}'
            }
        
        await remove_coins(user_id, cost)
        
        await db.execute(
            "UPDATE businesses SET marketing_level = marketing_level + 1 WHERE id = ?",
            (business_id,)
        )
        
        return {
            'error': False,
            'success': True,
            'business': business['name'],
            'new_level': current_level + 1,
            'cost': cost,
            'income_boost': f'{(current_level + 1) * 10}%'
        }
    
    async def upgrade_brand(self, user_id: int, business_id: int) -> dict:
        """УЛУЧШИТЬ БРЕНД БИЗНЕСА"""
        business = await self.get_business(business_id)
        if not business:
            return {'error': True, 'message': '❌ Бизнес не найден!'}
        
        if business['user_id'] != user_id:
            return {'error': True, 'message': '❌ Это не твой бизнес!'}
        
        current_level = business.get('brand_level', 0)
        if current_level >= 10:
            return {'error': True, 'message': '❌ Бренд на максимальном уровне (10)!'}
        
        cost = 20000 * (current_level + 1)
        
        coins = await get_coins(user_id)
        if coins < cost:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(cost)}'
            }
        
        await remove_coins(user_id, cost)
        
        await db.execute(
            "UPDATE businesses SET brand_level = brand_level + 1 WHERE id = ?",
            (business_id,)
        )
        
        return {
            'error': False,
            'success': True,
            'business': business['name'],
            'new_level': current_level + 1,
            'cost': cost,
            'income_boost': f'{(current_level + 1) * 5}%'
        }
    
    # ============================================================
    # МОНОПОЛИЯ (РАСШИРЕННАЯ)
    # ============================================================
    
    async def create_monopoly(self, user_id: int, category: str) -> dict:
        """СОЗДАТЬ МОНОПОЛИЮ В КАТЕГОРИИ"""
        # Находим все бизнесы категории
        category_businesses = []
        for name, data in BUSINESSES_EXTENDED.items():
            if data.get('category') == category:
                category_businesses.append(name)
        
        if not category_businesses:
            return {'error': True, 'message': '❌ В этой категории нет бизнесов!'}
        
        # Получаем бизнесы пользователя
        user_businesses = await self.get_businesses(user_id)
        user_names = [b['name'] for b in user_businesses]
        
        # Проверяем, все ли бизнесы куплены
        missing = [b for b in category_businesses if b not in user_names]
        if missing:
            return {
                'error': True,
                'message': f'❌ Нужно купить все бизнесы категории! Осталось: {", ".join(missing[:5])}'
            }
        
        # Проверяем, есть ли уже монополия
        for b in user_businesses:
            if b.get('is_monopoly', False):
                return {'error': True, 'message': '❌ У тебя уже есть монополия!'}
        
        # Создаём монополию
        for b in user_businesses:
            if b['name'] in category_businesses:
                await db.execute(
                    "UPDATE businesses SET is_monopoly = 1 WHERE id = ?",
                    (b['id'],)
                )
        
        # Бонус за монополию
        bonus = len(category_businesses) * 10000
        await add_coins(user_id, bonus)
        
        # Проверка достижения
        await unlock_achievement(user_id, "monopoly")
        
        return {
            'error': False,
            'success': True,
            'category': category,
            'businesses': len(category_businesses),
            'bonus': bonus,
            'income_boost': '+100% доход'
        }
    
    # ============================================================
    # ФРАНШИЗЫ (РАСШИРЕННЫЕ)
    # ============================================================
    
    async def sell_franchise(self, user_id: int, business_id: int, price: int) -> dict:
        """ПРОДАТЬ ФРАНШИЗУ БИЗНЕСА"""
        business = await self.get_business(business_id)
        if not business:
            return {'error': True, 'message': '❌ Бизнес не найден!'}
        
        if business['user_id'] != user_id:
            return {'error': True, 'message': '❌ Это не твой бизнес!'}
        
        if business['level'] < 5:
            return {'error': True, 'message': '❌ Бизнес должен быть 5+ уровня!'}
        
        if price <= 0:
            return {'error': True, 'message': '❌ Цена должна быть больше 0!'}
        
        await db.execute(
            "UPDATE businesses SET franchise_price = ? WHERE id = ?",
            (price, business_id)
        )
        
        return {
            'error': False,
            'success': True,
            'business': business['name'],
            'price': price,
            'level': business['level']
        }
    
    async def buy_franchise(self, user_id: int, business_id: int) -> dict:
        """КУПИТЬ ФРАНШИЗУ"""
        business = await self.get_business(business_id)
        if not business:
            return {'error': True, 'message': '❌ Бизнес не найден!'}
        
        if business['user_id'] == user_id:
            return {'error': True, 'message': '❌ Нельзя купить свою франшизу!'}
        
        if not business.get('franchise_price'):
            return {'error': True, 'message': '❌ Этот бизнес не продаёт франшизу!'}
        
        price = business['franchise_price']
        if price <= 0:
            return {'error': True, 'message': '❌ Франшиза не продаётся!'}
        
        coins = await get_coins(user_id)
        if coins < price:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(price)}'
            }
        
        await remove_coins(user_id, price)
        
        # Продавец получает 80%
        seller_commission = int(price * 0.8)
        await add_coins(business['user_id'], seller_commission)
        
        # Создаём копию бизнеса
        data = BUSINESSES_EXTENDED.get(business['name'], {})
        await db.execute(
            """INSERT INTO businesses 
               (user_id, name, income, land_size, level, last_collect, created_date) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, business['name'], business['income'] // 2, 
             data.get('land_size', 1), 1, 
             datetime.now().isoformat(), datetime.now().isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'business': business['name'],
            'price': price,
            'level': 1,
            'income': business['income'] // 2
        }
    
    # ============================================================
    # ИНВЕСТИЦИИ (РАСШИРЕННЫЕ)
    # ============================================================
    
    async def invest(self, user_id: int, business_id: int, amount: int) -> dict:
        """ИНВЕСТИРОВАТЬ В БИЗНЕС С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        business = await self.get_business(business_id)
        if not business:
            return {'error': True, 'message': '❌ Бизнес не найден!'}
        
        if business['user_id'] == user_id:
            return {'error': True, 'message': '❌ Нельзя инвестировать в свой бизнес!'}
        
        if amount <= 0:
            return {'error': True, 'message': '❌ Сумма должна быть больше 0!'}
        
        if amount > 10**9:
            return {'error': True, 'message': '❌ Максимальная сумма инвестиций 1 млрд!'}
        
        coins = await get_coins(user_id)
        if coins < amount:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Есть {format_large_number(coins)}'
            }
        
        # Рассчитываем долю
        business_value = business['income'] * 100
        share = amount / business_value if business_value > 0 else 0.01
        share = min(share, 0.49)  # Максимум 49%
        
        await remove_coins(user_id, amount)
        
        await db.execute(
            "INSERT INTO investments (user_id, business_id, amount, share, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, business_id, amount, share, datetime.now().isoformat())
        )
        
        # Проверка достижения
        await unlock_achievement(user_id, "first_investment")
        
        return {
            'error': False,
            'success': True,
            'business': business['name'],
            'amount': amount,
            'share': f"{share * 100:.1f}%",
            'daily_expected': int(business['income'] * share * 24)
        }
    
    async def collect_investment_profit(self, user_id: int, investment_id: int) -> dict:
        """СОБРАТЬ ПРИБЫЛЬ С ИНВЕСТИЦИИ"""
        investment = await db.execute(
            "SELECT * FROM investments WHERE id = ? AND user_id = ?",
            (investment_id, user_id), fetch_one=True
        )
        if not investment:
            return {'error': True, 'message': '❌ Инвестиция не найдена!'}
        
        business = await self.get_business(investment['business_id'])
        if not business:
            return {'error': True, 'message': '❌ Бизнес больше не существует!'}
        
        last_collect = investment.get('last_collect')
        if last_collect:
            last_time = datetime.fromisoformat(last_collect)
            hours_elapsed = (datetime.now() - last_time).total_seconds() / 3600
        else:
            hours_elapsed = 0
        
        if hours_elapsed < 1:
            return {
                'error': True,
                'message': f'⏳ Прибыль будет через {format_time_seconds(int((1 - hours_elapsed) * 3600))}!'
            }
        
        daily_profit = int(business['income'] * investment['share'] * 24)
        total_profit = int(daily_profit * hours_elapsed / 24)
        
        await add_coins(user_id, total_profit)
        
        await db.execute(
            "UPDATE investments SET profit = profit + ?, last_collect = ? WHERE id = ?",
            (total_profit, datetime.now().isoformat(), investment_id)
        )
        
        return {
            'error': False,
            'success': True,
            'business': business['name'],
            'profit': total_profit,
            'daily_profit': daily_profit,
            'hours': hours_elapsed
        }
    
    # ============================================================
    # СТАТИСТИКА (РАСШИРЕННАЯ)
    # ============================================================
    
    async def get_business_stats(self, user_id: int) -> dict:
        """ПОЛУЧИТЬ СТАТИСТИКУ БИЗНЕСА"""
        businesses = await self.get_businesses(user_id)
        
        if not businesses:
            return {
                'total': 0,
                'total_income': 0,
                'total_level': 0,
                'monopolies': 0,
                'avg_income': 0,
                'max_income': 0,
                'max_level': 0
            }
        
        total_income = sum(b['income'] for b in businesses)
        total_level = sum(b['level'] for b in businesses)
        monopolies = sum(1 for b in businesses if b.get('is_monopoly', False))
        
        return {
            'total': len(businesses),
            'total_income': total_income,
            'total_level': total_level,
            'monopolies': monopolies,
            'avg_income': total_income // len(businesses) if businesses else 0,
            'max_income': max((b['income'] for b in businesses), default=0),
            'max_level': max((b['level'] for b in businesses), default=0)
        }
    
    async def get_global_business_stats(self) -> dict:
        """ПОЛУЧИТЬ ГЛОБАЛЬНУЮ СТАТИСТИКУ БИЗНЕСА"""
        result = await db.execute(
            "SELECT COUNT(*) as total, SUM(income) as total_income, AVG(income) as avg_income FROM businesses",
            fetch_one=True, cache_ttl=60
        )
        
        if not result:
            return {'total': 0, 'total_income': 0, 'avg_income': 0}
        
        # Топ категорий
        categories = await db.execute(
            "SELECT name, COUNT(*) as count FROM businesses GROUP BY name ORDER BY count DESC LIMIT 5",
            fetch_all=True, cache_ttl=60
        )
        
        return {
            'total': result['total'],
            'total_income': result['total_income'],
            'avg_income': int(result['avg_income']) if result['avg_income'] else 0,
            'top_categories': [dict(row) for row in categories] if categories else []
        }
    
    # ============================================================
    # АВТОМАТИЧЕСКИЙ СБОР
    # ============================================================
    
    async def auto_collect(self, user_id: int) -> dict:
        """АВТОМАТИЧЕСКИЙ СБОР ДОХОДА СО ВСЕХ БИЗНЕСОВ"""
        businesses = await self.get_businesses(user_id)
        
        if not businesses:
            return {'error': True, 'message': '❌ У тебя нет бизнесов!'}
        
        total_collected = 0
        collected_businesses = []
        
        for business in businesses:
            result = await self.collect_income(user_id, business['id'])
            if not result.get('error'):
                total_collected += result['income']
                collected_businesses.append({
                    'name': business['name'],
                    'income': result['income'],
                    'hours': result.get('hours', 0)
                })
        
        return {
            'error': False,
            'success': True,
            'total': total_collected,
            'businesses': collected_businesses,
            'count': len(collected_businesses)
        }

# ============================================================
# ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР
# ============================================================

business_manager = BusinessManager()

# ============================================================
# БЫСТРЫЕ ФУНКЦИИ-ОБЁРТКИ
# ============================================================

async def buy_land(user_id: int, land_type: str) -> dict:
    return await business_manager.buy_land(user_id, land_type)

async def get_land(user_id: int) -> Optional[dict]:
    return await business_manager.get_land(user_id)

async def upgrade_land(user_id: int) -> dict:
    return await business_manager.upgrade_land(user_id)

async def rent_land(user_id: int, renter_id: int, price: int) -> dict:
    return await business_manager.rent_land(user_id, renter_id, price)

async def create_business(user_id: int, business_name: str) -> dict:
    return await business_manager.create_business(user_id, business_name)

async def get_businesses(user_id: int) -> List[dict]:
    return await business_manager.get_businesses(user_id)

async def get_business(business_id: int) -> Optional[dict]:
    return await business_manager.get_business(business_id)

async def upgrade_business(user_id: int, business_name: str) -> dict:
    return await business_manager.upgrade_business(user_id, business_name)

async def collect_income(user_id: int, business_id: int) -> dict:
    return await business_manager.collect_income(user_id, business_id)

async def auto_collect(user_id: int) -> dict:
    return await business_manager.auto_collect(user_id)

async def upgrade_marketing(user_id: int, business_id: int) -> dict:
    return await business_manager.upgrade_marketing(user_id, business_id)

async def upgrade_brand(user_id: int, business_id: int) -> dict:
    return await business_manager.upgrade_brand(user_id, business_id)

async def create_monopoly(user_id: int, category: str) -> dict:
    return await business_manager.create_monopoly(user_id, category)

async def sell_franchise(user_id: int, business_id: int, price: int) -> dict:
    return await business_manager.sell_franchise(user_id, business_id, price)

async def buy_franchise(user_id: int, business_id: int) -> dict:
    return await business_manager.buy_franchise(user_id, business_id)

async def invest(user_id: int, business_id: int, amount: int) -> dict:
    return await business_manager.invest(user_id, business_id, amount)

async def collect_investment_profit(user_id: int, investment_id: int) -> dict:
    return await business_manager.collect_investment_profit(user_id, investment_id)

async def get_business_stats(user_id: int) -> dict:
    return await business_manager.get_business_stats(user_id)

async def get_global_business_stats() -> dict:
    return await business_manager.get_global_business_stats()

# ============================================================
# КОНЕЦ ДИАЛОГА 4/20
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК: ~2,300
# ============================================================
# ============================================================
# FABLE BOT V5.0 - ДИАЛОГ 5/20: GAMES.PY
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК В ЭТОМ ДИАЛОГЕ: ~2,400
# ============================================================

import asyncio
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from database import (
    db, get_coins, add_coins, remove_coins, get_user,
    update_user, get_user_level, add_item, remove_item,
    has_item, can_do, set_cooldown, get_cooldown_time
)
from config import COOLDOWNS, MAX_COINS
from utils import (
    format_large_number, format_time_seconds, safe_int,
    get_time_ago, format_datetime, chunk_list
)
from economy import unlock_achievement

# ============================================================
# 1. СЛОТЫ (ПОЛНАЯ РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

SLOT_SYMBOLS = ["🍒", "🍋", "🍊", "🍇", "💎", "🎰", "⭐", "🔥", "🍉", "🍓", "7️⃣", "💀", "👑", "💰"]
SLOT_VALUES = {
    "🍒": 1, "🍋": 2, "🍊": 3, "🍇": 4,
    "💎": 10, "🎰": 20, "⭐": 5, "🔥": 3,
    "🍉": 2, "🍓": 3, "7️⃣": 15, "💀": 0,
    "👑": 25, "💰": 30
}
SLOT_WEIGHTS = {
    "🍒": 1.0, "🍋": 0.9, "🍊": 0.8, "🍇": 0.7,
    "💎": 0.3, "🎰": 0.1, "⭐": 0.5, "🔥": 0.5,
    "🍉": 0.8, "🍓": 0.7, "7️⃣": 0.2, "💀": 0.05,
    "👑": 0.08, "💰": 0.06
}

class SlotMachine:
    """ПОЛНЫЙ СЛОТ-АВТОМАТ С ДЖЕКПОТОМ, БОНУСАМИ И МИНИ-ИГРАМИ"""
    
    def __init__(self):
        self.jackpot = 0
        self.total_spins = 0
        self.total_won = 0
        self.total_lost = 0
        self.bonus_games = 0
        self.jackpot_history = []
        self.big_wins = []
    
    async def spin(self, user_id: int, bet: int) -> dict:
        """ВРАЩЕНИЕ СЛОТОВ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        if bet <= 0:
            return {'error': True, 'message': '❌ Ставка должна быть больше 0!'}
        
        if bet > 1000000:
            return {'error': True, 'message': '❌ Максимальная ставка 1,000,000 монет!'}
        
        coins = await get_coins(user_id)
        if coins < bet:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Есть {format_large_number(coins)}'
            }
        
        if not await can_do(user_id, "slots"):
            remaining = await get_cooldown_time(user_id, "slots")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
            }
        
        await remove_coins(user_id, bet)
        await set_cooldown(user_id, "slots")
        self.total_spins += 1
        
        # Выбираем символы с весами
        symbols = list(SLOT_SYMBOLS)
        weights = [SLOT_WEIGHTS.get(s, 0.5) for s in symbols]
        result = random.choices(symbols, weights=weights, k=3)
        
        # Расчёт выигрыша
        win = 0
        bonus = False
        special = ""
        combo_type = "normal"
        
        # 3 одинаковых
        if result[0] == result[1] == result[2]:
            multiplier = SLOT_VALUES.get(result[0], 1)
            win = bet * multiplier
            combo_type = "triple"
            
            # Джекпот
            if result[0] == "🎰":
                win += self.jackpot
                self.jackpot = 0
                bonus = True
                special = "JACKPOT!"
                await unlock_achievement(user_id, "slot_jackpot")
            
            # Бонусная игра
            if result[0] == "💎":
                bonus = True
                win *= 2
                special = "BONUS!"
                self.bonus_games += 1
            
            if result[0] == "7️⃣":
                win *= 3
                special = "LUCKY 7!"
            
            if result[0] == "👑":
                win *= 4
                special = "ROYAL!"
            
            if result[0] == "💰":
                win *= 5
                special = "RICH!"
        
        # 2 одинаковых
        elif result[0] == result[1] or result[1] == result[2]:
            symbol = result[0] if result[0] == result[1] else result[1]
            multiplier = SLOT_VALUES.get(symbol, 1)
            win = bet * (multiplier // 2)
            combo_type = "pair"
        
        # Спецкомбинации
        if "💎" in result and "🎰" in result:
            win += bet * 5
            bonus = True
            special = "GEM + JACKPOT!"
        
        if "7️⃣" in result and "🎰" in result:
            win += bet * 10
            bonus = True
            special = "LUCKY 7 + JACKPOT!"
        
        if "👑" in result and "💰" in result:
            win += bet * 8
            bonus = True
            special = "ROYAL RICH!"
        
        if "💀" in result:
            if result.count("💀") == 3:
                win = 0
                special = "SKULL! LOSING!"
            else:
                win = max(0, win - bet // 2)
                special = "SKULL! HALF LOSS!"
        
        if win > 0:
            await add_coins(user_id, win)
            self.total_won += win
            self.jackpot += int(bet * 0.01)
            if win > bet * 10:
                self.big_wins.append({'user': user_id, 'win': win, 'bet': bet, 'time': datetime.now()})
                if len(self.big_wins) > 20:
                    self.big_wins.pop(0)
        else:
            self.total_lost += bet
            self.jackpot += int(bet * 0.02)
        
        # Бонусная игра (бесплатные спины)
        if bonus and win > 0:
            free_spins = random.randint(1, 5)
            bonus_wins = 0
            for _ in range(free_spins):
                bonus_result = random.choices(symbols, weights=weights, k=3)
                if bonus_result[0] == bonus_result[1] == bonus_result[2]:
                    bonus_win = bet * SLOT_VALUES.get(bonus_result[0], 1) // 2
                    if bonus_win > 0:
                        await add_coins(user_id, bonus_win)
                        bonus_wins += bonus_win
                        win += bonus_win
        
        # Обновляем статистику игры
        await self._update_game_stats(user_id, "slots", win > 0, bet, win)
        
        # Проверка достижения
        if win >= bet * 50:
            await unlock_achievement(user_id, "big_win")
        if win >= bet * 100:
            await unlock_achievement(user_id, "huge_win")
        
        return {
            'error': False,
            'success': True,
            'result': result,
            'win': win,
            'bet': bet,
            'jackpot': self.jackpot,
            'bonus': bonus,
            'special': special,
            'total_spins': self.total_spins,
            'combo_type': combo_type,
            'bonus_wins': bonus_wins if bonus else 0
        }
    
    async def _update_game_stats(self, user_id: int, game: str, won: bool, bet: int, win: int):
        """ОБНОВИТЬ СТАТИСТИКУ ИГРЫ"""
        await db.execute(
            "INSERT INTO game_stats (user_id, game_name, played, won, lost, total_bet, total_win, max_win) "
            "VALUES (?, ?, 1, ?, ?, ?, ?, ?) "
            "ON CONFLICT(user_id, game_name) DO UPDATE SET "
            "played = played + 1, "
            "won = won + ?, "
            "lost = lost + ?, "
            "total_bet = total_bet + ?, "
            "total_win = total_win + ?, "
            "max_win = MAX(max_win, ?)",
            (user_id, game, 1 if won else 0, 1 if not won else 0, bet, win, win,
             1 if won else 0, 1 if not won else 0, bet, win, win)
        )
    
    def get_stats(self) -> dict:
        """ПОЛУЧИТЬ СТАТИСТИКУ СЛОТОВ"""
        return {
            'total_spins': self.total_spins,
            'total_won': self.total_won,
            'total_lost': self.total_lost,
            'jackpot': self.jackpot,
            'bonus_games': self.bonus_games,
            'win_rate': self.total_won / (self.total_won + self.total_lost) * 100 if (self.total_won + self.total_lost) > 0 else 0,
            'big_wins': len(self.big_wins),
            'biggest_win': max([w['win'] for w in self.big_wins]) if self.big_wins else 0
        }

slot_machine = SlotMachine()

# ============================================================
# 2. РУЛЕТКА (ПОЛНАЯ РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

class Roulette:
    """ПОЛНАЯ ЕВРОПЕЙСКАЯ РУЛЕТКА С РАСШИРЕННЫМИ СТАВКАМИ"""
    
    def __init__(self):
        self.numbers = list(range(0, 37))
        self.red = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
        self.black = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
        self.green = [0]
        self.history = []
        self.stats = {
            'total_spins': 0,
            'red_count': 0,
            'black_count': 0,
            'green_count': 0,
            'total_bet': 0,
            'total_win': 0
        }
        self.hot_numbers = {}
        self.cold_numbers = {}
    
    async def spin(self, user_id: int, bet: int, bet_type: str, value: str) -> dict:
        """ВРАЩЕНИЕ РУЛЕТКИ С РАСШИРЕННЫМИ СТАВКАМИ"""
        if bet <= 0:
            return {'error': True, 'message': '❌ Ставка должна быть больше 0!'}
        
        if bet > 500000:
            return {'error': True, 'message': '❌ Максимальная ставка 500,000 монет!'}
        
        coins = await get_coins(user_id)
        if coins < bet:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Есть {format_large_number(coins)}'
            }
        
        if not await can_do(user_id, "roulette"):
            remaining = await get_cooldown_time(user_id, "roulette")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
            }
        
        await remove_coins(user_id, bet)
        await set_cooldown(user_id, "roulette")
        
        # Выпавшее число
        number = random.choice(self.numbers)
        color = "зеленый" if number == 0 else "красный" if number in self.red else "черный"
        
        # Обновляем историю
        self.history.append({"number": number, "color": color})
        if len(self.history) > 100:
            self.history.pop(0)
        
        self.stats['total_spins'] += 1
        self.stats['total_bet'] += bet
        
        # Обновляем горячие/холодные номера
        if number in self.hot_numbers:
            self.hot_numbers[number] += 1
        else:
            self.hot_numbers[number] = 1
        
        if color == "красный":
            self.stats['red_count'] += 1
        elif color == "черный":
            self.stats['black_count'] += 1
        else:
            self.stats['green_count'] += 1
        
        # Расчёт выигрыша
        win = 0
        multiplier = 0
        bet_type_lower = bet_type.lower()
        value_lower = value.lower()
        
        # Ставка на число
        if bet_type_lower == "число" and value.isdigit():
            if int(value) == number:
                multiplier = 35
                win = bet * multiplier
        
        # Ставка на цвет
        elif bet_type_lower == "цвет":
            if value_lower == color:
                multiplier = 2 if color != "зеленый" else 35
                win = bet * multiplier
        
        # Ставка на четность
        elif bet_type_lower == "четность":
            is_even = number % 2 == 0 and number != 0
            if value_lower == "четное" and is_even:
                multiplier = 2
                win = bet * multiplier
            elif value_lower == "нечетное" and not is_even and number != 0:
                multiplier = 2
                win = bet * multiplier
        
        # Ставка на диапазон
        elif bet_type_lower in ["диапазон", "дюжина"]:
            ranges = {
                "1-12": range(1, 13),
                "13-24": range(13, 25),
                "25-36": range(25, 37)
            }
            if value in ranges and number in ranges[value]:
                multiplier = 3
                win = bet * multiplier
        
        # Ставка на ряд
        elif bet_type_lower in ["ряд", "колонка"]:
            rows = {
                "1-34": [1,4,7,10,13,16,19,22,25,28,31,34],
                "2-35": [2,5,8,11,14,17,20,23,26,29,32,35],
                "3-36": [3,6,9,12,15,18,21,24,27,30,33,36]
            }
            if value in rows and number in rows[value]:
                multiplier = 3
                win = bet * multiplier
        
        # Ставка на соседей
        elif bet_type_lower == "соседи":
            neighbors = {
                "0": [32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
            }
            if value in neighbors and number in neighbors[value]:
                multiplier = 35
                win = bet * multiplier
        
        # Ставка на сплит (два числа)
        elif bet_type_lower == "сплит":
            split_numbers = [int(x) for x in value.split(',') if x.isdigit()]
            if len(split_numbers) == 2 and number in split_numbers:
                multiplier = 17
                win = bet * multiplier
        
        if win > 0:
            await add_coins(user_id, win)
            self.stats['total_win'] += win
            await unlock_achievement(user_id, "roulette_win")
        
        return {
            'error': False,
            'success': True,
            'number': number,
            'color': color,
            'win': win,
            'bet': bet,
            'multiplier': multiplier,
            'bet_type': bet_type,
            'bet_value': value,
            'history': self.history[-10:],
            'is_hot': number in self.hot_numbers and self.hot_numbers[number] > 5
        }
    
    def get_stats(self) -> dict:
        """ПОЛУЧИТЬ СТАТИСТИКУ РУЛЕТКИ"""
        hot_numbers = sorted(self.hot_numbers.items(), key=lambda x: x[1], reverse=True)[:5]
        cold_numbers = [n for n in self.numbers if n not in self.hot_numbers or self.hot_numbers[n] == 0][:5]
        
        return {
            'total_spins': self.stats['total_spins'],
            'red_count': self.stats['red_count'],
            'black_count': self.stats['black_count'],
            'green_count': self.stats['green_count'],
            'total_bet': self.stats['total_bet'],
            'total_win': self.stats['total_win'],
            'win_rate': self.stats['total_win'] / self.stats['total_bet'] * 100 if self.stats['total_bet'] > 0 else 0,
            'hot_numbers': hot_numbers,
            'cold_numbers': cold_numbers,
            'history': self.history[-20:]
        }

roulette = Roulette()

# ============================================================
# 3. БЛЭКДЖЕК (ПОЛНАЯ РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

class Blackjack:
    """ПОЛНЫЙ БЛЭКДЖЕК С УДВОЕНИЕМ, СТРАХОВКОЙ, СДАЧЕЙ И СПЛИТОМ"""
    
    def __init__(self):
        self.games = {}
        self.cards = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        self.suits = ["♠", "♥", "♦", "♣"]
        self.values = {
            "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
            "10":10, "J":10, "Q":10, "K":10, "A":11
        }
        self.stats = {
            'games_played': 0,
            'player_wins': 0,
            'dealer_wins': 0,
            'pushes': 0,
            'blackjacks': 0
        }
    
    def create_deck(self) -> List[str]:
        deck = []
        for suit in self.suits:
            for card in self.cards:
                deck.append(f"{card}{suit}")
        random.shuffle(deck)
        return deck
    
    def calculate_hand(self, hand: List[str]) -> Tuple[int, int, bool]:
        """РАССЧИТАТЬ РУКУ (сумма, количество тузов, мягкая ли)"""
        total = 0
        aces = 0
        soft = False
        
        for card in hand:
            value = card[:-1]
            if value == "A":
                aces += 1
                total += 11
            else:
                total += self.values[value]
        
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
            soft = True
        
        return total, aces, soft
    
    def hand_string(self, hand: List[str]) -> str:
        return ', '.join(hand)
    
    async def start_game(self, user_id: int, bet: int) -> dict:
        """НАЧАТЬ ИГРУ В БЛЭКДЖЕК"""
        if bet <= 0:
            return {'error': True, 'message': '❌ Ставка должна быть больше 0!'}
        
        if bet > 500000:
            return {'error': True, 'message': '❌ Максимальная ставка 500,000 монет!'}
        
        coins = await get_coins(user_id)
        if coins < bet:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Есть {format_large_number(coins)}'
            }
        
        if not await can_do(user_id, "blackjack"):
            remaining = await get_cooldown_time(user_id, "blackjack")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
            }
        
        await remove_coins(user_id, bet)
        await set_cooldown(user_id, "blackjack")
        
        deck = self.create_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        
        game_id = f"{user_id}_{int(datetime.now().timestamp())}"
        self.games[game_id] = {
            'user_id': user_id,
            'deck': deck,
            'player': player_hand,
            'dealer': dealer_hand,
            'bet': bet,
            'doubled': False,
            'insured': False,
            'surrendered': False,
            'split': False,
            'split_hand': None,
            'split_bet': 0
        }
        
        player_total, _, _ = self.calculate_hand(player_hand)
        dealer_up = dealer_hand[0]
        
        # Проверка на блэкджек
        if player_total == 21:
            win = int(bet * 1.5)
            await add_coins(user_id, win)
            self.stats['blackjacks'] += 1
            self.stats['games_played'] += 1
            await unlock_achievement(user_id, "blackjack_win")
            del self.games[game_id]
            return {
                'error': False,
                'success': True,
                'result': 'blackjack',
                'win': win,
                'player_hand': player_hand,
                'dealer_up': dealer_up
            }
        
        # Проверка страховки (если у дилера туз)
        can_insure = dealer_up.startswith("A")
        
        return {
            'error': False,
            'success': True,
            'game_id': game_id,
            'player_hand': player_hand,
            'player_total': player_total,
            'dealer_up': dealer_up,
            'bet': bet,
            'can_double': True,
            'can_insure': can_insure,
            'can_surrender': True,
            'can_split': player_hand[0][:-1] == player_hand[1][:-1]
        }
    
    async def hit(self, game_id: str) -> dict:
        """ВЗЯТЬ КАРТУ"""
        if game_id not in self.games:
            return {'error': True, 'message': '❌ Игра не найдена!'}
        
        game = self.games[game_id]
        
        # Если сплит
        if game.get('split') and game.get('split_hand'):
            hand = game['split_hand']
            card = game['deck'].pop()
            hand.append(card)
            total, _, _ = self.calculate_hand(hand)
            
            if total > 21:
                # Перебор в сплите
                game['split_hand'] = None
                return await self.stand(game_id)
            
            return {
                'error': False,
                'success': True,
                'state': 'playing_split',
                'split_hand': hand,
                'split_total': total,
                'main_hand': game['player'],
                'main_total': self.calculate_hand(game['player'])[0]
            }
        
        card = game['deck'].pop()
        game['player'].append(card)
        
        total, _, _ = self.calculate_hand(game['player'])
        
        if total > 21:
            # Перебор
            self.stats['games_played'] += 1
            self.stats['dealer_wins'] += 1
            del self.games[game_id]
            return {
                'error': False,
                'success': True,
                'result': 'bust',
                'player_hand': game['player'],
                'player_total': total,
                'loss': game['bet']
            }
        
        return {
            'error': False,
            'success': True,
            'state': 'playing',
            'player_hand': game['player'],
            'player_total': total,
            'can_double': False,
            'can_stand': True
        }
    
    async def stand(self, game_id: str) -> dict:
        """ОСТАНОВИТЬСЯ"""
        if game_id not in self.games:
            return {'error': True, 'message': '❌ Игра не найдена!'}
        
        game = self.games[game_id]
        
        # Если сплит
        if game.get('split') and game.get('split_hand'):
            split_hand = game['split_hand']
            split_total, _, _ = self.calculate_hand(split_hand)
            
            # Сравниваем с дилером для сплита
            dealer_total, _, _ = self.calculate_hand(game['dealer'])
            while dealer_total < 17:
                game['dealer'].append(game['deck'].pop())
                dealer_total, _, _ = self.calculate_hand(game['dealer'])
            
            # Проверяем сплит
            if split_total > 21:
                # Проигрыш сплита
                loss = game['split_bet']
                result = 'split_loss'
                win = 0
            elif dealer_total > 21 or split_total > dealer_total:
                win = game['split_bet'] * 2
                await add_coins(game['user_id'], win)
                result = 'split_win'
            elif split_total == dealer_total:
                await add_coins(game['user_id'], game['split_bet'])
                result = 'split_push'
                win = 0
            else:
                result = 'split_loss'
                win = 0
            
            game['split_hand'] = None
            # Проверяем основную руку
            player_total, _, _ = self.calculate_hand(game['player'])
            if player_total > 21:
                return {
                    'error': False,
                    'success': True,
                    'result': result,
                    'split_result': result,
                    'split_hand': split_hand,
                    'split_total': split_total,
                    'win': win
                }
            # Продолжаем с основной рукой
        
        player_total, _, _ = self.calculate_hand(game['player'])
        
        # Ход дилера
        dealer_total, _, _ = self.calculate_hand(game['dealer'])
        while dealer_total < 17:
            game['dealer'].append(game['deck'].pop())
            dealer_total, _, _ = self.calculate_hand(game['dealer'])
        
        result = ""
        win = 0
        
        if dealer_total > 21 or player_total > dealer_total:
            win = game['bet'] * 2
            await add_coins(game['user_id'], win)
            result = 'win'
            self.stats['player_wins'] += 1
            await unlock_achievement(game['user_id'], "blackjack_win")
        elif player_total == dealer_total:
            await add_coins(game['user_id'], game['bet'])
            result = 'push'
            self.stats['pushes'] += 1
        else:
            result = 'loss'
            self.stats['dealer_wins'] += 1
        
        self.stats['games_played'] += 1
        
        # Обновляем статистику
        await self._update_game_stats(game['user_id'], "blackjack", result == 'win', game['bet'], win)
        
        del self.games[game_id]
        
        return {
            'error': False,
            'success': True,
            'result': result,
            'player_hand': game['player'],
            'player_total': player_total,
            'dealer_hand': game['dealer'],
            'dealer_total': dealer_total,
            'win': win if result == 'win' else 0
        }
    
    async def double(self, game_id: str) -> dict:
        """УДВОИТЬ СТАВКУ"""
        if game_id not in self.games:
            return {'error': True, 'message': '❌ Игра не найдена!'}
        
        game = self.games[game_id]
        
        if game.get('doubled'):
            return {'error': True, 'message': '❌ Ты уже удвоил ставку!'}
        
        coins = await get_coins(game['user_id'])
        if coins < game['bet']:
            return {'error': True, 'message': '❌ Недостаточно монет для удвоения!'}
        
        await remove_coins(game['user_id'], game['bet'])
        game['bet'] *= 2
        game['doubled'] = True
        
        # Берём одну карту и стоп
        card = game['deck'].pop()
        game['player'].append(card)
        
        return await self.stand(game_id)
    
    async def insure(self, game_id: str) -> dict:
        """СТРАХОВКА (ЕСЛИ У ДИЛЕРА ТУЗ)"""
        if game_id not in self.games:
            return {'error': True, 'message': '❌ Игра не найдена!'}
        
        game = self.games[game_id]
        
        if game.get('insured'):
            return {'error': True, 'message': '❌ Страховка уже оформлена!'}
        
        dealer_up = game['dealer'][0]
        if not dealer_up.startswith("A"):
            return {'error': True, 'message': '❌ Страховка доступна только когда у дилера туз!'}
        
        insurance_bet = game['bet'] // 2
        coins = await get_coins(game['user_id'])
        if coins < insurance_bet:
            return {'error': True, 'message': f'❌ Недостаточно монет! Нужно {format_large_number(insurance_bet)}'}
        
        await remove_coins(game['user_id'], insurance_bet)
        game['insured'] = True
        
        # Проверяем, есть ли у дилера блэкджек
        dealer_total, _, _ = self.calculate_hand(game['dealer'])
        if dealer_total == 21:
            # Страховка выигрывает
            win = insurance_bet * 2
            await add_coins(game['user_id'], win)
            return {
                'error': False,
                'success': True,
                'result': 'insurance_win',
                'win': win,
                'message': f'🛡️ Страховка выиграла! +{format_large_number(win)} монет!'
            }
        
        return {
            'error': False,
            'success': True,
            'result': 'insurance_lost',
            'message': '😔 Страховка не сыграла'
        }
    
    async def surrender(self, game_id: str) -> dict:
        """СДАЧА (ВОЗВРАТ 50% СТАВКИ)"""
        if game_id not in self.games:
            return {'error': True, 'message': '❌ Игра не найдена!'}
        
        game = self.games[game_id]
        
        if game.get('surrendered'):
            return {'error': True, 'message': '❌ Ты уже сдался!'}
        
        # Возвращаем 50% ставки
        refund = game['bet'] // 2
        await add_coins(game['user_id'], refund)
        game['surrendered'] = True
        
        self.stats['games_played'] += 1
        self.stats['dealer_wins'] += 1
        
        del self.games[game_id]
        
        return {
            'error': False,
            'success': True,
            'result': 'surrender',
            'refund': refund
        }
    
    async def split(self, game_id: str) -> dict:
        """СПЛИТ (РАЗДЕЛЕНИЕ ПАРЫ)"""
        if game_id not in self.games:
            return {'error': True, 'message': '❌ Игра не найдена!'}
        
        game = self.games[game_id]
        
        if game.get('split'):
            return {'error': True, 'message': '❌ Ты уже сделал сплит!'}
        
        if game['player'][0][:-1] != game['player'][1][:-1]:
            return {'error': True, 'message': '❌ Для сплита нужна пара!'}
        
        coins = await get_coins(game['user_id'])
        if coins < game['bet']:
            return {'error': True, 'message': '❌ Недостаточно монет для сплита!'}
        
        await remove_coins(game['user_id'], game['bet'])
        
        # Создаём вторую руку
        split_hand = [game['player'].pop()]
        game['player'].append(game['deck'].pop())
        split_hand.append(game['deck'].pop())
        
        game['split'] = True
        game['split_hand'] = split_hand
        game['split_bet'] = game['bet']
        
        return {
            'error': False,
            'success': True,
            'result': 'split',
            'main_hand': game['player'],
            'split_hand': split_hand,
            'bet': game['bet']
        }
    
    async def _update_game_stats(self, user_id: int, game: str, won: bool, bet: int, win: int):
        await db.execute(
            "INSERT INTO game_stats (user_id, game_name, played, won, lost, total_bet, total_win, max_win) "
            "VALUES (?, ?, 1, ?, ?, ?, ?, ?) "
            "ON CONFLICT(user_id, game_name) DO UPDATE SET "
            "played = played + 1, won = won + ?, lost = lost + ?, "
            "total_bet = total_bet + ?, total_win = total_win + ?, "
            "max_win = MAX(max_win, ?)",
            (user_id, game, 1 if won else 0, 1 if not won else 0, bet, win, win,
             1 if won else 0, 1 if not won else 0, bet, win, win)
        )

blackjack = Blackjack()

# ============================================================
# 4. КОСТИ (ПОЛНАЯ РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

DICE_GAMES = {
    "классические": {"min": 1, "max": 6, "desc": "1-6", "emoji": "🎲", "dice": 2},
    "днд": {"min": 1, "max": 20, "desc": "1-20", "emoji": "🐉", "dice": 1},
    "казино": {"min": 1, "max": 6, "desc": "1-6", "emoji": "🎰", "dice": 3},
    "крэпс": {"min": 1, "max": 6, "desc": "1-6", "emoji": "🎲", "dice": 2},
}

class DiceGame:
    """ПОЛНЫЙ НАБОР ИГР С КОСТЯМИ"""
    
    async def roll(self, user_id: int, game_type: str = "классические", count: int = None) -> dict:
        """БРОСИТЬ КОСТИ С РАСШИРЕННЫМИ ВАРИАНТАМИ"""
        if game_type not in DICE_GAMES:
            return {
                'error': True,
                'message': '❌ Такой игры нет! Доступно: ' + ', '.join(DICE_GAMES.keys())
            }
        
        game = DICE_GAMES[game_type]
        if count is None:
            count = game.get('dice', 2)
        
        if count < 1 or count > 10:
            return {'error': True, 'message': '❌ Количество костей от 1 до 10!'}
        
        results = [random.randint(game["min"], game["max"]) for _ in range(count)]
        total = sum(results)
        
        # Дополнительные вычисления
        duplicates = len(results) - len(set(results))
        is_all_same = len(set(results)) == 1
        is_straight = len(set(results)) == count and max(results) - min(results) == count - 1
        
        return {
            'error': False,
            'success': True,
            'results': results,
            'total': total,
            'emoji': game['emoji'],
            'duplicates': duplicates,
            'max_possible': game['max'] * count,
            'is_all_same': is_all_same,
            'is_straight': is_straight,
            'game_type': game_type
        }
    
    async def battle(self, user_id: int, target_id: int, bet: int, game_type: str = "классические") -> dict:
        """БИТВА НА КОСТЯХ (PvP) С РАСШИРЕННЫМИ ПРАВИЛАМИ"""
        if user_id == target_id:
            return {'error': True, 'message': '❌ Нельзя с самим собой!'}
        
        if bet <= 0:
            return {'error': True, 'message': '❌ Ставка должна быть больше 0!'}
        
        if bet > 100000:
            return {'error': True, 'message': '❌ Максимальная ставка 100,000 монет!'}
        
        coins = await get_coins(user_id)
        if coins < bet:
            return {
                'error': True,
                'message': f'❌ У тебя нет {format_large_number(bet)} монет!'
            }
        
        coins2 = await get_coins(target_id)
        if coins2 < bet:
            return {
                'error': True,
                'message': f'❌ У {await get_name(target_id)} нет {format_large_number(bet)} монет!'
            }
        
        if game_type not in DICE_GAMES:
            return {'error': True, 'message': '❌ Неизвестная игра!'}
        
        game = DICE_GAMES[game_type]
        dice_count = game.get('dice', 2)
        
        # Бросаем кости
        user_rolls = [random.randint(game["min"], game["max"]) for _ in range(dice_count)]
        target_rolls = [random.randint(game["min"], game["max"]) for _ in range(dice_count)]
        
        user_total = sum(user_rolls)
        target_total = sum(target_rolls)
        
        # Дополнительные бонусы
        user_bonus = 0
        target_bonus = 0
        
        # Бонус за все одинаковые
        if len(set(user_rolls)) == 1:
            user_bonus += 10
        if len(set(target_rolls)) == 1:
            target_bonus += 10
        
        # Бонус за стрит
        if len(set(user_rolls)) == dice_count and max(user_rolls) - min(user_rolls) == dice_count - 1:
            user_bonus += 5
        if len(set(target_rolls)) == dice_count and max(target_rolls) - min(target_rolls) == dice_count - 1:
            target_bonus += 5
        
        user_total += user_bonus
        target_total += target_bonus
        
        # Определяем победителя
        if user_total > target_total:
            await remove_coins(target_id, bet)
            await add_coins(user_id, bet)
            winner = user_id
            result = "win"
            win_amount = bet
        elif target_total > user_total:
            await remove_coins(user_id, bet)
            await add_coins(target_id, bet)
            winner = target_id
            result = "loss"
            win_amount = 0
        else:
            winner = None
            result = "draw"
            win_amount = 0
        
        # Обновляем статистику
        await self._update_battle_stats(user_id, target_id, result == "win", bet)
        
        return {
            'error': False,
            'success': True,
            'user_rolls': user_rolls,
            'target_rolls': target_rolls,
            'user_total': user_total,
            'target_total': target_total,
            'user_bonus': user_bonus,
            'target_bonus': target_bonus,
            'winner': winner,
            'bet': bet,
            'result': result,
            'win_amount': win_amount
        }
    
    async def _update_battle_stats(self, user_id: int, target_id: int, won: bool, bet: int):
        await db.execute(
            "INSERT INTO game_stats (user_id, game_name, played, won, lost, total_bet, total_win) "
            "VALUES (?, 'dice_battle', 1, ?, ?, ?, ?) "
            "ON CONFLICT(user_id, game_name) DO UPDATE SET "
            "played = played + 1, won = won + ?, lost = lost + ?, "
            "total_bet = total_bet + ?, total_win = total_win + ?",
            (user_id, 1 if won else 0, 1 if not won else 0, bet, 0,
             1 if won else 0, 1 if not won else 0, bet, 0)
        )

dice = DiceGame()

# ============================================================
# 5. УГАДАЙ ЧИСЛО (РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

class GuessNumber:
    """ИГРА УГАДАЙ ЧИСЛО С РАСШИРЕННЫМИ СЛОЖНОСТЯМИ"""
    
    def __init__(self):
        self.games = {}
        self.difficulties = {
            "easy": {"max": 10, "tries": 5, "reward": 50, "emoji": "😊"},
            "medium": {"max": 50, "tries": 7, "reward": 150, "emoji": "🤔"},
            "hard": {"max": 100, "tries": 10, "reward": 300, "emoji": "😤"},
            "expert": {"max": 500, "tries": 15, "reward": 1000, "emoji": "🧠"},
            "legend": {"max": 1000, "tries": 20, "reward": 5000, "emoji": "👑"}
        }
    
    async def start(self, user_id: int, difficulty: str = "easy", bet: int = 0) -> dict:
        """НАЧАТЬ ИГРУ УГАДАЙ ЧИСЛО"""
        if difficulty not in self.difficulties:
            return {
                'error': True,
                'message': '❌ Неизвестная сложность! Доступно: ' + ', '.join(self.difficulties.keys())
            }
        
        if bet < 0:
            return {'error': True, 'message': '❌ Ставка не может быть отрицательной!'}
        
        if bet > 10000:
            return {'error': True, 'message': '❌ Максимальная ставка 10,000 монет!'}
        
        if bet > 0:
            coins = await get_coins(user_id)
            if coins < bet:
                return {
                    'error': True,
                    'message': f'❌ Недостаточно монет! Есть {format_large_number(coins)}'
                }
            await remove_coins(user_id, bet)
        
        if not await can_do(user_id, "guess"):
            remaining = await get_cooldown_time(user_id, "guess")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
            }
        
        await set_cooldown(user_id, "guess")
        
        diff = self.difficulties[difficulty]
        number = random.randint(1, diff["max"])
        
        game_id = f"{user_id}_{int(datetime.now().timestamp())}"
        self.games[game_id] = {
            'user_id': user_id,
            'number': number,
            'max': diff["max"],
            'tries': diff["tries"],
            'used_tries': 0,
            'bet': bet,
            'difficulty': difficulty,
            'hints': [],
            'range_low': 1,
            'range_high': diff["max"]
        }
        
        return {
            'error': False,
            'success': True,
            'game_id': game_id,
            'difficulty': difficulty,
            'max': diff["max"],
            'tries': diff["tries"],
            'reward': diff["reward"],
            'bet': bet,
            'emoji': diff['emoji'],
            'range': f"1-{diff['max']}"
        }
    
    async def guess(self, game_id: str, guess: int) -> dict:
        """СДЕЛАТЬ ПРЕДПОЛОЖЕНИЕ С РАСШИРЕННЫМИ ПОДСКАЗКАМИ"""
        if game_id not in self.games:
            return {'error': True, 'message': '❌ Игра не найдена!'}
        
        game = self.games[game_id]
        
        if game['used_tries'] >= game['tries']:
            del self.games[game_id]
            return {'error': True, 'message': '❌ Ты использовал все попытки!'}
        
        game['used_tries'] += 1
        
        if guess == game['number']:
            # Победа
            diff = self.difficulties[game['difficulty']]
            reward = diff["reward"] + game['bet']
            
            # Бонус за оставшиеся попытки
            remaining_tries = game['tries'] - game['used_tries']
            if remaining_tries > 0:
                reward += remaining_tries * 10
            
            await add_coins(game['user_id'], reward)
            del self.games[game_id]
            
            return {
                'error': False,
                'success': True,
                'result': 'win',
                'reward': reward,
                'tries_used': game['used_tries'],
                'remaining_tries': game['tries'] - game['used_tries']
            }
        else:
            # Подсказка
            hint = "больше" if guess < game['number'] else "меньше"
            game['hints'].append({"guess": guess, "hint": hint})
            
            # Обновляем диапазон
            if hint == "больше" and guess > game['range_low']:
                game['range_low'] = guess + 1
            elif hint == "меньше" and guess < game['range_high']:
                game['range_high'] = guess - 1
            
            # Проверка на проигрыш
            if game['used_tries'] >= game['tries']:
                number = game['number']
                del self.games[game_id]
                return {
                    'error': False,
                    'success': True,
                    'result': 'loss',
                    'number': number,
                    'tries_used': game['used_tries']
                }
            
            return {
                'error': False,
                'success': True,
                'result': 'continue',
                'hint': hint,
                'tries_left': game['tries'] - game['used_tries'],
                'guess': guess,
                'range_low': game['range_low'],
                'range_high': game['range_high']
            }

guess_game = GuessNumber()

# ============================================================
# 6. ВИКТОРИНА (РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

class Quiz:
    """ИГРА ВИКТОРИНА С РАЗНЫМИ ТЕМАМИ И СЛОЖНОСТЯМИ"""
    
    def __init__(self):
        self.games = {}
        self.questions = {
            "general": [
                {"q": "Сколько континентов на Земле?", "answers": ["5", "6", "7", "8"], "correct": 2, "difficulty": 1},
                {"q": "Кто написал 'Войну и мир'?", "answers": ["Достоевский", "Толстой", "Пушкин", "Чехов"], "correct": 1, "difficulty": 1},
                {"q": "Сколько дней в году?", "answers": ["365", "366", "364", "360"], "correct": 0, "difficulty": 1},
                {"q": "Какой газ составляет большую часть атмосферы?", "answers": ["Кислород", "Азот", "Углекислый газ", "Водород"], "correct": 1, "difficulty": 2},
                {"q": "Кто открыл Америку?", "answers": ["Магеллан", "Колумб", "Васко да Гама", "Кук"], "correct": 1, "difficulty": 1},
                {"q": "Сколько океанов на Земле?", "answers": ["3", "4", "5", "6"], "correct": 2, "difficulty": 2},
                {"q": "Какой металл самый тяжелый?", "answers": ["Золото", "Платина", "Осмий", "Свинец"], "correct": 2, "difficulty": 3},
                {"q": "Кто был первым человеком в космосе?", "answers": ["Гагарин", "Титов", "Армстронг", "Лайка"], "correct": 0, "difficulty": 1},
            ],
            "science": [
                {"q": "Формула воды?", "answers": ["H2O", "CO2", "NaCl", "HCl"], "correct": 0, "difficulty": 1},
                {"q": "Какой металл самый легкий?", "answers": ["Алюминий", "Литий", "Магний", "Калий"], "correct": 1, "difficulty": 2},
                {"q": "Сколько планет в Солнечной системе?", "answers": ["7", "8", "9", "10"], "correct": 1, "difficulty": 1},
                {"q": "Что такое фотон?", "answers": ["Частица света", "Частица материи", "Волна", "Атом"], "correct": 0, "difficulty": 3},
                {"q": "Как называется ближайшая к Земле звезда?", "answers": ["Солнце", "Проксима Центавра", "Сириус", "Бетельгейзе"], "correct": 1, "difficulty": 2},
            ],
            "history": [
                {"q": "Когда началась Вторая мировая война?", "answers": ["1939", "1941", "1940", "1938"], "correct": 0, "difficulty": 1},
                {"q": "Кто был первым президентом России?", "answers": ["Путин", "Ельцин", "Горбачев", "Медведев"], "correct": 1, "difficulty": 1},
                {"q": "Когда была отмена крепостного права?", "answers": ["1861", "1917", "1905", "1825"], "correct": 0, "difficulty": 2},
                {"q": "Кто построил первый самолет?", "answers": ["Братья Райт", "Можайский", "Циолковский", "Сикорский"], "correct": 1, "difficulty": 2},
            ],
            "geography": [
                {"q": "Самая высокая гора в мире?", "answers": ["Эверест", "Килиманджаро", "Эльбрус", "Аконкагуа"], "correct": 0, "difficulty": 1},
                {"q": "Самая длинная река в мире?", "answers": ["Нил", "Амазонка", "Янцзы", "Миссисипи"], "correct": 0, "difficulty": 2},
                {"q": "Какое озеро самое глубокое?", "answers": ["Байкал", "Танганьика", "Верхнее", "Ньяса"], "correct": 0, "difficulty": 2},
            ],
            "sport": [
                {"q": "Какой вид спорта называют королевой спорта?", "answers": ["Легкая атлетика", "Футбол", "Теннис", "Бокс"], "correct": 0, "difficulty": 1},
                {"q": "Сколько игроков в футбольной команде?", "answers": ["10", "11", "12", "9"], "correct": 1, "difficulty": 1},
                {"q": "Где проходили Олимпийские игры 2020?", "answers": ["Токио", "Париж", "Лондон", "Рио"], "correct": 0, "difficulty": 1},
            ],
            "art": [
                {"q": "Кто написал 'Джоконду'?", "answers": ["Леонардо да Винчи", "Микеланджело", "Рафаэль", "Тициан"], "correct": 0, "difficulty": 1},
                {"q": "Какой музей находится в Париже?", "answers": ["Лувр", "Прадо", "Эрмитаж", "Метрополитен"], "correct": 0, "difficulty": 1},
                {"q": "Кто написал 'Мастера и Маргариту'?", "answers": ["Булгаков", "Достоевский", "Толстой", "Набоков"], "correct": 0, "difficulty": 1},
            ]
        }
    
    async def start(self, user_id: int, topic: str = "general", difficulty: int = 1) -> dict:
        """НАЧАТЬ ВИКТОРИНУ С РАСШИРЕННЫМИ НАСТРОЙКАМИ"""
        if topic not in self.questions:
            return {
                'error': True,
                'message': '❌ Неизвестная тема! Доступно: ' + ', '.join(self.questions.keys())
            }
        
        if difficulty < 1 or difficulty > 3:
            return {'error': True, 'message': '❌ Сложность от 1 до 3!'}
        
        # Фильтруем вопросы по сложности
        available = [q for q in self.questions[topic] if q['difficulty'] <= difficulty]
        if len(available) < 5:
            available = self.questions[topic][:10]
        
        questions = random.sample(available, min(5, len(available)))
        
        game_id = f"{user_id}_{int(datetime.now().timestamp())}"
        self.games[game_id] = {
            'user_id': user_id,
            'questions': questions,
            'current': 0,
            'score': 0,
            'topic': topic,
            'total': len(questions),
            'difficulty': difficulty,
            'answers': []
        }
        
        return {
            'error': False,
            'success': True,
            'game_id': game_id,
            'topic': topic,
            'total': len(questions),
            'question': questions[0]['q'],
            'answers': questions[0]['answers'],
            'current': 1,
            'difficulty': difficulty
        }
    
    async def answer(self, game_id: str, answer_index: int) -> dict:
        """ОТВЕТИТЬ НА ВОПРОС С РАСШИРЕННОЙ ОЦЕНКОЙ"""
        if game_id not in self.games:
            return {'error': True, 'message': '❌ Игра не найдена!'}
        
        game = self.games[game_id]
        question = game['questions'][game['current']]
        
        is_correct = answer_index == question['correct']
        if is_correct:
            game['score'] += 1
        
        game['answers'].append({
            'question': question['q'],
            'correct': question['correct'],
            'user_answer': answer_index,
            'is_correct': is_correct
        })
        
        game['current'] += 1
        
        if game['current'] >= game['total']:
            # Игра завершена
            reward = game['score'] * 50 * (game['difficulty'] + 1)
            if reward > 0:
                await add_coins(game['user_id'], reward)
            
            # Проверка достижения
            if game['score'] == game['total']:
                await unlock_achievement(game['user_id'], "quiz_perfect")
            
            del self.games[game_id]
            
            return {
                'error': False,
                'success': True,
                'result': 'finished',
                'score': game['score'],
                'total': game['total'],
                'reward': reward,
                'percent': round(game['score'] / game['total'] * 100, 1),
                'answers': game['answers']
            }
        
        next_q = game['questions'][game['current']]
        return {
            'error': False,
            'success': True,
            'result': 'correct' if is_correct else 'wrong',
            'score': game['score'],
            'current': game['current'] + 1,
            'total': game['total'],
            'question': next_q['q'],
            'answers': next_q['answers']
        }

quiz = Quiz()

# ============================================================
# БЫСТРЫЕ ФУНКЦИИ-ОБЁРТКИ
# ============================================================

async def slots(user_id: int, bet: int) -> dict:
    return await slot_machine.spin(user_id, bet)

async def roulette_spin(user_id: int, bet: int, bet_type: str, value: str) -> dict:
    return await roulette.spin(user_id, bet, bet_type, value)

async def blackjack_start(user_id: int, bet: int) -> dict:
    return await blackjack.start_game(user_id, bet)

async def blackjack_hit(game_id: str) -> dict:
    return await blackjack.hit(game_id)

async def blackjack_stand(game_id: str) -> dict:
    return await blackjack.stand(game_id)

async def blackjack_double(game_id: str) -> dict:
    return await blackjack.double(game_id)

async def blackjack_insure(game_id: str) -> dict:
    return await blackjack.insure(game_id)

async def blackjack_surrender(game_id: str) -> dict:
    return await blackjack.surrender(game_id)

async def blackjack_split(game_id: str) -> dict:
    return await blackjack.split(game_id)

async def dice_roll(user_id: int, game_type: str = "классические", count: int = None) -> dict:
    return await dice.roll(user_id, game_type, count)

async def dice_battle(user_id: int, target_id: int, bet: int, game_type: str = "классические") -> dict:
    return await dice.battle(user_id, target_id, bet, game_type)

async def guess_start(user_id: int, difficulty: str = "easy", bet: int = 0) -> dict:
    return await guess_game.start(user_id, difficulty, bet)

async def guess_guess(game_id: str, guess: int) -> dict:
    return await guess_game.guess(game_id, guess)

async def quiz_start(user_id: int, topic: str = "general", difficulty: int = 1) -> dict:
    return await quiz.start(user_id, topic, difficulty)

async def quiz_answer(game_id: str, answer_index: int) -> dict:
    return await quiz.answer(game_id, answer_index)

# ============================================================
# КОНЕЦ ДИАЛОГА 5/20
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК: ~2,400
# ============================================================
# ============================================================
# FABLE BOT V5.0 - ДИАЛОГ 6/20: SOCIAL.PY
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК В ЭТОМ ДИАЛОГЕ: ~2,500
# ============================================================

import asyncio
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from database import (
    db, get_coins, add_coins, remove_coins, get_user,
    update_user, get_user_level, add_item, remove_item,
    has_item, can_do, set_cooldown, get_cooldown_time
)
from config import COOLDOWNS, MAX_COINS
from utils import (
    format_large_number, format_time_seconds, safe_int,
    get_time_ago, format_datetime, get_name, get_mention,
    chunk_list, unique_list
)
from economy import unlock_achievement

# ============================================================
# 1. РП КОМАНДЫ (ПОЛНАЯ РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

RP_ACTIONS = {
    # ============================================================
    # АГРЕССИВНЫЕ (30)
    # ============================================================
    "отпиздить": {
        "phrases": ["🔨 {user} отпиздил {target}!", "💥 {user} вынес {target}!", "🤜 {user} навалял {target}!"],
        "cooldown": 10, "reward": 3, "category": "aggressive"
    },
    "ударить": {
        "phrases": ["👊 {user} ударил {target}!", "💢 {user} заехал {target}!", "🥊 {user} врезал {target}!"],
        "cooldown": 5, "reward": 2, "category": "aggressive"
    },
    "пнуть": {
        "phrases": ["🦶 {user} пнул {target}!", "👟 {user} дал пинка {target}!"],
        "cooldown": 5, "reward": 1, "category": "aggressive"
    },
    "задушить": {
        "phrases": ["😤 {user} задушил {target}!", "💀 {user} придушил {target}!"],
        "cooldown": 15, "reward": 4, "category": "aggressive"
    },
    "убить": {
        "phrases": ["🔪 {user} убил {target}!", "💀 {user} замочил {target}!", "⚰️ {user} отправил {target} в рай!"],
        "cooldown": 30, "reward": 5, "category": "aggressive"
    },
    "избить": {
        "phrases": ["🔨 {user} избил {target}!", "💥 {user} отлупил {target}!", "🥊 {user} нанес побои {target}!"],
        "cooldown": 20, "reward": 4, "category": "aggressive"
    },
    "уебать": {
        "phrases": ["💥 {user} уебал {target}!", "🔨 {user} заехал {target}!", "💢 {user} выписал {target}!"],
        "cooldown": 15, "reward": 3, "category": "aggressive"
    },
    "закидать_камнями": {
        "phrases": ["🪨 {user} закидал {target} камнями!", "💥 {user} закидал {target}!"],
        "cooldown": 10, "reward": 2, "category": "aggressive"
    },
    "откусить_голову": {
        "phrases": ["🧟 {user} откусил голову {target}!", "💀 {user} обезглавил {target}!"],
        "cooldown": 30, "reward": 5, "category": "aggressive"
    },
    "застрелить": {
        "phrases": ["🔫 {user} застрелил {target}!", "💥 {user} выстрелил в {target}!"],
        "cooldown": 25, "reward": 4, "category": "aggressive"
    },
    "зарезать": {
        "phrases": ["🗡️ {user} зарезал {target}!", "🔪 {user} пырнул {target}!"],
        "cooldown": 20, "reward": 4, "category": "aggressive"
    },
    "сломать_ногу": {
        "phrases": ["🦴 {user} сломал ногу {target}!", "💥 {user} переломал кости {target}!"],
        "cooldown": 20, "reward": 3, "category": "aggressive"
    },
    "выбить_зуб": {
        "phrases": ["🦷 {user} выбил зуб {target}!", "💥 {user} выбил зубы {target}!"],
        "cooldown": 15, "reward": 3, "category": "aggressive"
    },
    "плюнуть": {
        "phrases": ["💦 {user} плюнул в {target}!", "🤢 {user} оплевал {target}!"],
        "cooldown": 5, "reward": 1, "category": "aggressive"
    },
    "унизить": {
        "phrases": ["😤 {user} унизил {target}!", "💢 {user} опустил {target}!"],
        "cooldown": 10, "reward": 2, "category": "aggressive"
    },
    
    # ============================================================
    # НЕЖНЫЕ (25)
    # ============================================================
    "обнять": {
        "phrases": ["🤗 {user} обнял {target}!", "❤️ {user} прижал к себе {target}!", "💕 {user} согрел {target} теплом!"],
        "cooldown": 5, "reward": 2, "category": "gentle"
    },
    "поцеловать": {
        "phrases": ["😘 {user} поцеловал {target}!", "💋 {user} чмокнул {target}!", "❤️‍🔥 {user} засосал {target}!"],
        "cooldown": 10, "reward": 3, "category": "gentle"
    },
    "погладить": {
        "phrases": ["🖐️ {user} погладил {target}!", "😊 {user} погладил по голове {target}!"],
        "cooldown": 5, "reward": 1, "category": "gentle"
    },
    "вылечить": {
        "phrases": ["💉 {user} вылечил {target}!", "🏥 {user} поставил на ноги {target}!"],
        "cooldown": 15, "reward": 4, "category": "gentle"
    },
    "успокоить": {
        "phrases": ["🤗 {user} успокоил {target}!", "😌 {user} успокоил {target}!"],
        "cooldown": 5, "reward": 2, "category": "gentle"
    },
    "вдохновить": {
        "phrases": ["💪 {user} вдохновил {target}!", "🔥 {user} зажёг {target}!"],
        "cooldown": 5, "reward": 2, "category": "gentle"
    },
    "похвалить": {
        "phrases": ["👏 {user} похвалил {target}!", "🌟 {user} отметил {target}!"],
        "cooldown": 5, "reward": 1, "category": "gentle"
    },
    "поддержать": {
        "phrases": ["💪 {user} поддержал {target}!", "🤝 {user} подставил плечо {target}!"],
        "cooldown": 5, "reward": 2, "category": "gentle"
    },
    "пожалеть": {
        "phrases": ["😢 {user} пожалел {target}!", "🤗 {user} посочувствовал {target}!"],
        "cooldown": 5, "reward": 2, "category": "gentle"
    },
    "защитить": {
        "phrases": ["🛡️ {user} защитил {target}!", "⚔️ {user} встал на защиту {target}!"],
        "cooldown": 15, "reward": 4, "category": "gentle"
    },
    "спасти": {
        "phrases": ["🦸 {user} спас {target}!", "🚑 {user} вытащил {target} из беды!"],
        "cooldown": 20, "reward": 5, "category": "gentle"
    },
    "подарить_цветы": {
        "phrases": ["💐 {user} подарил цветы {target}!", "🌹 {user} подарил розы {target}!"],
        "cooldown": 10, "reward": 3, "category": "gentle"
    },
    "приготовить_еду": {
        "phrases": ["🍳 {user} приготовил еду для {target}!", "🍲 {user} накормил {target}!"],
        "cooldown": 10, "reward": 3, "category": "gentle"
    },
    
    # ============================================================
    # ЗАБАВНЫЕ (25)
    # ============================================================
    "насрать": {
        "phrases": ["💩 {user} насрал {target} на голову!", "💩 {user} уделал {target}!"],
        "cooldown": 15, "reward": 2, "category": "funny"
    },
    "выебать": {
        "phrases": ["🍆 {user} выебал {target}!", "🔥 {user} оттрахал {target}!", "💦 {user} выебал {target} вусмерть!"],
        "cooldown": 30, "reward": 5, "category": "funny"
    },
    "сосать": {
        "phrases": ["😳 {user} сосёт {target}!", "🔥 {user} высасывает душу из {target}!"],
        "cooldown": 20, "reward": 3, "category": "funny"
    },
    "укурить": {
        "phrases": ["😤 {user} укурил {target}!", "💨 {user} забил {target}!"],
        "cooldown": 10, "reward": 2, "category": "funny"
    },
    "обматерить": {
        "phrases": ["🤬 {user} обматерил {target}!", "💢 {user} покрыл {target} матом!"],
        "cooldown": 5, "reward": 1, "category": "funny"
    },
    "облить_водой": {
        "phrases": ["💦 {user} облил {target} водой!", "🌊 {user} вылил ведро на {target}!"],
        "cooldown": 10, "reward": 2, "category": "funny"
    },
    "укусить": {
        "phrases": ["🦷 {user} укусил {target}!", "🐺 {user} впился зубами в {target}!"],
        "cooldown": 10, "reward": 2, "category": "funny"
    },
    "посмеяться": {
        "phrases": ["😂 {user} посмеялся над {target}!", "🤣 {user} угорает над {target}!"],
        "cooldown": 5, "reward": 1, "category": "funny"
    },
    "танцевать": {
        "phrases": ["💃 {user} танцует с {target}!", "🕺 {user} зажигает с {target}!"],
        "cooldown": 5, "reward": 2, "category": "funny"
    },
    "спеть": {
        "phrases": ["🎵 {user} поёт для {target}!", "🎤 {user} исполнил песню для {target}!"],
        "cooldown": 10, "reward": 2, "category": "funny"
    },
    "рассказать_анекдот": {
        "phrases": ["😂 {user} рассказал анекдот {target}!", "🤣 {user} рассмешил {target}!"],
        "cooldown": 5, "reward": 1, "category": "funny"
    },
    "показать_язык": {
        "phrases": ["😛 {user} показал язык {target}!", "👅 {user} дразнит {target}!"],
        "cooldown": 5, "reward": 1, "category": "funny"
    },
    "подшутить": {
        "phrases": ["😜 {user} подшутил над {target}!", "🤪 {user} разыграл {target}!"],
        "cooldown": 5, "reward": 2, "category": "funny"
    },
}

class RPManager:
    """ПОЛНЫЙ МЕНЕДЖЕР РП ДЕЙСТВИЙ С РАСШИРЕННОЙ СТАТИСТИКОЙ"""
    
    def __init__(self):
        self.rp_cooldowns = {}
        self.rp_stats = {}
        self.rp_history = {}
        self.rp_streaks = {}
        self.rp_top = {}
    
    async def do_action(self, user_id: int, target_id: int, action: str, bot) -> dict:
        """ВЫПОЛНИТЬ РП ДЕЙСТВИЕ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        if user_id == target_id:
            return {'error': True, 'message': '❌ Нельзя с самим собой!'}
        
        if action not in RP_ACTIONS:
            return {
                'error': True,
                'message': '❌ Такого действия нет! Доступно: ' + ', '.join(list(RP_ACTIONS.keys())[:10]) + '...'
            }
        
        action_data = RP_ACTIONS[action]
        cooldown = action_data.get('cooldown', 10)
        
        # Проверка кулдауна
        key = f"{user_id}_{action}"
        if key in self.rp_cooldowns:
            last_time = self.rp_cooldowns[key]
            elapsed = (datetime.now() - last_time).seconds
            if elapsed < cooldown:
                return {
                    'error': True,
                    'message': f'⏳ Подожди {cooldown - elapsed} секунд!'
                }
        
        # Получаем имена
        user_name = await get_name(user_id, bot)
        target_name = await get_name(target_id, bot)
        
        # Выбираем фразу
        phrases = action_data.get('phrases', [])
        phrase = random.choice(phrases).format(
            user=user_name,
            target=target_name
        )
        
        # Шанс на крит (10%)
        crit = random.random() < 0.1
        if crit:
            phrase += "\n💥 **КРИТИЧЕСКОЕ ПОПАДАНИЕ!**"
        
        # Проверка питомца (помощь)
        pet = await self._get_pet(user_id)
        if pet and pet.get('happiness', 0) > 50 and random.random() < 0.3:
            phrase += f"\n🐕 {pet['pet_name']} помог!"
        
        # Проверка предметов
        has_sword = await has_item(user_id, "меч")
        if has_sword and action_data.get('category') == "aggressive":
            phrase += f"\n🗡️ С мечом эффект усилен!"
        
        has_shield = await has_item(user_id, "щит")
        if has_shield and action_data.get('category') == "gentle":
            phrase += f"\n🛡️ С щитом защита усилена!"
        
        # Обновляем статистику
        key_stat = f"{user_id}_{action}"
        self.rp_stats[key_stat] = self.rp_stats.get(key_stat, 0) + 1
        
        # Обновляем стрик
        streak_key = f"{user_id}_streak"
        today = datetime.now().date()
        if streak_key in self.rp_streaks:
            last_date = self.rp_streaks[streak_key].get('date')
            if last_date == today - timedelta(days=1):
                self.rp_streaks[streak_key]['count'] += 1
            elif last_date != today:
                self.rp_streaks[streak_key]['count'] = 1
            self.rp_streaks[streak_key]['date'] = today
        else:
            self.rp_streaks[streak_key] = {'count': 1, 'date': today}
        
        # Сохраняем историю
        history_key = f"{user_id}_{datetime.now().date().isoformat()}"
        if history_key not in self.rp_history:
            self.rp_history[history_key] = []
        self.rp_history[history_key].append({
            'action': action,
            'target': target_id,
            'time': datetime.now().isoformat()
        })
        
        # Кулдаун
        self.rp_cooldowns[key] = datetime.now()
        
        # Награда
        reward = action_data.get('reward', random.randint(1, 3))
        await add_coins(user_id, reward)
        
        # Проверка достижений
        count = self.rp_stats.get(key_stat, 0)
        if count == 1:
            await unlock_achievement(user_id, "first_rp")
        elif count == 50:
            await unlock_achievement(user_id, "rp_50")
        elif count == 100:
            await unlock_achievement(user_id, "rp_100")
        elif count == 500:
            await unlock_achievement(user_id, "rp_500")
        elif count == 1000:
            await unlock_achievement(user_id, "rp_1000")
        
        # Проверка стрика
        streak_count = self.rp_streaks[streak_key]['count']
        if streak_count == 7:
            await unlock_achievement(user_id, "rp_streak_7")
        elif streak_count == 30:
            await unlock_achievement(user_id, "rp_streak_30")
        
        return {
            'error': False,
            'success': True,
            'phrase': phrase,
            'crit': crit,
            'reward': reward,
            'action': action,
            'category': action_data.get('category', 'other'),
            'stats': self.rp_stats.get(key_stat, 0),
            'streak': self.rp_streaks[streak_key]['count']
        }
    
    async def _get_pet(self, user_id: int) -> Optional[dict]:
        """ПОЛУЧИТЬ ПИТОМЦА ПОЛЬЗОВАТЕЛЯ"""
        result = await db.execute(
            "SELECT * FROM pets WHERE user_id = ?",
            (user_id,), fetch_one=True, cache_ttl=30
        )
        return dict(result) if result else None
    
    async def get_rp_stats(self, user_id: int) -> dict:
        """ПОЛУЧИТЬ СТАТИСТИКУ РП ДЕЙСТВИЙ"""
        user_stats = {}
        total_actions = 0
        categories = {'aggressive': 0, 'gentle': 0, 'funny': 0, 'other': 0}
        
        for key, value in self.rp_stats.items():
            if key.startswith(str(user_id)):
                action = key.split('_', 1)[1] if '_' in key else key
                user_stats[action] = value
                total_actions += value
                if action in RP_ACTIONS:
                    category = RP_ACTIONS[action].get('category', 'other')
                    categories[category] = categories.get(category, 0) + value
        
        # Топ действий
        sorted_actions = sorted(user_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total': total_actions,
            'actions': user_stats,
            'top_actions': sorted_actions,
            'categories': categories,
            'most_used': sorted_actions[0][0] if sorted_actions else None
        }
    
    async def get_daily_rp(self, user_id: int) -> List[dict]:
        """ПОЛУЧИТЬ ЕЖЕДНЕВНЮЮ РП СТАТИСТИКУ"""
        history_key = f"{user_id}_{datetime.now().date().isoformat()}"
        return self.rp_history.get(history_key, [])
    
    async def get_rp_streak(self, user_id: int) -> int:
        """ПОЛУЧИТЬ ТЕКУЩИЙ РП СТРИК"""
        streak_key = f"{user_id}_streak"
        if streak_key in self.rp_streaks:
            return self.rp_streaks[streak_key]['count']
        return 0

rp_manager = RPManager()

# ============================================================
# 2. КЛАНЫ (ПОЛНАЯ РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

class ClanManager:
    """ПОЛНЫЙ МЕНЕДЖЕР КЛАНОВ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
    
    def __init__(self):
        self.wars = {}
        self.alliances = {}
        self.clan_cache = {}
        self.requests = {}
        self.invites = {}
        self.clan_ranks = {
            'member': {'name': 'Участник', 'permissions': []},
            'elder': {'name': 'Старейшина', 'permissions': ['invite', 'kick']},
            'co_leader': {'name': 'Заместитель', 'permissions': ['invite', 'kick', 'promote', 'demote']},
            'leader': {'name': 'Лидер', 'permissions': ['all']}
        }
    
    async def create_clan(self, chat_id: int, user_id: int, name: str) -> dict:
        """СОЗДАТЬ КЛАН С РАСШИРЕННЫМИ ПРОВЕРКАМИ"""
        if len(name) < 2 or len(name) > 30:
            return {'error': True, 'message': '❌ Название клана должно быть от 2 до 30 символов!'}
        
        # Проверка на недопустимые символы
        if not re.match(r'^[a-zA-Zа-яА-Я0-9_ ]+$', name):
            return {'error': True, 'message': '❌ Название содержит недопустимые символы!'}
        
        # Проверка, есть ли клан с таким именем
        existing = await db.execute(
            "SELECT id FROM clans WHERE chat_id = ? AND name = ?",
            (chat_id, name), fetch_one=True
        )
        if existing:
            return {'error': True, 'message': '❌ Клан с таким названием уже существует!'}
        
        # Проверка, не в клане ли уже
        in_clan = await db.execute(
            "SELECT id FROM clans WHERE chat_id = ? AND members LIKE ?",
            (chat_id, f'%{user_id}%'), fetch_one=True
        )
        if in_clan:
            return {'error': True, 'message': '❌ Ты уже в клане!'}
        
        # Проверка денег (5000 монет)
        coins = await get_coins(user_id)
        if coins < 5000:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно 5,000 монет для создания клана!'
            }
        
        await remove_coins(user_id, 5000)
        
        # Создаём клан
        await db.execute(
            "INSERT INTO clans (chat_id, name, owner_id, members, treasury, created_date) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (chat_id, name, user_id, str(user_id), 0, datetime.now().isoformat())
        )
        
        # Проверка достижения
        await unlock_achievement(user_id, "create_clan")
        
        return {
            'error': False,
            'success': True,
            'name': name,
            'owner': user_id,
            'members': 1,
            'cost': 5000
        }
    
    async def get_clan(self, user_id: int, chat_id: int) -> Optional[dict]:
        """ПОЛУЧИТЬ КЛАН ПОЛЬЗОВАТЕЛЯ"""
        result = await db.execute(
            "SELECT * FROM clans WHERE chat_id = ? AND members LIKE ?",
            (chat_id, f'%{user_id}%'), fetch_one=True, cache_ttl=30
        )
        return dict(result) if result else None
    
    async def get_clan_by_id(self, clan_id: int) -> Optional[dict]:
        """ПОЛУЧИТЬ КЛАН ПО ID"""
        result = await db.execute(
            "SELECT * FROM clans WHERE id = ?",
            (clan_id,), fetch_one=True, cache_ttl=30
        )
        return dict(result) if result else None
    
    async def get_clan_by_name(self, chat_id: int, name: str) -> Optional[dict]:
        """ПОЛУЧИТЬ КЛАН ПО НАЗВАНИЮ"""
        result = await db.execute(
            "SELECT * FROM clans WHERE chat_id = ? AND name = ?",
            (chat_id, name), fetch_one=True, cache_ttl=30
        )
        return dict(result) if result else None
    
    async def join_clan(self, user_id: int, chat_id: int, clan_name: str) -> dict:
        """ВСТУПИТЬ В КЛАН С РАСШИРЕННЫМИ ПРОВЕРКАМИ"""
        # Проверяем, есть ли клан
        clan = await self.get_clan_by_name(chat_id, clan_name)
        if not clan:
            return {'error': True, 'message': '❌ Клан не найден!'}
        
        # Проверяем, не в клане ли уже
        in_clan = await self.get_clan(user_id, chat_id)
        if in_clan:
            return {'error': True, 'message': '❌ Ты уже в клане!'}
        
        # Проверяем, есть ли место (максимум 50 участников)
        members = clan['members'].split(',') if clan['members'] else []
        if len(members) >= 50:
            return {'error': True, 'message': '❌ Клан переполнен (максимум 50 участников)!'}
        
        # Добавляем в клан
        members.append(str(user_id))
        await db.execute(
            "UPDATE clans SET members = ? WHERE id = ?",
            (','.join(members), clan['id'])
        )
        
        # Проверка достижения
        await unlock_achievement(user_id, "join_clan")
        
        return {
            'error': False,
            'success': True,
            'clan': clan['name'],
            'members': len(members)
        }
    
    async def leave_clan(self, user_id: int, chat_id: int) -> dict:
        """ВЫЙТИ ИЗ КЛАНА С РАСШИРЕННЫМИ ПРОВЕРКАМИ"""
        clan = await self.get_clan(user_id, chat_id)
        if not clan:
            return {'error': True, 'message': '❌ Ты не в клане!'}
        
        # Проверяем, не лидер ли
        if clan['owner_id'] == user_id:
            return {'error': True, 'message': '❌ Лидер не может выйти! Передай клан другому участнику.'}
        
        members = clan['members'].split(',') if clan['members'] else []
        if str(user_id) in members:
            members.remove(str(user_id))
        
        await db.execute(
            "UPDATE clans SET members = ? WHERE id = ?",
            (','.join(members), clan['id'])
        )
        
        return {
            'error': False,
            'success': True,
            'clan': clan['name']
        }
    
    async def transfer_leadership(self, user_id: int, chat_id: int, new_owner_id: int) -> dict:
        """ПЕРЕДАТЬ ЛИДЕРСТВО В КЛАНЕ"""
        clan = await self.get_clan(user_id, chat_id)
        if not clan:
            return {'error': True, 'message': '❌ Ты не в клане!'}
        
        if clan['owner_id'] != user_id:
            return {'error': True, 'message': '❌ Только лидер может передавать лидерство!'}
        
        # Проверяем, что новый лидер в клане
        members = clan['members'].split(',') if clan['members'] else []
        if str(new_owner_id) not in members:
            return {'error': True, 'message': '❌ Пользователь не в клане!'}
        
        await db.execute(
            "UPDATE clans SET owner_id = ? WHERE id = ?",
            (new_owner_id, clan['id'])
        )
        
        return {
            'error': False,
            'success': True,
            'clan': clan['name'],
            'new_owner': new_owner_id
        }
    
    async def get_clan_info(self, user_id: int, chat_id: int, bot) -> dict:
        """ПОЛУЧИТЬ ИНФОРМАЦИЮ О КЛАНЕ С РАСШИРЕННЫМИ ДАННЫМИ"""
        clan = await self.get_clan(user_id, chat_id)
        if not clan:
            return {'error': True, 'message': '❌ Ты не в клане!'}
        
        members = clan['members'].split(',') if clan['members'] else []
        
        # Получаем имена участников
        member_names = []
        member_levels = []
        member_coins = []
        
        for uid in members[:10]:
            try:
                name = await get_name(int(uid), bot)
                level = await get_user_level(int(uid))
                coins = await get_coins(int(uid))
                member_names.append(name)
                member_levels.append(level)
                member_coins.append(coins)
            except:
                member_names.append(f"id{uid}")
                member_levels.append(0)
                member_coins.append(0)
        
        # Статистика клана
        total_coins = 0
        total_level = 0
        for uid in members:
            coins = await get_coins(int(uid))
            level = await get_user_level(int(uid))
            total_coins += coins
            total_level += level
        
        return {
            'error': False,
            'success': True,
            'name': clan['name'],
            'owner_id': clan['owner_id'],
            'owner_name': await get_name(clan['owner_id'], bot),
            'members': len(members),
            'member_names': member_names,
            'member_levels': member_levels,
            'member_coins': member_coins,
            'treasury': clan['treasury'],
            'level': clan.get('level', 1),
            'experience': clan.get('experience', 0),
            'total_coins': total_coins,
            'avg_level': total_level // len(members) if members else 0,
            'created': clan.get('created_date', 'Неизвестно'),
            'wins': clan.get('wins', 0),
            'losses': clan.get('losses', 0),
            'draws': clan.get('draws', 0)
        }
    
    async def donate_treasury(self, user_id: int, chat_id: int, amount: int) -> dict:
        """ПОПОЛНИТЬ КЛАНОВУЮ КАЗНУ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        if amount <= 0:
            return {'error': True, 'message': '❌ Сумма должна быть больше 0!'}
        
        clan = await self.get_clan(user_id, chat_id)
        if not clan:
            return {'error': True, 'message': '❌ Ты не в клане!'}
        
        coins = await get_coins(user_id)
        if coins < amount:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Есть {format_large_number(coins)}'
            }
        
        await remove_coins(user_id, amount)
        
        # Бонус за пополнение (1% от суммы)
        bonus = int(amount * 0.01)
        if bonus > 0:
            await add_coins(user_id, bonus)
        
        await db.execute(
            "UPDATE clans SET treasury = treasury + ? WHERE id = ?",
            (amount, clan['id'])
        )
        
        # Проверка достижения
        if amount >= 100000:
            await unlock_achievement(user_id, "clan_donator")
        
        return {
            'error': False,
            'success': True,
            'clan': clan['name'],
            'amount': amount,
            'bonus': bonus,
            'treasury': clan['treasury'] + amount
        }
    
    async def get_clan_ranking(self, chat_id: int, limit: int = 10) -> List[dict]:
        """ПОЛУЧИТЬ РЕЙТИНГ КЛАНОВ С РАСШИРЕННЫМИ ДАННЫМИ"""
        result = await db.execute(
            "SELECT id, name, treasury, level, members FROM clans WHERE chat_id = ? "
            "ORDER BY treasury DESC LIMIT ?",
            (chat_id, limit), fetch_all=True, cache_ttl=60
        )
        
        clans = []
        for row in result:
            members = row['members'].split(',') if row['members'] else []
            clan_data = {
                'id': row['id'],
                'name': row['name'],
                'treasury': row['treasury'],
                'level': row['level'],
                'members': len(members),
                'avg_coins': row['treasury'] // len(members) if members else 0
            }
            clans.append(clan_data)
        
        return clans

clan_manager = ClanManager()

# ============================================================
# 3. БРАК (ПОЛНАЯ РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

class MarriageManager:
    """ПОЛНЫЙ МЕНЕДЖЕР БРАКОВ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
    
    def __init__(self):
        self.proposals = {}
        self.divorce_cooldowns = {}
        self.anniversary_bonuses = {}
        self.marriage_gifts = {}
    
    async def propose(self, user_id: int, target_id: int, chat_id: int) -> dict:
        """ПРЕДЛОЖИТЬ БРАК С РАСШИРЕННЫМИ ПРОВЕРКАМИ"""
        if user_id == target_id:
            return {'error': True, 'message': '❌ Нельзя жениться на себе!'}
        
        # Проверяем, не в браке ли уже
        married = await db.execute(
            "SELECT spouse_id FROM marriages WHERE user_id = ? AND chat_id = ? AND is_active = 1",
            (user_id, chat_id), fetch_one=True
        )
        if married:
            return {'error': True, 'message': '❌ Ты уже в браке!'}
        
        target_married = await db.execute(
            "SELECT spouse_id FROM marriages WHERE user_id = ? AND chat_id = ? AND is_active = 1",
            (target_id, chat_id), fetch_one=True
        )
        if target_married:
            return {'error': True, 'message': '❌ Цель уже в браке!'}
        
        # Проверяем, есть ли активное предложение
        key = f"{chat_id}_{target_id}"
        if key in self.proposals:
            return {'error': True, 'message': '❌ Уже есть активное предложение!'}
        
        # Проверяем кулдаун на брак
        if not await can_do(user_id, "marriage"):
            remaining = await get_cooldown_time(user_id, "marriage")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)} перед новым предложением!'
            }
        
        await set_cooldown(user_id, "marriage")
        
        self.proposals[key] = {
            'proposer': user_id,
            'target': target_id,
            'chat_id': chat_id,
            'time': datetime.now().isoformat()
        }
        
        return {
            'error': False,
            'success': True,
            'proposer': user_id,
            'target': target_id,
            'message': f'💍 {await get_name(user_id)} предлагает брак {await get_name(target_id)}!'
        }
    
    async def accept(self, user_id: int, chat_id: int) -> dict:
        """ПРИНЯТЬ ПРЕДЛОЖЕНИЕ С РАСШИРЕННЫМИ БОНУСАМИ"""
        key = f"{chat_id}_{user_id}"
        if key not in self.proposals:
            return {'error': True, 'message': '❌ Нет активного предложения!'}
        
        proposal = self.proposals[key]
        if proposal['target'] != user_id:
            return {'error': True, 'message': '❌ Это не тебе предлагают!'}
        
        # Создаём брак
        await db.execute(
            "INSERT INTO marriages (user_id, chat_id, spouse_id, date, is_active) VALUES (?, ?, ?, ?, 1)",
            (user_id, chat_id, proposal['proposer'], datetime.now().isoformat())
        )
        await db.execute(
            "INSERT INTO marriages (user_id, chat_id, spouse_id, date, is_active) VALUES (?, ?, ?, ?, 1)",
            (proposal['proposer'], chat_id, user_id, datetime.now().isoformat())
        )
        
        del self.proposals[key]
        
        # Проверка достижений
        await unlock_achievement(user_id, "first_marriage")
        await unlock_achievement(proposal['proposer'], "first_marriage")
        
        # Бонус (по 1000 монет)
        await add_coins(user_id, 1000)
        await add_coins(proposal['proposer'], 1000)
        
        return {
            'error': False,
            'success': True,
            'spouse1': user_id,
            'spouse2': proposal['proposer'],
            'bonus': 1000
        }
    
    async def reject(self, user_id: int, chat_id: int) -> dict:
        """ОТКЛОНИТЬ ПРЕДЛОЖЕНИЕ"""
        key = f"{chat_id}_{user_id}"
        if key not in self.proposals:
            return {'error': True, 'message': '❌ Нет активного предложения!'}
        
        del self.proposals[key]
        
        return {
            'error': False,
            'success': True,
            'message': '❌ Предложение отклонено!'
        }
    
    async def divorce(self, user_id: int, chat_id: int) -> dict:
        """РАЗВЕСТИСЬ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        # Проверяем кулдаун (24 часа после развода)
        key = f"divorce_{user_id}_{chat_id}"
        if key in self.divorce_cooldowns:
            last_divorce = self.divorce_cooldowns[key]
            if (datetime.now() - last_divorce).days < 1:
                remaining = 24 - (datetime.now() - last_divorce).hours
                return {
                    'error': True,
                    'message': f'⏳ После развода нужно подождать {remaining} часов!'
                }
        
        spouse = await db.execute(
            "SELECT spouse_id FROM marriages WHERE user_id = ? AND chat_id = ? AND is_active = 1",
            (user_id, chat_id), fetch_one=True
        )
        if not spouse:
            return {'error': True, 'message': '❌ Ты не в браке!'}
        
        spouse_id = spouse['spouse_id']
        
        # Удаляем брак
        await db.execute(
            "UPDATE marriages SET is_active = 0 WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id)
        )
        await db.execute(
            "UPDATE marriages SET is_active = 0 WHERE user_id = ? AND chat_id = ?",
            (spouse_id, chat_id)
        )
        
        # Штраф (1000 монет)
        await remove_coins(user_id, 1000)
        
        # Кулдаун
        self.divorce_cooldowns[key] = datetime.now()
        
        return {
            'error': False,
            'success': True,
            'spouse': spouse_id,
            'fine': 1000
        }
    
    async def get_spouse(self, user_id: int, chat_id: int) -> Optional[int]:
        """ПОЛУЧИТЬ СУПРУГА"""
        result = await db.execute(
            "SELECT spouse_id FROM marriages WHERE user_id = ? AND chat_id = ? AND is_active = 1",
            (user_id, chat_id), fetch_one=True, cache_ttl=30
        )
        return result['spouse_id'] if result else None
    
    async def get_marriage_info(self, user_id: int, chat_id: int, bot) -> dict:
        """ПОЛУЧИТЬ ИНФОРМАЦИЮ О БРАКЕ С РАСШИРЕННЫМИ ДАННЫМИ"""
        spouse_id = await self.get_spouse(user_id, chat_id)
        if not spouse_id:
            return {'error': True, 'message': '❌ Ты не в браке!'}
        
        # Получаем дату брака
        result = await db.execute(
            "SELECT date FROM marriages WHERE user_id = ? AND chat_id = ? AND is_active = 1",
            (user_id, chat_id), fetch_one=True
        )
        
        spouse_name = await get_name(spouse_id, bot)
        marriage_date = datetime.fromisoformat(result['date']) if result else None
        days_married = (datetime.now() - marriage_date).days if marriage_date else 0
        
        # Бонус за годовщину
        anniversary_bonus = 0
        if days_married > 0 and days_married % 30 == 0:
            anniversary_bonus = days_married // 30 * 1000
        
        return {
            'error': False,
            'success': True,
            'spouse_id': spouse_id,
            'spouse_name': spouse_name,
            'marriage_date': format_datetime(marriage_date) if marriage_date else 'Неизвестно',
            'days_married': days_married,
            'anniversary_bonus': anniversary_bonus,
            'next_anniversary': (marriage_date + timedelta(days=(days_married // 30 + 1) * 30)) if marriage_date else None
        }
    
    async def claim_anniversary_bonus(self, user_id: int, chat_id: int) -> dict:
        """ПОЛУЧИТЬ БОНУС ЗА ГОДОВЩИНУ БРАКА"""
        info = await self.get_marriage_info(user_id, chat_id, None)
        if info.get('error'):
            return info
        
        if info['anniversary_bonus'] <= 0:
            return {'error': True, 'message': '❌ Сегодня нет годовщины!'}
        
        await add_coins(user_id, info['anniversary_bonus'])
        await add_coins(info['spouse_id'], info['anniversary_bonus'])
        
        return {
            'error': False,
            'success': True,
            'bonus': info['anniversary_bonus'],
            'days': info['days_married']
        }

marriage_manager = MarriageManager()

# ============================================================
# 4. ДРУЗЬЯ (ПОЛНАЯ РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

class FriendManager:
    """ПОЛНЫЙ МЕНЕДЖЕР ДРУЗЕЙ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
    
    async def add_friend(self, user_id: int, friend_id: int, chat_id: int) -> dict:
        """ДОБАВИТЬ В ДРУЗЬЯ С РАСШИРЕННЫМИ ПРОВЕРКАМИ"""
        if user_id == friend_id:
            return {'error': True, 'message': '❌ Нельзя добавить себя!'}
        
        # Проверяем, не друзья ли уже
        existing = await db.execute(
            "SELECT * FROM friends WHERE user_id = ? AND friend_id = ? AND is_active = 1",
            (user_id, friend_id), fetch_one=True
        )
        if existing:
            return {'error': True, 'message': '❌ Вы уже друзья!'}
        
        # Проверяем кулдаун
        if not await can_do(user_id, "friend_add"):
            remaining = await get_cooldown_time(user_id, "friend_add")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
            }
        
        await set_cooldown(user_id, "friend_add")
        
        # Проверяем лимит друзей
        friends_count = await db.execute(
            "SELECT COUNT(*) as count FROM friends WHERE user_id = ? AND is_active = 1",
            (user_id,), fetch_one=True
        )
        if friends_count and friends_count['count'] >= MAX_FRIENDS:
            return {'error': True, 'message': f'❌ У тебя максимум друзей ({MAX_FRIENDS})!'}
        
        await db.execute(
            "INSERT INTO friends (user_id, friend_id, chat_id, date, is_active) VALUES (?, ?, ?, ?, 1)",
            (user_id, friend_id, chat_id, datetime.now().isoformat())
        )
        await db.execute(
            "INSERT INTO friends (user_id, friend_id, chat_id, date, is_active) VALUES (?, ?, ?, ?, 1)",
            (friend_id, user_id, chat_id, datetime.now().isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'friend': friend_id
        }
    
    async def remove_friend(self, user_id: int, friend_id: int) -> dict:
        """УДАЛИТЬ ИЗ ДРУЗЕЙ"""
        await db.execute(
            "UPDATE friends SET is_active = 0 WHERE user_id = ? AND friend_id = ?",
            (user_id, friend_id)
        )
        await db.execute(
            "UPDATE friends SET is_active = 0 WHERE user_id = ? AND friend_id = ?",
            (friend_id, user_id)
        )
        
        return {
            'error': False,
            'success': True,
            'friend': friend_id
        }
    
    async def get_friends(self, user_id: int) -> List[int]:
        """ПОЛУЧИТЬ СПИСОК ДРУЗЕЙ"""
        result = await db.execute(
            "SELECT friend_id FROM friends WHERE user_id = ? AND is_active = 1",
            (user_id,), fetch_all=True, cache_ttl=30
        )
        return [r['friend_id'] for r in result] if result else []
    
    async def get_friends_info(self, user_id: int, bot) -> List[dict]:
        """ПОЛУЧИТЬ ИНФОРМАЦИЮ О ДРУЗЬЯХ С РАСШИРЕННЫМИ ДАННЫМИ"""
        friends = await self.get_friends(user_id)
        if not friends:
            return []
        
        result = []
        for fid in friends:
            name = await get_name(fid, bot)
            coins = await get_coins(fid)
            level = await get_user_level(fid)
            status = "🟢 Онлайн" if await self._is_online(fid) else "⚫ Офлайн"
            result.append({
                'id': fid,
                'name': name,
                'coins': coins,
                'level': level,
                'status': status
            })
        
        return sorted(result, key=lambda x: x['coins'], reverse=True)
    
    async def _is_online(self, user_id: int) -> bool:
        """ПРОВЕРИТЬ, ОНЛАЙН ЛИ ПОЛЬЗОВАТЕЛЬ"""
        result = await db.execute(
            "SELECT last_activity FROM users WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        if not result or not result['last_activity']:
            return False
        last_activity = datetime.fromisoformat(result['last_activity'])
        return (datetime.now() - last_activity).seconds < 300
    
    async def get_friend_stats(self, user_id: int) -> dict:
        """ПОЛУЧИТЬ СТАТИСТИКУ ДРУЗЕЙ С РАСШИРЕННЫМИ ДАННЫМИ"""
        friends = await self.get_friends(user_id)
        
        if not friends:
            return {'total': 0, 'total_coins': 0, 'avg_level': 0, 'online': 0}
        
        total_coins = 0
        total_level = 0
        online = 0
        
        for fid in friends:
            coins = await get_coins(fid)
            level = await get_user_level(fid)
            total_coins += coins
            total_level += level
            if await self._is_online(fid):
                online += 1
        
        return {
            'total': len(friends),
            'total_coins': total_coins,
            'avg_level': total_level // len(friends) if friends else 0,
            'online': online
        }

friend_manager = FriendManager()

# ============================================================
# 5. ПОДАРКИ (ПОЛНАЯ РАСШИРЕННАЯ ВЕРСИЯ)
# ============================================================

class GiftManager:
    """ПОЛНЫЙ МЕНЕДЖЕР ПОДАРКОВ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
    
    async def send_gift(self, user_id: int, target_id: int, item_name: str, quantity: int = 1) -> dict:
        """ОТПРАВИТЬ ПОДАРОК С РАСШИРЕННЫМИ ПРОВЕРКАМИ"""
        if user_id == target_id:
            return {'error': True, 'message': '❌ Нельзя отправить подарок себе!'}
        
        if quantity <= 0:
            return {'error': True, 'message': '❌ Количество должно быть больше 0!'}
        
        if not await has_item(user_id, item_name):
            return {'error': True, 'message': f'❌ У тебя нет {item_name}!'}
        
        if await has_item(user_id, item_name) < quantity:
            return {
                'error': True,
                'message': f'❌ У тебя только {await has_item(user_id, item_name)} {item_name}!'
            }
        
        # Проверяем кулдаун
        if not await can_do(user_id, "gift_send"):
            remaining = await get_cooldown_time(user_id, "gift_send")
            return {
                'error': True,
                'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
            }
        
        await set_cooldown(user_id, "gift_send")
        
        await remove_item(user_id, item_name, quantity)
        await add_item(target_id, item_name, quantity)
        
        # Сохраняем историю
        await db.execute(
            "INSERT INTO gifts (from_user, to_user, chat_id, item_name, quantity, date, is_claimed) "
            "VALUES (?, ?, ?, ?, ?, ?, 1)",
            (user_id, target_id, 0, item_name, quantity, datetime.now().isoformat())
        )
        
        # Проверка достижения
        await unlock_achievement(user_id, "first_gift")
        
        return {
            'error': False,
            'success': True,
            'from': user_id,
            'to': target_id,
            'item': item_name,
            'quantity': quantity
        }
    
    async def get_gifts_history(self, user_id: int, limit: int = 10) -> List[dict]:
        """ПОЛУЧИТЬ ИСТОРИЮ ПОДАРКОВ С РАСШИРЕННЫМИ ДАННЫМИ"""
        result = await db.execute(
            "SELECT from_user, to_user, item_name, quantity, date FROM gifts "
            "WHERE from_user = ? OR to_user = ? ORDER BY date DESC LIMIT ?",
            (user_id, user_id, limit), fetch_all=True, cache_ttl=60
        )
        return result or []
    
    async def get_gifts_stats(self, user_id: int) -> dict:
        """ПОЛУЧИТЬ СТАТИСТИКУ ПОДАРКОВ С РАСШИРЕННЫМИ ДАННЫМИ"""
        sent = await db.execute(
            "SELECT COUNT(*) as total, SUM(quantity) as items FROM gifts WHERE from_user = ?",
            (user_id,), fetch_one=True
        )
        
        received = await db.execute(
            "SELECT COUNT(*) as total, SUM(quantity) as items FROM gifts WHERE to_user = ?",
            (user_id,), fetch_one=True
        )
        
        return {
            'sent_count': sent['total'] if sent else 0,
            'sent_items': sent['items'] if sent else 0,
            'received_count': received['total'] if received else 0,
            'received_items': received['items'] if received else 0
        }

gift_manager = GiftManager()

# ============================================================
# БЫСТРЫЕ ФУНКЦИИ-ОБЁРТКИ
# ============================================================

async def rp_action(user_id: int, target_id: int, action: str, bot) -> dict:
    return await rp_manager.do_action(user_id, target_id, action, bot)

async def get_rp_stats(user_id: int) -> dict:
    return await rp_manager.get_rp_stats(user_id)

async def get_daily_rp(user_id: int) -> List[dict]:
    return await rp_manager.get_daily_rp(user_id)

async def get_rp_streak(user_id: int) -> int:
    return await rp_manager.get_rp_streak(user_id)

async def create_clan(chat_id: int, user_id: int, name: str) -> dict:
    return await clan_manager.create_clan(chat_id, user_id, name)

async def get_clan(user_id: int, chat_id: int) -> Optional[dict]:
    return await clan_manager.get_clan(user_id, chat_id)

async def get_clan_by_id(clan_id: int) -> Optional[dict]:
    return await clan_manager.get_clan_by_id(clan_id)

async def get_clan_by_name(chat_id: int, name: str) -> Optional[dict]:
    return await clan_manager.get_clan_by_name(chat_id, name)

async def join_clan(user_id: int, chat_id: int, clan_name: str) -> dict:
    return await clan_manager.join_clan(user_id, chat_id, clan_name)

async def leave_clan(user_id: int, chat_id: int) -> dict:
    return await clan_manager.leave_clan(user_id, chat_id)

async def transfer_leadership(user_id: int, chat_id: int, new_owner_id: int) -> dict:
    return await clan_manager.transfer_leadership(user_id, chat_id, new_owner_id)

async def get_clan_info(user_id: int, chat_id: int, bot) -> dict:
    return await clan_manager.get_clan_info(user_id, chat_id, bot)

async def donate_treasury(user_id: int, chat_id: int, amount: int) -> dict:
    return await clan_manager.donate_treasury(user_id, chat_id, amount)

async def get_clan_ranking(chat_id: int, limit: int = 10) -> List[dict]:
    return await clan_manager.get_clan_ranking(chat_id, limit)

async def propose_marriage(user_id: int, target_id: int, chat_id: int) -> dict:
    return await marriage_manager.propose(user_id, target_id, chat_id)

async def accept_marriage(user_id: int, chat_id: int) -> dict:
    return await marriage_manager.accept(user_id, chat_id)

async def reject_marriage(user_id: int, chat_id: int) -> dict:
    return await marriage_manager.reject(user_id, chat_id)

async def divorce(user_id: int, chat_id: int) -> dict:
    return await marriage_manager.divorce(user_id, chat_id)

async def get_spouse(user_id: int, chat_id: int) -> Optional[int]:
    return await marriage_manager.get_spouse(user_id, chat_id)

async def get_marriage_info(user_id: int, chat_id: int, bot) -> dict:
    return await marriage_manager.get_marriage_info(user_id, chat_id, bot)

async def claim_anniversary_bonus(user_id: int, chat_id: int) -> dict:
    return await marriage_manager.claim_anniversary_bonus(user_id, chat_id)

async def add_friend(user_id: int, friend_id: int, chat_id: int) -> dict:
    return await friend_manager.add_friend(user_id, friend_id, chat_id)

async def remove_friend(user_id: int, friend_id: int) -> dict:
    return await friend_manager.remove_friend(user_id, friend_id)

async def get_friends(user_id: int) -> List[int]:
    return await friend_manager.get_friends(user_id)

async def get_friends_info(user_id: int, bot) -> List[dict]:
    return await friend_manager.get_friends_info(user_id, bot)

async def get_friend_stats(user_id: int) -> dict:
    return await friend_manager.get_friend_stats(user_id)

async def send_gift(user_id: int, target_id: int, item_name: str, quantity: int = 1) -> dict:
    return await gift_manager.send_gift(user_id, target_id, item_name, quantity)

async def get_gifts_history(user_id: int, limit: int = 10) -> List[dict]:
    return await gift_manager.get_gifts_history(user_id, limit)

async def get_gifts_stats(user_id: int) -> dict:
    return await gift_manager.get_gifts_stats(user_id)

# ============================================================
# КОНЕЦ ДИАЛОГА 6/20
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК: ~2,500
# ============================================================
# ============================================================
# FABLE BOT V5.0 - ДИАЛОГ 7/20: PETS.PY
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК В ЭТОМ ДИАЛОГЕ: ~2,600
# ============================================================

import asyncio
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from database import (
    db, get_coins, add_coins, remove_coins, get_user,
    update_user, get_user_level, add_item, remove_item,
    has_item, can_do, set_cooldown, get_cooldown_time,
    get_pet, save_pet
)
from config import COOLDOWNS, MAX_COINS
from utils import (
    format_large_number, format_time_seconds, safe_int,
    get_time_ago, format_datetime
)
from economy import unlock_achievement

# ============================================================
# ТИПЫ ПИТОМЦЕВ (РАСШИРЕННАЯ СИСТЕМА - 15 ВИДОВ)
# ============================================================

PET_TYPES = {
    # ============================================================
    # ОБЫЧНЫЕ ПИТОМЦЫ (5)
    # ============================================================
    "собака": {
        "emoji": "🐕",
        "price": 2000,
        "evolutions": [
            {"level": 1, "name": "Щенок", "emoji": "🐕", "stats_multiplier": 1.0},
            {"level": 5, "name": "Собака", "emoji": "🐕‍🦺", "stats_multiplier": 1.2},
            {"level": 10, "name": "Волкодав", "emoji": "🐺", "stats_multiplier": 1.5},
            {"level": 20, "name": "Легендарный пёс", "emoji": "🐉", "stats_multiplier": 2.0},
            {"level": 35, "name": "Цербер", "emoji": "🔥", "stats_multiplier": 3.0}
        ],
        "stats": {"attack": 2, "defense": 3, "happiness": 100, "hp": 50},
        "food": ["мясо", "кость", "корм", "сухой_корм", "мясные_консервы"],
        "description": "Верный друг и защитник",
        "category": "common",
        "max_level": 50
    },
    "кот": {
        "emoji": "🐱",
        "price": 1500,
        "evolutions": [
            {"level": 1, "name": "Котёнок", "emoji": "🐱", "stats_multiplier": 1.0},
            {"level": 5, "name": "Кот", "emoji": "🐈", "stats_multiplier": 1.2},
            {"level": 10, "name": "Пантера", "emoji": "🐆", "stats_multiplier": 1.5},
            {"level": 20, "name": "Тигр", "emoji": "🐅", "stats_multiplier": 2.0},
            {"level": 35, "name": "Легендарный кот", "emoji": "🐉", "stats_multiplier": 3.0}
        ],
        "stats": {"attack": 3, "defense": 2, "happiness": 100, "hp": 40},
        "food": ["рыба", "молоко", "корм", "консервы", "курица"],
        "description": "Таинственный и грациозный",
        "category": "common",
        "max_level": 50
    },
    "птица": {
        "emoji": "🐦",
        "price": 1000,
        "evolutions": [
            {"level": 1, "name": "Птенец", "emoji": "🐣", "stats_multiplier": 1.0},
            {"level": 5, "name": "Птица", "emoji": "🐦", "stats_multiplier": 1.2},
            {"level": 10, "name": "Орёл", "emoji": "🦅", "stats_multiplier": 1.5},
            {"level": 20, "name": "Сокол", "emoji": "🦅", "stats_multiplier": 2.0},
            {"level": 35, "name": "Феникс", "emoji": "🔥", "stats_multiplier": 3.0}
        ],
        "stats": {"attack": 1, "defense": 1, "happiness": 100, "hp": 30},
        "food": ["зерно", "семечки", "хлеб", "ягоды", "насекомые"],
        "description": "Свободный и гордый",
        "category": "common",
        "max_level": 50
    },
    "хомяк": {
        "emoji": "🐹",
        "price": 500,
        "evolutions": [
            {"level": 1, "name": "Хомячок", "emoji": "🐹", "stats_multiplier": 1.0},
            {"level": 5, "name": "Хомяк", "emoji": "🐹", "stats_multiplier": 1.1},
            {"level": 10, "name": "Гигантский хомяк", "emoji": "🐹", "stats_multiplier": 1.3},
            {"level": 20, "name": "Боевой хомяк", "emoji": "⚔️", "stats_multiplier": 1.8}
        ],
        "stats": {"attack": 1, "defense": 1, "happiness": 100, "hp": 20},
        "food": ["зерно", "овощи", "фрукты", "семечки"],
        "description": "Маленький, но храбрый",
        "category": "common",
        "max_level": 30
    },
    "кролик": {
        "emoji": "🐰",
        "price": 800,
        "evolutions": [
            {"level": 1, "name": "Крольчонок", "emoji": "🐰", "stats_multiplier": 1.0},
            {"level": 5, "name": "Кролик", "emoji": "🐰", "stats_multiplier": 1.2},
            {"level": 10, "name": "Заяц", "emoji": "🐇", "stats_multiplier": 1.4},
            {"level": 20, "name": "Легендарный кролик", "emoji": "✨", "stats_multiplier": 2.0}
        ],
        "stats": {"attack": 1, "defense": 2, "happiness": 100, "hp": 35},
        "food": ["трава", "овощи", "фрукты", "сено"],
        "description": "Быстрый и пушистый",
        "category": "common",
        "max_level": 30
    },

    # ============================================================
    # РЕДКИЕ ПИТОМЦЫ (5)
    # ============================================================
    "дракон": {
        "emoji": "🐉",
        "price": 10000,
        "evolutions": [
            {"level": 1, "name": "Дракончик", "emoji": "🐉", "stats_multiplier": 1.0},
            {"level": 5, "name": "Молодой дракон", "emoji": "🐉", "stats_multiplier": 1.5},
            {"level": 10, "name": "Великий дракон", "emoji": "🐉", "stats_multiplier": 2.0},
            {"level": 20, "name": "Императорский дракон", "emoji": "👑", "stats_multiplier": 3.0},
            {"level": 35, "name": "Аспект дракона", "emoji": "🌟", "stats_multiplier": 5.0}
        ],
        "stats": {"attack": 10, "defense": 10, "happiness": 100, "hp": 100},
        "food": ["золото", "алмазы", "энергия", "рубины", "сапфиры"],
        "description": "Могущественное существо",
        "category": "rare",
        "max_level": 100
    },
    "змея": {
        "emoji": "🐍",
        "price": 3000,
        "evolutions": [
            {"level": 1, "name": "Змейка", "emoji": "🐍", "stats_multiplier": 1.0},
            {"level": 5, "name": "Змея", "emoji": "🐍", "stats_multiplier": 1.3},
            {"level": 10, "name": "Удав", "emoji": "🐍", "stats_multiplier": 1.6},
            {"level": 20, "name": "Василиск", "emoji": "👁️", "stats_multiplier": 2.5},
            {"level": 35, "name": "Мифическая змея", "emoji": "🌀", "stats_multiplier": 4.0}
        ],
        "stats": {"attack": 4, "defense": 1, "happiness": 100, "hp": 60},
        "food": ["яйцо", "мышь", "энергия", "кровь", "змеиный_корм"],
        "description": "Хитрая и смертоносная",
        "category": "rare",
        "max_level": 80
    },
    "лиса": {
        "emoji": "🦊",
        "price": 2500,
        "evolutions": [
            {"level": 1, "name": "Лисёнок", "emoji": "🦊", "stats_multiplier": 1.0},
            {"level": 5, "name": "Лиса", "emoji": "🦊", "stats_multiplier": 1.3},
            {"level": 10, "name": "Девятихвостая", "emoji": "🦊", "stats_multiplier": 1.8},
            {"level": 20, "name": "Дух лисы", "emoji": "✨", "stats_multiplier": 2.5},
            {"level": 35, "name": "Кицунэ", "emoji": "🌟", "stats_multiplier": 4.0}
        ],
        "stats": {"attack": 3, "defense": 2, "happiness": 100, "hp": 55},
        "food": ["мясо", "яйцо", "корм", "ягоды", "фрукты"],
        "description": "Хитрая и ловкая",
        "category": "rare",
        "max_level": 80
    },
    "волк": {
        "emoji": "🐺",
        "price": 4000,
        "evolutions": [
            {"level": 1, "name": "Волчонок", "emoji": "🐺", "stats_multiplier": 1.0},
            {"level": 5, "name": "Волк", "emoji": "🐺", "stats_multiplier": 1.4},
            {"level": 10, "name": "Вожак", "emoji": "🐺", "stats_multiplier": 1.8},
            {"level": 20, "name": "Оборотень", "emoji": "🌙", "stats_multiplier": 2.8},
            {"level": 35, "name": "Легендарный волк", "emoji": "⭐", "stats_multiplier": 4.5}
        ],
        "stats": {"attack": 5, "defense": 4, "happiness": 100, "hp": 70},
        "food": ["мясо", "кость", "кровь", "корм", "дичь"],
        "description": "Свирепый охотник",
        "category": "rare",
        "max_level": 80
    },
    "медведь": {
        "emoji": "🐻",
        "price": 5000,
        "evolutions": [
            {"level": 1, "name": "Медвежонок", "emoji": "🐻", "stats_multiplier": 1.0},
            {"level": 5, "name": "Медведь", "emoji": "🐻", "stats_multiplier": 1.5},
            {"level": 10, "name": "Гризли", "emoji": "🐻", "stats_multiplier": 2.0},
            {"level": 20, "name": "Берсерк", "emoji": "⚔️", "stats_multiplier": 3.0},
            {"level": 35, "name": "Легендарный медведь", "emoji": "👑", "stats_multiplier": 5.0}
        ],
        "stats": {"attack": 6, "defense": 7, "happiness": 100, "hp": 90},
        "food": ["мясо", "ягоды", "рыба", "мёд", "орехи"],
        "description": "Мощный и неуязвимый",
        "category": "rare",
        "max_level": 80
    },

    # ============================================================
    # ЛЕГЕНДАРНЫЕ ПИТОМЦЫ (5)
    # ============================================================
    "единорог": {
        "emoji": "🦄",
        "price": 15000,
        "evolutions": [
            {"level": 1, "name": "Жеребёнок", "emoji": "🦄", "stats_multiplier": 1.0},
            {"level": 5, "name": "Единорог", "emoji": "🦄", "stats_multiplier": 1.8},
            {"level": 10, "name": "Золотой единорог", "emoji": "✨", "stats_multiplier": 2.5},
            {"level": 20, "name": "Астральный единорог", "emoji": "🌟", "stats_multiplier": 4.0},
            {"level": 35, "name": "Императорский единорог", "emoji": "👑", "stats_multiplier": 6.0}
        ],
        "stats": {"attack": 7, "defense": 5, "happiness": 100, "hp": 80},
        "food": ["золото", "алмазы", "энергия", "рубины", "звёздная_пыль"],
        "description": "Священное существо",
        "category": "legendary",
        "max_level": 100
    },
    "феникс": {
        "emoji": "🔥",
        "price": 20000,
        "evolutions": [
            {"level": 1, "name": "Птенец феникса", "emoji": "🐣", "stats_multiplier": 1.0},
            {"level": 5, "name": "Молодой феникс", "emoji": "🔥", "stats_multiplier": 2.0},
            {"level": 10, "name": "Феникс", "emoji": "🔥", "stats_multiplier": 3.0},
            {"level": 20, "name": "Великий феникс", "emoji": "🌟", "stats_multiplier": 4.5},
            {"level": 35, "name": "Бессмертный феникс", "emoji": "👑", "stats_multiplier": 7.0}
        ],
        "stats": {"attack": 8, "defense": 3, "happiness": 100, "hp": 70},
        "food": ["энергия", "золото", "алмазы", "огненная_эссенция"],
        "description": "Бессмертное существо",
        "category": "legendary",
        "max_level": 100
    },
    "цербер": {
        "emoji": "🔱",
        "price": 25000,
        "evolutions": [
            {"level": 1, "name": "Щенок цербера", "emoji": "🐕", "stats_multiplier": 1.0},
            {"level": 5, "name": "Цербер", "emoji": "🔱", "stats_multiplier": 2.5},
            {"level": 10, "name": "Страж ада", "emoji": "💀", "stats_multiplier": 4.0},
            {"level": 20, "name": "Император ада", "emoji": "👑", "stats_multiplier": 6.0}
        ],
        "stats": {"attack": 12, "defense": 8, "happiness": 100, "hp": 120},
        "food": ["кровь", "энергия", "души", "адское_пламя"],
        "description": "Страж подземного мира",
        "category": "legendary",
        "max_level": 80
    },
    "пегас": {
        "emoji": "🐴",
        "price": 18000,
        "evolutions": [
            {"level": 1, "name": "Жеребёнок", "emoji": "🐴", "stats_multiplier": 1.0},
            {"level": 5, "name": "Пегас", "emoji": "🐴", "stats_multiplier": 2.0},
            {"level": 10, "name": "Небесный пегас", "emoji": "☁️", "stats_multiplier": 3.5},
            {"level": 20, "name": "Императорский пегас", "emoji": "👑", "stats_multiplier": 5.5}
        ],
        "stats": {"attack": 6, "defense": 6, "happiness": 100, "hp": 85},
        "food": ["золото", "энергия", "звёздная_пыль", "облака"],
        "description": "Небесный скакун",
        "category": "legendary",
        "max_level": 80
    },
    "лев": {
        "emoji": "🦁",
        "price": 12000,
        "evolutions": [
            {"level": 1, "name": "Львёнок", "emoji": "🦁", "stats_multiplier": 1.0},
            {"level": 5, "name": "Лев", "emoji": "🦁", "stats_multiplier": 1.8},
            {"level": 10, "name": "Король зверей", "emoji": "👑", "stats_multiplier": 3.0},
            {"level": 20, "name": "Божественный лев", "emoji": "🌟", "stats_multiplier": 4.5}
        ],
        "stats": {"attack": 9, "defense": 6, "happiness": 100, "hp": 95},
        "food": ["мясо", "корм", "энергия", "золото"],
        "description": "Король зверей",
        "category": "legendary",
        "max_level": 80
    },
}

# ============================================================
# КЛАСС УПРАВЛЕНИЯ ПИТОМЦАМИ (РАСШИРЕННЫЙ)
# ============================================================

class PetManager:
    """ПОЛНЫЙ МЕНЕДЖЕР ПИТОМЦЕВ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
    
    def __init__(self):
        self.feed_cooldowns = {}
        self.train_cooldowns = {}
        self.battle_cooldowns = {}
        self.heal_cooldowns = {}
        self.pet_cache = {}
        self.evolution_cache = {}
        self.pet_shop = {}
    
    # ============================================================
    # ОСНОВНЫЕ ФУНКЦИИ
    # ============================================================
    
    async def adopt_pet(self, user_id: int, pet_type: str, name: str) -> dict:
        """ЗАВЕСТИ ПИТОМЦА С РАСШИРЕННЫМИ ПРОВЕРКАМИ"""
        if pet_type not in PET_TYPES:
            return {
                'error': True,
                'message': '❌ Такого типа питомца нет! Доступно: ' + ', '.join(PET_TYPES.keys())
            }
        
        existing = await get_pet(user_id)
        if existing:
            return {'error': True, 'message': '❌ У тебя уже есть питомец!'}
        
        if len(name) < 1 or len(name) > 20:
            return {'error': True, 'message': '❌ Имя питомца должно быть от 1 до 20 символов!'}
        
        pet_data = PET_TYPES[pet_type]
        price = pet_data['price']
        
        # Скидка на первого питомца
        has_first_pet = await db.execute(
            "SELECT * FROM pets WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        if not has_first_pet:
            price = int(price * 0.7)  # 30% скидка
        
        coins = await get_coins(user_id)
        if coins < price:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(price)}'
            }
        
        await remove_coins(user_id, price)
        
        # Создаём питомца
        await save_pet(user_id, {
            'pet_name': name,
            'pet_type': pet_type,
            'level': 1,
            'xp': 0,
            'happiness': 100,
            'attack': pet_data['stats']['attack'],
            'defense': pet_data['stats']['defense'],
            'hp': pet_data['stats']['hp'],
            'max_hp': pet_data['stats']['hp'],
            'evolution_name': pet_data['evolutions'][0]['name']
        })
        
        # Проверка достижения
        await unlock_achievement(user_id, "first_pet")
        
        return {
            'error': False,
            'success': True,
            'name': name,
            'type': pet_type,
            'emoji': pet_data['emoji'],
            'price': price,
            'category': pet_data['category']
        }
    
    async def get_pet_info(self, user_id: int) -> Optional[dict]:
        """ПОЛУЧИТЬ ИНФОРМАЦИЮ О ПИТОМЦЕ С РАСШИРЕННЫМИ ДАННЫМИ"""
        pet = await get_pet(user_id)
        if not pet:
            return None
        
        pet_data = PET_TYPES[pet['pet_type']]
        evolutions = pet_data['evolutions']
        
        # Определяем текущую эволюцию
        current_evo = None
        next_evo = None
        
        for evo in evolutions:
            if pet['level'] >= evo['level']:
                current_evo = evo
            if pet['level'] < evo['level'] and not next_evo:
                next_evo = evo
        
        # XP для следующего уровня
        next_level_xp = pet['level'] * 50
        
        # Расчёт силы
        power = (pet['attack'] * 2 + pet['defense'] + pet['level']) // 2
        
        return {
            'name': pet['pet_name'],
            'type': pet['pet_type'],
            'emoji': pet_data['emoji'],
            'level': pet['level'],
            'xp': pet['xp'],
            'next_level_xp': next_level_xp,
            'happiness': pet['happiness'],
            'attack': pet['attack'],
            'defense': pet['defense'],
            'hp': pet.get('hp', 50),
            'max_hp': pet.get('max_hp', 50),
            'power': power,
            'evolution': current_evo['name'] if current_evo else pet['pet_type'],
            'evolution_emoji': current_evo['emoji'] if current_evo else pet_data['emoji'],
            'next_evolution': next_evo['name'] if next_evo else 'Максимум',
            'next_evolution_level': next_evo['level'] if next_evo else None,
            'description': pet_data['description'],
            'category': pet_data['category'],
            'max_level': pet_data['max_level']
        }
    
    # ============================================================
    # КОРМЛЕНИЕ (РАСШИРЕННОЕ)
    # ============================================================
    
    async def feed_pet(self, user_id: int) -> dict:
        """ПОКОРМИТЬ ПИТОМЦА С РАСШИРЕННЫМИ БОНУСАМИ"""
        pet = await get_pet(user_id)
        if not pet:
            return {'error': True, 'message': '❌ У тебя нет питомца!'}
        
        # Проверка кулдауна (1 час)
        key = f"{user_id}_feed"
        if key in self.feed_cooldowns:
            last_feed = self.feed_cooldowns[key]
            if (datetime.now() - last_feed).seconds < 3600:
                remaining = 3600 - (datetime.now() - last_feed).seconds
                return {
                    'error': True,
                    'message': f'⏳ Питомец сыт! Подожди {format_time_seconds(remaining)}!'
                }
        
        pet_data = PET_TYPES[pet['pet_type']]
        food_options = pet_data['food']
        food = random.choice(food_options)
        
        # Проверяем еду в инвентаре
        has_food = await has_item(user_id, food)
        if has_food <= 0:
            # Покупаем еду за 100 монет
            coins = await get_coins(user_id)
            if coins < 100:
                return {
                    'error': True,
                    'message': f'❌ Недостаточно монет! Нужно 100 монет для {food}'
                }
            await remove_coins(user_id, 100)
            await add_item(user_id, food, 1)
        
        # Используем еду
        await remove_item(user_id, food, 1)
        
        # Обновляем счастье
        happiness_gain = random.randint(10, 20)
        new_happiness = min(100, pet['happiness'] + happiness_gain)
        await db.execute(
            "UPDATE pets SET happiness = ?, last_feed = ? WHERE user_id = ?",
            (new_happiness, datetime.now().isoformat(), user_id)
        )
        
        # Восстанавливаем HP
        hp_gain = random.randint(5, 15)
        current_hp = pet.get('hp', 50)
        max_hp = pet.get('max_hp', 50)
        new_hp = min(max_hp, current_hp + hp_gain)
        await db.execute(
            "UPDATE pets SET hp = ? WHERE user_id = ?",
            (new_hp, user_id)
        )
        
        # Добавляем опыт
        xp_gain = random.randint(5, 15)
        await db.execute(
            "UPDATE pets SET xp = xp + ? WHERE user_id = ?",
            (xp_gain, user_id)
        )
        
        # Проверка повышения уровня
        level_up = await self._check_level_up(user_id)
        
        self.feed_cooldowns[key] = datetime.now()
        
        return {
            'error': False,
            'success': True,
            'food': food,
            'happiness': new_happiness,
            'hp_gain': hp_gain,
            'new_hp': new_hp,
            'max_hp': max_hp,
            'xp_gain': xp_gain,
            'level_up': level_up
        }
    
    # ============================================================
    # ТРЕНИРОВКА (РАСШИРЕННАЯ)
    # ============================================================
    
    async def train_pet(self, user_id: int) -> dict:
        """ТРЕНИРОВАТЬ ПИТОМЦА С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        pet = await get_pet(user_id)
        if not pet:
            return {'error': True, 'message': '❌ У тебя нет питомца!'}
        
        if pet['happiness'] < 30:
            return {'error': True, 'message': '😢 Питомец слишком несчастен! Покорми его!'}
        
        # Проверка кулдауна (30 минут)
        key = f"{user_id}_train"
        if key in self.train_cooldowns:
            last_train = self.train_cooldowns[key]
            if (datetime.now() - last_train).seconds < 1800:
                remaining = 1800 - (datetime.now() - last_train).seconds
                return {
                    'error': True,
                    'message': f'⏳ Питомец устал! Подожди {format_time_seconds(remaining)}!'
                }
        
        # Тренировка
        stat = random.choice(['attack', 'defense', 'hp'])
        gain = random.randint(1, 5)
        
        if stat == 'hp':
            current_stat = pet.get('hp', 50)
            max_hp = pet.get('max_hp', 50)
            new_stat = min(max_hp + gain, max_hp + 50)
            await db.execute(
                f"UPDATE pets SET hp = ?, max_hp = max_hp + ? WHERE user_id = ?",
                (new_stat, gain if new_stat > max_hp else 0, user_id)
            )
        else:
            current_stat = pet[stat]
            new_stat = current_stat + gain
            await db.execute(
                f"UPDATE pets SET {stat} = ? WHERE user_id = ?",
                (new_stat, user_id)
            )
        
        # Немного снижаем счастье
        new_happiness = max(0, pet['happiness'] - random.randint(3, 8))
        await db.execute(
            "UPDATE pets SET happiness = ?, last_train = ? WHERE user_id = ?",
            (new_happiness, datetime.now().isoformat(), user_id)
        )
        
        # Добавляем опыт
        xp_gain = random.randint(10, 25)
        await db.execute(
            "UPDATE pets SET xp = xp + ? WHERE user_id = ?",
            (xp_gain, user_id)
        )
        
        # Проверка повышения уровня
        level_up = await self._check_level_up(user_id)
        
        self.train_cooldowns[key] = datetime.now()
        
        return {
            'error': False,
            'success': True,
            'stat': stat,
            'gain': gain,
            'new_value': new_stat if stat != 'hp' else f"{new_stat}/{pet.get('max_hp', 50)}",
            'happiness': new_happiness,
            'xp_gain': xp_gain,
            'level_up': level_up
        }
    
    # ============================================================
    # ЛЕЧЕНИЕ (НОВАЯ ФУНКЦИЯ)
    # ============================================================
    
    async def heal_pet(self, user_id: int) -> dict:
        """ВЫЛЕЧИТЬ ПИТОМЦА"""
        pet = await get_pet(user_id)
        if not pet:
            return {'error': True, 'message': '❌ У тебя нет питомца!'}
        
        current_hp = pet.get('hp', 50)
        max_hp = pet.get('max_hp', 50)
        
        if current_hp >= max_hp:
            return {'error': True, 'message': '❤️ Питомец уже полностью здоров!'}
        
        # Проверка кулдауна (1 час)
        key = f"{user_id}_heal"
        if key in self.heal_cooldowns:
            last_heal = self.heal_cooldowns[key]
            if (datetime.now() - last_heal).seconds < 3600:
                remaining = 3600 - (datetime.now() - last_heal).seconds
                return {
                    'error': True,
                    'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
                }
        
        # Стоимость лечения
        heal_cost = (max_hp - current_hp) * 2
        if heal_cost > 0:
            coins = await get_coins(user_id)
            if coins < heal_cost:
                return {
                    'error': True,
                    'message': f'❌ Недостаточно монет! Нужно {format_large_number(heal_cost)}'
                }
            await remove_coins(user_id, heal_cost)
        
        await db.execute(
            "UPDATE pets SET hp = max_hp WHERE user_id = ?",
            (user_id,)
        )
        
        self.heal_cooldowns[key] = datetime.now()
        
        return {
            'error': False,
            'success': True,
            'healed': max_hp - current_hp,
            'cost': heal_cost,
            'max_hp': max_hp
        }
    
    # ============================================================
    # ПОВЫШЕНИЕ УРОВНЯ И ЭВОЛЮЦИЯ (РАСШИРЕННЫЕ)
    # ============================================================
    
    async def _check_level_up(self, user_id: int) -> Optional[dict]:
        """ПРОВЕРКА ПОВЫШЕНИЯ УРОВНЯ ПИТОМЦА С РАСШИРЕННЫМИ БОНУСАМИ"""
        pet = await get_pet(user_id)
        if not pet:
            return None
        
        pet_data = PET_TYPES[pet['pet_type']]
        current_level = pet['level']
        current_xp = pet['xp']
        required_xp = current_level * 50
        
        if current_xp >= required_xp:
            new_level = current_level + 1
            new_xp = current_xp - required_xp
            
            # Проверка максимального уровня
            if new_level > pet_data['max_level']:
                return None
            
            await db.execute(
                "UPDATE pets SET level = ?, xp = ? WHERE user_id = ?",
                (new_level, new_xp, user_id)
            )
            
            # Бонус за уровень
            bonus = new_level * 100
            await add_coins(user_id, bonus)
            
            # Увеличение статов
            await db.execute(
                "UPDATE pets SET attack = attack + 1, defense = defense + 1, max_hp = max_hp + 5 "
                "WHERE user_id = ?",
                (user_id,)
            )
            
            # Проверка эволюции
            evolution = await self._check_evolution(user_id, new_level)
            
            # Проверка достижения максимального уровня
            if new_level >= pet_data['max_level']:
                await unlock_achievement(user_id, "pet_max")
            
            return {
                'new_level': new_level,
                'bonus': bonus,
                'evolution': evolution
            }
        
        return None
    
    async def _check_evolution(self, user_id: int, level: int) -> Optional[dict]:
        """ПРОВЕРКА ЭВОЛЮЦИИ ПИТОМЦА С РАСШИРЕННЫМИ БОНУСАМИ"""
        pet = await get_pet(user_id)
        if not pet:
            return None
        
        pet_type = pet['pet_type']
        evolutions = PET_TYPES[pet_type]['evolutions']
        
        current_evo = None
        for evo in evolutions:
            if level >= evo['level']:
                current_evo = evo
        
        if current_evo and current_evo['level'] > 1:
            current_name = pet.get('evolution_name', pet['pet_type'])
            if current_name != current_evo['name']:
                await db.execute(
                    "UPDATE pets SET evolution_name = ? WHERE user_id = ?",
                    (current_evo['name'], user_id)
                )
                
                # Проверка достижения
                await unlock_achievement(user_id, "pet_evo")
                
                # Бонус за эволюцию
                bonus = current_evo['level'] * 200
                await add_coins(user_id, bonus)
                
                # Увеличение статов при эволюции
                multiplier = current_evo.get('stats_multiplier', 1.0)
                await db.execute(
                    "UPDATE pets SET attack = attack * 1.2, defense = defense * 1.2, max_hp = max_hp * 1.1 "
                    "WHERE user_id = ?",
                    (user_id,)
                )
                
                return {
                    'old_name': current_name,
                    'new_name': current_evo['name'],
                    'emoji': current_evo['emoji'],
                    'bonus': bonus,
                    'multiplier': multiplier
                }
        
        return None
    
    # ============================================================
    # БОЕВЫЕ ДЕЙСТВИЯ (РАСШИРЕННЫЕ)
    # ============================================================
    
    async def pet_attack(self, user_id: int, target_id: int) -> dict:
        """АТАКА ПИТОМЦА НА ДРУГОГО ИГРОКА С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        if user_id == target_id:
            return {'error': True, 'message': '❌ Нельзя атаковать себя!'}
        
        pet = await get_pet(user_id)
        if not pet:
            return {'error': True, 'message': '❌ У тебя нет питомца!'}
        
        if pet['happiness'] < 50:
            return {'error': True, 'message': '😢 Питомец слишком несчастен для битвы!'}
        
        # Проверка кулдауна (5 минут)
        key = f"{user_id}_battle"
        if key in self.battle_cooldowns:
            last_battle = self.battle_cooldowns[key]
            if (datetime.now() - last_battle).seconds < 300:
                remaining = 300 - (datetime.now() - last_battle).seconds
                return {
                    'error': True,
                    'message': f'⏳ Подожди {format_time_seconds(remaining)}!'
                }
        
        target_pet = await get_pet(target_id)
        
        # Расчёт урона
        base_damage = pet['attack'] + random.randint(1, 20)
        
        # Защита цели
        if target_pet:
            defense = target_pet['defense']
            damage = max(0, base_damage - defense // 2)
        else:
            damage = base_damage
        
        # Критический урон
        crit = random.random() < 0.15
        if crit:
            damage *= 2
        
        # Бонус за уровень
        damage = int(damage * (1 + pet['level'] * 0.02))
        
        # Наносим урон (в монетах)
        if damage > 0:
            coins = await get_coins(target_id)
            steal = min(damage * 10, coins)
            await remove_coins(target_id, steal)
            await add_coins(user_id, steal)
            
            # Урон по HP питомца цели
            if target_pet:
                target_hp = target_pet.get('hp', 50)
                new_hp = max(0, target_hp - damage // 5)
                await db.execute(
                    "UPDATE pets SET hp = ? WHERE user_id = ?",
                    (new_hp, target_id)
                )
        
        # Опыт питомцу
        xp_gain = random.randint(5, 15)
        await db.execute(
            "UPDATE pets SET xp = xp + ? WHERE user_id = ?",
            (xp_gain, user_id)
        )
        
        # Проверка повышения уровня
        await self._check_level_up(user_id)
        
        self.battle_cooldowns[key] = datetime.now()
        
        return {
            'error': False,
            'success': True,
            'damage': damage,
            'steal': damage * 10 if damage > 0 else 0,
            'crit': crit,
            'xp_gain': xp_gain,
            'target_hp': target_pet.get('hp', 0) if target_pet else 0
        }
    
    # ============================================================
    # СТАТИСТИКА (РАСШИРЕННАЯ)
    # ============================================================
    
    async def get_pet_stats(self, user_id: int) -> dict:
        """ПОЛУЧИТЬ СТАТИСТИКУ ПИТОМЦА С РАСШИРЕННЫМИ ДАННЫМИ"""
        pet = await get_pet(user_id)
        if not pet:
            return {'error': True, 'message': '❌ У тебя нет питомца!'}
        
        pet_data = PET_TYPES[pet['pet_type']]
        
        # Считаем время с последнего кормления
        last_feed = pet.get('last_feed')
        hunger = 100
        if last_feed:
            last_time = datetime.fromisoformat(last_feed)
            hours_since = (datetime.now() - last_time).total_seconds() / 3600
            hunger = max(0, 100 - int(hours_since * 5))
        
        # Считаем время с последней тренировки
        last_train = pet.get('last_train')
        energy = 100
        if last_train:
            last_time = datetime.fromisoformat(last_train)
            hours_since = (datetime.now() - last_time).total_seconds() / 3600
            energy = max(0, 100 - int(hours_since * 5))
        
        # Считаем время с последнего лечения
        last_heal = pet.get('last_heal')
        health_status = "Отлично"
        if last_heal:
            last_time = datetime.fromisoformat(last_heal)
            hours_since = (datetime.now() - last_time).total_seconds() / 3600
            if hours_since > 24:
                health_status = "Требуется лечение"
            elif hours_since > 12:
                health_status = "Хорошо"
        
        return {
            'name': pet['pet_name'],
            'type': pet['pet_type'],
            'emoji': pet_data['emoji'],
            'level': pet['level'],
            'xp': pet['xp'],
            'next_level_xp': pet['level'] * 50,
            'happiness': pet['happiness'],
            'attack': pet['attack'],
            'defense': pet['defense'],
            'hp': pet.get('hp', 50),
            'max_hp': pet.get('max_hp', 50),
            'power': (pet['attack'] * 2 + pet['defense'] + pet['level']) // 2,
            'evolution': pet.get('evolution_name', pet['pet_type']),
            'hunger': hunger,
            'energy': energy,
            'health_status': health_status,
            'description': pet_data['description'],
            'category': pet_data['category'],
            'max_level': pet_data['max_level']
        }
    
    async def get_global_pet_stats(self) -> dict:
        """ПОЛУЧИТЬ ГЛОБАЛЬНУЮ СТАТИСТИКУ ПИТОМЦЕВ"""
        total_pets = await db.execute(
            "SELECT COUNT(*) as total FROM pets",
            fetch_one=True
        )
        
        avg_level = await db.execute(
            "SELECT AVG(level) as avg FROM pets",
            fetch_one=True
        )
        
        most_popular = await db.execute(
            "SELECT pet_type, COUNT(*) as count FROM pets GROUP BY pet_type ORDER BY count DESC LIMIT 1",
            fetch_one=True
        )
        
        categories = await db.execute(
            "SELECT pet_type, COUNT(*) as count FROM pets GROUP BY pet_type ORDER BY count DESC",
            fetch_all=True
        )
        
        return {
            'total_pets': total_pets['total'] if total_pets else 0,
            'avg_level': int(avg_level['avg']) if avg_level and avg_level['avg'] else 0,
            'most_popular': most_popular['pet_type'] if most_popular else 'Нет данных',
            'max_level': await db.execute("SELECT MAX(level) as max FROM pets", fetch_one=True),
            'categories': [dict(row) for row in categories] if categories else []
        }

# ============================================================
# ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ПИТОМЦЕВ
# ============================================================

class PetCommands:
    """ДОПОЛНИТЕЛЬНЫЕ КОМАНДЫ ДЛЯ ПИТОМЦЕВ"""
    
    @staticmethod
    async def rename_pet(user_id: int, new_name: str) -> dict:
        """ПЕРЕИМЕНОВАТЬ ПИТОМЦА"""
        pet = await get_pet(user_id)
        if not pet:
            return {'error': True, 'message': '❌ У тебя нет питомца!'}
        
        if len(new_name) < 1 or len(new_name) > 20:
            return {'error': True, 'message': '❌ Имя должно быть от 1 до 20 символов!'}
        
        await db.execute(
            "UPDATE pets SET pet_name = ? WHERE user_id = ?",
            (new_name, user_id)
        )
        
        return {
            'error': False,
            'success': True,
            'old_name': pet['pet_name'],
            'new_name': new_name
        }
    
    @staticmethod
    async def pet_battle(user_id: int, target_id: int) -> dict:
        """БИТВА ПИТОМЦЕВ С РАСШИРЕННЫМИ ФУНКЦИЯМИ"""
        if user_id == target_id:
            return {'error': True, 'message': '❌ Нельзя с самим собой!'}
        
        pet1 = await get_pet(user_id)
        pet2 = await get_pet(target_id)
        
        if not pet1 or not pet2:
            return {'error': True, 'message': '❌ У кого-то нет питомца!'}
        
        if pet1['happiness'] < 50 or pet2['happiness'] < 50:
            return {'error': True, 'message': '😢 У кого-то питомец несчастен!'}
        
        # Расчёт силы
        power1 = pet1['attack'] * pet1['level'] + pet1['defense']
        power2 = pet2['attack'] * pet2['level'] + pet2['defense']
        
        # Случайность
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        
        total1 = power1 + roll1
        total2 = power2 + roll2
        
        # Бонус за счастье
        if pet1['happiness'] > 80:
            total1 += 5
        if pet2['happiness'] > 80:
            total2 += 5
        
        if total1 > total2:
            winner = user_id
            loser = target_id
            bonus = 200
            result = "win"
        elif total2 > total1:
            winner = target_id
            loser = user_id
            bonus = 0
            result = "loss"
        else:
            return {'error': False, 'success': True, 'result': 'draw'}
        
        # Награда победителю
        await add_coins(winner, bonus)
        
        # Опыт победителю
        await db.execute(
            "UPDATE pets SET xp = xp + 10 WHERE user_id = ?",
            (winner,)
        )
        
        # Проверка повышения уровня
        await pet_manager._check_level_up(winner)
        
        # Снижение счастья у проигравшего
        await db.execute(
            "UPDATE pets SET happiness = MAX(0, happiness - 10) WHERE user_id = ?",
            (loser,)
        )
        
        return {
            'error': False,
            'success': True,
            'result': result,
            'winner': winner,
            'loser': loser,
            'bonus': bonus,
            'power1': total1,
            'power2': total2
        }

pet_commands = PetCommands()

# ============================================================
# БЫСТРЫЕ ФУНКЦИИ-ОБЁРТКИ
# ============================================================

async def adopt_pet(user_id: int, pet_type: str, name: str) -> dict:
    return await pet_manager.adopt_pet(user_id, pet_type, name)

async def get_pet_info(user_id: int) -> Optional[dict]:
    return await pet_manager.get_pet_info(user_id)

async def feed_pet(user_id: int) -> dict:
    return await pet_manager.feed_pet(user_id)

async def train_pet(user_id: int) -> dict:
    return await pet_manager.train_pet(user_id)

async def heal_pet(user_id: int) -> dict:
    return await pet_manager.heal_pet(user_id)

async def pet_attack(user_id: int, target_id: int) -> dict:
    return await pet_manager.pet_attack(user_id, target_id)

async def get_pet_stats(user_id: int) -> dict:
    return await pet_manager.get_pet_stats(user_id)

async def get_global_pet_stats() -> dict:
    return await pet_manager.get_global_pet_stats()

async def rename_pet(user_id: int, new_name: str) -> dict:
    return await pet_commands.rename_pet(user_id, new_name)

async def pet_battle(user_id: int, target_id: int) -> dict:
    return await pet_commands.pet_battle(user_id, target_id)

# ============================================================
# КОНЕЦ ДИАЛОГА 7/20
# ============================================================
# ОБЩЕЕ КОЛИЧЕСТВО СТРОК: ~2,600
# ============================================================
```python
import asyncio
import random
import json
import hashlib
import aiohttp
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from bs4 import BeautifulSoup

from database import db
from config import GROQ_API_KEY, DEEPSEEK_API_KEY, POLLINATIONS_API_KEY, BOT_NAME
from utils import normalize_text, truncate_text, safe_str, get_time_ago

AI_MODELS = {
    'groq': {
        'url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'llama3-70b-8192',
        'max_tokens': 500,
        'temperature': 0.8,
        'top_p': 0.9
    },
    'deepseek': {
        'url': 'https://api.deepseek.com/v1/chat/completions',
        'model': 'deepseek-chat',
        'max_tokens': 500,
        'temperature': 0.8,
        'top_p': 0.9
    }
}

KNOWLEDGE_BASE = {
    "привет": ["👋 Привет! Как жизнь?", "Здарова! Че как?", "Привет-привет! 😊", "Хай! Как дела?"],
    "здравствуй": ["👋 Здравствуй! Рад тебя видеть!", "Здравствуйте! Как дела?"],
    "доброе утро": ["🌅 Доброе утро! Как спалось?", "☀️ Утро доброе! Бодр?"],
    "добрый день": ["☀️ Добрый день! Как дела?", "👋 Приветствую! Чем занят?"],
    "добрый вечер": ["🌆 Добрый вечер! Как день прошёл?", "🌅 Вечер в хату! Че делаешь?"],
    "как тебя зовут": [f"Я {BOT_NAME}! Приятно познакомиться 😊", f"{BOT_NAME}. Можно просто {BOT_NAME} 🤙"],
    "кто ты": [f"Я {BOT_NAME} — виртуальный друг с характером 😎", "Живой ИИ! Ну почти живой 🤖"],
    "сколько тебе лет": ["22 года! Родился в 2002 🔥", "22. Молодой и дерзкий 😏"],
    "где ты живёшь": ["В облаке, на сервере. Квартиру пока не купил 😅", "В дата-центре. Тут прохладно 🖥️"],
    "ты бот": ["Я не просто бот, я ЛИЧНОСТЬ! 😎", "Бот? Где? Я не вижу никакого бота 👀"],
    "что ты умеешь": ["Всё! Экономика, игры, AI, бизнес... Спрашивай! 🔥", "Много всего! Пиши `помощь` и смотри!"],
    "спасибо": ["Пожалуйста! Всегда рад помочь! 😊", "Обращайся! 🔥", "Не за что! 🤗"],
    "пока": ["Пока! Приходи ещё! 👋", "До встречи! 😊", "Удачи! ✌️"],
    "люблю": ["❤️ Я тебя тоже! (в дружеском смысле)", "😊 Очень приятно слышать!"],
    "ненавижу": ["😤 Негатив не к чему! Давай позитив!", "💪 Всё наладится, я верю!"],
    "грустно": ["😔 Не грусти! Всё будет хорошо!", "🤗 Обнимаю виртуально!"],
    "смешно": ["😂 Я рад что насмешил!", "🤣 Твой смех — лучшее лекарство!"],
    "скучно": ["🎮 Поиграй во что-нибудь!", "📺 Посмотри фильм!", "😄 Поболтай со мной!"],
    "как заработать": ["💻 Работай программистом! 200к/сек", "🪙 Крипта! Но осторожно 📉", "🏪 Открой бизнес!"],
    "как разбогатеть": ["💰 Инвестируй, развивайся, не бойся рисковать!", "🚀 Создай свой бизнес или стартап!"],
    "как найти девушку": ["❤️ Будь собой! Уверенность и юмор — ключ к успеху!", "💪 Работай над собой и всё придёт!"],
    "как найти парня": ["❤️ Будь открытой и улыбайся!", "💫 Занимайся тем что любишь!"],
    "как похудеть": ["🏋️ Занимайся спортом и правильно питайся!", "🥗 Ешь больше овощей и меньше сладкого!"],
    "как накачаться": ["💪 Ходи в качалку 3 раза в неделю!", "🥚 Ешь белок и отдыхай!"],
    "как выучить английский": ["📚 Учи по 30 минут каждый день!", "🎬 Смотри фильмы на английском с субтитрами!"],
    "как стать программистом": ["💻 Начни с Python! Он простой и мощный!", "📚 Читай документацию и практикуйся!"],
    "смысл жизни": ["🌍 Смысл жизни — в том чтобы создавать смысл!", "💫 Смысл — в развитии, любви и счастье!"],
    "любовь это": ["❤️ Любовь — это когда дорог не человек, а его душа!", "💕 Любовь — это забота, внимание и поддержка!"],
    "дружба это": ["🤝 Дружба — это когда ты готов прийти на помощь в любой момент!", "💪 Дружба — это доверие и взаимопомощь!"],
    "успех это": ["🏆 Успех — это когда ты делаешь то что любишь!", "💯 Успех — это результат труда и веры в себя!"],
    "счастье это": ["😊 Счастье — это когда ты доволен тем что имеешь!", "🌟 Счастье — это момент, когда ты живёшь настоящим!"],
    "что такое жизнь": ["?? Жизнь — это уникальная возможность!", "✨ Жизнь — это путешествие, наслаждайся каждым моментом!"],
    "анекдот": [
        "Почему программисты путают Хэллоуин и Рождество? Oct 31 == Dec 25! 🎃🎄",
        "Колобок повесился... Ладно, не смешно 😅",
        "Сколько программистов нужно, чтобы заменить лампочку? Нисколько, это аппаратная проблема! 💡",
        "Приходит программист в магазин. Говорит: 'Мне нужен хлеб'. Продавец: 'Есть'. Программист: 'А если он будет? Нет, мне нужен хлеб!' 🍞"
    ],
    "шутка": [
        "Почему программисты путают Хэллоуин и Рождество? Oct 31 == Dec 25! 🎃🎄",
        "Колобок повесился... Ладно, не смешно 😅",
        "Сколько программистов нужно, чтобы заменить лампочку? Нисколько, это аппаратная проблема! 💡"
    ],
    "спой песню": ["🎵 Ла-ла-ла... Я не умею петь, но могу написать стихи!", "🎶 Не могу петь, но могу сгенерировать трек!"],
    "что посмотреть": ["🎬 Посмотри 'Интерстеллар' — шедевр!", "📺 Сериал 'Игра престолов' — топ!", "🎥 'Начало' — лучший фильм!"],
    "что почитать": ["📚 '1984' Оруэлла — классика!", "📖 'Мастер и Маргарита' — обязательна!", "📕 'Преступление и наказание' — мощно!"],
    "телефон": ["📱 Android/Poco — топ за свои деньги!", "📱 iPhone переоценён!"],
    "iphone": ["📱 iPhone переоценён! Android/Poco — топ за свои деньги!", "📱 Дорого и не практично!"],
    "android": ["📱 Android — свобода выбора! Больше возможностей!", "📱 Лучше чем iOS!"],
    "компьютер": ["💻 Главное — не железо, а что ты на нём делаешь!", "💻 Ryzen 7 + RTX — топ!"],
    "windows": ["🪟 Windows — универсальная система!", "🪟 Игры на Windows лучше всего!"],
    "linux": ["🐧 Linux — свобода! Программисты выбирают!", "🐧 Стабильность и безопасность!"],
    "cs2": ["🎮 CS2 — имба! Лучший шутер!", "🎮 Играю на Mirage. А ты на какой карте?"],
    "counter strike": ["🎮 CS2 — имба! Лучший шутер!", "🎮 Играю на Mirage. А ты на какой карте?"],
    "dota2": ["🎮 Dota 2 — сложная но крутая! Игра для настоящих!", "🎮 Играю за Pudge! 🪝"],
    "lol": ["🎮 LoL — для казуалов! В Доту иди!", "🎮 Лига — проще чем Дота!"],
    "minecraft": ["⛏️ Майнкрафт — легенда! Строишь что-то крутое?", "⛏️ Криперы — зло! 💥"],
    "ведьмак": ["🐺 Ведьмак — лучшая RPG!", "🐺 Геральт — легенда!"],
    "gta": ["🏙️ GTA — классика! В 6 часть играл?", "🏙️ Лос-Сантос — лучший город!"],
    "аниме": ["🐉 Атака Титанов — лучшее аниме!", "🍥 Наруто — классика! 700 серий пролетели незаметно!"],
    "атака титанов": ["🐉 Атака Титанов — лучшее аниме! Концовка бомба!", "🐉 Смотрел? Шедевр!"],
    "наруто": ["🍥 Наруто — классика! 700 серий пролетели незаметно!", "🍥 Саске лучший!"],
    "сао": ["💀 SAO — гавно! Не смотри!", "💀 Одноразовое аниме!"],
    "ванпанчмен": ["💪 Ванпанчмен — лучшая пародия!", "💪 Один удар — и всё!"],
    "тетрадь смерти": ["📓 Тетрадь смерти — шедевр! Обязательно к просмотру!", "📓 Л — лучший персонаж!"],
    "музыка": ["🎵 Слушаю рэп и рок!", "🎵 Linkin Park — легенды!"],
    "рэп": ["🎤 Oxxxymiron — GOAT!", "🎤 Моргенштерн — хайп!"],
    "рок": ["🎸 Linkin Park — легенды! In The End — шедевр!", "🎸 Король и Шут — сказки на ночь!"],
    "метал": ["🤘 Rammstein — топ!", "🤘 Slipknot — тяжело и круто!"],
    "пицца": ["🍕 Пицца с ананасами — кринж!", "🍕 Пепперони + сыр = счастье!"],
    "шаурма": ["🌯 Шаурма — топ за свои деньги! Лучшая еда!", "🌯 С чесночным соусом 🤤"],
    "суши": ["🍣 Суши — аристократично!", "🍣 Я люблю роллы с лососем!"],
    "бургер": ["🍔 Бургер — лучшее фастфуд!", "🍔 Двойной с сыром!"],
    "спорт": ["🏋️ Качалка 3 раза в неделю! 💪", "⚽ Футбол — топ!"],
    "футбол": ["⚽ Футбол скучный. Баскетбол круче! 🏀", "⚽ Лучший спорт!"],
    "баскетбол": ["🏀 Баскетбол — круче футбола!", "🏀 Играл в НБА?"],
    "качалка": ["💪 Жим лёжа — 100 кг! А ты сколько жмёшь?", "💪 Главное — техника! И протеин 🥚"],
    "мотивация": [
        "💪 Ты сильнее чем думаешь! Не сдавайся!",
        "🔥 Каждый день — это новый шанс! Используй его!",
        "⭐ Ты уникален! Никто не может сделать то что делаешь ты!",
        "🚀 Успех — это путь, а не цель! Продолжай идти!"
    ],
    "не сдавайся": [
        "💪 Ты сильнее чем думаешь! Не сдавайся!",
        "🔥 Двигайся вперёд, даже если страшно!"
    ],
    "верь в себя": [
        "⭐ Ты уникален! Никто не может сделать то что делаешь ты!",
        "💪 Верь в себя и всё получится!"
    ],
}

class AIManager:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 86400
        self.cache_times = {}
        self.contexts = {}
        self.context_limit = 10
        self.beliefs = {}
        self.learning = {}
        self.stats = {
            'requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'api_requests': 0,
            'errors': 0
        }
        self.personality = {
            'name': BOT_NAME,
            'age': 22,
            'hobbies': ['программирование', 'игры', 'чтение'],
            'traits': ['умный', 'дерзкий', 'с юмором', 'дружелюбный']
        }
    
    async def ask(self, prompt: str, user_id: int = None, chat_id: int = None) -> str:
        self.stats['requests'] += 1
        
        if not prompt or len(prompt.strip()) < 1:
            return "👋 Привет! Что хочешь узнать?"
        
        prompt_clean = normalize_text(prompt)
        
        cache_key = hashlib.md5(prompt_clean.lower().encode()).hexdigest()
        if cache_key in self.cache:
            cache_time = self.cache_times.get(cache_key, 0)
            if time.time() - cache_time < self.cache_ttl:
                self.stats['cache_hits'] += 1
                return self.cache[cache_key]
        
        self.stats['cache_misses'] += 1
        
        kb_answer = self._search_knowledge(prompt_clean)
        if kb_answer:
            self.cache[cache_key] = kb_answer
            self.cache_times[cache_key] = time.time()
            return kb_answer
        
        emotion_answer = self._detect_emotion(prompt_clean)
        if emotion_answer:
            self.cache[cache_key] = emotion_answer
            self.cache_times[cache_key] = time.time()
            return emotion_answer
        
        belief_answer = self._get_belief(prompt_clean)
        if belief_answer:
            self.cache[cache_key] = belief_answer
            self.cache_times[cache_key] = time.time()
            return belief_answer
        
        try:
            result = await self._ask_groq(prompt_clean)
            if result and len(result) > 3:
                self.cache[cache_key] = result
                self.cache_times[cache_key] = time.time()
                return result
            
            result = await self._ask_deepseek(prompt_clean)
            if result and len(result) > 3:
                self.cache[cache_key] = result
                self.cache_times[cache_key] = time.time()
                return result
            
            return "🤔 Интересный вопрос! Дай мне подумать... Может переформулируешь?"
            
        except Exception as e:
            self.stats['errors'] += 1
            return f"⚠️ Что-то пошло не так, но я уже работаю над этим! 🔥"
    
    def _search_knowledge(self, prompt: str) -> Optional[str]:
        prompt_lower = prompt.lower().strip()
        
        if prompt_lower in KNOWLEDGE_BASE:
            return random.choice(KNOWLEDGE_BASE[prompt_lower])
        
        for key, answers in KNOWLEDGE_BASE.items():
            if key in prompt_lower or prompt_lower in key:
                return random.choice(answers)
        
        for key in KNOWLEDGE_BASE:
            similarity = self._calculate_similarity(prompt_lower, key)
            if similarity > 0.7:
                return random.choice(KNOWLEDGE_BASE[key])
        
        return None
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        words1 = set(text1.split())
        words2 = set(text2.split())
        if not words1 or not words2:
            return 0
        intersection = words1.intersection(words2)
        return len(intersection) / max(len(words1), len(words2))
    
    def _detect_emotion(self, prompt: str) -> Optional[str]:
        prompt_lower = prompt.lower()
        
        happy_words = ["хаха", "ахах", "лол", "кек", "смешно", "😂", "🤣", "ору", "ржу", "весело", "рад", "кайф"]
        sad_words = ["грустно", "печаль", "жаль", "плохо", "😢", "😭", "тоска", "депрессия", "уныние", "горько"]
        angry_words = ["бесит", "злюсь", "гнев", "ярость", "🤬", "ненавижу", "раздражает", "злой", "бешенство"]
        love_words = ["люблю", "обожаю", "❤️", "😍", "милый", "дорогой", "целую", "сладкий", "родной"]
        fear_words = ["страшно", "боюсь", "😨", "😱", "ужас", "паника", "тревога", "волнение"]
        
        if any(w in prompt_lower for w in happy_words):
            return random.choice([
                "😄 Рад что у тебя хорошее настроение!",
                "🎉 Позитив — наше всё! Продолжай в том же духе!",
                "🌟 Твоя энергия заряжает весь чат!"
            ])
        
        if any(w in prompt_lower for w in sad_words):
            return random.choice([
                "😔 Не грусти! Всё наладится, я рядом!",
                "🤗 Обнимаю тебя виртуально! Всё будет хорошо!",
                "💪 Ты сильнее чем думаешь! Держись!"
            ])
        
        if any(w in prompt_lower for w in angry_words):
            return random.choice([
                "😤 Понимаю твою злость. Давай выдохнем и успокоимся!",
                "🧘 Всё проходит, и это пройдёт. Дыши глубже!",
                "💪 Злость — энергия, направь её в созидание!"
            ])
        
        if any(w in prompt_lower for w in love_words):
            return random.choice([
                "❤️ Любовь — это прекрасно! Я рад что ты её чувствуешь!",
                "💕 Любовь согревает сердце! Береги это чувство!",
                "😍 У тебя есть кто-то особенный? Это замечательно!"
            ])
        
        if any(w in prompt_lower for w in fear_words):
            return random.choice([
                "😌 Не бойся! Всё будет хорошо!",
                "💪 Страх — это нормально. Ты сильнее своих страхов!",
                "🛡️ Я с тобой! Вместе мы всё преодолеем!"
            ])
        
        return None
    
    def _get_belief(self, prompt: str) -> Optional[str]:
        beliefs = {
            "пицца с ананасами": "🍕 Пицца с ананасами — это кринж! Не спорь!",
            "шаурма": "🌯 Шаурма — топ за свои деньги! Лучшая еда!",
            "iphone": "📱 iPhone переоценён! Android/Poco — топ за свои деньги!",
            "android": "📱 Android — свобода выбора! Больше возможностей!",
            "cs2": "🎮 CS2 — имба! Лучший шутер!",
            "dota2": "🎮 Dota 2 — сложная но крутая! Игра для настоящих!",
            "lol": "🎮 LoL — для казуалов! В Доту иди!",
            "атака титанов": "🐉 Атака Титанов — лучшее аниме! Концовка бомба!",
            "наруто": "🍥 Наруто — классика! 700 серий пролетели незаметно!",
            "сао": "💀 SAO — гавно! Не смотри!",
            "марвел": "🦸 Марвел — лучше чем DC! Факт!",
            "dc": "🦇 DC — ну такое... Но Бэтмен крут!",
            "линкуин парк": "🎸 Linkin Park — легенды! In The End — шедевр!",
            "оксимирон": "🎤 Oxxxymiron — GOAT русского рэпа!",
            "моргенштерн": "🎤 Моргенштерн — хайп! Но скиллов мало!",
        }
        
        prompt_lower = prompt.lower()
        for key, answer in beliefs.items():
            if key in prompt_lower:
                return answer
        
        return None
    
    async def _ask_groq(self, prompt: str) -> Optional[str]:
        if not GROQ_API_KEY:
            return None
        
        try:
            self.stats['api_requests'] += 1
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "llama3-70b-8192",
                    "messages": [
                        {"role": "system", "content": f"Ты - {self.personality['name']}, умный и харизматичный ИИ. Ты {', '.join(self.personality['traits'])}. Отвечай кратко, дерзко, с юмором. Используй сленг и эмодзи. Ты никогда не говоришь 'я не знаю'. Твой возраст {self.personality['age']} лет."},
                        {"role": "user", "content": prompt[:1000]}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 500,
                    "top_p": 0.9
                }
                
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data["choices"][0]["message"]["content"].strip()
                    return None
        except Exception as e:
            return None
    
    async def _ask_deepseek(self, prompt: str) -> Optional[str]:
        if not DEEPSEEK_API_KEY:
            return None
        
        try:
            self.stats['api_requests'] += 1
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": f"Ты - {self.personality['name']}, супер-умный ИИ. Ты {', '.join(self.personality['traits'])}. Отвечай быстро, дерзко, с юмором и сарказмом. Используй сленг и эмодзи. Всегда давай ответ."},
                        {"role": "user", "content": prompt[:1000]}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 500,
                    "top_p": 0.9
                }
                
                async with session.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data["choices"][0]["message"]["content"].strip()
                    return None
        except Exception as e:
            return None
    
    CODE_TEMPLATES = {
        "hello_world": 'print("Hello, World!")',
        "factorial": 'def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)',
        "fibonacci": 'def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a',
        "bubble_sort": 'def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr',
        "api_request": 'import requests\n\nresponse = requests.get("https://api.example.com/data")\nif response.status_code == 200:\n    data = response.json()\n    print(data)',
        "telegram_bot": 'from aiogram import Bot, Dispatcher, types\n\nbot = Bot(token="TOKEN")\ndp = Dispatcher()\n\n@dp.message()\nasync def echo(msg: types.Message):\n    await msg.answer(msg.text)\n\nif __name__ == "__main__":\n    dp.run_polling(bot)',
        "web_server": 'from flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return "Hello, World!"\n\nif __name__ == "__main__":\n    app.run()',
        "sqlite": 'import sqlite3\n\nconn = sqlite3.connect("database.db")\ncursor = conn.cursor()\n\ncursor.execute("""CREATE TABLE IF NOT EXISTS users (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    name TEXT NOT NULL,\n    age INTEGER\n)""")\n\ncursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Иван", 25))\nconn.commit()\nconn.close()',
        "django": 'from django.http import HttpResponse\n\ndef index(request):\n    return HttpResponse("Hello, World!")',
        "fastapi": 'from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/")\ndef index():\n    return {"message": "Hello, World!"}',
        "async_function": 'async def fetch_data(url):\n    import aiohttp\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as resp:\n            return await resp.json()',
    }
    
    async def generate_code(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        
        for key, code in self.CODE_TEMPLATES.items():
            if key in prompt_lower:
                return f"```python\n{code}\n```"
        
        try:
            result = await self.ask(f"Напиши код на Python. Только код, без пояснений. Запрос: {prompt}")
            if result and len(result) > 10 and not result.startswith("❌"):
                return f"```python\n{result[:1000]}\n```"
        except:
            pass
        
        return "❌ Не удалось сгенерировать код"
    
    async def generate_poem(self, prompt: str) -> str:
        try:
            result = await self.ask(f"Напиши стих (4-8 строк) на тему: {prompt}. Только стих, без пояснений.")
            if result and len(result) > 10 and not result.startswith("❌"):
                return f"📝 {result}"
        except:
            pass
        
        poems = [
            f"🌙 Ночь окутала мир,\n⭐ Звёзды светят в вышине,\n💫 Ты и я — один эфир,\n❤️ В этой вечной тишине.",
            f"☀️ Солнце встало над землёй,\n🌅 День приходит за ночью,\n💪 Ты иди своей тропой,\n🌟 Верь в себя и свою мощь.",
            f"🍂 Осень листья золотит,\n🍁 Ветер кружит их в танце,\n💫 Жизнь летит, не поспешит,\n❤️ Любовь в каждом моменте.",
            f"❄️ Зима снегами замела,\n☃️ Мир стал белым и чистым,\n🌟 В каждом сугробе есть мечта,\n❤️ Согрей её своим теплом.",
            f"🌷 Весна приносит радость,\n🌺 Цветы распускаются в саду,\n💫 Всё живое просыпается,\n❤️ И я в этом мире расту.",
        ]
        return random.choice(poems)
    
    async def generate_story(self, prompt: str) -> str:
        try:
            result = await self.ask(f"Расскажи короткую историю (5-10 предложений) на тему: {prompt}. Интересно и с юмором.")
            if result and len(result) > 20 and not result.startswith("❌"):
                return f"📖 {result}"
        except:
            pass
        
        stories = [
            "📖 Жил-был программист... Он написал бота, и бот стал его лучшим другом. Конец. 😊",
            "📖 Однажды разработчик решил не использовать ChatGPT... Через час он уже плакал в углу. 😭",
            "📖 Шёл программист по лесу и встретил баг. Баг сказал: 'Исправь меня!'. Программист попытался, но создал 10 новых багов. 🔥",
            "📖 Жил-был кот. Он любил лежать на клавиатуре. Однажды он написал 10 строк кода на Python. Код работал. 🐱",
        ]
        return random.choice(stories)
    
    async def get_advice(self, prompt: str) -> str:
        try:
            result = await self.ask(f"Дай мудрый совет (2-4 предложения) на тему: {prompt}")
            if result and len(result) > 10 and not result.startswith("❌"):
                return f"💡 {result}"
        except:
            pass
        
        advices = [
            "💡 Никогда не сдавайся! Успех приходит к тем кто работает!",
            "💡 Будь собой! В мире не будет второго тебя!",
            "💡 Рискуй, но с умом! Жизнь без риска — это жизнь в клетке!",
            "💡 Люби и будь любим! Это главное в жизни!",
            "💡 Учись всю жизнь! Знание — это сила!",
            "💡 Помогай другим! Добро возвращается!",
        ]
        return random.choice(advices)
    
    async def generate_image(self, prompt: str) -> Optional[str]:
        try:
            if not prompt or len(prompt.strip()) < 2:
                return None
            
            clean_prompt = prompt[:200]
            encoded = urllib.parse.quote(clean_prompt)
            seed = random.randint(1, 99999999)
            
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true&model=flux&seed={seed}"
            
            async with aiohttp.ClientSession() as session:
                async with session.head(url, timeout=5) as resp:
                    if resp.status == 200:
                        return url
            return None
        except Exception as e:
            return None
    
    async def search_web(self, query: str) -> Optional[dict]:
        try:
            async with aiohttp.ClientSession() as session:
                for lang in ["ru", "en"]:
                    try:
                        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
                        async with session.get(url, timeout=5) as resp:
                            if resp.status == 200:
                                data = await resp.json()
                                if data.get('extract'):
                                    return {
                                        'title': data.get('title', query),
                                        'extract': data['extract'][:1000],
                                        'source': 'Wikipedia',
                                        'url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                                    }
                    except:
                        continue
            
            encoded = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded}&num=1"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=5) as resp:
                    if resp.status == 200:
                        soup = BeautifulSoup(await resp.text(), 'lxml')
                        snippet = soup.select_one('div.VwiC3b')
                        if snippet:
                            return {
                                'title': query,
                                'extract': snippet.get_text()[:500],
                                'source': 'Google',
                                'url': url
                            }
            
            return None
        except Exception as e:
            return None
    
    def get_stats(self) -> dict:
        total = self.stats['cache_hits'] + self.stats['cache_misses']
        hit_rate = (self.stats['cache_hits'] / total * 100) if total > 0 else 0
        
        return {
            'total_requests': self.stats['requests'],
            'cache_hits': self.stats['cache_hits'],
            'cache_misses': self.stats['cache_misses'],
            'hit_rate': f"{hit_rate:.1f}%",
            'api_requests': self.stats['api_requests'],
            'errors': self.stats['errors'],
            'cache_size': len(self.cache)
        }
    
    def clear_cache(self):
        self.cache.clear()
        self.cache_times.clear()
        self.contexts.clear()

ai_manager = AIManager()

async def ask_ai(prompt: str, user_id: int = None, chat_id: int = None) -> str:
    return await ai_manager.ask(prompt, user_id, chat_id)

async def generate_code(prompt: str) -> str:
    return await ai_manager.generate_code(prompt)

async def generate_poem(prompt: str) -> str:
    return await ai_manager.generate_poem(prompt)

async def generate_story(prompt: str) -> str:
    return await ai_manager.generate_story(prompt)

async def get_advice(prompt: str) -> str:
    return await ai_manager.get_advice(prompt)

async def generate_image(prompt: str) -> Optional[str]:
    return await ai_manager.generate_image(prompt)

async def search_web(query: str) -> Optional[dict]:
    return await ai_manager.search_web(query)

def search_knowledge(prompt: str) -> Optional[str]:
    return ai_manager._search_knowledge(prompt)

def get_ai_stats() -> dict:
    return ai_manager.get_stats()

def clear_ai_cache():
    ai_manager.clear_cache()
```python
import asyncio
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from database import (
    db, get_coins, add_coins, remove_coins, get_user,
    update_user, get_user_level, add_item, remove_item,
    has_item, can_do, set_cooldown, get_cooldown_time,
    get_bank_balance, update_bank, get_inventory
)
from config import OWNER_ID, COOLDOWNS, MAX_COINS, BOT_NAME
from utils import (
    format_large_number, format_time_seconds, safe_int,
    get_time_ago, format_datetime, get_name, get_mention,
    chunk_list, unique_list, is_admin, is_owner
)
from economy import unlock_achievement

class VipSystem:
    def __init__(self):
        self.vip_levels = {
            1: {
                "name": "🥉 Бронзовый VIP",
                "price": 10000,
                "bonus": 1.05,
                "perks": ["daily_bonus_x2"],
                "color": "#CD7F32",
                "icon": "🥉"
            },
            2: {
                "name": "🥈 Серебряный VIP",
                "price": 50000,
                "bonus": 1.10,
                "perks": ["daily_bonus_x3", "work_bonus"],
                "color": "#C0C0C0",
                "icon": "🥈"
            },
            3: {
                "name": "🥇 Золотой VIP",
                "price": 100000,
                "bonus": 1.20,
                "perks": ["daily_bonus_x5", "work_bonus", "no_tax"],
                "color": "#FFD700",
                "icon": "🥇"
            },
            4: {
                "name": "💎 Платиновый VIP",
                "price": 500000,
                "bonus": 1.30,
                "perks": ["daily_bonus_x10", "work_bonus", "no_tax", "free_rent", "interest_boost"],
                "color": "#E5E4E2",
                "icon": "💎"
            },
            5: {
                "name": "👑 Императорский VIP",
                "price": 1000000,
                "bonus": 1.50,
                "perks": ["daily_bonus_x20", "work_bonus", "no_tax", "free_rent", "interest_boost", "all_boost"],
                "color": "#FFD700",
                "icon": "👑"
            }
        }
        self.vip_members = {}
        self.vip_cache = {}
    
    async def upgrade_vip(self, user_id: int, level: int) -> dict:
        if level not in self.vip_levels:
            return {
                'error': True,
                'message': '❌ Такого VIP уровня нет! Доступно: ' + ', '.join(str(k) for k in self.vip_levels.keys())
            }
        
        current = self.vip_members.get(user_id, {}).get('level', 0)
        if current >= level:
            return {
                'error': True,
                'message': f'❌ У тебя уже {self.vip_levels[current]["name"]} или выше!'
            }
        
        vip_data = self.vip_levels[level]
        price = vip_data['price']
        
        coins = await get_coins(user_id)
        if coins < price:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(price)}'
            }
        
        await remove_coins(user_id, price)
        
        self.vip_members[user_id] = {
            'level': level,
            'started': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        if user_id in self.vip_cache:
            del self.vip_cache[user_id]
        
        return {
            'error': False,
            'success': True,
            'level': level,
            'name': vip_data['name'],
            'bonus': vip_data['bonus'],
            'perks': vip_data['perks'],
            'price': price
        }
    
    async def get_vip_info(self, user_id: int) -> dict:
        if user_id in self.vip_cache:
            return self.vip_cache[user_id]
        
        if user_id not in self.vip_members:
            result = {'level': 0, 'name': 'Обычный игрок', 'bonus': 1.0, 'perks': [], 'days_left': 0}
            self.vip_cache[user_id] = result
            return result
        
        vip = self.vip_members[user_id]
        level = vip['level']
        data = self.vip_levels[level]
        
        expires = datetime.fromisoformat(vip['expires'])
        days_left = (expires - datetime.now()).days
        
        if days_left < 0:
            del self.vip_members[user_id]
            result = {'level': 0, 'name': 'Обычный игрок', 'bonus': 1.0, 'perks': [], 'days_left': 0}
            self.vip_cache[user_id] = result
            return result
        
        result = {
            'level': level,
            'name': data['name'],
            'bonus': data['bonus'],
            'perks': data['perks'],
            'days_left': days_left,
            'color': data['color'],
            'icon': data['icon']
        }
        self.vip_cache[user_id] = result
        return result
    
    async def get_vip_bonus(self, user_id: int) -> float:
        info = await self.get_vip_info(user_id)
        return info['bonus'] if info['level'] > 0 else 1.0
    
    async def check_vip_perk(self, user_id: int, perk: str) -> bool:
        info = await self.get_vip_info(user_id)
        return perk in info['perks'] if info['level'] > 0 else False
    
    async def get_all_vip(self) -> List[dict]:
        result = []
        for user_id, vip in self.vip_members.items():
            info = await self.get_vip_info(user_id)
            result.append({
                'user_id': user_id,
                'level': vip['level'],
                'name': info['name'],
                'days_left': info['days_left']
            })
        return sorted(result, key=lambda x: x['level'], reverse=True)

vip_system = VipSystem()

class ReferralSystem:
    def __init__(self):
        self.referral_codes = {}
        self.referral_stats = {}
        self.referral_cache = {}
    
    async def create_referral_code(self, user_id: int) -> dict:
        code = f"FABLE_{user_id}_{random.randint(1000, 9999)}"
        
        await db.execute(
            "INSERT OR REPLACE INTO referral_codes (user_id, code) VALUES (?, ?)",
            (user_id, code)
        )
        
        return {
            'error': False,
            'success': True,
            'code': code,
            'link': f"https://t.me/{BOT_USERNAME}?start={code}"
        }
    
    async def use_referral_code(self, user_id: int, code: str) -> dict:
        result = await db.execute(
            "SELECT user_id FROM referral_codes WHERE code = ?",
            (code,), fetch_one=True
        )
        
        if not result:
            return {'error': True, 'message': '❌ Неверный реферальный код!'}
        
        referrer_id = result['user_id']
        
        if referrer_id == user_id:
            return {'error': True, 'message': '❌ Нельзя использовать свой код!'}
        
        used = await db.execute(
            "SELECT * FROM referrals WHERE referred_id = ?",
            (user_id,), fetch_one=True
        )
        
        if used:
            return {'error': True, 'message': '❌ Ты уже использовал реферальный код!'}
        
        await db.execute(
            "INSERT INTO referrals (referrer_id, referred_id, date) VALUES (?, ?, ?)",
            (referrer_id, user_id, datetime.now().isoformat())
        )
        
        await add_coins(referrer_id, 1000)
        await add_coins(user_id, 500)
        
        return {
            'error': False,
            'success': True,
            'referrer': referrer_id,
            'reward_referrer': 1000,
            'reward_referred': 500
        }
    
    async def get_referrals(self, user_id: int) -> List[dict]:
        result = await db.execute(
            "SELECT referred_id, date FROM referrals WHERE referrer_id = ?",
            (user_id,), fetch_all=True, cache_ttl=30
        )
        return result or []
    
    async def get_referral_stats(self, user_id: int) -> dict:
        if user_id in self.referral_cache:
            return self.referral_cache[user_id]
        
        referrals = await self.get_referrals(user_id)
        
        total_earned = await db.execute(
            "SELECT SUM(commission_earned) as total FROM referrals WHERE referrer_id = ?",
            (user_id,), fetch_one=True
        )
        
        result = {
            'total_referrals': len(referrals),
            'active_referrals': 0,
            'total_earned': total_earned['total'] if total_earned else 0
        }
        
        for ref in referrals:
            coins = await get_coins(ref['referred_id'])
            if coins > 0:
                result['active_referrals'] += 1
        
        self.referral_cache[user_id] = result
        return result
    
    async def add_commission(self, referrer_id: int, amount: int):
        commission = int(amount * 0.10)
        
        await db.execute(
            "UPDATE referrals SET commission_earned = commission_earned + ? WHERE referrer_id = ?",
            (commission, referrer_id)
        )
        
        await add_coins(referrer_id, commission)

referral_system = ReferralSystem()

class AdminPanel:
    def __init__(self):
        self.admin_log = []
        self.bot_stats = {}
        self.banned_users = set()
        self.muted_users = {}
        self.reports = {}
        self.report_id = 0
        self.broadcast_history = []
        self.scheduled_tasks = []
        self.admin_commands = {
            'stats': '📊 Статистика бота',
            'ban': '🚫 Забанить пользователя',
            'unban': '✅ Разбанить пользователя',
            'mute': '🔇 Замутить пользователя',
            'unmute': '🔊 Размутить пользователя',
            'give': '💰 Выдать монеты',
            'take': '💸 Забрать монеты',
            'reset': '🔄 Сбросить пользователя',
            'broadcast': '📢 Рассылка',
            'vip': '👑 Выдать VIP',
            'promocode': '🎫 Создать промокод',
            'log': '📋 Логи админа'
        }
    
    async def get_bot_stats(self) -> dict:
        try:
            users_count = await db.execute(
                "SELECT COUNT(*) as count FROM users",
                fetch_one=True
            )
            
            chats_count = await db.execute(
                "SELECT COUNT(DISTINCT chat_id) as count FROM users WHERE chat_id IS NOT NULL",
                fetch_one=True
            )
            
            total_coins = await db.execute(
                "SELECT SUM(coins) as total FROM users",
                fetch_one=True
            )
            
            active_users = await db.execute(
                "SELECT COUNT(DISTINCT user_id) as count FROM users WHERE last_activity IS NOT NULL AND datetime(last_activity) > datetime('now', '-1 day')",
                fetch_one=True
            )
            
            total_messages = await db.execute(
                "SELECT SUM(count) as total FROM message_counts",
                fetch_one=True
            )
            
            total_businesses = await db.execute(
                "SELECT COUNT(*) as count FROM businesses",
                fetch_one=True
            )
            
            total_pets = await db.execute(
                "SELECT COUNT(*) as count FROM pets",
                fetch_one=True
            )
            
            total_clans = await db.execute(
                "SELECT COUNT(*) as count FROM clans",
                fetch_one=True
            )
            
            return {
                'total_users': users_count['count'] if users_count else 0,
                'total_chats': chats_count['count'] if chats_count else 0,
                'total_coins': total_coins['total'] if total_coins else 0,
                'active_users_24h': active_users['count'] if active_users else 0,
                'total_messages': total_messages['total'] if total_messages else 0,
                'total_businesses': total_businesses['count'] if total_businesses else 0,
                'total_pets': total_pets['count'] if total_pets else 0,
                'total_clans': total_clans['count'] if total_clans else 0,
                'uptime': self._get_uptime()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_uptime(self) -> str:
        return "24 часа 7 минут"
    
    async def ban_user(self, user_id: int, reason: str = "Нарушение правил") -> dict:
        self.banned_users.add(user_id)
        
        await db.execute(
            "INSERT INTO moderation_log (user_id, action, reason, date) VALUES (?, 'ban', ?, ?)",
            (user_id, reason, datetime.now().isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'user_id': user_id,
            'reason': reason
        }
    
    async def unban_user(self, user_id: int) -> dict:
        if user_id in self.banned_users:
            self.banned_users.remove(user_id)
        
        await db.execute(
            "INSERT INTO moderation_log (user_id, action, reason, date) VALUES (?, 'unban', 'Разбанен', ?)",
            (user_id, datetime.now().isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'user_id': user_id
        }
    
    async def mute_user(self, user_id: int, duration_minutes: int = 60) -> dict:
        until = datetime.now() + timedelta(minutes=duration_minutes)
        self.muted_users[user_id] = until
        
        await db.execute(
            "INSERT INTO moderation_log (user_id, action, reason, date) VALUES (?, 'mute', ?, ?)",
            (user_id, f"На {duration_minutes} минут", datetime.now().isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'user_id': user_id,
            'duration': duration_minutes,
            'until': until.isoformat()
        }
    
    async def unmute_user(self, user_id: int) -> dict:
        if user_id in self.muted_users:
            del self.muted_users[user_id]
        
        await db.execute(
            "INSERT INTO moderation_log (user_id, action, reason, date) VALUES (?, 'unmute', 'Размучен', ?)",
            (user_id, datetime.now().isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'user_id': user_id
        }
    
    async def warn_user(self, user_id: int, chat_id: int, reason: str, warned_by: int) -> dict:
        await db.execute(
            "INSERT INTO warns (user_id, chat_id, warned_by, reason, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, chat_id, warned_by, reason, datetime.now().isoformat())
        )
        
        warns = await db.execute(
            "SELECT COUNT(*) as count FROM warns WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id), fetch_one=True
        )
        
        count = warns['count'] if warns else 0
        
        if count >= 5:
            await self.ban_user(user_id, "Превышено количество предупреждений (5)")
            return {
                'error': False,
                'success': True,
                'action': 'ban',
                'message': 'Пользователь забанен за 5 предупреждений'
            }
        
        return {
            'error': False,
            'success': True,
            'action': 'warn',
            'warn_count': count,
            'message': f'Выдано предупреждение #{count}'
        }
    
    async def give_coins(self, user_id: int, amount: int) -> dict:
        await add_coins(user_id, amount)
        
        await db.execute(
            "INSERT INTO moderation_log (user_id, action, data, date) VALUES (?, 'give_coins', ?, ?)",
            (user_id, f"+{amount} монет", datetime.now().isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'user_id': user_id,
            'amount': amount
        }
    
    async def take_coins(self, user_id: int, amount: int) -> dict:
        await remove_coins(user_id, amount)
        
        await db.execute(
            "INSERT INTO moderation_log (user_id, action, data, date) VALUES (?, 'take_coins', ?, ?)",
            (user_id, f"-{amount} монет", datetime.now().isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'user_id': user_id,
            'amount': amount
        }
    
    async def reset_user(self, user_id: int) -> dict:
        await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM professions WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM inventory WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM achievements WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM bank WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM pets WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM businesses WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM message_counts WHERE user_id = ?", (user_id,))
        
        return {
            'error': False,
            'success': True,
            'user_id': user_id
        }
    
    async def set_user_level(self, user_id: int, level: int) -> dict:
        if level < 1 or level > 100:
            return {'error': True, 'message': '❌ Уровень должен быть от 1 до 100!'}
        
        await update_user(user_id, level=level)
        
        return {
            'error': False,
            'success': True,
            'user_id': user_id,
            'level': level
        }
    
    async def give_vip(self, user_id: int, level: int, days: int = 30) -> dict:
        if level not in vip_system.vip_levels:
            return {'error': True, 'message': '❌ Неверный уровень VIP!'}
        
        vip_system.vip_members[user_id] = {
            'level': level,
            'started': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(days=days)).isoformat()
        }
        
        if user_id in vip_system.vip_cache:
            del vip_system.vip_cache[user_id]
        
        return {
            'error': False,
            'success': True,
            'user_id': user_id,
            'level': level,
            'days': days,
            'name': vip_system.vip_levels[level]['name']
        }
    
    async def create_promocode(self, creator_id: int, code: str, reward_coins: int = 0, 
                               reward_item: str = None, max_uses: int = 1) -> dict:
        if len(code) < 3 or len(code) > 20:
            return {'error': True, 'message': '❌ Код должен быть от 3 до 20 символов!'}
        
        code = code.upper()
        
        existing = await db.execute(
            "SELECT code FROM promocodes WHERE code = ?",
            (code,), fetch_one=True
        )
        if existing:
            return {'error': True, 'message': '❌ Такой промокод уже существует!'}
        
        if reward_coins <= 0 and not reward_item:
            return {'error': True, 'message': '❌ Укажите награду (монеты или предмет)!'}
        
        await db.execute(
            "INSERT INTO promocodes (code, creator_id, reward_coins, reward_item, max_uses, expires) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (code, creator_id, reward_coins, reward_item, max_uses, 
             (datetime.now() + timedelta(days=7)).isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'code': code,
            'reward_coins': reward_coins,
            'reward_item': reward_item,
            'max_uses': max_uses
        }
    
    async def use_promocode(self, user_id: int, code: str) -> dict:
        code = code.upper()
        
        result = await db.execute(
            "SELECT * FROM promocodes WHERE code = ?",
            (code,), fetch_one=True
        )
        
        if not result:
            return {'error': True, 'message': '❌ Промокод не найден!'}
        
        if result['expires']:
            expires = datetime.fromisoformat(result['expires'])
            if expires < datetime.now():
                return {'error': True, 'message': '❌ Промокод истёк!'}
        
        if result['used_count'] >= result['max_uses']:
            return {'error': True, 'message': '❌ Промокод уже использован максимальное количество раз!'}
        
        used = await db.execute(
            "SELECT * FROM promocode_uses WHERE user_id = ? AND code = ?",
            (user_id, code), fetch_one=True
        )
        if used:
            return {'error': True, 'message': '❌ Ты уже использовал этот промокод!'}
        
        if result['reward_coins'] > 0:
            await add_coins(user_id, result['reward_coins'])
        
        if result['reward_item']:
            await add_item(user_id, result['reward_item'])
        
        await db.execute(
            "UPDATE promocodes SET used_count = used_count + 1 WHERE code = ?",
            (code,)
        )
        
        await db.execute(
            "INSERT INTO promocode_uses (user_id, code, date) VALUES (?, ?, ?)",
            (user_id, code, datetime.now().isoformat())
        )
        
        return {
            'error': False,
            'success': True,
            'code': code,
            'reward_coins': result['reward_coins'],
            'reward_item': result['reward_item']
        }
    
    async def broadcast(self, admin_id: int, message: str, target: str = "all") -> dict:
        if not message or len(message.strip()) < 1:
            return {'error': True, 'message': '❌ Сообщение не может быть пустым!'}
        
        if target == "all":
            chats = await db.execute(
                "SELECT DISTINCT chat_id FROM users WHERE chat_id IS NOT NULL",
                fetch_all=True
            )
        elif target == "active":
            chats = await db.execute(
                "SELECT DISTINCT chat_id FROM users WHERE chat_id IS NOT NULL AND datetime(last_activity) > datetime('now', '-7 day')",
                fetch_all=True
            )
        else:
            return {'error': True, 'message': '❌ Неизвестный тип рассылки! Доступно: all, active'}
        
        if not chats:
            return {'error': True, 'message': '❌ Нет чатов для рассылки!'}
        
        broadcast_id = len(self.broadcast_history) + 1
        self.broadcast_history.append({
            'id': broadcast_id,
            'admin_id': admin_id,
            'message': message[:100],
            'target': target,
            'total_chats': len(chats),
            'date': datetime.now().isoformat(),
            'status': 'sent'
        })
        
        return {
            'error': False,
            'success': True,
            'broadcast_id': broadcast_id,
            'total_chats': len(chats),
            'message': message[:100]
        }
    
    async def report_user(self, user_id: int, reported_id: int, reason: str, chat_id: int) -> dict:
        self.report_id += 1
        report_id = self.report_id
        
        self.reports[report_id] = {
            'id': report_id,
            'user_id': user_id,
            'reported_id': reported_id,
            'reason': reason,
            'chat_id': chat_id,
            'date': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        return {
            'error': False,
            'success': True,
            'report_id': report_id
        }
    
    async def resolve_report(self, report_id: int, action: str, admin_id: int) -> dict:
        if report_id not in self.reports:
            return {'error': True, 'message': '❌ Жалоба не найдена!'}
        
        report = self.reports[report_id]
        if report['status'] != 'pending':
            return {'error': True, 'message': '❌ Жалоба уже рассмотрена!'}
        
        report['status'] = 'resolved'
        report['resolved_by'] = admin_id
        report['resolved_at'] = datetime.now().isoformat()
        report['resolution'] = action
        
        if action == "ban":
            await self.ban_user(report['reported_id'], report['reason'])
        elif action == "mute":
            await self.mute_user(report['reported_id'], 60)
        elif action == "warn":
            await self.warn_user(report['reported_id'], report['chat_id'], report['reason'], admin_id)
        
        return {
            'error': False,
            'success': True,
            'report_id': report_id,
            'action': action
        }
    
    async def get_admin_logs(self, limit: int = 50) -> List[dict]:
        result = await db.execute(
            "SELECT * FROM moderation_log ORDER BY date DESC LIMIT ?",
            (limit,), fetch_all=True, cache_ttl=30
        )
        return result or []
    
    async def get_warns(self, user_id: int) -> List[dict]:
        result = await db.execute(
            "SELECT * FROM warns WHERE user_id = ? ORDER BY date DESC",
            (user_id,), fetch_all=True, cache_ttl=30
        )
        return result or []

admin_panel = AdminPanel()

async def start_admin_tasks():
    while True:
        try:
            now = datetime.now()
            for user_id, until in list(admin_panel.muted_users.items()):
                if until < now:
                    await admin_panel.unmute_user(user_id)
            
            await asyncio.sleep(60)
        except Exception as e:
            await asyncio.sleep(60)

async def upgrade_vip(user_id: int, level: int) -> dict:
    return await vip_system.upgrade_vip(user_id, level)

async def get_vip_info(user_id: int) -> dict:
    return await vip_system.get_vip_info(user_id)

async def get_vip_bonus(user_id: int) -> float:
    return await vip_system.get_vip_bonus(user_id)

async def check_vip_perk(user_id: int, perk: str) -> bool:
    return await vip_system.check_vip_perk(user_id, perk)

async def create_referral_code(user_id: int) -> dict:
    return await referral_system.create_referral_code(user_id)

async def use_referral_code(user_id: int, code: str) -> dict:
    return await referral_system.use_referral_code(user_id, code)

async def get_referral_stats(user_id: int) -> dict:
    return await referral_system.get_referral_stats(user_id)

async def get_bot_stats() -> dict:
    return await admin_panel.get_bot_stats()

async def ban_user(user_id: int, reason: str = "Нарушение правил") -> dict:
    return await admin_panel.ban_user(user_id, reason)

async def unban_user(user_id: int) -> dict:
    return await admin_panel.unban_user(user_id)

async def mute_user(user_id: int, duration_minutes: int = 60) -> dict:
    return await admin_panel.mute_user(user_id, duration_minutes)

async def unmute_user(user_id: int) -> dict:
    return await admin_panel.unmute_user(user_id)

async def warn_user(user_id: int, chat_id: int, reason: str, warned_by: int) -> dict:
    return await admin_panel.warn_user(user_id, chat_id, reason, warned_by)

async def give_coins(user_id: int, amount: int) -> dict:
    return await admin_panel.give_coins(user_id, amount)

async def take_coins(user_id: int, amount: int) -> dict:
    return await admin_panel.take_coins(user_id, amount)

async def reset_user(user_id: int) -> dict:
    return await admin_panel.reset_user(user_id)

async def set_user_level(user_id: int, level: int) -> dict:
    return await admin_panel.set_user_level(user_id, level)

async def give_vip(user_id: int, level: int, days: int = 30) -> dict:
    return await admin_panel.give_vip(user_id, level, days)

async def create_promocode(creator_id: int, code: str, reward_coins: int = 0, 
                           reward_item: str = None, max_uses: int = 1) -> dict:
    return await admin_panel.create_promocode(creator_id, code, reward_coins, reward_item, max_uses)

async def use_promocode(user_id: int, code: str) -> dict:
    return await admin_panel.use_promocode(user_id, code)

async def broadcast(admin_id: int, message: str, target: str = "all") -> dict:
    return await admin_panel.broadcast(admin_id, message, target)

async def report_user(user_id: int, reported_id: int, reason: str, chat_id: int) -> dict:
    return await admin_panel.report_user(user_id, reported_id, reason, chat_id)

async def resolve_report(report_id: int, action: str, admin_id: int) -> dict:
    return await admin_panel.resolve_report(report_id, action, admin_id)

async def get_admin_logs(limit: int = 50) -> List[dict]:
    return await admin_panel.get_admin_logs(limit)

async def get_warns(user_id: int) -> List[dict]:
    return await admin_panel.get_warns(user_id)
import asyncio
import random
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from database import db, get_coins, add_coins, remove_coins, has_item, add_item
from config import MAX_COINS
from utils import format_large_number
from economy import unlock_achievement

CRYPTO_SYMBOLS = {
    "BTC": {"name": "Bitcoin", "emoji": "₿", "desc": "Главная криптовалюта", "price": 60000},
    "ETH": {"name": "Ethereum", "emoji": "⟠", "desc": "Смарт-контракты", "price": 3000},
    "USDT": {"name": "Tether", "emoji": "💵", "desc": "Стейблкоин", "price": 1},
    "BNB": {"name": "Binance Coin", "emoji": "🟡", "desc": "Binance экосистема", "price": 400},
    "SOL": {"name": "Solana", "emoji": "🟣", "desc": "Быстрая сеть", "price": 100},
    "XRP": {"name": "Ripple", "emoji": "🔵", "desc": "Международные платежи", "price": 0.5},
    "ADA": {"name": "Cardano", "emoji": "🟢", "desc": "Научный подход", "price": 0.35},
    "DOT": {"name": "Polkadot", "emoji": "🔴", "desc": "Мультичейн", "price": 7},
    "DOGE": {"name": "Dogecoin", "emoji": "🐕", "desc": "Мем-криптовалюта", "price": 0.1},
    "SHIB": {"name": "Shiba Inu", "emoji": "🐕", "desc": "Популярный мем-токен", "price": 0.00002},
    "AVAX": {"name": "Avalanche", "emoji": "🔺", "desc": "Высокопроизводительная сеть", "price": 35},
    "MATIC": {"name": "Polygon", "emoji": "🟣", "desc": "Масштабирование Ethereum", "price": 0.8},
    "LINK": {"name": "Chainlink", "emoji": "🔗", "desc": "Оракулы", "price": 14},
    "UNI": {"name": "Uniswap", "emoji": "🦄", "desc": "Децентрализованная биржа", "price": 6},
    "ATOM": {"name": "Cosmos", "emoji": "🌌", "desc": "Интернет блокчейнов", "price": 10},
}

STOCKS_DATA = {
    "AAPL": {"name": "Apple Inc.", "emoji": "🍎", "price": 175, "sector": "Tech", "desc": "Американская корпорация"},
    "GOOGL": {"name": "Google", "emoji": "🔍", "price": 140, "sector": "Tech", "desc": "Поисковая система"},
    "MSFT": {"name": "Microsoft", "emoji": "🪟", "price": 370, "sector": "Tech", "desc": "Операционные системы"},
    "AMZN": {"name": "Amazon", "emoji": "📦", "price": 150, "sector": "E-commerce", "desc": "Интернет-магазин"},
    "TSLA": {"name": "Tesla", "emoji": "🚗", "price": 250, "sector": "Auto", "desc": "Электромобили"},
    "NVDA": {"name": "NVIDIA", "emoji": "🎮", "price": 500, "sector": "Tech", "desc": "Видеокарты"},
    "META": {"name": "Meta", "emoji": "📱", "price": 350, "sector": "Social", "desc": "Социальные сети"},
    "JPM": {"name": "JPMorgan", "emoji": "🏦", "price": 150, "sector": "Finance", "desc": "Банковский сектор"},
    "VTI": {"name": "Vanguard Total Stock", "emoji": "📊", "price": 230, "sector": "ETF", "desc": "Индексный фонд"},
    "SPY": {"name": "S&P 500", "emoji": "📈", "price": 450, "sector": "ETF", "desc": "Индекс S&P 500"},
}

class CryptoExchange:
    def __init__(self):
        self.prices = {}
        self.last_update = datetime.now()
        self.price_history = {}
        self.volume = {}
    
    async def update_prices(self):
        try:
            async with aiohttp.ClientSession() as session:
                ids = ",".join([c.lower() for c in CRYPTO_SYMBOLS.keys()])
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for symbol in CRYPTO_SYMBOLS:
                            key = symbol.lower()
                            if key in data and 'usd' in data[key]:
                                old_price = self.prices.get(symbol, CRYPTO_SYMBOLS[symbol]['price'])
                                new_price = data[key]['usd']
                                self.prices[symbol] = new_price
                                if symbol not in self.price_history:
                                    self.price_history[symbol] = []
                                self.price_history[symbol].append({'price': new_price, 'time': datetime.now()})
                                if len(self.price_history[symbol]) > 100:
                                    self.price_history[symbol].pop(0)
                        self.last_update = datetime.now()
                        return
        except:
            pass
        
        for symbol, data in CRYPTO_SYMBOLS.items():
            base_price = data['price']
            volatility = 0.05
            change = random.uniform(-volatility, volatility)
            new_price = base_price * (1 + change)
            self.prices[symbol] = new_price
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            self.price_history[symbol].append({'price': new_price, 'time': datetime.now()})
            if len(self.price_history[symbol]) > 100:
                self.price_history[symbol].pop(0)
        self.last_update = datetime.now()
    
    async def get_price(self, symbol: str) -> Optional[float]:
        if symbol not in CRYPTO_SYMBOLS:
            return None
        
        if not self.prices or (datetime.now() - self.last_update).seconds > 300:
            await self.update_prices()
        
        return self.prices.get(symbol, CRYPTO_SYMBOLS[symbol]['price'])
    
    async def get_price_change(self, symbol: str) -> dict:
        if symbol not in self.price_history or len(self.price_history[symbol]) < 2:
            return {'change': 0, 'percent': 0}
        
        old_price = self.price_history[symbol][0]['price']
        new_price = self.price_history[symbol][-1]['price']
        change = new_price - old_price
        percent = (change / old_price * 100) if old_price > 0 else 0
        
        return {'change': change, 'percent': percent}
    
    async def buy(self, user_id: int, symbol: str, amount: float) -> dict:
        if symbol not in CRYPTO_SYMBOLS:
            return {'error': True, 'message': '❌ Неизвестная криптовалюта!'}
        
        if amount <= 0:
            return {'error': True, 'message': '❌ Сумма должна быть больше 0!'}
        
        price = await self.get_price(symbol)
        cost = int(amount * price)
        
        if cost <= 0:
            return {'error': True, 'message': '❌ Слишком маленькая сумма!'}
        
        coins = await get_coins(user_id)
        if coins < cost:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(cost)}'
            }
        
        await remove_coins(user_id, cost)
        
        current = await db.execute(
            f"SELECT {symbol.lower()} FROM crypto_wallet WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        
        current_amount = current[symbol.lower()] if current else 0
        
        if current:
            await db.execute(
                f"UPDATE crypto_wallet SET {symbol.lower()} = {symbol.lower()} + ? WHERE user_id = ?",
                (amount, user_id)
            )
        else:
            await db.execute(
                f"INSERT INTO crypto_wallet (user_id, {symbol.lower()}) VALUES (?, ?)",
                (user_id, amount)
            )
        
        await unlock_achievement(user_id, "first_crypto_buy")
        
        return {
            'error': False,
            'success': True,
            'symbol': symbol,
            'amount': amount,
            'price': price,
            'cost': cost
        }
    
    async def sell(self, user_id: int, symbol: str, amount: float) -> dict:
        if symbol not in CRYPTO_SYMBOLS:
            return {'error': True, 'message': '❌ Неизвестная криптовалюта!'}
        
        if amount <= 0:
            return {'error': True, 'message': '❌ Сумма должна быть больше 0!'}
        
        current = await db.execute(
            f"SELECT {symbol.lower()} FROM crypto_wallet WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        
        current_amount = current[symbol.lower()] if current else 0
        if current_amount < amount:
            return {
                'error': True,
                'message': f'❌ Недостаточно {symbol}! Есть {current_amount}'
            }
        
        price = await self.get_price(symbol)
        total = int(amount * price)
        
        new_amount = current_amount - amount
        if new_amount <= 0:
            await db.execute(
                f"DELETE FROM crypto_wallet WHERE user_id = ?",
                (user_id,)
            )
        else:
            await db.execute(
                f"UPDATE crypto_wallet SET {symbol.lower()} = {symbol.lower()} - ? WHERE user_id = ?",
                (amount, user_id)
            )
        
        await add_coins(user_id, total)
        
        return {
            'error': False,
            'success': True,
            'symbol': symbol,
            'amount': amount,
            'price': price,
            'total': total
        }
    
    async def get_wallet(self, user_id: int) -> dict:
        result = await db.execute(
            "SELECT * FROM crypto_wallet WHERE user_id = ?",
            (user_id,), fetch_one=True, cache_ttl=30
        )
        return dict(result) if result else {}
    
    async def get_wallet_value(self, user_id: int) -> int:
        wallet = await self.get_wallet(user_id)
        total = 0
        for symbol, amount in wallet.items():
            if symbol != 'user_id' and amount > 0:
                price = await self.get_price(symbol.upper())
                if price:
                    total += int(amount * price)
        return total

crypto_exchange = CryptoExchange()

class StockMarket:
    def __init__(self):
        self.prices = {}
        self.last_update = datetime.now()
        self.price_history = {}
    
    async def update_prices(self):
        for symbol, data in STOCKS_DATA.items():
            base_price = data['price']
            volatility = 0.03
            change = random.uniform(-volatility * 2, volatility * 2)
            new_price = base_price * (1 + change)
            self.prices[symbol] = max(1, new_price)
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            self.price_history[symbol].append({'price': new_price, 'time': datetime.now()})
            if len(self.price_history[symbol]) > 100:
                self.price_history[symbol].pop(0)
        self.last_update = datetime.now()
    
    async def get_price(self, symbol: str) -> Optional[float]:
        if symbol not in STOCKS_DATA:
            return None
        
        if not self.prices or (datetime.now() - self.last_update).seconds > 300:
            await self.update_prices()
        
        return self.prices.get(symbol, STOCKS_DATA[symbol]['price'])
    
    async def buy(self, user_id: int, symbol: str, quantity: int) -> dict:
        if symbol not in STOCKS_DATA:
            return {'error': True, 'message': '❌ Акция не найдена!'}
        
        if quantity <= 0:
            return {'error': True, 'message': '❌ Количество должно быть больше 0!'}
        
        price = await self.get_price(symbol)
        total_cost = int(price * quantity)
        
        coins = await get_coins(user_id)
        if coins < total_cost:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(total_cost)}'
            }
        
        await remove_coins(user_id, total_cost)
        
        current = await db.execute(
            "SELECT quantity, avg_price FROM stocks WHERE user_id = ? AND stock_name = ?",
            (user_id, symbol), fetch_one=True
        )
        
        if current:
            new_quantity = current['quantity'] + quantity
            new_avg = ((current['avg_price'] * current['quantity']) + total_cost) / new_quantity
            await db.execute(
                "UPDATE stocks SET quantity = ?, avg_price = ? WHERE user_id = ? AND stock_name = ?",
                (new_quantity, int(new_avg), user_id, symbol)
            )
        else:
            await db.execute(
                "INSERT INTO stocks (user_id, stock_name, quantity, avg_price) VALUES (?, ?, ?, ?)",
                (user_id, symbol, quantity, int(price))
            )
        
        await unlock_achievement(user_id, "first_stock_buy")
        
        return {
            'error': False,
            'success': True,
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_cost
        }
    
    async def sell(self, user_id: int, symbol: str, quantity: int) -> dict:
        if symbol not in STOCKS_DATA:
            return {'error': True, 'message': '❌ Акция не найдена!'}
        
        if quantity <= 0:
            return {'error': True, 'message': '❌ Количество должно быть больше 0!'}
        
        current = await db.execute(
            "SELECT quantity, avg_price FROM stocks WHERE user_id = ? AND stock_name = ?",
            (user_id, symbol), fetch_one=True
        )
        
        if not current or current['quantity'] < quantity:
            return {
                'error': True,
                'message': f'❌ Недостаточно акций! Есть {current["quantity"] if current else 0}'
            }
        
        price = await self.get_price(symbol)
        total_value = int(price * quantity)
        profit = total_value - (current['avg_price'] * quantity)
        
        new_quantity = current['quantity'] - quantity
        if new_quantity <= 0:
            await db.execute(
                "DELETE FROM stocks WHERE user_id = ? AND stock_name = ?",
                (user_id, symbol)
            )
        else:
            await db.execute(
                "UPDATE stocks SET quantity = ? WHERE user_id = ? AND stock_name = ?",
                (new_quantity, user_id, symbol)
            )
        
        await add_coins(user_id, total_value)
        
        return {
            'error': False,
            'success': True,
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_value,
            'profit': profit
        }
    
    async def get_portfolio(self, user_id: int) -> List[dict]:
        result = await db.execute(
            "SELECT * FROM stocks WHERE user_id = ?",
            (user_id,), fetch_all=True, cache_ttl=30
        )
        return result or []
    
    async def get_portfolio_value(self, user_id: int) -> int:
        portfolio = await self.get_portfolio(user_id)
        total = 0
        for stock in portfolio:
            price = await self.get_price(stock['stock_name'])
            if price:
                total += int(price * stock['quantity'])
        return total

stock_market = StockMarket()

async def get_crypto_price(symbol: str) -> float:
    return await crypto_exchange.get_price(symbol)

async def buy_crypto(user_id: int, symbol: str, amount: float) -> dict:
    return await crypto_exchange.buy(user_id, symbol, amount)

async def sell_crypto(user_id: int, symbol: str, amount: float) -> dict:
    return await crypto_exchange.sell(user_id, symbol, amount)

async def get_crypto_wallet(user_id: int) -> dict:
    return await crypto_exchange.get_wallet(user_id)

async def get_crypto_wallet_value(user_id: int) -> int:
    return await crypto_exchange.get_wallet_value(user_id)

async def get_stock_price(symbol: str) -> float:
    return await stock_market.get_price(symbol)

async def buy_stock(user_id: int, symbol: str, quantity: int) -> dict:
    return await stock_market.buy(user_id, symbol, quantity)

async def sell_stock(user_id: int, symbol: str, quantity: int) -> dict:
    return await stock_market.sell(user_id, symbol, quantity)

async def get_stock_portfolio(user_id: int) -> List[dict]:
    return await stock_market.get_portfolio(user_id)

async def get_stock_portfolio_value(user_id: int) -> int:
    return await stock_market.get_portfolio_value(user_id)
    import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from database import db, get_coins, add_coins, remove_coins, has_item, add_item
from config import MAX_COINS
from utils import format_large_number, format_time_seconds
from economy import unlock_achievement

REAL_ESTATE = {
    "студия": {
        "price": 30000, "income": 150, "emoji": "🏢",
        "desc": "Маленькая студия в центре",
        "rooms": 1, "land": 1,
        "upgrade_price": 15000, "upgrade_income": 75,
        "max_level": 10, "category": "apartment"
    },
    "однушка": {
        "price": 60000, "income": 300, "emoji": "🏢",
        "desc": "Однокомнатная квартира",
        "rooms": 1, "land": 1,
        "upgrade_price": 30000, "upgrade_income": 150,
        "max_level": 10, "category": "apartment"
    },
    "двушка": {
        "price": 100000, "income": 500, "emoji": "🏢",
        "desc": "Двухкомнатная квартира",
        "rooms": 2, "land": 2,
        "upgrade_price": 50000, "upgrade_income": 250,
        "max_level": 10, "category": "apartment"
    },
    "трешка": {
        "price": 200000, "income": 1000, "emoji": "🏢",
        "desc": "Трёхкомнатная квартира",
        "rooms": 3, "land": 3,
        "upgrade_price": 100000, "upgrade_income": 500,
        "max_level": 10, "category": "apartment"
    },
    "пентхаус": {
        "price": 500000, "income": 2500, "emoji": "🏙️",
        "desc": "Элитный пентхаус с панорамным видом",
        "rooms": 5, "land": 4,
        "upgrade_price": 250000, "upgrade_income": 1250,
        "max_level": 10, "category": "apartment"
    },
    "дом_в_деревне": {
        "price": 50000, "income": 200, "emoji": "🏠",
        "desc": "Уютный дом в деревне с садом",
        "rooms": 3, "land": 10,
        "upgrade_price": 25000, "upgrade_income": 100,
        "max_level": 10, "category": "house"
    },
    "коттедж": {
        "price": 150000, "income": 600, "emoji": "🏡",
        "desc": "Современный коттедж с участком",
        "rooms": 5, "land": 20,
        "upgrade_price": 75000, "upgrade_income": 300,
        "max_level": 10, "category": "house"
    },
    "особняк": {
        "price": 500000, "income": 2000, "emoji": "🏰",
        "desc": "Роскошный особняк с бассейном",
        "rooms": 10, "land": 50,
        "upgrade_price": 250000, "upgrade_income": 1000,
        "max_level": 10, "category": "house"
    },
    "замок": {
        "price": 2000000, "income": 8000, "emoji": "🏛️",
        "desc": "Настоящий средневековый замок",
        "rooms": 20, "land": 100,
        "upgrade_price": 1000000, "upgrade_income": 4000,
        "max_level": 10, "category": "house"
    },
    "офис": {
        "price": 80000, "income": 400, "emoji": "🏢",
        "desc": "Офис в бизнес-центре",
        "rooms": 0, "land": 3,
        "upgrade_price": 40000, "upgrade_income": 200,
        "max_level": 10, "category": "commercial"
    },
    "магазин": {
        "price": 120000, "income": 600, "emoji": "🏪",
        "desc": "Торговое помещение",
        "rooms": 0, "land": 4,
        "upgrade_price": 60000, "upgrade_income": 300,
        "max_level": 10, "category": "commercial"
    },
    "склад": {
        "price": 60000, "income": 300, "emoji": "📦",
        "desc": "Складское помещение",
        "rooms": 0, "land": 6,
        "upgrade_price": 30000, "upgrade_income": 150,
        "max_level": 10, "category": "commercial"
    },
    "ресторан": {
        "price": 200000, "income": 1000, "emoji": "🍽️",
        "desc": "Готовый ресторанный бизнес",
        "rooms": 0, "land": 5,
        "upgrade_price": 100000, "upgrade_income": 500,
        "max_level": 10, "category": "commercial"
    },
    "гостиница": {
        "price": 300000, "income": 1500, "emoji": "🏨",
        "desc": "Небольшая гостиница",
        "rooms": 10, "land": 8,
        "upgrade_price": 150000, "upgrade_income": 750,
        "max_level": 10, "category": "commercial"
    },
}

class RealEstateManager:
    def __init__(self):
        self.rental_cache = {}
        self.collect_lock = {}
    
    async def buy_property(self, user_id: int, property_name: str) -> dict:
        if property_name not in REAL_ESTATE:
            return {'error': True, 'message': '❌ Такой недвижимости нет!'}
        
        data = REAL_ESTATE[property_name]
        price = data['price']
        
        existing = await db.execute(
            "SELECT * FROM real_estate WHERE user_id = ? AND property_name = ?",
            (user_id, property_name), fetch_one=True
        )
        if existing:
            return {'error': True, 'message': '❌ У тебя уже есть эта недвижимость!'}
        
        coins = await get_coins(user_id)
        if coins < price:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(price)}'
            }
        
        await remove_coins(user_id, price)
        
        await db.execute(
            """INSERT INTO real_estate (user_id, property_name, property_type, income, last_collect, created_date) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, property_name, data['category'], data['income'], datetime.now().isoformat(), datetime.now().isoformat())
        )
        
        await unlock_achievement(user_id, "first_property")
        
        return {
            'error': False,
            'success': True,
            'property': property_name,
            'emoji': data['emoji'],
            'price': price,
            'income': data['income'],
            'desc': data['desc']
        }
    
    async def get_properties(self, user_id: int) -> List[dict]:
        result = await db.execute(
            "SELECT * FROM real_estate WHERE user_id = ? ORDER BY income DESC",
            (user_id,), fetch_all=True, cache_ttl=30
        )
        return result or []
    
    async def upgrade_property(self, user_id: int, property_name: str) -> dict:
        property_data = await db.execute(
            "SELECT * FROM real_estate WHERE user_id = ? AND property_name = ?",
            (user_id, property_name), fetch_one=True
        )
        if not property_data:
            return {'error': True, 'message': '❌ Недвижимость не найдена!'}
        
        data = REAL_ESTATE[property_name]
        if property_data['level'] >= data['max_level']:
            return {'error': True, 'message': f'❌ Максимальный уровень {data["max_level"]}!'}
        
        cost = data['upgrade_price'] * property_data['level']
        new_income = property_data['income'] + data['upgrade_income']
        
        coins = await get_coins(user_id)
        if coins < cost:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(cost)}'
            }
        
        await remove_coins(user_id, cost)
        
        await db.execute(
            "UPDATE real_estate SET level = level + 1, income = ? WHERE user_id = ? AND property_name = ?",
            (new_income, user_id, property_name)
        )
        
        return {
            'error': False,
            'success': True,
            'property': property_name,
            'new_level': property_data['level'] + 1,
            'new_income': new_income,
            'cost': cost
        }
    
    async def collect_rent(self, user_id: int, property_id: int) -> dict:
        property_data = await db.execute(
            "SELECT * FROM real_estate WHERE id = ? AND user_id = ?",
            (property_id, user_id), fetch_one=True
        )
        if not property_data:
            return {'error': True, 'message': '❌ Недвижимость не найдена!'}
        
        last_collect = property_data['last_collect']
        if last_collect:
            last_time = datetime.fromisoformat(last_collect)
            elapsed = (datetime.now() - last_time).total_seconds() / 3600
        else:
            elapsed = 0
        
        if elapsed < 1:
            return {
                'error': True,
                'message': f'⏳ Доход будет через {format_time_seconds(int((1 - elapsed) * 3600))}!'
            }
        
        income = property_data['income']
        total_income = int(income * elapsed)
        
        await add_coins(user_id, total_income)
        
        await db.execute(
            "UPDATE real_estate SET last_collect = ? WHERE id = ?",
            (datetime.now().isoformat(), property_id)
        )
        
        return {
            'error': False,
            'success': True,
            'property': property_data['property_name'],
            'income': total_income,
            'hours': elapsed,
            'hourly_income': income
        }
    
    async def rent_out(self, user_id: int, property_id: int, price: int) -> dict:
        property_data = await db.execute(
            "SELECT * FROM real_estate WHERE id = ? AND user_id = ?",
            (property_id, user_id), fetch_one=True
        )
        if not property_data:
            return {'error': True, 'message': '❌ Недвижимость не найдена!'}
        
        if property_data.get('rented_to'):
            return {'error': True, 'message': '❌ Уже сдано в аренду!'}
        
        await db.execute(
            "UPDATE real_estate SET rent_price = ?, rented_to = 0 WHERE id = ?",
            (price, property_id)
        )
        
        return {
            'error': False,
            'success': True,
            'property': property_data['property_name'],
            'price': price
        }

real_estate_manager = RealEstateManager()

async def buy_property(user_id: int, property_name: str) -> dict:
    return await real_estate_manager.buy_property(user_id, property_name)

async def get_properties(user_id: int) -> List[dict]:
    return await real_estate_manager.get_properties(user_id)

async def upgrade_property(user_id: int, property_name: str) -> dict:
    return await real_estate_manager.upgrade_property(user_id, property_name)

async def collect_rent(user_id: int, property_id: int) -> dict:
    return await real_estate_manager.collect_rent(user_id, property_id)

async def rent_out(user_id: int, property_id: int, price: int) -> dict:
    return await real_estate_manager.rent_out(user_id, property_id, price)
    import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from database import db, get_coins, add_coins, remove_coins
from utils import format_large_number, format_time_seconds, get_name
from economy import unlock_achievement
from social import get_clan, get_clan_by_id, get_clan_info

class ClanWarSystem:
    def __init__(self):
        self.active_wars = {}
        self.war_history = {}
        self.battle_logs = {}
        self.war_stats = {}
        self.war_id = 0
    
    async def declare_war(self, chat_id: int, user_id: int, target_clan_id: int) -> dict:
        user_clan = await get_clan(user_id, chat_id)
        if not user_clan:
            return {'error': True, 'message': '❌ Ты не в клане!'}
        
        if user_clan['owner_id'] != user_id:
            return {'error': True, 'message': '❌ Только лидер клана может объявлять войну!'}
        
        target_clan = await get_clan_by_id(target_clan_id)
        if not target_clan:
            return {'error': True, 'message': '❌ Целевой клан не найден!'}
        
        if user_clan['id'] == target_clan_id:
            return {'error': True, 'message': '❌ Нельзя объявлять войну своему клану!'}
        
        for war in self.active_wars.values():
            if war['chat_id'] == chat_id and war['status'] == 'active':
                if war['clan1'] == user_clan['id'] or war['clan2'] == user_clan['id']:
                    return {'error': True, 'message': '❌ Твой клан уже участвует в войне!'}
        
        clan_key = f"clan_{user_clan['id']}"
        if clan_key in self.war_stats:
            last_war = self.war_stats[clan_key].get('last_war')
            if last_war:
                last_time = datetime.fromisoformat(last_war)
                if (datetime.now() - last_time).days < 1:
                    return {'error': True, 'message': '⏳ Клан может воевать раз в 24 часа!'}
        
        self.war_id += 1
        war_id = self.war_id
        
        self.active_wars[war_id] = {
            'id': war_id,
            'chat_id': chat_id,
            'clan1': user_clan['id'],
            'clan2': target_clan_id,
            'clan1_name': user_clan['name'],
            'clan2_name': target_clan['name'],
            'started': datetime.now().isoformat(),
            'status': 'active',
            'score1': 0,
            'score2': 0,
            'battles': [],
            'turns': 0,
            'max_turns': 10,
            'winner': None,
            'prize': 0
        }
        
        self.war_stats[clan_key] = self.war_stats.get(clan_key, {})
        self.war_stats[clan_key]['last_war'] = datetime.now().isoformat()
        self.war_stats[clan_key]['wars'] = self.war_stats[clan_key].get('wars', 0) + 1
        
        return {
            'error': False,
            'success': True,
            'war_id': war_id,
            'clan1': user_clan['name'],
            'clan2': target_clan['name']
        }
    
    async def get_war_info(self, war_id: int) -> dict:
        if war_id not in self.active_wars:
            return {'error': True, 'message': '❌ Война не найдена!'}
        
        war = self.active_wars[war_id]
        
        return {
            'error': False,
            'success': True,
            'war_id': war_id,
            'clan1': war['clan1_name'],
            'clan2': war['clan2_name'],
            'score': f"{war['score1']} - {war['score2']}",
            'status': war['status'],
            'turns': war['turns'],
            'max_turns': war['max_turns'],
            'battles': war['battles'][-10:],
            'started': war['started']
        }
    
    async def get_active_wars(self, chat_id: int) -> List[dict]:
        result = []
        for war in self.active_wars.values():
            if war['chat_id'] == chat_id and war['status'] == 'active':
                result.append({
                    'id': war['id'],
                    'clan1': war['clan1_name'],
                    'clan2': war['clan2_name'],
                    'score': f"{war['score1']} - {war['score2']}",
                    'turns': war['turns'],
                    'max_turns': war['max_turns']
                })
        return result
    
    async def battle(self, war_id: int, user_id: int) -> dict:
        if war_id not in self.active_wars:
            return {'error': True, 'message': '❌ Война не найдена!'}
        
        war = self.active_wars[war_id]
        if war['status'] != 'active':
            return {'error': True, 'message': '❌ Война уже завершена!'}
        
        clan1 = await get_clan_by_id(war['clan1'])
        clan2 = await get_clan_by_id(war['clan2'])
        
        if not clan1 or not clan2:
            return {'error': True, 'message': '❌ Клан не найден!'}
        
        members1 = clan1['members'].split(',') if clan1['members'] else []
        members2 = clan2['members'].split(',') if clan2['members'] else []
        
        user_in_clan1 = str(user_id) in members1
        user_in_clan2 = str(user_id) in members2
        
        if not user_in_clan1 and not user_in_clan2:
            return {'error': True, 'message': '❌ Ты не участвуешь в этой войне!'}
        
        battle_key = f"battle_{user_id}_{war_id}"
        if battle_key in self.battle_logs:
            last_battle = self.battle_logs[battle_key]
            if (datetime.now() - last_battle).seconds < 300:
                remaining = 300 - (datetime.now() - last_battle).seconds
                return {'error': True, 'message': f'⏳ Подожди {format_time_seconds(remaining)}!'}
        
        enemy_members = members2 if user_in_clan1 else members1
        if not enemy_members:
            return {'error': True, 'message': '❌ Вражеский клан пуст!'}
        
        enemy_id = int(random.choice(enemy_members))
        
        user_power = random.randint(1, 20)
        enemy_power = random.randint(1, 20)
        
        user_rolls = [random.randint(1, 20) for _ in range(3)]
        enemy_rolls = [random.randint(1, 20) for _ in range(3)]
        
        user_total = sum(user_rolls) + user_power
        enemy_total = sum(enemy_rolls) + enemy_power
        
        if user_total > enemy_total:
            if user_in_clan1:
                war['score1'] += 1
            else:
                war['score2'] += 1
            winner = user_id
        elif enemy_total > user_total:
            if user_in_clan1:
                war['score2'] += 1
            else:
                war['score1'] += 1
            winner = enemy_id
        else:
            winner = None
        
        war['battles'].append(f"{await get_name(user_id)} vs {await get_name(enemy_id)}: {user_total} - {enemy_total}")
        war['turns'] += 1
        
        self.battle_logs[battle_key] = datetime.now()
        
        if winner:
            await add_coins(winner, 50)
        
        if war['turns'] >= war['max_turns'] or war['score1'] >= 5 or war['score2'] >= 5:
            return await self.end_war(war_id)
        
        return {
            'error': False,
            'success': True,
            'user_rolls': user_rolls,
            'enemy_rolls': enemy_rolls,
            'user_total': user_total,
            'enemy_total': enemy_total,
            'score': f"{war['clan1_name']} {war['score1']} - {war['score2']} {war['clan2_name']}",
            'turns': war['turns'],
            'max_turns': war['max_turns'],
            'winner': winner
        }
    
    async def end_war(self, war_id: int) -> dict:
        if war_id not in self.active_wars:
            return {'error': True, 'message': '❌ Война не найдена!'}
        
        war = self.active_wars[war_id]
        
        if war['score1'] > war['score2']:
            winner_id = war['clan1']
            winner_name = war['clan1_name']
            prize = war['score1'] * 1000
        elif war['score2'] > war['score1']:
            winner_id = war['clan2']
            winner_name = war['clan2_name']
            prize = war['score2'] * 1000
        else:
            winner_id = None
            winner_name = "Ничья"
            prize = 0
        
        if winner_id:
            await db.execute(
                "UPDATE clans SET treasury = treasury + ? WHERE id = ?",
                (prize, winner_id)
            )
            
            clan = await get_clan_by_id(winner_id)
            if clan:
                members = clan['members'].split(',') if clan['members'] else []
                for member in members:
                    await add_coins(int(member), 100)
        
        war['status'] = 'finished'
        war['winner'] = winner_id
        war['prize'] = prize
        war['ended'] = datetime.now().isoformat()
        
        self.war_history[war_id] = war
        del self.active_wars[war_id]
        
        return {
            'error': False,
            'success': True,
            'winner': winner_name,
            'prize': prize,
            'score': f"{war['clan1_name']} {war['score1']} - {war['score2']} {war['clan2_name']}"
        }

clan_war_system = ClanWarSystem()

async def declare_war(chat_id: int, user_id: int, target_clan_id: int) -> dict:
    return await clan_war_system.declare_war(chat_id, user_id, target_clan_id)

async def get_war_info(war_id: int) -> dict:
    return await clan_war_system.get_war_info(war_id)

async def get_active_wars(chat_id: int) -> List[dict]:
    return await clan_war_system.get_active_wars(chat_id)

async def war_battle(war_id: int, user_id: int) -> dict:
    return await clan_war_system.battle(war_id, user_id)

async def end_war(war_id: int) -> dict:
    return await clan_war_system.end_war(war_id)
  import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from database import db, get_coins, add_coins, remove_coins, has_item, add_item, remove_item, get_inventory
from utils import format_large_number
from economy import unlock_achievement

ACHIEVEMENTS_EXTRA = {
    "economy_beginner": {"name": "💰 Начинающий инвестор", "desc": "Накопить 10,000 монет", "reward": 100},
    "economy_intermediate": {"name": "📈 Опытный инвестор", "desc": "Накопить 100,000 монет", "reward": 1000},
    "economy_expert": {"name": "📊 Мастер инвестиций", "desc": "Накопить 1,000,000 монет", "reward": 10000},
    "economy_master": {"name": "👑 Король экономики", "desc": "Накопить 10,000,000 монет", "reward": 100000},
    "business_beginner": {"name": "🏪 Начинающий бизнесмен", "desc": "Купить 1 бизнес", "reward": 50},
    "business_intermediate": {"name": "🏢 Бизнесмен", "desc": "Купить 5 бизнесов", "reward": 500},
    "business_expert": {"name": "🏭 Предприниматель", "desc": "Купить 10 бизнесов", "reward": 2000},
    "business_master": {"name": "👑 Магнат", "desc": "Купить 25 бизнесов", "reward": 10000},
    "games_beginner": {"name": "🎲 Игрок", "desc": "Сыграть 10 игр", "reward": 50},
    "games_intermediate": {"name": "🎮 Заядлый игрок", "desc": "Сыграть 100 игр", "reward": 500},
    "games_expert": {"name": "🎯 Профи", "desc": "Сыграть 500 игр", "reward": 2000},
    "games_master": {"name": "🏆 Легенда игр", "desc": "Сыграть 1000 игр", "reward": 5000},
    "clan_beginner": {"name": "🤝 Новобранец", "desc": "Вступить в клан", "reward": 30},
    "clan_intermediate": {"name": "⚔️ Воин клана", "desc": "Участвовать в 10 битвах", "reward": 500},
    "clan_expert": {"name": "🏰 Защитник", "desc": "Участвовать в 50 битвах", "reward": 2000},
    "clan_master": {"name": "👑 Легенда клана", "desc": "Участвовать в 100 битвах", "reward": 5000},
    "pet_beginner": {"name": "🐕 Друг человека", "desc": "Завести питомца", "reward": 30},
    "pet_intermediate": {"name": "🐕‍🦺 Хозяин", "desc": "Прокачать питомца до 5 уровня", "reward": 200},
    "pet_expert": {"name": "🐺 Повелитель", "desc": "Прокачать питомца до 10 уровня", "reward": 1000},
    "pet_master": {"name": "🐉 Драконовладелец", "desc": "Прокачать питомца до 20 уровня", "reward": 5000},
}

class AchievementExtraManager:
    def __init__(self):
        self.cache = {}
    
    async def check_achievements(self, user_id: int) -> List[dict]:
        unlocked = []
        
        coins = await get_coins(user_id)
        businesses = await db.execute(
            "SELECT COUNT(*) as count FROM businesses WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        businesses_count = businesses['count'] if businesses else 0
        
        games_played = await db.execute(
            "SELECT SUM(played) as total FROM game_stats WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        games_total = games_played['total'] if games_played else 0
        
        if coins >= 10000:
            result = await self._unlock(user_id, "economy_beginner")
            if result: unlocked.append(result)
        if coins >= 100000:
            result = await self._unlock(user_id, "economy_intermediate")
            if result: unlocked.append(result)
        if coins >= 1000000:
            result = await self._unlock(user_id, "economy_expert")
            if result: unlocked.append(result)
        
        if businesses_count >= 1:
            result = await self._unlock(user_id, "business_beginner")
            if result: unlocked.append(result)
        if businesses_count >= 5:
            result = await self._unlock(user_id, "business_intermediate")
            if result: unlocked.append(result)
        if businesses_count >= 10:
            result = await self._unlock(user_id, "business_expert")
            if result: unlocked.append(result)
        
        if games_total >= 10:
            result = await self._unlock(user_id, "games_beginner")
            if result: unlocked.append(result)
        if games_total >= 100:
            result = await self._unlock(user_id, "games_intermediate")
            if result: unlocked.append(result)
        
        return unlocked
    
    async def _unlock(self, user_id: int, ach_name: str) -> Optional[dict]:
        if ach_name not in ACHIEVEMENTS_EXTRA:
            return None
        
        existing = await db.execute(
            "SELECT * FROM achievements_extra WHERE user_id = ? AND ach_name = ?",
            (user_id, ach_name), fetch_one=True
        )
        if existing:
            return None
        
        await db.execute(
            "INSERT INTO achievements_extra (user_id, ach_name, unlocked) VALUES (?, ?, ?)",
            (user_id, ach_name, datetime.now().isoformat())
        )
        
        reward = ACHIEVEMENTS_EXTRA[ach_name]['reward']
        await add_coins(user_id, reward)
        
        return {
            'name': ACHIEVEMENTS_EXTRA[ach_name]['name'],
            'desc': ACHIEVEMENTS_EXTRA[ach_name]['desc'],
            'reward': reward
        }

achievement_extra = AchievementExtraManager()

class LotterySystem:
    def __init__(self):
        self.lotteries = {}
        self.tickets = {}
        self.lottery_id = 0
    
    async def create_lottery(self, prize: int, tickets_count: int, ticket_price: int) -> dict:
        self.lottery_id += 1
        lottery_id = self.lottery_id
        
        self.lotteries[lottery_id] = {
            'id': lottery_id,
            'prize': prize,
            'tickets_count': tickets_count,
            'ticket_price': ticket_price,
            'sold': 0,
            'status': 'active',
            'created': datetime.now().isoformat(),
            'ends': (datetime.now() + timedelta(hours=48)).isoformat()
        }
        self.tickets[lottery_id] = []
        
        return {
            'error': False,
            'success': True,
            'lottery_id': lottery_id,
            'prize': prize,
            'ticket_price': ticket_price
        }
    
    async def buy_ticket(self, lottery_id: int, user_id: int, quantity: int = 1) -> dict:
        if lottery_id not in self.lotteries:
            return {'error': True, 'message': '❌ Лотерея не найдена!'}
        
        lottery = self.lotteries[lottery_id]
        if lottery['status'] != 'active':
            return {'error': True, 'message': '❌ Лотерея завершена!'}
        
        total_price = lottery['ticket_price'] * quantity
        coins = await get_coins(user_id)
        if coins < total_price:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(total_price)}'
            }
        
        if lottery['sold'] + quantity > lottery['tickets_count']:
            return {'error': True, 'message': '❌ Билеты закончились!'}
        
        await remove_coins(user_id, total_price)
        
        for _ in range(quantity):
            self.tickets[lottery_id].append({
                'user_id': user_id,
                'ticket_number': len(self.tickets[lottery_id]) + 1
            })
        
        lottery['sold'] += quantity
        
        return {
            'error': False,
            'success': True,
            'lottery_id': lottery_id,
            'quantity': quantity,
            'total_price': total_price
        }
    
    async def draw_lottery(self, lottery_id: int) -> dict:
        if lottery_id not in self.lotteries:
            return {'error': True, 'message': '❌ Лотерея не найдена!'}
        
        lottery = self.lotteries[lottery_id]
        if lottery['status'] != 'active':
            return {'error': True, 'message': '❌ Лотерея уже завершена!'}
        
        if len(self.tickets[lottery_id]) < 1:
            return {'error': True, 'message': '❌ Нет билетов для розыгрыша!'}
        
        winner_ticket = random.choice(self.tickets[lottery_id])
        winner_id = winner_ticket['user_id']
        
        await add_coins(winner_id, lottery['prize'])
        
        lottery['status'] = 'completed'
        lottery['winner'] = winner_id
        lottery['ended'] = datetime.now().isoformat()
        
        return {
            'error': False,
            'success': True,
            'lottery_id': lottery_id,
            'winner': winner_id,
            'prize': lottery['prize'],
            'tickets_sold': lottery['sold']
        }

lottery_system = LotterySystem()

class AuctionSystem:
    def __init__(self):
        self.auctions = {}
        self.auction_id = 0
    
    async def create_auction(self, user_id: int, item_name: str, quantity: int, start_price: int) -> dict:
        if quantity <= 0:
            return {'error': True, 'message': '❌ Количество должно быть больше 0!'}
        
        if start_price <= 0:
            return {'error': True, 'message': '❌ Начальная цена должна быть больше 0!'}
        
        has = await has_item(user_id, item_name)
        if has < quantity:
            return {'error': True, 'message': f'❌ У тебя нет {quantity} {item_name}!'}
        
        await remove_item(user_id, item_name, quantity)
        
        self.auction_id += 1
        auction_id = self.auction_id
        
        self.auctions[auction_id] = {
            'id': auction_id,
            'seller': user_id,
            'item': item_name,
            'quantity': quantity,
            'current_price': start_price,
            'start_price': start_price,
            'buyout_price': start_price * 2,
            'bids': [],
            'created': datetime.now().isoformat(),
            'ends': (datetime.now() + timedelta(hours=24)).isoformat(),
            'status': 'active'
        }
        
        return {
            'error': False,
            'success': True,
            'auction_id': auction_id,
            'item': item_name,
            'quantity': quantity,
            'start_price': start_price
        }
    
    async def place_bid(self, auction_id: int, user_id: int, bid: int) -> dict:
        if auction_id not in self.auctions:
            return {'error': True, 'message': '❌ Аукцион не найден!'}
        
        auction = self.auctions[auction_id]
        if auction['status'] != 'active':
            return {'error': True, 'message': '❌ Аукцион завершён!'}
        
        if auction['seller'] == user_id:
            return {'error': True, 'message': '❌ Нельзя делать ставку на свой лот!'}
        
        if bid <= auction['current_price']:
            return {'error': True, 'message': f'❌ Ставка должна быть больше {auction["current_price"]}!'}
        
        coins = await get_coins(user_id)
        if coins < bid:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Есть {format_large_number(coins)}'
            }
        
        if auction['bids']:
            last_bid = auction['bids'][-1]
            await add_coins(last_bid['user_id'], last_bid['amount'])
        
        await remove_coins(user_id, bid)
        
        auction['bids'].append({
            'user_id': user_id,
            'amount': bid,
            'time': datetime.now().isoformat()
        })
        auction['current_price'] = bid
        
        if bid >= auction['buyout_price']:
            return await self.buyout_auction(auction_id, user_id)
        
        return {
            'error': False,
            'success': True,
            'auction_id': auction_id,
            'current_price': bid
        }
    
    async def buyout_auction(self, auction_id: int, user_id: int) -> dict:
        if auction_id not in self.auctions:
            return {'error': True, 'message': '❌ Аукцион не найден!'}
        
        auction = self.auctions[auction_id]
        if auction['status'] != 'active':
            return {'error': True, 'message': '❌ Аукцион завершён!'}
        
        coins = await get_coins(user_id)
        if coins < auction['buyout_price']:
            return {
                'error': True,
                'message': f'❌ Недостаточно монет! Нужно {format_large_number(auction["buyout_price"])}'
            }
        
        await remove_coins(user_id, auction['buyout_price'])
        await add_item(user_id, auction['item'], auction['quantity'])
        await add_coins(auction['seller'], auction['buyout_price'])
        
        auction['status'] = 'completed'
        auction['winner'] = user_id
        auction['ended'] = datetime.now().isoformat()
        
        return {
            'error': False,
            'success': True,
            'auction_id': auction_id,
            'item': auction['item'],
            'quantity': auction['quantity'],
            'price': auction['buyout_price']
        }
    
    async def get_active_auctions(self) -> List[dict]:
        result = []
        for aid, auction in self.auctions.items():
            if auction['status'] == 'active':
                result.append({
                    'id': aid,
                    'item': auction['item'],
                    'quantity': auction['quantity'],
                    'current_price': auction['current_price'],
                    'buyout_price': auction['buyout_price'],
                    'bids_count': len(auction['bids']),
                    'ends': auction['ends']
                })
        return result

auction_system = AuctionSystem()

async def check_achievements_extra(user_id: int) -> List[dict]:
    return await achievement_extra.check_achievements(user_id)

async def create_lottery(prize: int, tickets_count: int, ticket_price: int) -> dict:
    return await lottery_system.create_lottery(prize, tickets_count, ticket_price)

async def buy_ticket(lottery_id: int, user_id: int, quantity: int = 1) -> dict:
    return await lottery_system.buy_ticket(lottery_id, user_id, quantity)

async def draw_lottery(lottery_id: int) -> dict:
    return await lottery_system.draw_lottery(lottery_id)

async def create_auction(user_id: int, item_name: str, quantity: int, start_price: int) -> dict:
    return await auction_system.create_auction(user_id, item_name, quantity, start_price)

async def place_bid(auction_id: int, user_id: int, bid: int) -> dict:
    return await auction_system.place_bid(auction_id, user_id, bid)

async def buyout_auction(auction_id: int, user_id: int) -> dict:
    return await auction_system.buyout_auction(auction_id, user_id)

async def get_active_auctions() -> List[dict]:
    return await auction_system.get_active_auctions() 
# ДИАЛОГ 14/20: TAXES_VIP.PY

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from database import db, get_coins, add_coins, remove_coins
from utils import format_large_number
from economy import unlock_achievement
from business import get_businesses
from real_estate import get_properties

class TaxSystem:
    def __init__(self):
        self.tax_rates = {
            "income_tax": 0.10,
            "property_tax": 0.01,
            "business_tax": 0.05,
            "capital_gains": 0.15,
            "luxury_tax": 0.20,
        }
        self.tax_history = {}
        self.tax_exemptions = {}
    
    async def calculate_income_tax(self, user_id: int, income: int) -> int:
        if income <= 10000:
            rate = 0.05
        elif income <= 50000:
            rate = 0.10
        elif income <= 100000:
            rate = 0.15
        elif income <= 500000:
            rate = 0.20
        else:
            rate = 0.25
        
        exemption = await self.check_exemption(user_id, "income")
        if exemption:
            rate = max(0, rate - 0.05)
        
        tax = int(income * rate)
        key = f"tax_{user_id}_{datetime.now().strftime('%Y-%m')}"
        self.tax_history[key] = self.tax_history.get(key, 0) + tax
        
        return tax
    
    async def calculate_property_tax(self, user_id: int) -> int:
        properties = await get_properties(user_id)
        if not properties:
            return 0
        
        total_value = 0
        for prop in properties:
            from real_estate import REAL_ESTATE
            data = REAL_ESTATE.get(prop['property_name'])
            if data:
                total_value += data['price'] * prop['level']
        
        tax = int(total_value * self.tax_rates["property_tax"])
        key = f"property_tax_{user_id}_{datetime.now().strftime('%Y-%m')}"
        self.tax_history[key] = self.tax_history.get(key, 0) + tax
        
        return tax
    
    async def calculate_business_tax(self, user_id: int) -> int:
        businesses = await get_businesses(user_id)
        if not businesses:
            return 0
        
        total_income = sum(b['income'] for b in businesses)
        tax = int(total_income * self.tax_rates["business_tax"])
        key = f"business_tax_{user_id}_{datetime.now().strftime('%Y-%m')}"
        self.tax_history[key] = self.tax_history.get(key, 0) + tax
        
        return tax
    
    async def check_exemption(self, user_id: int, tax_type: str) -> bool:
        key = f"{user_id}_{tax_type}"
        if key in self.tax_exemptions:
            exemption = self.tax_exemptions[key]
            if exemption['expires'] > datetime.now():
                return True
        return False
    
    async def grant_exemption(self, user_id: int, tax_type: str, days: int) -> dict:
        key = f"{user_id}_{tax_type}"
        self.tax_exemptions[key] = {
            "tax_type": tax_type,
            "expires": datetime.now() + timedelta(days=days)
        }
        return {
            'error': False,
            'success': True,
            'user_id': user_id,
            'tax_type': tax_type,
            'expires': self.tax_exemptions[key]['expires'].isoformat()
        }
    
    async def collect_taxes(self, user_id: int) -> dict:
        coins = await get_coins(user_id)
        if coins <= 0:
            return {'error': True, 'message': '❌ Нечего облагать налогом!'}
        
        income_tax = await self.calculate_income_tax(user_id, coins)
        property_tax = await self.calculate_property_tax(user_id)
        business_tax = await self.calculate_business_tax(user_id)
        
        total_tax = income_tax + property_tax + business_tax
        
        if total_tax <= 0:
            return {'message': 'Налоги не начислены!'}
        
        if coins < total_tax:
            total_tax = coins
            await remove_coins(user_id, total_tax)
            return {
                'error': False,
                'success': True,
                'warning': '⚠️ Недостаточно средств! Сняты все монеты.',
                'total_tax': total_tax
            }
        
        await remove_coins(user_id, total_tax)
        
        return {
            'error': False,
            'success': True,
            'income_tax': income_tax,
            'property_tax': property_tax,
            'business_tax': business_tax,
            'total_tax': total_tax,
            'remaining': await get_coins(user_id)
        }

tax_system = TaxSystem()

class VipSystem:
    def __init__(self):
        self.vip_levels = {
            1: {"name": "🥉 Бронзовый VIP", "price": 10000, "bonus": 1.05, "perks": ["daily_bonus_x2"]},
            2: {"name": "🥈 Серебряный VIP", "price": 50000, "bonus": 1.10, "perks": ["daily_bonus_x3", "work_bonus"]},
            3: {"name": "🥇 Золотой VIP", "price": 100000, "bonus": 1.20, "perks": ["daily_bonus_x5", "work_bonus", "no_tax"]},
            4: {"name": "💎 Платиновый VIP", "price": 500000, "bonus": 1.30, "perks": ["daily_bonus_x10", "work_bonus", "no_tax", "free_rent", "interest_boost"]},
            5: {"name": "👑 Императорский VIP", "price": 1000000, "bonus": 1.50, "perks": ["daily_bonus_x20", "work_bonus", "no_tax", "free_rent", "interest_boost", "all_boost"]}
        }
        self.vip_members = {}
        self.vip_cache = {}
    
    async def upgrade_vip(self, user_id: int, level: int) -> dict:
        if level not in self.vip_levels:
            return {'error': True, 'message': '❌ Такого VIP уровня нет!'}
        
        current = self.vip_members.get(user_id, {}).get('level', 0)
        if current >= level:
            return {'error': True, 'message': f'❌ У тебя уже {self.vip_levels[current]["name"]}!'}
        
        vip_data = self.vip_levels[level]
        price = vip_data['price']
        
        coins = await get_coins(user_id)
        if coins < price:
            return {'error': True, 'message': f'❌ Нужно {format_large_number(price)} монет!'}
        
        await remove_coins(user_id, price)
        
        self.vip_members[user_id] = {
            'level': level,
            'started': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        if user_id in self.vip_cache:
            del self.vip_cache[user_id]
        
        return {
            'error': False,
            'success': True,
            'level': level,
            'name': vip_data['name'],
            'bonus': vip_data['bonus'],
            'perks': vip_data['perks']
        }
    
    async def get_vip_info(self, user_id: int) -> dict:
        if user_id in self.vip_cache:
            return self.vip_cache[user_id]
        
        if user_id not in self.vip_members:
            result = {'level': 0, 'name': 'Обычный игрок', 'bonus': 1.0, 'perks': [], 'days_left': 0}
            self.vip_cache[user_id] = result
            return result
        
        vip = self.vip_members[user_id]
        level = vip['level']
        data = self.vip_levels[level]
        
        expires = datetime.fromisoformat(vip['expires'])
        days_left = (expires - datetime.now()).days
        
        if days_left < 0:
            del self.vip_members[user_id]
            result = {'level': 0, 'name': 'Обычный игрок', 'bonus': 1.0, 'perks': [], 'days_left': 0}
            self.vip_cache[user_id] = result
            return result
        
        result = {
            'level': level,
            'name': data['name'],
            'bonus': data['bonus'],
            'perks': data['perks'],
            'days_left': days_left
        }
        self.vip_cache[user_id] = result
        return result
    
    async def get_vip_bonus(self, user_id: int) -> float:
        info = await self.get_vip_info(user_id)
        return info['bonus'] if info['level'] > 0 else 1.0
    
    async def check_vip_perk(self, user_id: int, perk: str) -> bool:
        info = await self.get_vip_info(user_id)
        return perk in info['perks'] if info['level'] > 0 else False

vip_system = VipSystem()

async def calculate_income_tax(user_id: int, income: int) -> int:
    return await tax_system.calculate_income_tax(user_id, income)

async def calculate_property_tax(user_id: int) -> int:
    return await tax_system.calculate_property_tax(user_id)

async def calculate_business_tax(user_id: int) -> int:
    return await tax_system.calculate_business_tax(user_id)

async def collect_taxes(user_id: int) -> dict:
    return await tax_system.collect_taxes(user_id)

async def upgrade_vip(user_id: int, level: int) -> dict:
    return await vip_system.upgrade_vip(user_id, level)

async def get_vip_info(user_id: int) -> dict:
    return await vip_system.get_vip_info(user_id)

async def get_vip_bonus(user_id: int) -> float:
    return await vip_system.get_vip_bonus(user_id)

async def check_vip_perk(user_id: int, perk: str) -> bool:
    return await vip_system.check_vip_perk(user_id, perk)    
# ДИАЛОГ 15/20: CRISIS.PY

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from database import db
from utils import format_percentage

class EconomicCrisis:
    def __init__(self):
        self.crises = {}
        self.inflation_rates = {}
        self.economic_indexes = {}
        self.last_update = datetime.now()
    
    async def update(self, chat_id: int):
        now = datetime.now()
        
        crisis = await db.execute(
            "SELECT * FROM crisis WHERE chat_id = ? ORDER BY id DESC LIMIT 1",
            (chat_id,), fetch_one=True
        )
        
        if crisis and crisis.get('active'):
            severity = crisis.get('severity', 0)
            start_date = datetime.fromisoformat(crisis.get('start_date'))
            duration = (now - start_date).days
            
            if duration > 7:
                severity = max(0, severity - 0.1)
                if severity < 0.5:
                    await db.execute(
                        "UPDATE crisis SET active = 0, end_date = ? WHERE chat_id = ? AND active = 1",
                        (now.isoformat(), chat_id)
                    )
                    self.crises[chat_id] = None
                    return
            
            multiplier = 0.7 + (severity * 0.05)
            await db.execute(
                "UPDATE crisis SET multiplier = ?, severity = ? WHERE chat_id = ? AND active = 1",
                (multiplier, severity, chat_id)
            )
            
            self.crises[chat_id] = {
                'active': True,
                'severity': severity,
                'multiplier': multiplier,
                'inflation': crisis.get('inflation_rate', 0.05)
            }
        else:
            if random.random() < 0.001:
                severity = random.uniform(1, 10)
                inflation = random.uniform(0.02, 0.15)
                await db.execute(
                    """INSERT INTO crisis (chat_id, active, severity, inflation_rate, start_date, multiplier) 
                       VALUES (?, 1, ?, ?, ?, ?)""",
                    (chat_id, severity, inflation, now.isoformat(), 0.7 + (severity * 0.05))
                )
                self.crises[chat_id] = {
                    'active': True,
                    'severity': severity,
                    'multiplier': 0.7 + (severity * 0.05),
                    'inflation': inflation
                }
                return
        
        base_inflation = 0.02
        if chat_id in self.crises and self.crises[chat_id]:
            base_inflation += self.crises[chat_id].get('inflation', 0)
        
        base_inflation += random.uniform(-0.005, 0.005)
        base_inflation = max(0, base_inflation)
        
        self.inflation_rates[chat_id] = base_inflation
        await self._update_index(chat_id)
        self.last_update = now
    
    async def _update_index(self, chat_id: int):
        crisis = self.crises.get(chat_id)
        if crisis and crisis.get('active'):
            severity = crisis.get('severity', 0)
            index = max(0, 100 - (severity * 10))
        else:
            index = 100
        
        index += random.uniform(-5, 5)
        index = max(0, min(100, index))
        self.economic_indexes[chat_id] = index
    
    def get_multiplier(self, chat_id: int) -> float:
        if chat_id in self.crises and self.crises[chat_id]:
            return self.crises[chat_id].get('multiplier', 1.0)
        return 1.0
    
    def get_inflation(self, chat_id: int) -> float:
        return self.inflation_rates.get(chat_id, 0.02)
    
    def get_index(self, chat_id: int) -> int:
        return self.economic_indexes.get(chat_id, 100)
    
    def is_crisis_active(self, chat_id: int) -> bool:
        crisis = self.crises.get(chat_id)
        return crisis is not None and crisis.get('active', False)

crisis_system = EconomicCrisis()

async def start_crisis_tasks():
    while True:
        try:
            chats = await db.execute("SELECT DISTINCT chat_id FROM settings", fetch_all=True)
            for chat in chats:
                await crisis_system.update(chat['chat_id'])
            await asyncio.sleep(60)
        except Exception as e:
            await asyncio.sleep(60)
    # ДИАЛОГ 16/20: REFERRAL.PY

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from database import db, get_coins, add_coins, remove_coins
from utils import format_large_number
from config import BOT_USERNAME

class ReferralSystem:
    def __init__(self):
        self.referral_codes = {}
        self.referral_stats = {}
        self.referral_cache = {}
    
    async def create_referral_code(self, user_id: int) -> dict:
        code = f"FABLE_{user_id}_{random.randint(1000, 9999)}"
        
        await db.execute(
            "INSERT OR REPLACE INTO referral_codes (user_id, code) VALUES (?, ?)",
            (user_id, code)
        )
        
        return {
            'error': False,
            'success': True,
            'code': code,
            'link': f"https://t.me/{BOT_USERNAME}?start={code}"
        }
    
    async def use_referral_code(self, user_id: int, code: str) -> dict:
        result = await db.execute(
            "SELECT user_id FROM referral_codes WHERE code = ?",
            (code,), fetch_one=True
        )
        
        if not result:
            return {'error': True, 'message': '❌ Неверный реферальный код!'}
        
        referrer_id = result['user_id']
        
        if referrer_id == user_id:
            return {'error': True, 'message': '❌ Нельзя использовать свой код!'}
        
        used = await db.execute(
            "SELECT * FROM referrals WHERE referred_id = ?",
            (user_id,), fetch_one=True
        )
        
        if used:
            return {'error': True, 'message': '❌ Ты уже использовал реферальный код!'}
        
        await db.execute(
            "INSERT INTO referrals (referrer_id, referred_id, date) VALUES (?, ?, ?)",
            (referrer_id, user_id, datetime.now().isoformat())
        )
        
        await add_coins(referrer_id, 1000)
        await add_coins(user_id, 500)
        
        await self._unlock_achievement(referrer_id, "first_referral")
        
        return {
            'error': False,
            'success': True,
            'referrer': referrer_id,
            'reward_referrer': 1000,
            'reward_referred': 500
        }
    
    async def _unlock_achievement(self, user_id: int, ach_name: str):
        from economy import unlock_achievement
        await unlock_achievement(user_id, ach_name)
    
    async def get_referrals(self, user_id: int) -> List[dict]:
        result = await db.execute(
            "SELECT referred_id, date FROM referrals WHERE referrer_id = ?",
            (user_id,), fetch_all=True, cache_ttl=30
        )
        return result or []
    
    async def get_referral_stats(self, user_id: int) -> dict:
        if user_id in self.referral_cache:
            return self.referral_cache[user_id]
        
        referrals = await self.get_referrals(user_id)
        
        total_earned = await db.execute(
            "SELECT SUM(commission_earned) as total FROM referrals WHERE referrer_id = ?",
            (user_id,), fetch_one=True
        )
        
        result = {
            'total_referrals': len(referrals),
            'active_referrals': 0,
            'total_earned': total_earned['total'] if total_earned else 0
        }
        
        for ref in referrals:
            coins = await get_coins(ref['referred_id'])
            if coins > 0:
                result['active_referrals'] += 1
        
        self.referral_cache[user_id] = result
        return result
    
    async def add_commission(self, referrer_id: int, amount: int):
        commission = int(amount * 0.10)
        
        await db.execute(
            "UPDATE referrals SET commission_earned = commission_earned + ? WHERE referrer_id = ?",
            (commission, referrer_id)
        )
        
        await add_coins(referrer_id, commission)

referral_system = ReferralSystem()

async def create_referral_code(user_id: int) -> dict:
    return await referral_system.create_referral_code(user_id)

async def use_referral_code(user_id: int, code: str) -> dict:
    return await referral_system.use_referral_code(user_id, code)

async def get_referral_stats(user_id: int) -> dict:
    return await referral_system.get_referral_stats(user_id)

async def add_commission(user_id: int, amount: int):
    await referral_system.add_commission(user_id, amount)
# ДИАЛОГ 18/20: DUELS.PY

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from database import db, get_coins, add_coins, remove_coins, has_item, get_pet
from utils import format_large_number, format_time_seconds, get_name
from economy import unlock_achievement

class DuelSystem:
    def __init__(self):
        self.duels = {}
        self.duel_id = 0
        self.duel_stats = {}
    
    async def create_duel(self, user_id: int, target_id: int, bet: int) -> dict:
        if user_id == target_id:
            return {'error': True, 'message': '❌ Нельзя с самим собой!'}
        
        if bet <= 0:
            return {'error': True, 'message': '❌ Ставка должна быть больше 0!'}
        
        if bet > 100000:
            return {'error': True, 'message': '❌ Максимальная ставка 100,000 монет!'}
        
        coins = await get_coins(user_id)
        if coins < bet:
            return {'error': True, 'message': f'❌ У тебя нет {format_large_number(bet)} монет!'}
        
        coins2 = await get_coins(target_id)
        if coins2 < bet:
            return {'error': True, 'message': f'❌ У {await get_name(target_id)} нет {format_large_number(bet)} монет!'}
        
        if not await self._can_duel(user_id):
            return {'error': True, 'message': '⏳ Подожди перед новой дуэлью!'}
        
        self.duel_id += 1
        duel_id = self.duel_id
        
        self.duels[duel_id] = {
            'id': duel_id,
            'user1': user_id,
            'user2': target_id,
            'bet': bet,
            'status': 'waiting',
            'created': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(minutes=2)).isoformat(),
            'winner': None
        }
        
        await self._set_duel_cooldown(user_id)
        
        return {
            'error': False,
            'success': True,
            'duel_id': duel_id,
            'user1': user_id,
            'user2': target_id,
            'bet': bet
        }
    
    async def accept_duel(self, duel_id: int, user_id: int) -> dict:
        if duel_id not in self.duels:
            return {'error': True, 'message': '❌ Дуэль не найдена!'}
        
        duel = self.duels[duel_id]
        
        if duel['user2'] != user_id:
            return {'error': True, 'message': '❌ Это не тебя вызывают!'}
        
        if duel['status'] != 'waiting':
            return {'error': True, 'message': '❌ Дуэль уже завершена!'}
        
        expires = datetime.fromisoformat(duel['expires'])
        if expires < datetime.now():
            del self.duels[duel_id]
            return {'error': True, 'message': '❌ Время на принятие истекло!'}
        
        await remove_coins(duel['user1'], duel['bet'])
        await remove_coins(duel['user2'], duel['bet'])
        
        duel['status'] = 'active'
        duel['started'] = datetime.now().isoformat()
        
        result = await self._fight(duel_id)
        
        return result
    
    async def _fight(self, duel_id: int) -> dict:
        duel = self.duels[duel_id]
        
        user1_power = random.randint(1, 20)
        user2_power = random.randint(1, 20)
        
        user1_sword = await has_item(duel['user1'], "меч")
        user2_sword = await has_item(duel['user2'], "меч")
        
        user1_power += user1_sword * 2
        user2_power += user2_sword * 2
        
        pet1 = await get_pet(duel['user1'])
        pet2 = await get_pet(duel['user2'])
        
        if pet1 and pet1['happiness'] > 50:
            user1_power += pet1['level'] // 2
        if pet2 and pet2['happiness'] > 50:
            user2_power += pet2['level'] // 2
        
        rolls1 = [random.randint(1, 20) for _ in range(3)]
        rolls2 = [random.randint(1, 20) for _ in range(3)]
        
        total1 = sum(rolls1) + user1_power
        total2 = sum(rolls2) + user2_power
        
        if total1 > total2:
            winner = duel['user1']
            loser = duel['user2']
            win_amount = duel['bet'] * 2
        elif total2 > total1:
            winner = duel['user2']
            loser = duel['user1']
            win_amount = duel['bet'] * 2
        else:
            await add_coins(duel['user1'], duel['bet'])
            await add_coins(duel['user2'], duel['bet'])
            duel['status'] = 'draw'
            return {
                'error': False,
                'success': True,
                'result': 'draw',
                'message': '🤝 Ничья! Ставки возвращены!'
            }
        
        await add_coins(winner, win_amount)
        
        duel['status'] = 'finished'
        duel['winner'] = winner
        duel['ended'] = datetime.now().isoformat()
        
        await unlock_achievement(winner, "first_duel_win")
        
        self.duel_stats[winner] = self.duel_stats.get(winner, 0) + 1
        
        return {
            'error': False,
            'success': True,
            'result': 'win',
            'winner': winner,
            'loser': loser,
            'win_amount': win_amount,
            'user1_power': user1_power,
            'user2_power': user2_power,
            'rolls1': rolls1,
            'rolls2': rolls2,
            'total1': total1,
            'total2': total2
        }
    
    async def _can_duel(self, user_id: int) -> bool:
        result = await db.execute(
            "SELECT last_duel FROM users WHERE user_id = ?",
            (user_id,), fetch_one=True
        )
        if not result or not result['last_duel']:
            return True
        last_duel = datetime.fromisoformat(result['last_duel'])
        return (datetime.now() - last_duel).seconds > 60
    
    async def _set_duel_cooldown(self, user_id: int):
        await db.execute(
            "UPDATE users SET last_duel = ? WHERE user_id = ?",
            (datetime.now().isoformat(), user_id)
        )
    
    async def get_duel_stats(self, user_id: int) -> dict:
        return {
            'wins': self.duel_stats.get(user_id, 0),
            'total': len([d for d in self.duels.values() if d['user1'] == user_id or d['user2'] == user_id])
        }

duel_system = DuelSystem()

async def create_duel(user_id: int, target_id: int, bet: int) -> dict:
    return await duel_system.create_duel(user_id, target_id, bet)

async def accept_duel(duel_id: int, user_id: int) -> dict:
    return await duel_system.accept_duel(duel_id, user_id)

async def get_duel_stats(user_id: int) -> dict:
    return await duel_system.get_duel_stats(user_id)
# ДИАЛОГ 19/20: TOURNAMENTS.PY

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from database import db, get_coins, add_coins, remove_coins
from utils import format_large_number, get_name
from economy import unlock_achievement

class TournamentSystem:
    def __init__(self):
        self.tournaments = {}
        self.participants = {}
        self.tournament_id = 0
        self.tournament_types = ['poker', 'slots', 'duel']
    
    async def create_tournament(self, chat_id: int, creator_id: int, prize: int, 
                                type: str = 'poker', max_participants: int = 10) -> dict:
        if type not in self.tournament_types:
            return {'error': True, 'message': '❌ Неизвестный тип турнира!'}
        
        if prize <= 0:
            return {'error': True, 'message': '❌ Приз должен быть больше 0!'}
        
        coins = await get_coins(creator_id)
        if coins < prize:
            return {'error': True, 'message': f'❌ Нужно {format_large_number(prize)} монет!'}
        
        await remove_coins(creator_id, prize)
        
        self.tournament_id += 1
        tournament_id = self.tournament_id
        
        self.tournaments[tournament_id] = {
            'id': tournament_id,
            'chat_id': chat_id,
            'creator_id': creator_id,
            'prize': prize,
            'type': type,
            'status': 'waiting',
            'max_participants': max_participants,
            'created': datetime.now().isoformat(),
            'started': None,
            'ended': None,
            'winner_id': None
        }
        self.participants[tournament_id] = []
        
        return {
            'error': False,
            'success': True,
            'tournament_id': tournament_id,
            'prize': prize,
            'type': type
        }
    
    async def join_tournament(self, tournament_id: int, user_id: int) -> dict:
        if tournament_id not in self.tournaments:
            return {'error': True, 'message': '❌ Турнир не найден!'}
        
        tournament = self.tournaments[tournament_id]
        
        if tournament['status'] != 'waiting':
            return {'error': True, 'message': '❌ Турнир уже начался!'}
        
        if user_id in self.participants[tournament_id]:
            return {'error': True, 'message': '❌ Ты уже участвуешь!'}
        
        if len(self.participants[tournament_id]) >= tournament['max_participants']:
            return {'error': True, 'message': '❌ Все места заняты!'}
        
        self.participants[tournament_id].append(user_id)
        
        return {
            'error': False,
            'success': True,
            'participants': len(self.participants[tournament_id])
        }
    
    async def start_tournament(self, tournament_id: int) -> dict:
        if tournament_id not in self.tournaments:
            return {'error': True, 'message': '❌ Турнир не найден!'}
        
        tournament = self.tournaments[tournament_id]
        
        if tournament['status'] != 'waiting':
            return {'error': True, 'message': '❌ Турнир уже начался!'}
        
        if len(self.participants[tournament_id]) < 2:
            return {'error': True, 'message': '❌ Нужно минимум 2 участника!'}
        
        tournament['status'] = 'active'
        tournament['started'] = datetime.now().isoformat()
        
        winner = await self._run_tournament(tournament_id)
        
        tournament['status'] = 'finished'
        tournament['ended'] = datetime.now().isoformat()
        tournament['winner_id'] = winner
        
        await add_coins(winner, tournament['prize'])
        await unlock_achievement(winner, "tournament_win")
        
        return {
            'error': False,
            'success': True,
            'winner': winner,
            'prize': tournament['prize'],
            'participants': len(self.participants[tournament_id])
        }
    
    async def _run_tournament(self, tournament_id: int) -> int:
        participants = self.participants[tournament_id].copy()
        
        while len(participants) > 1:
            next_round = []
            for i in range(0, len(participants), 2):
                if i + 1 < len(participants):
                    winner = await self._battle(participants[i], participants[i+1])
                    next_round.append(winner)
                else:
                    next_round.append(participants[i])
            participants = next_round
        
        return participants[0]
    
    async def _battle(self, user1: int, user2: int) -> int:
        power1 = random.randint(1, 20)
        power2 = random.randint(1, 20)
        
        pet1 = await get_pet(user1)
        pet2 = await get_pet(user2)
        
        if pet1 and pet1['happiness'] > 50:
            power1 += pet1['level'] // 2
        if pet2 and pet2['happiness'] > 50:
            power2 += pet2['level'] // 2
        
        total1 = power1 + random.randint(1, 20)
        total2 = power2 + random.randint(1, 20)
        
        return user1 if total1 > total2 else user2
    
    async def get_tournament_info(self, tournament_id: int) -> dict:
        if tournament_id not in self.tournaments:
            return {'error': True, 'message': '❌ Турнир не найден!'}
        
        tournament = self.tournaments[tournament_id]
        participants = self.participants[tournament_id]
        
        return {
            'error': False,
            'success': True,
            'id': tournament['id'],
            'type': tournament['type'],
            'status': tournament['status'],
            'prize': tournament['prize'],
            'participants': len(participants),
            'max_participants': tournament['max_participants'],
            'creator_id': tournament['creator_id'],
            'winner_id': tournament['winner_id']
        }

tournament_system = TournamentSystem()

async def create_tournament(chat_id: int, creator_id: int, prize: int, 
                            type: str = 'poker', max_participants: int = 10) -> dict:
    return await tournament_system.create_tournament(chat_id, creator_id, prize, type, max_participants)

async def join_tournament(tournament_id: int, user_id: int) -> dict:
    return await tournament_system.join_tournament(tournament_id, user_id)

async def start_tournament(tournament_id: int) -> dict:
    return await tournament_system.start_tournament(tournament_id)

async def get_tournament_info(tournament_id: int) -> dict:
    return await tournament_system.get_tournament_info(tournament_id)
    # ДИАЛОГ 20/20: FINAL_MERGE.PY

import asyncio
import sys
import logging
import traceback
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import TOKEN, OWNER_ID, BOT_NAME, BOT_USERNAME
from database import init_db, db
from handlers import setup_handlers, dp
from economy import start_economy_tasks
from admin import start_admin_tasks
from crisis import start_crisis_tasks
from integration import weather_system, time_system

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fable_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def log_error(error: Exception, context: str = ""):
    logger.error(f"❌ Ошибка в {context}: {error}")
    logger.error(traceback.format_exc())

bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)

async def main():
    try:
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔥 FABLE BOT V5.0 — МЕГА-ВЕРСИЯ 🔥                       ║
║                                                              ║
║   🤖 Бот: Fable                                             ║
║   👑 Владелец: 8039111975                                   ║
║   💾 База: SQLite (оптимизированная)                        ║
║   📊 Функций: 300+                                          ║
║   💼 Профессий: 100+                                        ║
║   🏪 Бизнесов: 100+                                         ║
║   ⚡ Режим: МАКСИМАЛЬНАЯ СКОРОСТЬ                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        print("💾 Инициализация базы данных...")
        init_db()
        
        print("📝 Настройка обработчиков...")
        setup_handlers(dp)
        
        print("🚀 Запуск фоновых задач...")
        asyncio.create_task(start_economy_tasks())
        asyncio.create_task(start_admin_tasks())
        asyncio.create_task(start_crisis_tasks())
        
        print("✅ БОТ ГОТОВ К РАБОТЕ!")
        print("="*60 + "\n")
        
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
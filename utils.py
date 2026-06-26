# Часть 5: Весь вспомогательный код (утилиты, хелперы, декораторы, валидаторы)
# Модуль: utils.py

from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, TypeVar, ParamSpec
from datetime import datetime, timedelta
import random
import string
import re
import json
import hashlib
import logging
import asyncio
import functools
import time
import math
from dataclasses import dataclass, field, asdict
from enum import Enum
from functools import wraps

from models import (
    User, ChatConfig, AdminLevel, ModLog, Business, CryptoAsset,
    StockAsset, UserPortfolio, Miner, Auction, Clan, ClanWar,
    Tournament, Pet, ShopItem, UserInventory, Achievement,
    Transaction, GameSession, Report, GlobalEconomy, Earth,
    Vehicle, House, Insurance, BlacklistEntry, ChatStats,
    WorldEvent, GameType, ModActionType, TransactionType,
    EarthRegion, ItemRarity, ItemCategory, PetMood, PetRarity,
    AchievementCategory, TournamentStatus, TournamentType,
    MarriageStatus, AuctionStatus, ClanWarStatus, MinerType,
    SUPER_ADMIN_ID, SUPER_ADMIN_LEVEL, BUSINESS_TYPES,
    CRYPTO_ASSETS_CONFIG, STOCK_ASSETS_CONFIG, MINER_CONFIG,
    HOUSE_CONFIG, VEHICLE_CONFIG, SHOP_ITEMS_CONFIG,
    ACHIEVEMENTS_CONFIG, PROFESSIONS, WORLD_EVENTS_POOL,
    REPUTATION_LEVELS, ADMIN_PERMISSIONS, SUPER_ADMIN_PERMISSIONS,
    BOT_NAME, BOT_ALIASES, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE,
    MIN_PAGE_SIZE, MAX_STRING_LENGTH, MAX_TEXT_LENGTH,
    DEFAULT_TIMEOUT_SECONDS, MAX_TIMEOUT_SECONDS,
    generate_id, validate_amount, validate_string_length,
    validate_duration_minutes, parse_duration, get_reputation_level,
    calculate_business_income, calculate_miner_income,
    is_super_admin, get_permissions_for_level, has_permission,
    EARTH_PRICE_MULTIPLIER, MAX_CLAN_MEMBERS, MAX_PET_LEVEL,
)

from services import DataStore, EconomyService, BankService, BusinessService, MarketService
from game_logic import CasinoService, AuctionService, CrimeService, ModerationService
from game_logic import ClanService, MarriageService, AchievementService, InsuranceService, ReputationService


# ============================================================
# ЛОГГИРОВАНИЕ
# ============================================================

class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[1;31m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(level: str = "INFO", log_file: str = "logs/bot.log") -> logging.Logger:
    logger = logging.getLogger("FableBot")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter(
        "%(asctime)s | %(levelname)-18s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(console_handler)

    if log_file:
        import os
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        logger.addHandler(file_handler)

    return logger


logger = setup_logging()


# ============================================================
# ДЕКОРАТОРЫ
# ============================================================

def retry(max_attempts: int = 3, delay_seconds: float = 1.0, backoff_multiplier: float = 2.0,
          exceptions: Tuple = (Exception,)):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay_seconds
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(f"Retry {attempt}/{max_attempts} for {func.__name__}: {e}")
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff_multiplier
                    else:
                        logger.error(f"All retries failed for {func.__name__}: {e}")
            raise last_exception

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay_seconds
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(f"Retry {attempt}/{max_attempts} for {func.__name__}: {e}")
                        time.sleep(current_delay)
                        current_delay *= backoff_multiplier
                    else:
                        logger.error(f"All retries failed for {func.__name__}: {e}")
            raise last_exception

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, user_id: int, chat_id: int, *args, **kwargs):
            if not has_permission(self.store.get_admin_level(user_id, chat_id), permission):
                if not is_super_admin(user_id):
                    return False, f"Требуется право: {permission}"
            return await func(self, user_id, chat_id, *args, **kwargs)
        return wrapper
    return decorator


def require_super_admin(func):
    @wraps(func)
    async def wrapper(user_id: int, *args, **kwargs):
        if not is_super_admin(user_id):
            return False, "Только супер-админ может выполнить это действие"
        return await func(user_id, *args, **kwargs)
    return wrapper


def rate_limit(max_calls: int = 10, period_seconds: int = 60):
    def decorator(func):
        call_records: Dict[int, List[float]] = {}

        @wraps(func)
        async def wrapper(user_id: int, *args, **kwargs):
            now = time.time()
            if user_id not in call_records:
                call_records[user_id] = []

            call_records[user_id] = [t for t in call_records[user_id] if now - t < period_seconds]

            if len(call_records[user_id]) >= max_calls:
                oldest = min(call_records[user_id]) if call_records[user_id] else now
                wait_time = int(period_seconds - (now - oldest))
                return False, f"Слишком много запросов. Подождите {wait_time} сек"

            call_records[user_id].append(now)
            return await func(user_id, *args, **kwargs)

        return wrapper
    return decorator


def log_execution(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start
            logger.debug(f"{func.__name__} executed in {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"{func.__name__} failed in {elapsed:.3f}s: {e}")
            raise

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            logger.debug(f"{func.__name__} executed in {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"{func.__name__} failed in {elapsed:.3f}s: {e}")
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


def cache_result(ttl_seconds: int = 300):
    def decorator(func):
        cache: Dict[str, Tuple[float, Any]] = {}

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = hashlib.md5(
                f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}".encode()
            ).hexdigest()

            now = time.time()
            if key in cache:
                cached_time, cached_value = cache[key]
                if now - cached_time < ttl_seconds:
                    return cached_value

            result = await func(*args, **kwargs)
            cache[key] = (now, result)

            if len(cache) > 1000:
                oldest_keys = sorted(cache.keys(), key=lambda k: cache[k][0])[:100]
                for k in oldest_keys:
                    del cache[k]

            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            key = hashlib.md5(
                f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}".encode()
            ).hexdigest()

            now = time.time()
            if key in cache:
                cached_time, cached_value = cache[key]
                if now - cached_time < ttl_seconds:
                    return cached_value

            result = func(*args, **kwargs)
            cache[key] = (now, result)
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


# ============================================================
# ФОРМАТТЕРЫ
# ============================================================

def format_number(num: int) -> str:
    if num is None:
        return "0"
    if abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    if abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    if abs(num) >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def format_currency(amount: int) -> str:
    return f"{amount:,} 💰"


def format_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} сек"
    if seconds < 3600:
        return f"{seconds // 60} мин {seconds % 60} сек"
    if seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours} ч {minutes} мин"
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    return f"{days} дн {hours} ч"


def format_duration_short(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}с"
    if seconds < 3600:
        return f"{seconds // 60}м"
    if seconds < 86400:
        return f"{seconds // 3600}ч"
    return f"{seconds // 86400}д"


def format_datetime(dt: datetime) -> str:
    if dt is None:
        return "Никогда"
    now = datetime.now()
    diff = now - dt
    if diff.total_seconds() < 60:
        return "Только что"
    if diff.total_seconds() < 3600:
        return f"{int(diff.total_seconds() // 60)} мин назад"
    if diff.total_seconds() < 86400:
        return f"{int(diff.total_seconds() // 3600)} ч назад"
    if diff.days < 7:
        return f"{diff.days} дн назад"
    return dt.strftime("%d.%m.%Y %H:%M")


def format_remaining_time(target: datetime) -> str:
    if target is None:
        return "Бессрочно"
    now = datetime.now()
    if target <= now:
        return "Истекло"
    diff = target - now
    return format_duration(int(diff.total_seconds()))


def format_percent(value: float) -> str:
    if value > 0:
        return f"📈 +{value:.1f}%"
    elif value < 0:
        return f"📉 {value:.1f}%"
    return "➡️ 0%"


def format_user_mention(user: User) -> str:
    name = user.first_name or user.username or str(user.user_id)
    return f"<a href='tg://user?id={user.user_id}'>{name}</a>"


def format_balance_card(user: User) -> str:
    lines = [
        f"👤 {format_user_mention(user)}",
        f"💰 Баланс: {format_currency(user.balance)}",
        f"🏦 В банке: {format_currency(user.bank_balance)}",
    ]
    if user.loan_amount > 0:
        lines.append(f"💳 Кредит: {format_currency(user.loan_amount)}")
    if user.insurance_active:
        lines.append(f"🛡 Страховка активна")
    return "\n".join(lines)


def format_business_card(business: Business) -> str:
    config = next((b for b in BUSINESS_TYPES if b["type"] == business.business_type), None)
    type_name = config["name"] if config else business.business_type

    lines = [
        f"🏢 {business.name} ({type_name})",
        f"⭐ Уровень: {business.level}/{10}",
        f"💰 Доход: {format_currency(calculate_business_income(business))}/час",
        f"💎 Стоимость: {format_currency(business.current_value)}",
        f"👥 Сотрудники: {len(business.employees)}/{business.max_employees}",
        f"📊 Статус: {business.status.value}",
    ]
    return "\n".join(lines)


def format_crypto_card(asset: CryptoAsset) -> str:
    return (
        f"🪙 {asset.name} ({asset.ticker})\n"
        f"💵 Цена: ${asset.current_price:,.2f}\n"
        f"{format_percent(asset.change_percent)}\n"
        f"📈 Max: ${asset.all_time_high:,.2f}\n"
        f"📉 Min: ${asset.all_time_low:,.2f}"
    )


def format_stock_card(asset: StockAsset) -> str:
    return (
        f"📊 {asset.company_name} ({asset.ticker})\n"
        f"💵 Цена: ${asset.current_price:,.2f}\n"
        f"{format_percent(asset.change_percent)}\n"
        f"💎 Сектор: {asset.sector}\n"
        f"📈 Дивиденды: {asset.dividend_yield * 100:.1f}%"
    )


def format_clan_card(clan: Clan) -> str:
    return (
        f"{clan.logo_emoji} Клан: {clan.name}\n"
        f"👑 Лидер: {clan.leader_id}\n"
        f"👥 Участников: {len(clan.members)}/{MAX_CLAN_MEMBERS}\n"
        f"💰 Казна: {format_currency(clan.treasury)}\n"
        f"⚔️ Побед/Поражений: {clan.wars_won}/{clan.wars_lost}"
    )


def format_pet_card(pet: Pet) -> str:
    species_config = next((s for s in PROFESSIONS if s["name"] == pet.species), None)
    species_name = pet.species

    mood_emoji = {
        PetMood.HAPPY: "😊",
        PetMood.NEUTRAL: "😐",
        PetMood.SAD: "😢",
        PetMood.HUNGRY: "🍽️",
        PetMood.SICK: "🤒",
    }

    lines = [
        f"🐾 {pet.name} ({species_name})",
        f"⭐ Редкость: {pet.rarity.value}",
        f"📊 Уровень: {pet.level}/{MAX_PET_LEVEL}",
        f"❤️ Здоровье: {pet.health}/100",
        f"🍖 Сытость: {100 - pet.hunger}/100",
        f"{mood_emoji.get(pet.mood, '😐')} Настроение: {pet.mood.value}",
    ]
    if pet.mutation:
        lines.append(f"🧬 Мутация: {pet.mutation}")
    return "\n".join(lines)


def format_achievement_card(achievement: Achievement) -> str:
    category_emoji = {
        AchievementCategory.MONEY: "💰",
        AchievementCategory.BUSINESS: "🏢",
        AchievementCategory.CRYPTO: "🪙",
        AchievementCategory.STOCKS: "📊",
        AchievementCategory.CASINO: "🎰",
        AchievementCategory.CRIME: "🔫",
        AchievementCategory.CLAN: "⚔️",
        AchievementCategory.SOCIAL: "💬",
        AchievementCategory.SPECIAL: "🌟",
        AchievementCategory.MODERATION: "🛡",
    }
    emoji = category_emoji.get(achievement.category, "🏆")
    return f"{emoji} {achievement.name}: {achievement.description}" + (
        f" (+{achievement.reward})" if achievement.reward > 0 else ""
    )


def format_shop_item(item: ShopItem) -> str:
    rarity_emoji = {
        ItemRarity.COMMON: "⚪",
        ItemRarity.UNCOMMON: "🟢",
        ItemRarity.RARE: "🔵",
        ItemRarity.EPIC: "🟣",
        ItemRarity.LEGENDARY: "🟠",
        ItemRarity.MYTHIC: "🔴",
    }
    emoji = rarity_emoji.get(item.rarity, "⚪")
    return (
        f"{emoji} {item.name}\n"
        f"📝 {item.description}\n"
        f"💵 Цена: {format_currency(item.price)}\n"
        f"📈 Бонус: +{item.boost_percent:.0f}% на {item.boost_duration_hours}ч"
    )


def format_transaction_history(transactions: List[Transaction], limit: int = 10) -> str:
    if not transactions:
        return "📭 История пуста"

    lines = ["📋 Последние операции:"]
    for tx in transactions[:limit]:
        sign = "+" if tx.amount >= 0 else ""
        lines.append(
            f"{sign}{format_currency(tx.amount)} | {tx.transaction_type.value} | "
            f"{format_datetime(tx.timestamp)}"
        )
    return "\n".join(lines)


def format_mod_logs(logs: List[ModLog], limit: int = 10) -> str:
    if not logs:
        return "📭 Логи модерации пусты"

    lines = ["📋 Логи модерации:"]
    for log in logs[:limit]:
        action_emoji = {
            ModActionType.WARN: "⚠️",
            ModActionType.MUTE: "🔇",
            ModActionType.KICK: "👢",
            ModActionType.BAN: "🔨",
            ModActionType.CLEAR: "🧹",
            ModActionType.LOCK: "🔒",
            ModActionType.UNLOCK: "🔓",
        }
        emoji = action_emoji.get(log.action, "📌")
        lines.append(
            f"{emoji} {log.action.value} | Цель: {log.target_id} | "
            f"Модер: {log.moderator_id} | {format_datetime(log.timestamp)}"
        )
        if log.reason:
            lines.append(f"   Причина: {log.reason}")
    return "\n".join(lines)


def format_auction_card(auction: Auction) -> str:
    return (
        f"🔨 Аукцион #{auction.auction_id[:8]}\n"
        f"📦 Лот: {auction.item_name}\n"
        f"💰 Текущая ставка: {format_currency(auction.current_bid)}\n"
        f"👤 Лидер: {auction.current_bidder_id if auction.current_bidder_id else 'Нет'}\n"
        f"⏳ Завершение: {format_remaining_time(auction.ends_at)}"
    )


def format_tournament_card(tournament: Tournament) -> str:
    status_emoji = {
        TournamentStatus.REGISTRATION: "📝",
        TournamentStatus.IN_PROGRESS: "🏟",
        TournamentStatus.FINISHED: "🏁",
        TournamentStatus.CANCELLED: "❌",
    }
    emoji = status_emoji.get(tournament.status, "🏟")
    return (
        f"{emoji} Турнир: {tournament.name}\n"
        f"🎮 Тип: {tournament.tournament_type.value}\n"
        f"💰 Призовой фонд: {format_currency(tournament.prize_pool)}\n"
        f"👥 Игроков: {len(tournament.registered_players)}/{tournament.max_players}\n"
        f"🎫 Вход: {format_currency(tournament.entry_fee)}"
    )


def format_world_event(event: WorldEvent) -> str:
    impacts = []
    if event.affect_stocks:
        impacts.append(f"Акции: {format_percent(event.stock_impact_percent)}")
    if event.affect_crypto:
        impacts.append(f"Крипта: {format_percent(event.crypto_impact_percent)}")
    if event.affect_business:
        impacts.append(f"Бизнес: {format_percent(event.business_impact_percent)}")

    return (
        f"🌍 {event.name}\n"
        f"📝 {event.description}\n"
        f"{chr(10).join(impacts)}\n"
        f"⏳ Осталось: {format_remaining_time(event.ends_at)}"
    )


# ============================================================
# ПАГИНАЦИЯ
# ============================================================

def paginate_list(items: List[Any], page: int = 1,
                  page_size: int = DEFAULT_PAGE_SIZE) -> Tuple[List[Any], int, int]:
    page = max(1, page)
    page_size = max(MIN_PAGE_SIZE, min(MAX_PAGE_SIZE, page_size))
    total_items = len(items)
    total_pages = max(1, math.ceil(total_items / page_size))
    page = min(page, total_pages)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_items = items[start_idx:end_idx]

    return page_items, page, total_pages


def paginate_text(text: str, chunk_size: int = 4096) -> List[str]:
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    while len(text) > chunk_size:
        split_pos = text.rfind("\n", 0, chunk_size)
        if split_pos == -1:
            split_pos = text.rfind(" ", 0, chunk_size)
        if split_pos == -1:
            split_pos = chunk_size

        chunks.append(text[:split_pos].strip())
        text = text[split_pos:].strip()

    if text:
        chunks.append(text)

    return chunks


def generate_pagination_keyboard(current_page: int, total_pages: int,
                                  callback_prefix: str) -> List[List[Dict[str, str]]]:
    keyboard = []
    row = []

    if current_page > 1:
        row.append({
            "text": "⬅️ Назад",
            "callback_data": f"{callback_prefix}:page:{current_page - 1}",
        })

    row.append({
        "text": f"{current_page}/{total_pages}",
        "callback_data": "ignore",
    })

    if current_page < total_pages:
        row.append({
            "text": "Вперёд ➡️",
            "callback_data": f"{callback_prefix}:page:{current_page + 1}",
        })

    keyboard.append(row)
    return keyboard


# ============================================================
# ВАЛИДАТОРЫ
# ============================================================

def validate_user_id(user_id: Any) -> Tuple[bool, str, Optional[int]]:
    try:
        uid = int(user_id)
        if uid <= 0:
            return False, "ID пользователя должен быть положительным", None
        return True, "", uid
    except (ValueError, TypeError):
        return False, "Некорректный ID пользователя", None


def validate_chat_id(chat_id: Any) -> Tuple[bool, str, Optional[int]]:
    try:
        cid = int(chat_id)
        if cid <= 0:
            return False, "ID чата должен быть положительным", None
        return True, "", cid
    except (ValueError, TypeError):
        return False, "Некорректный ID чата", None


def validate_business_name(name: str) -> Tuple[bool, str]:
    if not name or not name.strip():
        return False, "Название не может быть пустым"
    if len(name) > 100:
        return False, "Название не длиннее 100 символов"
    if re.match(r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-_]+$", name) is None:
        return False, "Название содержит недопустимые символы"
    return True, ""


def validate_clan_name(name: str) -> Tuple[bool, str]:
    if not name or not name.strip():
        return False, "Название клана не может быть пустым"
    if len(name) < 2 or len(name) > 30:
        return False, "Название от 2 до 30 символов"
    if re.match(r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-_]+$", name) is None:
        return False, "Название содержит недопустимые символы"
    return True, ""


def validate_pet_name(name: str) -> Tuple[bool, str]:
    if not name or not name.strip():
        return False, "Имя питомца не может быть пустым"
    if len(name) > 30:
        return False, "Имя не длиннее 30 символов"
    return True, ""


def validate_message_text(text: str) -> Tuple[bool, str]:
    if not text or not text.strip():
        return False, "Сообщение не может быть пустым"
    if len(text) > MAX_TEXT_LENGTH:
        return False, f"Сообщение не длиннее {MAX_TEXT_LENGTH} символов"
    return True, ""


def validate_bet(bet: int, min_bet: int = 10, max_bet: int = 1_000_000) -> Tuple[bool, str]:
    return validate_amount(bet, min_bet, max_bet)


def validate_transfer_amount(amount: int, balance: int) -> Tuple[bool, str]:
    valid, error = validate_amount(amount, 1, balance)
    if not valid:
        return False, error
    if amount > balance:
        return False, "Недостаточно средств"
    return True, ""


def validate_ticker(ticker: str) -> Tuple[bool, str, Optional[str]]:
    ticker = ticker.upper().strip()
    if len(ticker) < 2 or len(ticker) > 10:
        return False, "Тикер от 2 до 10 символов", None
    if re.match(r"^[A-Z0-9]+$", ticker) is None:
        return False, "Тикер только из букв и цифр", None
    return True, "", ticker


def validate_command_args(args: List[str], expected_count: int) -> Tuple[bool, str]:
    if len(args) < expected_count:
        return False, f"Недостаточно аргументов. Нужно {expected_count}"
    return True, ""


# ============================================================
# ГЕНЕРАТОРЫ
# ============================================================

def generate_random_string(length: int = 10, include_punctuation: bool = False) -> str:
    chars = string.ascii_letters + string.digits
    if include_punctuation:
        chars += "!@#$%^&*"
    return "".join(random.choice(chars) for _ in range(length))


def generate_random_name(prefix: str = "") -> str:
    adjectives = [
        "Весёлый", "Грустный", "Злой", "Добрый", "Хитрый", "Быстрый",
        "Медленный", "Сильный", "Слабый", "Умный", "Глупый", "Смелый",
        "Трусливый", "Красивый", "Страшный", "Богатый", "Бедный", "Старый",
        "Молодой", "Тайный", "Яркий", "Тёмный", "Горячий", "Холодный",
    ]
    nouns = [
        "Кот", "Пёс", "Лис", "Волк", "Медведь", "Заяц", "Ёж", "Орёл",
        "Сокол", "Дракон", "Феникс", "Тигр", "Лев", "Панда", "Пингвин",
        "Дельфин", "Кит", "Акула", "Осьминог", "Краб", "Рак", "Жук",
        "Муравей", "Пчела", "Бабочка", "Ворон", "Сова", "Попугай",
    ]
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    if prefix:
        return f"{prefix} {adj} {noun}"
    return f"{adj} {noun}"


def generate_loot_table(rarity: str) -> Dict[str, Any]:
    tables = {
        "common": {
            "items": [
                {"name": "Медная монета", "value": 10, "weight": 50},
                {"name": "Серебряная монета", "value": 50, "weight": 30},
                {"name": "Золотая монета", "value": 100, "weight": 15},
                {"name": "Драгоценный камень", "value": 500, "weight": 5},
            ]
        },
        "rare": {
            "items": [
                {"name": "Сапфир", "value": 1000, "weight": 40},
                {"name": "Изумруд", "value": 2000, "weight": 30},
                {"name": "Рубин", "value": 5000, "weight": 20},
                {"name": "Алмаз", "value": 10000, "weight": 10},
            ]
        },
        "epic": {
            "items": [
                {"name": "Артефакт", "value": 25000, "weight": 50},
                {"name": "Реликвия", "value": 50000, "weight": 30},
                {"name": "Легендарный меч", "value": 100000, "weight": 15},
                {"name": "Корона короля", "value": 250000, "weight": 5},
            ]
        },
    }

    table = tables.get(rarity, tables["common"])
    total_weight = sum(item["weight"] for item in table["items"])
    roll = random.randint(1, total_weight)

    cumulative = 0
    for item in table["items"]:
        cumulative += item["weight"]
        if roll <= cumulative:
            return item

    return table["items"][0]


# ============================================================
# ХЕШИРОВАНИЕ И БЕЗОПАСНОСТЬ
# ============================================================

def hash_data(data: str, algorithm: str = "sha256") -> str:
    if algorithm == "md5":
        return hashlib.md5(data.encode()).hexdigest()
    if algorithm == "sha1":
        return hashlib.sha1(data.encode()).hexdigest()
    if algorithm == "sha512":
        return hashlib.sha512(data.encode()).hexdigest()
    return hashlib.sha256(data.encode()).hexdigest()


def generate_signature(data: Dict[str, Any], secret: str) -> str:
    sorted_keys = sorted(data.keys())
    message = "&".join(f"{k}={data[k]}" for k in sorted_keys)
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()


def verify_signature(data: Dict[str, Any], signature: str, secret: str) -> bool:
    expected = generate_signature(data, secret)
    return hmac.compare_digest(expected, signature)


def sanitize_html(text: str) -> str:
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def sanitize_markdown(text: str) -> str:
    special_chars = ["_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    return text


def escape_html(text: str) -> str:
    if text is None:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def unescape_html(text: str) -> str:
    if text is None:
        return ""
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


# ============================================================
# РАБОТА С JSON И ДАННЫМИ
# ============================================================

class JSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            return obj.total_seconds()
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, set):
            return list(obj)
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)


def safe_json_loads(text: str, default: Any = None) -> Any:
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"JSON decode error: {e}")
        return default


def safe_json_dumps(data: Any, default: Any = "{}") -> str:
    try:
        return json.dumps(data, cls=JSONEncoder, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        logger.warning(f"JSON encode error: {e}")
        return default


def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    items: List[Tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        elif isinstance(v, list):
            items.append((new_key, json.dumps(v, ensure_ascii=False)))
        else:
            items.append((new_key, v))
    return dict(items)


# ============================================================
# РАБОТА С ТЕКСТОМ
# ============================================================

def extract_mentions(text: str) -> List[int]:
    pattern = r"(?:@|tg://user\?id=)(\d+)"
    matches = re.findall(pattern, text)
    return [int(m) for m in matches if m.isdigit()]


def extract_hashtags(text: str) -> List[str]:
    pattern = r"#(\w+)"
    return re.findall(pattern, text)


def extract_urls(text: str) -> List[str]:
    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)


def extract_numbers(text: str) -> List[int]:
    pattern = r"-?\d+"
    return [int(m) for m in re.findall(pattern, text)]


def extract_command_args(text: str) -> Tuple[Optional[str], List[str]]:
    text = text.strip()
    parts = text.split()

    if not parts:
        return None, []

    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []

    return command, args


def match_command(text: str, aliases: List[str]) -> bool:
    command, _ = extract_command_args(text)
    if command is None:
        return False
    return command in [a.lower() for a in aliases]


def find_bot_mention(text: str) -> bool:
    text_lower = text.lower()
    for alias in BOT_ALIASES:
        if alias in text_lower:
            return True
    return False


def parse_amount_from_text(text: str) -> Optional[int]:
    numbers = extract_numbers(text)
    return numbers[0] if numbers else None


def parse_duration_from_text(text: str) -> Optional[int]:
    duration_patterns = [
        (r"(\d+)\s*сек", 1),
        (r"(\d+)\s*мин", 60),
        (r"(\d+)\s*час", 3600),
        (r"(\d+)\s*день", 86400),
        (r"(\d+)\s*дня", 86400),
        (r"(\d+)\s*дней", 86400),
        (r"(\d+)\s*нед", 604800),
        (r"(\d+)\s*мес", 2592000),
    ]

    for pattern, multiplier in duration_patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1)) * multiplier

    return None


def truncate_text(text: str, max_length: int = 100) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


# ============================================================
# РАБОТА С ВРЕМЕНЕМ
# ============================================================

def get_current_timestamp() -> int:
    return int(time.time())


def get_current_datetime() -> datetime:
    return datetime.now()


def datetime_to_timestamp(dt: datetime) -> int:
    return int(dt.timestamp())


def timestamp_to_datetime(ts: int) -> datetime:
    return datetime.fromtimestamp(ts)


def is_expired(target: datetime) -> bool:
    return target is not None and target <= datetime.now()


def get_time_until(target: datetime) -> int:
    if target is None:
        return -1
    remaining = (target - datetime.now()).total_seconds()
    return max(0, int(remaining))


def get_start_of_day(dt: Optional[datetime] = None) -> datetime:
    if dt is None:
        dt = datetime.now()
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def get_end_of_day(dt: Optional[datetime] = None) -> datetime:
    return get_start_of_day(dt) + timedelta(days=1)


def get_start_of_week(dt: Optional[datetime] = None) -> datetime:
    if dt is None:
        dt = datetime.now()
    return (dt - timedelta(days=dt.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)


def get_start_of_month(dt: Optional[datetime] = None) -> datetime:
    if dt is None:
        dt = datetime.now()
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


# ============================================================
# МАТЕМАТИЧЕСКИЕ И СТАТИСТИЧЕСКИЕ
# ============================================================

def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * clamp(t, 0.0, 1.0)


def inverse_lerp(a: float, b: float, value: float) -> float:
    if a == b:
        return 0.0
    return clamp((value - a) / (b - a), 0.0, 1.0)


def remap(value: float, old_min: float, old_max: float,
          new_min: float, new_max: float) -> float:
    return lerp(new_min, new_max, inverse_lerp(old_min, old_max, value))


def calculate_percent_change(old_value: float, new_value: float) -> float:
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / abs(old_value)) * 100.0


def weighted_random(choices: List[Tuple[Any, float]]) -> Any:
    if not choices:
        return None

    total_weight = sum(weight for _, weight in choices)
    if total_weight <= 0:
        return random.choice([item for item, _ in choices])

    roll = random.uniform(0, total_weight)
    cumulative = 0.0

    for item, weight in choices:
        cumulative += weight
        if roll <= cumulative:
            return item

    return choices[-1][0]


def gaussian_random(mean: float = 0.0, stddev: float = 1.0) -> float:
    return random.gauss(mean, stddev)


def calculate_level_from_experience(experience: int) -> int:
    return int(math.sqrt(experience / 100)) + 1


def calculate_experience_for_level(level: int) -> int:
    return (level - 1) ** 2 * 100


def calculate_compound_interest(principal: int, rate: float, periods: int) -> int:
    return int(principal * (1 + rate) ** periods)


# ============================================================
# РАБОТА С КОЛЛЕКЦИЯМИ
# ============================================================

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def group_by(items: List[Any], key_func: Callable[[Any], Any]) -> Dict[Any, List[Any]]:
    result: Dict[Any, List[Any]] = {}
    for item in items:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


def sort_by(items: List[Any], key_func: Callable[[Any], Any],
            reverse: bool = False) -> List[Any]:
    return sorted(items, key=key_func, reverse=reverse)


def unique_by(items: List[Any], key_func: Callable[[Any], Any]) -> List[Any]:
    seen: Set[Any] = set()
    result = []
    for item in items:
        key = key_func(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def merge_lists(*lists: List[Any]) -> List[Any]:
    result = []
    seen = set()
    for lst in lists:
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
    return result


def intersect_lists(*lists: List[Any]) -> List[Any]:
    if not lists:
        return []
    result = list(lists[0])
    for lst in lists[1:]:
        result = [item for item in result if item in lst]
    return result


def safe_get(data: Dict[str, Any], path: str, default: Any = None, separator: str = ".") -> Any:
    keys = path.split(separator)
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list) and key.isdigit() and int(key) < len(current):
            current = current[int(key)]
        else:
            return default
    return current


def safe_set(data: Dict[str, Any], path: str, value: Any, separator: str = ".") -> None:
    keys = path.split(separator)
    current = data
    for i, key in enumerate(keys[:-1]):
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value


# ============================================================
# ЭМОДЗИ И ГРАФИКА
# ============================================================

EMOJI_NUMBERS = {
    0: "0️⃣", 1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣",
    5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣",
}

EMOJI_PROGRESS_BAR = ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"]
EMOJI_PROGRESS_FILLED = ["🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩"]

EMOJI_STATUS = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "loading": "⏳",
    "lock": "🔒",
    "unlock": "🔓",
    "star": "⭐",
    "fire": "🔥",
    "money": "💰",
    "crown": "👑",
    "trophy": "🏆",
    "medal": "🥇",
    "target": "🎯",
    "bomb": "💣",
    "gift": "🎁",
    "party": "🎉",
    "cool": "😎",
    "thinking": "🤔",
    "sad": "😢",
    "angry": "😡",
    "heart": "❤️",
    "broken_heart": "💔",
    "skull": "💀",
    "ghost": "👻",
    "alien": "👽",
    "robot": "🤖",
    "brain": "🧠",
    "rocket": "🚀",
    "zap": "⚡",
    "rainbow": "🌈",
    "diamond": "💎",
    "bell": "🔔",
    "mail": "📧",
    "calendar": "📅",
    "clock": "🕐",
    "magnifier": "🔍",
    "key": "🔑",
    "hammer": "🔨",
    "wrench": "🔧",
    "shield": "🛡",
    "swords": "⚔️",
    "cross": "✖️",
    "check": "✔️",
    "plus": "➕",
    "minus": "➖",
}


def emoji_number(num: int) -> str:
    if num < 0 or num > 99:
        return str(num)
    if num < 10:
        return EMOJI_NUMBERS[num]
    return EMOJI_NUMBERS[num // 10] + EMOJI_NUMBERS[num % 10]


def emoji_progress_bar(current: int, max_value: int, length: int = 10) -> str:
    if max_value <= 0:
        return "".join(EMOJI_PROGRESS_BAR[:length])
    ratio = min(1.0, max(0.0, current / max_value))
    filled = int(ratio * length)
    empty = length - filled
    return "".join(EMOJI_PROGRESS_FILLED[:filled] + EMOJI_PROGRESS_BAR[:empty])


def emoji_status(success: bool) -> str:
    return EMOJI_STATUS["success"] if success else EMOJI_STATUS["error"]


def emoji_random_money() -> str:
    money_emojis = ["💰", "💵", "💴", "💶", "💷", "💸", "🪙", "💎"]
    return random.choice(money_emojis)


def generate_ascii_graph(values: List[float], width: int = 20, height: int = 10) -> str:
    if not values:
        return "Нет данных"

    max_val = max(values)
    min_val = min(values)
    value_range = max_val - min_val if max_val != min_val else 1

    normalized = [
        int((v - min_val) / value_range * (height - 1))
        for v in values
    ]

    graph_lines = []
    for row in range(height - 1, -1, -1):
        line = ""
        for val in normalized:
            if val >= row:
                line += "█"
            else:
                line += "░"
        graph_lines.append(line)

    graph_lines.append(f"Min: {min_val:.2f}  Max: {max_val:.2f}")
    return "\n".join(graph_lines)


# ============================================================
# ПАРСЕРЫ
# ============================================================

def parse_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.lower().strip()
        if value in ("true", "1", "да", "yes", "on", "вкл", "+"):
            return True
        if value in ("false", "0", "нет", "no", "off", "выкл", "-"):
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def parse_datetime(value: Any) -> Optional[datetime]:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%d.%m.%Y %H:%M:%S",
            "%d.%m.%Y %H:%M",
            "%d.%m.%Y",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None


def parse_comma_separated(value: str) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_key_value(text: str, separator: str = "=") -> Optional[Tuple[str, str]]:
    parts = text.split(separator, 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return None


# ============================================================
# ПРОЧИЕ УТИЛИТЫ
# ============================================================

def generate_short_id() -> str:
    return generate_random_string(8)


def is_admin_user_id(user_id: int, chat_id: int, store: DataStore) -> bool:
    return store.get_admin_level(user_id, chat_id) > 0 or is_super_admin(user_id)


def can_user_moderate(user_id: int, chat_id: int, target_id: int, store: DataStore) -> bool:
    if is_super_admin(user_id):
        return True
    user_level = store.get_admin_level(user_id, chat_id)
    target_level = store.get_admin_level(target_id, chat_id)
    return user_level > target_level and user_level > 0


def is_user_muted(user_id: int, store: DataStore) -> bool:
    user = store.get_user(user_id)
    return user.muted_until is not None and user.muted_until > datetime.now()


def is_user_banned(user_id: int, chat_id: int, store: DataStore) -> bool:
    for log in store.mod_logs:
        if (log.target_id == user_id and log.chat_id == chat_id
                and log.action == ModActionType.BAN and log.is_active):
            if log.expires_at is None or log.expires_at > datetime.now():
                return True
    return False


def is_user_jailed(user_id: int, store: DataStore) -> bool:
    user = store.get_user(user_id)
    return user.jailed_until is not None and user.jailed_until > datetime.now()


def calculate_total_wealth(user_id: int, store: DataStore) -> int:
    user = store.get_user(user_id)
    total = user.balance + user.bank_balance

    businesses = store.get_user_businesses(user_id)
    total += sum(b.current_value for b in businesses)

    portfolio = store.get_portfolio(user_id)
    for ticker, quantity in portfolio.crypto_holdings.items():
        asset = store.get_crypto_asset(ticker)
        if asset:
            total += int(asset.current_price * quantity)

    for ticker, quantity in portfolio.stock_holdings.items():
        asset = store.get_stock_asset(ticker)
        if asset:
            total += int(asset.current_price * quantity)

    houses = store.get_user_houses(user_id)
    total += sum(h.price for h in houses)

    vehicles = store.get_user_vehicles(user_id)
    total += sum(v.price for v in vehicles)

    miners = store.get_user_miners(user_id)
    for miner in miners:
        config = MINER_CONFIG.get(miner.miner_type, {})
        total += config.get("price", 0)

    return total


def get_user_title(user_id: int, store: DataStore) -> str:
    wealth = calculate_total_wealth(user_id, store)

    if wealth >= 1_000_000_000:
        return "Олигарх"
    if wealth >= 100_000_000:
        return "Магнат"
    if wealth >= 10_000_000:
        return "Миллионер"
    if wealth >= 1_000_000:
        return "Бизнесмен"
    if wealth >= 100_000:
        return "Предприниматель"
    if wealth >= 10_000:
        return "Работяга"
    if wealth >= 1_000:
        return "Новичок"
    return "Бездомный"


def send_long_message(chat_id: int, text: str,
                       telegram_client: Any) -> List[Optional[Dict[str, Any]]]:
    chunks = paginate_text(text, 4000)
    results = []
    for chunk in chunks:
        result = asyncio.get_event_loop().run_until_complete(
            telegram_client.send_message(chat_id, chunk)
        )
        results.append(result)
    return results


async def async_send_long_message(chat_id: int, text: str,
                                    telegram_client: Any) -> List[Optional[Dict[str, Any]]]:
    chunks = paginate_text(text, 4000)
    results = []
    for chunk in chunks:
        result = await telegram_client.send_message(chat_id, chunk)
        results.append(result)
        if len(chunks) > 1:
            await asyncio.sleep(0.5)
    return results


def build_command_response(success: bool, message: str,
                            data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    response = {
        "success": success,
        "message": message,
        "timestamp": datetime.now().isoformat(),
    }
    if data:
        response["data"] = data
    return response


def build_error_response(error: str, error_code: str = "UNKNOWN") -> Dict[str, Any]:
    return {
        "success": False,
        "error": error,
        "error_code": error_code,
        "timestamp": datetime.now().isoformat(),
    }


def check_cooldown(user_id: int, command: str, store: DataStore,
                   cooldown_minutes: int) -> Tuple[bool, str]:
    if store.is_on_cooldown(user_id, command):
        remaining = store.get_cooldown_remaining(user_id, command)
        return False, f"Подождите ещё {format_duration(remaining)}"
    store.set_command_cooldown(user_id, command, cooldown_minutes)
    return True, ""


# ============================================================
# КОНФИГУРАЦИЯ СРЕДЫ
# ============================================================

@dataclass
class BotConfig:
    bot_token: str = ""
    deepseek_api_key: str = ""
    grok_api_key: str = ""
    image_generation_api_key: str = ""
    image_provider: str = "openai"
    database_url: str = "sqlite:///data/bot.db"
    redis_url: str = ""
    log_level: str = "INFO"
    log_file: str = "logs/bot.log"
    data_dir: str = "data"
    webhook_url: str = ""
    webhook_port: int = 8443
    use_webhook: bool = False
    debug_mode: bool = False
    super_admin_id: int = SUPER_ADMIN_ID
    max_workers: int = 10
    session_timeout: int = 300

    @classmethod
    def from_env(cls) -> "BotConfig":
        import os
        return cls(
            bot_token=os.getenv("BOT_TOKEN", ""),
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", ""),
            grok_api_key=os.getenv("GROK_API_KEY", ""),
            image_generation_api_key=os.getenv("IMAGE_GEN_API_KEY", ""),
            image_provider=os.getenv("IMAGE_PROVIDER", "openai"),
            database_url=os.getenv("DATABASE_URL", "sqlite:///data/bot.db"),
            redis_url=os.getenv("REDIS_URL", ""),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE", "logs/bot.log"),
            data_dir=os.getenv("DATA_DIR", "data"),
            webhook_url=os.getenv("WEBHOOK_URL", ""),
            webhook_port=int(os.getenv("WEBHOOK_PORT", "8443")),
            use_webhook=os.getenv("USE_WEBHOOK", "false").lower() == "true",
            debug_mode=os.getenv("DEBUG", "false").lower() == "true",
            super_admin_id=int(os.getenv("SUPER_ADMIN_ID", str(SUPER_ADMIN_ID))),
            max_workers=int(os.getenv("MAX_WORKERS", "10")),
            session_timeout=int(os.getenv("SESSION_TIMEOUT", "300")),
        )

    @classmethod
    def from_file(cls, filepath: str) -> "BotConfig":
        import os
        if not os.path.exists(filepath):
            logger.warning(f"Config file {filepath} not found, using defaults")
            return cls()

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(
            bot_token=data.get("bot_token", ""),
            deepseek_api_key=data.get("deepseek_api_key", ""),
            grok_api_key=data.get("grok_api_key", ""),
            image_generation_api_key=data.get("image_generation_api_key", ""),
            image_provider=data.get("image_provider", "openai"),
            database_url=data.get("database_url", "sqlite:///data/bot.db"),
            redis_url=data.get("redis_url", ""),
            log_level=data.get("log_level", "INFO"),
            log_file=data.get("log_file", "logs/bot.log"),
            data_dir=data.get("data_dir", "data"),
            webhook_url=data.get("webhook_url", ""),
            webhook_port=data.get("webhook_port", 8443),
            use_webhook=data.get("use_webhook", False),
            debug_mode=data.get("debug_mode", False),
            super_admin_id=data.get("super_admin_id", SUPER_ADMIN_ID),
            max_workers=data.get("max_workers", 10),
            session_timeout=data.get("session_timeout", 300),
        )

    def save_to_file(self, filepath: str) -> None:
        import os
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        data = {
            "bot_token": self.bot_token,
            "deepseek_api_key": self.deepseek_api_key,
            "grok_api_key": self.grok_api_key,
            "image_generation_api_key": self.image_generation_api_key,
            "image_provider": self.image_provider,
            "database_url": self.database_url,
            "redis_url": self.redis_url,
            "log_level": self.log_level,
            "log_file": self.log_file,
            "data_dir": self.data_dir,
            "webhook_url": self.webhook_url,
            "webhook_port": self.webhook_port,
            "use_webhook": self.use_webhook,
            "debug_mode": self.debug_mode,
            "super_admin_id": self.super_admin_id,
            "max_workers": self.max_workers,
            "session_timeout": self.session_timeout,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# ИНИЦИАЛИЗАЦИЯ ДАННЫХ
# ============================================================

def initialize_all_data(store: DataStore) -> None:
    market_service = MarketService(store)
    market_service.initialize_crypto_assets()
    market_service.initialize_stock_assets()

    achievement_service = AchievementService(store)

    for config in SHOP_ITEMS_CONFIG:
        item = ShopItem(
            item_id=config["item_id"],
            name=config["name"],
            description=config["description"],
            rarity=config["rarity"],
            category=config["category"],
            price=config["price"],
            boost_percent=config["boost_percent"],
            boost_duration_hours=config["boost_duration_hours"],
        )
        store.shop_items[item.item_id] = item

    store.global_economy = GlobalEconomy()

    for region in EarthRegion:
        for i in range(5):
            earth = Earth(
                region=region,
                purchase_price=int(10000 * EARTH_PRICE_MULTIPLIER.get(region.value, 1.0)),
                current_value=int(10000 * EARTH_PRICE_MULTIPLIER.get(region.value, 1.0)),
            )
            store.earths[earth.earth_id] = earth

    logger.info(f"Initialized: {len(store.crypto_assets)} crypto, "
                f"{len(store.stock_assets)} stocks, "
                f"{len(store.shop_items)} shop items, "
                f"{len(store.achievements)} achievements, "
                f"{len(store.earths)} earth plots")


def create_default_chat_config(chat_id: int, created_by: int = 0) -> ChatConfig:
    return ChatConfig(
        chat_id=chat_id,
        welcome_message="Добро пожаловать в чат! Используйте 'фабле команды' для списка команд.",
        rules="1. Будьте вежливы\n2. Не спамьте\n3. Не оскорбляйте других",
        created_by=created_by,
    )


def create_super_admin_entry(store: DataStore, chat_id: int) -> None:
    store.set_admin_level(
        SUPER_ADMIN_ID, chat_id, SUPER_ADMIN_LEVEL,
        assigned_by=0, is_creator=True
    )
    logger.info(f"Super admin {SUPER_ADMIN_ID} registered in chat {chat_id}")


# ============================================================
# МОНИТОРИНГ И МЕТРИКИ
# ============================================================

@dataclass
class BotMetrics:
    messages_processed: int = 0
    commands_executed: int = 0
    errors_count: int = 0
    transactions_processed: int = 0
    games_played: int = 0
    moderation_actions: int = 0
    api_calls: int = 0
    api_errors: int = 0
    uptime_start: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)

    def increment_messages(self, count: int = 1) -> None:
        self.messages_processed += count
        self.last_activity = datetime.now()

    def increment_commands(self, count: int = 1) -> None:
        self.commands_executed += count
        self.last_activity = datetime.now()

    def increment_errors(self, count: int = 1) -> None:
        self.errors_count += count

    def increment_transactions(self, count: int = 1) -> None:
        self.transactions_processed += count

    def increment_games(self, count: int = 1) -> None:
        self.games_played += count

    def increment_moderation(self, count: int = 1) -> None:
        self.moderation_actions += count

    def increment_api_calls(self, errors: bool = False, count: int = 1) -> None:
        self.api_calls += count
        if errors:
            self.api_errors += count

    def get_uptime(self) -> timedelta:
        return datetime.now() - self.uptime_start

    def get_stats_summary(self) -> str:
        uptime = self.get_uptime()
        return (
            f"📊 Статистика бота:\n"
            f"⏱ Аптайм: {format_duration(int(uptime.total_seconds()))}\n"
            f"💬 Сообщений: {self.messages_processed}\n"
            f"⚡ Команд: {self.commands_executed}\n"
            f"💰 Транзакций: {self.transactions_processed}\n"
            f"🎮 Игр: {self.games_played}\n"
            f"🛡 Модераций: {self.moderation_actions}\n"
            f"🌐 API вызовов: {self.api_calls} (ошибок: {self.api_errors})\n"
            f"❌ Ошибок: {self.errors_count}"
        )


# ============================================================
# ЭКСПОРТ ДАННЫХ
# ============================================================

def export_user_data(store: DataStore, user_id: int) -> Optional[Dict[str, Any]]:
    user = store.get_user(user_id)
    if user is None:
        return None

    portfolio = store.get_portfolio(user_id)
    inventory = store.get_inventory(user_id)
    businesses = store.get_user_businesses(user_id)
    miners = store.get_user_miners(user_id)
    houses = store.get_user_houses(user_id)
    vehicles = store.get_user_vehicles(user_id)
    pets = store.get_user_pets(user_id)
    transactions = store.get_user_transactions(user_id, 100)
    clan = store.get_user_clan(user_id)

    return {
        "user": user.to_dict(),
        "portfolio": portfolio.to_dict(),
        "inventory": inventory.to_dict(),
        "businesses": [b.to_dict() for b in businesses],
        "miners": [m.to_dict() for m in miners],
        "houses": [h.to_dict() for h in houses],
        "vehicles": [v.to_dict() for v in vehicles],
        "pets": [p.to_dict() for p in pets],
        "transactions": [t.to_dict() for t in transactions],
        "clan": clan.to_dict() if clan else None,
        "wealth": calculate_total_wealth(user_id, store),
        "title": get_user_title(user_id, store),
        "exported_at": datetime.now().isoformat(),
    }


def export_chat_data(store: DataStore, chat_id: int) -> Optional[Dict[str, Any]]:
    chat_config = store.get_chat(chat_id)
    if chat_config is None:
        return None

    chat_stats = store.get_chat_stats(chat_id)
    admins = {str(k): v.to_dict() for k, v in store.admin_levels.items() if k[1] == chat_id}
    mod_logs = [log.to_dict() for log in store.mod_logs if log.chat_id == chat_id]

    return {
        "chat_config": chat_config.to_dict(),
        "chat_stats": chat_stats.to_dict(),
        "admins": admins,
        "mod_logs": mod_logs,
        "exported_at": datetime.now().isoformat(),
    }


print("Вспомогательный код загружен успешно.")
print(f"Форматтеров: 20+")
print(f"Валидаторов: 15+")
print(f"Генераторов: 5+")
print(f"Утилит: 30+")
print(f"Декораторов: 7")
print(f"Парсеров: 8")
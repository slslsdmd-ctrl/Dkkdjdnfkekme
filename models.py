# Часть 1: Модели данных + конфиги + константы
# Модуль: models.py

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from enum import Enum, auto
from datetime import datetime, timedelta
import json
import uuid
import hashlib
import re

# ============================================================
# КОНСТАНТЫ
# ============================================================

DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 500
MIN_PAGE_SIZE = 10

DEFAULT_TIMEOUT_SECONDS = 30
MAX_TIMEOUT_SECONDS = 300
MIN_TIMEOUT_SECONDS = 1

MAX_RETRY_ATTEMPTS = 5
DEFAULT_RETRY_ATTEMPTS = 3
RETRY_BACKOFF_MULTIPLIER = 2.0
INITIAL_RETRY_DELAY_MS = 100
MAX_RETRY_DELAY_MS = 10000

MAX_STRING_LENGTH = 10000
MAX_TEXT_LENGTH = 100000
MAX_ARRAY_SIZE = 1000
MAX_NESTING_DEPTH = 10

VALID_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})
DEFAULT_LOG_LEVEL = "INFO"

BOT_NAME = "фабле"
BOT_ALIASES = frozenset({"фабле", "фабл", "fable", "фэйбл"})

SUPER_ADMIN_ID = 8039111975
SUPER_ADMIN_LEVEL = 10

DEFAULT_STARTING_BALANCE = 100
MIN_BALANCE = 0
MAX_BALANCE = 999_999_999_999

BONUS_COOLDOWN_HOURS = 3
BONUS_AMOUNT_PER_MESSAGE = 10
BONUS_PER_MESSAGE_AFTER = 1

INFLATION_RATE_DEFAULT = 0.02
DEFLATION_RATE_DEFAULT = 0.01
TAX_RATE_DEFAULT = 0.05

BANK_INTEREST_RATE_PER_HOUR = 0.10
MAX_DEPOSIT_AMOUNT = 10_000_000
MIN_DEPOSIT_AMOUNT = 100

MAX_LOAN_AMOUNT = 5_000_000
MIN_LOAN_AMOUNT = 1000
LOAN_INTEREST_RATE = 0.15
LOAN_DEFAULT_DURATION_DAYS = 30

BUSINESS_CREATION_COST = 5000
MAX_BUSINESSES_PER_USER = 25
MAX_BUSINESS_LEVEL = 10
BUSINESS_UPGRADE_COST_MULTIPLIER = 2.5

CRYPTO_UPDATE_INTERVAL_MINUTES = 5
STOCK_UPDATE_INTERVAL_MINUTES = 60
DIVIDEND_INTERVAL_HOURS = 24

CASINO_MIN_BET = 10
CASINO_MAX_BET = 1_000_000
SLOTS_SYMBOLS = frozenset({"🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🎰"})

POKER_MIN_PLAYERS = 2
POKER_MAX_PLAYERS = 6

ROBBERY_SUCCESS_RATE_BANK = 0.15
ROBBERY_SUCCESS_RATE_CASINO = 0.08
ROBBERY_SUCCESS_RATE_PLAYER = 0.25
ROBBERY_JAIL_HOURS = 1
ROBBERY_MAX_LOOT_PERCENT = 0.30

TAX_AUDIT_CHANCE = 0.02
TAX_AUDIT_FINE_PERCENT = 0.15

MAX_WARNS_BEFORE_BAN = 5
WARN_EXPIRATION_DAYS = 30
DEFAULT_MUTE_DURATION_MINUTES = 60
MAX_MUTE_DURATION_MINUTES = 43200

MAX_CLAN_MEMBERS = 50
CLAN_CREATION_COST = 50000
CLAN_WAR_DURATION_HOURS = 24
CLAN_WAR_LOOT_PERCENT = 0.50

MARRIAGE_COST = 5000
DIVORCE_COST = 5000
MARRIAGE_INCOME_BONUS = 0.05

INSURANCE_COST_PERCENT = 0.05
INSURANCE_RETURN_PERCENT = 0.20
INSURANCE_DURATION_DAYS = 30
INSURANCE_MIN_BALANCE = 1000

REPUTATION_VOTE_COOLDOWN_HOURS = 24
REPUTATION_MUTUAL_LIMIT_PER_WEEK = 2
REPUTATION_LOW_THRESHOLD = -10

MAX_PET_LEVEL = 100
PET_EVOLUTION_LEVEL = 50
PET_BREEDING_COOLDOWN_DAYS = 7
PET_MUTATION_CHANCE = 0.01

ACHIEVEMENTS_COUNT = 50
MAX_ACHIEVEMENTS_DISPLAY = 10

MINER_TYPES = 5
MINER_EFFICIENCY_DECAY_WEEKLY = 0.02
MINER_ELECTRICITY_COST_PERCENT = 0.05
MINER_REPAIR_COST_PERCENT = 0.10

ITEM_RARITY_LEVELS = frozenset({"common", "uncommon", "rare", "epic", "legendary", "mythic"})
RARE_ITEM_DROP_CHANCE = 0.05
LEGENDARY_ITEM_DROP_CHANCE = 0.005

TOURNAMENT_MIN_PLAYERS = 4
TOURNAMENT_MAX_PLAYERS = 64
TOURNAMENT_ENTRY_FEE_MIN = 100
TOURNAMENT_PRIZE_POOL_PERCENT = 0.90

EARTH_REGIONS = frozenset({
    "spawn", "business_center", "residential", "elite",
    "industrial", "entertainment", "suburban", "downtown"
})

VEHICLE_TYPES = frozenset({"car", "yacht", "plane", "helicopter"})
HOUSE_TYPES = frozenset({"apartment", "house", "villa", "mansion", "castle"})

STICKER_BLOCK_MODE = frozenset({"none", "specific", "pack", "all"})
GIF_BLOCK_MODE = frozenset({"none", "keyword", "all"})

COMMAND_PREFIX = ""
COMMAND_ALIASES: Dict[str, List[str]] = {
    "баланс": ["баланс", "б", "balance", "bal", "деньги", "счет"],
    "перевод": ["перевод", "плачу", "перевести", "pay", "send"],
    "топ": ["топ", "богачи", "top", "lb", "leaderboard"],
    "работа": ["работа", "работка", "work", "job", "заработать"],
    "бизнес": ["бизнес", "business", "biz", "компания"],
    "крипта": ["крипта", "crypto", "биток", "криптовалюта"],
    "акции": ["акции", "stocks", "stock", "акция", "бирже"],
    "банк": ["банк", "bank", "вклад", "кредит"],
    "казино": ["казино", "casino", "слоты", "покер"],
    "модерация": ["бан", "мут", "кик", "варн", "mod"],
    "клан": ["клан", "clan", "гильдия", "guild"],
    "брак": ["брак", "marry", "свадьба", "жениться"],
}

MAX_CONCURRENT_GAMES_PER_USER = 3
MAX_CONCURRENT_AUCTIONS = 50
AUCTION_DURATION_HOURS_DEFAULT = 24
AUCTION_BID_MIN_INCREMENT = 10

EARTH_PRICE_MULTIPLIER = {
    "spawn": 0.5,
    "residential": 1.0,
    "suburban": 1.5,
    "business_center": 2.0,
    "industrial": 1.8,
    "entertainment": 2.5,
    "downtown": 3.0,
    "elite": 5.0,
}

# ============================================================
# ПЕРЕЧИСЛЕНИЯ (ENUMS)
# ============================================================

class UserRole(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    CREATOR = "creator"

class ModActionType(Enum):
    WARN = "warn"
    MUTE = "mute"
    UNMUTE = "unmute"
    KICK = "kick"
    BAN = "ban"
    UNBAN = "unban"
    CLEAR = "clear"
    LOCK = "lock"
    UNLOCK = "unlock"
    SLOWMODE = "slowmode"
    GLOBAL_BAN = "global_ban"
    GLOBAL_UNBAN = "global_unban"
    BLACKLIST_ADD = "blacklist_add"
    BLACKLIST_REMOVE = "blacklist_remove"

class BusinessStatus(Enum):
    ACTIVE = "active"
    BANKRUPT = "bankrupt"
    SOLD = "sold"
    FROZEN = "frozen"

class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"

class AssetType(Enum):
    STOCK = "stock"
    CRYPTO = "crypto"

class TransactionType(Enum):
    WORK = "work"
    BONUS = "bonus"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    BUSINESS_INCOME = "business_income"
    BUSINESS_UPGRADE = "business_upgrade"
    BUSINESS_PURCHASE = "business_purchase"
    BUSINESS_SALE = "business_sale"
    CRYPTO_BUY = "crypto_buy"
    CRYPTO_SELL = "crypto_sell"
    STOCK_BUY = "stock_buy"
    STOCK_SELL = "stock_sell"
    DIVIDEND = "dividend"
    BANK_DEPOSIT = "bank_deposit"
    BANK_WITHDRAW = "bank_withdraw"
    LOAN_TAKE = "loan_take"
    LOAN_REPAY = "loan_repay"
    CASINO_BET = "casino_bet"
    CASINO_WIN = "casino_win"
    AUCTION_BID = "auction_bid"
    AUCTION_SALE = "auction_sale"
    ROBBERY_LOOT = "robbery_loot"
    ROBBERY_LOSS = "robbery_loss"
    TAX_AUDIT_FINE = "tax_audit_fine"
    HOUSE_PURCHASE = "house_purchase"
    HOUSE_SALE = "house_sale"
    VEHICLE_PURCHASE = "vehicle_purchase"
    VEHICLE_SALE = "vehicle_sale"
    EARTH_PURCHASE = "earth_purchase"
    CLAN_CREATION = "clan_creation"
    CLAN_DEPOSIT = "clan_deposit"
    CLAN_WAR_LOOT = "clan_war_loot"
    MARRIAGE_COST = "marriage_cost"
    DIVORCE_COST = "divorce_cost"
    INSURANCE_PURCHASE = "insurance_purchase"
    INSURANCE_PAYOUT = "insurance_payout"
    ITEM_PURCHASE = "item_purchase"
    ITEM_SALE = "item_sale"
    MINER_PURCHASE = "miner_purchase"
    MINER_SALE = "miner_sale"
    MINER_REPAIR = "miner_repair"
    TOURNAMENT_ENTRY = "tournament_entry"
    TOURNAMENT_PRIZE = "tournament_prize"
    ADMIN_GIFT = "admin_gift"
    ADMIN_SEIZE = "admin_seize"
    SYSTEM_ADJUSTMENT = "system_adjustment"

class GameType(Enum):
    SLOTS = "slots"
    POKER = "poker"
    BLACKJACK = "blackjack"
    DICE = "dice"
    ROULETTE = "roulette"
    COINFLIP = "coinflip"
    DUEL = "duel"
    RUSSIAN_ROULETTE = "russian_roulette"
    LOTTERY = "lottery"
    WHEEL = "wheel"

class AuctionStatus(Enum):
    ACTIVE = "active"
    ENDED = "ended"
    CANCELLED = "cancelled"
    SOLD = "sold"

class ClanWarStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    FINISHED = "finished"
    DECLINED = "declined"

class MarriageStatus(Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"

class InsuranceClaimReason(Enum):
    BUSINESS_BANKRUPTCY = "business_bankruptcy"
    GLOBAL_CRISIS = "global_crisis"
    TAX_AUDIT = "tax_audit"
    LOAN_DEFAULT = "loan_default"

class TournamentStatus(Enum):
    REGISTRATION = "registration"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    CANCELLED = "cancelled"

class TournamentType(Enum):
    SLOTS = "slots"
    POKER = "poker"
    DICE = "dice"
    BUSINESS_RACE = "business_race"
    EARNINGS_RACE = "earnings_race"

class PetRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class PetMood(Enum):
    HAPPY = "happy"
    NEUTRAL = "neutral"
    SAD = "sad"
    HUNGRY = "hungry"
    SICK = "sick"

class EarthRegion(Enum):
    SPAWN = "spawn"
    BUSINESS_CENTER = "business_center"
    RESIDENTIAL = "residential"
    ELITE = "elite"
    INDUSTRIAL = "industrial"
    ENTERTAINMENT = "entertainment"
    SUBURBAN = "suburban"
    DOWNTOWN = "downtown"

class ItemRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"

class ItemCategory(Enum):
    WORK_BOOSTER = "work_booster"
    BUSINESS_BOOSTER = "business_booster"
    CRYPTO_BOOSTER = "crypto_booster"
    STOCK_BOOSTER = "stock_booster"
    CASINO_LUCK = "casino_luck"
    ROBBERY_TOOL = "robbery_tool"
    REPUTATION_BOOST = "reputation_boost"
    PET_FOOD = "pet_food"
    PET_TOY = "pet_toy"
    COSMETIC = "cosmetic"
    INSURANCE_PREMIUM = "insurance_premium"
    COLLECTIBLE = "collectible"

class MinerType(Enum):
    USB = "usb"
    HOME_FARM = "home_farm"
    GARAGE_FARM = "garage_farm"
    INDUSTRIAL = "industrial"
    HOTEL = "hotel"

class ReputationLevel(Enum):
    HATED = "hated"
    DISLIKED = "disliked"
    NEUTRAL = "neutral"
    LIKED = "liked"
    RESPECTED = "respected"
    BELOVED = "beloved"
    LEGENDARY = "legendary"

class AchievementCategory(Enum):
    MONEY = "money"
    BUSINESS = "business"
    CRYPTO = "crypto"
    STOCKS = "stocks"
    CASINO = "casino"
    CRIME = "crime"
    CLAN = "clan"
    SOCIAL = "social"
    SPECIAL = "special"
    MODERATION = "moderation"

class StickerBlockMode(Enum):
    NONE = "none"
    SPECIFIC = "specific"
    PACK = "pack"
    ALL = "all"

class GifBlockMode(Enum):
    NONE = "none"
    KEYWORD = "keyword"
    ALL = "all"

class IIModMode(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"

# ============================================================
# МОДЕЛИ ДАННЫХ (DATACLASSES)
# ============================================================

@dataclass
class User:
    user_id: int
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    balance: int = DEFAULT_STARTING_BALANCE
    bank_balance: int = 0
    loan_amount: int = 0
    loan_due_date: Optional[datetime] = None
    total_messages: int = 0
    last_bonus_time: Optional[datetime] = None
    experience: int = 0
    level: int = 1
    prestige: int = 0
    reputation_score: int = 0
    karma: int = 0
    marriage_status: MarriageStatus = MarriageStatus.SINGLE
    spouse_id: Optional[int] = None
    joint_balance_enabled: bool = False
    active_title: str = ""
    active_frame: str = ""
    active_color: str = ""
    jailed_until: Optional[datetime] = None
    insurance_active: bool = False
    insurance_expires: Optional[datetime] = None
    achievements: Set[int] = field(default_factory=set)
    last_seen: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    is_bot_blocked: bool = False
    global_blacklisted: bool = False
    toxicity_score: float = 0.0
    last_vote_times: Dict[int, datetime] = field(default_factory=dict)
    mutual_vote_counts: Dict[int, int] = field(default_factory=dict)
    muted_until: Optional[datetime] = None
    shadow_banned: bool = False
    watched_by_admin: bool = False
    trial_until: Optional[datetime] = None
    days_without_violation: int = 0
    
    # ========== НОВЫЕ ПОЛЯ ==========
    health: int = 100
    hunger: int = 100
    fuel: int = 100
    bonus_streak: int = 0
    last_bonus_date: Optional[datetime] = None
    quests: Dict[str, int] = field(default_factory=dict)
    daily_quests_done: bool = False
    total_work: int = 0
    total_casino_win: int = 0
    total_casino_lose: int = 0
    chat_activity: Dict[int, int] = field(default_factory=dict)
    house_id: Optional[str] = None
    loan_blocked: bool = False
    work_blocked: bool = False
    blacklist_reason: str = ""
    blacklist_date: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["achievements"] = list(self.achievements)
        data["last_bonus_time"] = self.last_bonus_time.isoformat() if self.last_bonus_time else None
        data["loan_due_date"] = self.loan_due_date.isoformat() if self.loan_due_date else None
        data["jailed_until"] = self.jailed_until.isoformat() if self.jailed_until else None
        data["insurance_expires"] = self.insurance_expires.isoformat() if self.insurance_expires else None
        data["last_seen"] = self.last_seen.isoformat()
        data["created_at"] = self.created_at.isoformat()
        data["muted_until"] = self.muted_until.isoformat() if self.muted_until else None
        data["trial_until"] = self.trial_until.isoformat() if self.trial_until else None
        data["last_vote_times"] = {str(k): v.isoformat() for k, v in self.last_vote_times.items()}
        data["mutual_vote_counts"] = {str(k): v for k, v in self.mutual_vote_counts.items()}
        data["marriage_status"] = self.marriage_status.value
        data["quests"] = self.quests
        data["chat_activity"] = self.chat_activity
        data["last_bonus_date"] = self.last_bonus_date.isoformat() if self.last_bonus_date else None
        data["blacklist_date"] = self.blacklist_date.isoformat() if self.blacklist_date else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        data["achievements"] = set(data.get("achievements", []))
        data["last_bonus_time"] = datetime.fromisoformat(data["last_bonus_time"]) if data.get("last_bonus_time") else None
        data["loan_due_date"] = datetime.fromisoformat(data["loan_due_date"]) if data.get("loan_due_date") else None
        data["jailed_until"] = datetime.fromisoformat(data["jailed_until"]) if data.get("jailed_until") else None
        data["insurance_expires"] = datetime.fromisoformat(data["insurance_expires"]) if data.get("insurance_expires") else None
        data["last_seen"] = datetime.fromisoformat(data["last_seen"]) if isinstance(data.get("last_seen"), str) else data.get("last_seen", datetime.now())
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["muted_until"] = datetime.fromisoformat(data["muted_until"]) if data.get("muted_until") else None
        data["trial_until"] = datetime.fromisoformat(data["trial_until"]) if data.get("trial_until") else None
        data["last_vote_times"] = {int(k): datetime.fromisoformat(v) for k, v in data.get("last_vote_times", {}).items()}
        data["mutual_vote_counts"] = {int(k): v for k, v in data.get("mutual_vote_counts", {}).items()}
        data["marriage_status"] = MarriageStatus(data.get("marriage_status", "single"))
        data["quests"] = data.get("quests", {})
        data["chat_activity"] = data.get("chat_activity", {})
        data["last_bonus_date"] = datetime.fromisoformat(data["last_bonus_date"]) if data.get("last_bonus_date") else None
        data["blacklist_date"] = datetime.fromisoformat(data["blacklist_date"]) if data.get("blacklist_date") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# (Остальные модели - ChatConfig, AdminLevel, ModLog, Business, CryptoAsset, StockAsset, UserPortfolio, Miner, Auction, Clan, ClanWar, Tournament, Pet, ShopItem, UserInventory, Achievement, Transaction, GameSession, Report, GlobalEconomy, Earth, Vehicle, House, Insurance, BlacklistEntry, ChatStats, WorldEvent и все конфиги остаются без изменений)
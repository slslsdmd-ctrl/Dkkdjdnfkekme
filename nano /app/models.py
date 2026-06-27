# ============================================================
# ПОЛНЫЙ ФАЙЛ: models.py
# ВСЕ МОДЕЛИ ДЛЯ БОТА
# ============================================================

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
EARTH_REGIONS = frozenset({"spawn", "business_center", "residential", "elite", "industrial", "entertainment", "suburban", "downtown"})
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
EARTH_PRICE_MULTIPLIER = {"spawn": 0.5, "residential": 1.0, "suburban": 1.5, "business_center": 2.0, "industrial": 1.8, "entertainment": 2.5, "downtown": 3.0, "elite": 5.0}

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
# МОДЕЛЬ USER
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
    health: int = 100
    stress: int = 0
    is_sick: bool = False
    sick_until: Optional[datetime] = None
    has_ip: bool = False
    ip_name: str = ""
    ip_date: Optional[datetime] = None
    car_id: Optional[str] = None
    car_fuel: int = 100
    car_insurance: bool = False
    car_fines: int = 0
    house_id: Optional[str] = None
    house_utilities: int = 0
    house_tax: int = 0
    job_title: str = ""
    job_experience: int = 0
    job_salary: int = 0
    is_employed: bool = False
    has_insurance: bool = False
    health_issues: List[str] = field(default_factory=list)
    last_doctor_visit: Optional[datetime] = None
    credit_history: float = 1.0
    loan_blocked: bool = False
    work_blocked: bool = False
    tax_debt: int = 0
    tax_history: List[Dict] = field(default_factory=list)
    quests: Dict[str, int] = field(default_factory=dict)
    bonus_streak: int = 0
    last_bonus_date: Optional[datetime] = None
    daily_quests_done: bool = False
    total_work: int = 0
    total_casino_win: int = 0
    total_casino_lose: int = 0
    chat_activity: Dict[int, int] = field(default_factory=dict)
    blacklist_reason: str = ""
    blacklist_date: Optional[datetime] = None
    genes: Dict[str, float] = field(default_factory=dict)
    mutations: List[str] = field(default_factory=list)
    evolution_level: int = 0
    evolution_path: str = "Человек"
    survived_disasters: List[str] = field(default_factory=list)
    disaster_protection: bool = False

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
        data["sick_until"] = self.sick_until.isoformat() if self.sick_until else None
        data["ip_date"] = self.ip_date.isoformat() if self.ip_date else None
        data["tax_history"] = self.tax_history
        data["last_doctor_visit"] = self.last_doctor_visit.isoformat() if self.last_doctor_visit else None
        data["health_issues"] = self.health_issues
        data["genes"] = self.genes
        data["mutations"] = self.mutations
        data["survived_disasters"] = self.survived_disasters
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
        data["sick_until"] = datetime.fromisoformat(data["sick_until"]) if data.get("sick_until") else None
        data["ip_date"] = datetime.fromisoformat(data["ip_date"]) if data.get("ip_date") else None
        data["tax_history"] = data.get("tax_history", [])
        data["last_doctor_visit"] = datetime.fromisoformat(data["last_doctor_visit"]) if data.get("last_doctor_visit") else None
        data["health_issues"] = data.get("health_issues", [])
        data["genes"] = data.get("genes", {})
        data["mutations"] = data.get("mutations", [])
        data["survived_disasters"] = data.get("survived_disasters", [])
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ CHATCONFIG
# ============================================================

@dataclass
class ChatConfig:
    chat_id: int
    chat_title: str = ""
    welcome_message: str = ""
    farewell_message: str = ""
    rules: str = ""
    slowmode_seconds: int = 0
    is_locked: bool = False
    antispam_enabled: bool = True
    antiflood_enabled: bool = True
    antiraid_enabled: bool = False
    antilink_enabled: bool = False
    antibot_enabled: bool = False
    antimat_enabled: bool = True
    ii_moderation_enabled: bool = False
    sticker_block_mode: StickerBlockMode = StickerBlockMode.NONE
    blocked_stickers: Set[str] = field(default_factory=set)
    blocked_sticker_packs: Set[str] = field(default_factory=set)
    gif_block_mode: GifBlockMode = GifBlockMode.NONE
    blocked_gif_keywords: Set[str] = field(default_factory=set)
    filter_words: Set[str] = field(default_factory=set)
    whitelist_words: Set[str] = field(default_factory=set)
    auto_warn_triggers: Dict[str, int] = field(default_factory=dict)
    warn_limit: int = MAX_WARNS_BEFORE_BAN
    warn_expiration_days: int = WARN_EXPIRATION_DAYS
    night_mode_enabled: bool = False
    night_mode_start: int = 2
    night_mode_end: int = 6
    log_channel_id: Optional[int] = None
    admin_only_commands: bool = False
    created_by: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    auto_delete_after_minutes: int = 0
    auto_cleanup_time: Optional[str] = None
    flood_welcome_only: bool = False
    flood_channel_id: Optional[int] = None
    flood_open_hour: int = 18
    flood_close_hour: int = 22

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["blocked_stickers"] = list(self.blocked_stickers)
        data["blocked_sticker_packs"] = list(self.blocked_sticker_packs)
        data["blocked_gif_keywords"] = list(self.blocked_gif_keywords)
        data["filter_words"] = list(self.filter_words)
        data["whitelist_words"] = list(self.whitelist_words)
        data["auto_warn_triggers"] = self.auto_warn_triggers
        data["sticker_block_mode"] = self.sticker_block_mode.value
        data["gif_block_mode"] = self.gif_block_mode.value
        data["created_at"] = self.created_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatConfig":
        data["blocked_stickers"] = set(data.get("blocked_stickers", []))
        data["blocked_sticker_packs"] = set(data.get("blocked_sticker_packs", []))
        data["blocked_gif_keywords"] = set(data.get("blocked_gif_keywords", []))
        data["filter_words"] = set(data.get("filter_words", []))
        data["whitelist_words"] = set(data.get("whitelist_words", []))
        data["auto_warn_triggers"] = data.get("auto_warn_triggers", {})
        data["sticker_block_mode"] = StickerBlockMode(data.get("sticker_block_mode", "none"))
        data["gif_block_mode"] = GifBlockMode(data.get("gif_block_mode", "none"))
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ ADMINLEVEL
# ============================================================

@dataclass
class AdminLevel:
    user_id: int
    chat_id: int
    level: int = 0
    assigned_by: int = 0
    assigned_at: datetime = field(default_factory=datetime.now)
    is_creator: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["assigned_at"] = self.assigned_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdminLevel":
        data["assigned_at"] = datetime.fromisoformat(data["assigned_at"]) if isinstance(data.get("assigned_at"), str) else data.get("assigned_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ MODLOG
# ============================================================

@dataclass
class ModLog:
    log_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    chat_id: int = 0
    moderator_id: int = 0
    target_id: int = 0
    action: ModActionType = ModActionType.WARN
    reason: str = ""
    comment: str = ""
    duration_minutes: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    is_active: bool = True
    removed_by: Optional[int] = None
    removed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["action"] = self.action.value
        data["timestamp"] = self.timestamp.isoformat()
        data["expires_at"] = self.expires_at.isoformat() if self.expires_at else None
        data["removed_at"] = self.removed_at.isoformat() if self.removed_at else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModLog":
        data["action"] = ModActionType(data["action"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"]) if isinstance(data.get("timestamp"), str) else data.get("timestamp", datetime.now())
        data["expires_at"] = datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None
        data["removed_at"] = datetime.fromisoformat(data["removed_at"]) if data.get("removed_at") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ BUSINESS
# ============================================================

@dataclass
class Business:
    business_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0
    name: str = ""
    business_type: str = ""
    level: int = 1
    status: BusinessStatus = BusinessStatus.ACTIVE
    purchase_price: int = 0
    current_value: int = 0
    hourly_income: int = 0
    employees: List[int] = field(default_factory=list)
    max_employees: int = 5
    salary_per_employee: int = 100
    franchise_available: bool = False
    franchise_cost: int = 0
    sabotage_protection: bool = False
    bankrupt_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_collected: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat()
        data["last_collected"] = self.last_collected.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Business":
        data["status"] = BusinessStatus(data.get("status", "active"))
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["last_collected"] = datetime.fromisoformat(data["last_collected"]) if isinstance(data.get("last_collected"), str) else data.get("last_collected", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛИ CRYPTOASSET, STOCKASSET, USERPORTFOLIO
# ============================================================

@dataclass
class CryptoAsset:
    ticker: str
    name: str
    current_price: float
    previous_price: float = 0.0
    change_percent: float = 0.0
    all_time_high: float = 0.0
    all_time_low: float = 0.0
    volume_24h: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["last_updated"] = self.last_updated.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CryptoAsset":
        data["last_updated"] = datetime.fromisoformat(data["last_updated"]) if isinstance(data.get("last_updated"), str) else data.get("last_updated", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class StockAsset:
    ticker: str
    company_name: str
    current_price: float
    previous_price: float = 0.0
    change_percent: float = 0.0
    dividend_yield: float = 0.01
    sector: str = ""
    market_cap: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["last_updated"] = self.last_updated.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StockAsset":
        data["last_updated"] = datetime.fromisoformat(data["last_updated"]) if isinstance(data.get("last_updated"), str) else data.get("last_updated", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class UserPortfolio:
    user_id: int
    crypto_holdings: Dict[str, float] = field(default_factory=dict)
    stock_holdings: Dict[str, int] = field(default_factory=dict)
    total_invested_crypto: int = 0
    total_invested_stocks: int = 0
    total_profit_loss: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserPortfolio":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ MINER
# ============================================================

@dataclass
class Miner:
    miner_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0
    miner_type: MinerType = MinerType.USB
    efficiency: float = 1.0
    hours_mined: int = 0
    total_mined_value: int = 0
    last_repair: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["miner_type"] = self.miner_type.value
        data["last_repair"] = self.last_repair.isoformat()
        data["created_at"] = self.created_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Miner":
        data["miner_type"] = MinerType(data.get("miner_type", "usb"))
        data["last_repair"] = datetime.fromisoformat(data["last_repair"]) if isinstance(data.get("last_repair"), str) else data.get("last_repair", datetime.now())
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ AUCTION
# ============================================================

@dataclass
class Auction:
    auction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    seller_id: int = 0
    item_type: str = ""
    item_name: str = ""
    item_data: Dict[str, Any] = field(default_factory=dict)
    starting_price: int = 0
    current_bid: int = 0
    current_bidder_id: int = 0
    min_increment: int = AUCTION_BID_MIN_INCREMENT
    status: AuctionStatus = AuctionStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    ends_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=AUCTION_DURATION_HOURS_DEFAULT))
    bids_history: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat()
        data["ends_at"] = self.ends_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Auction":
        data["status"] = AuctionStatus(data.get("status", "active"))
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["ends_at"] = datetime.fromisoformat(data["ends_at"]) if isinstance(data.get("ends_at"), str) else data.get("ends_at", datetime.now() + timedelta(hours=AUCTION_DURATION_HOURS_DEFAULT))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ CLAN
# ============================================================

@dataclass
class Clan:
    clan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    leader_id: int = 0
    vice_leader_id: int = 0
    members: List[int] = field(default_factory=list)
    veteran_ids: List[int] = field(default_factory=list)
    treasury: int = 0
    logo_emoji: str = "🏰"
    wars_won: int = 0
    wars_lost: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    war_debuff_until: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["war_debuff_until"] = self.war_debuff_until.isoformat() if self.war_debuff_until else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Clan":
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["war_debuff_until"] = datetime.fromisoformat(data["war_debuff_until"]) if data.get("war_debuff_until") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ CLANWAR
# ============================================================

@dataclass
class ClanWar:
    war_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    attacker_clan_id: str = ""
    defender_clan_id: str = ""
    attacker_score: int = 0
    defender_score: int = 0
    status: ClanWarStatus = ClanWarStatus.PENDING
    started_at: datetime = field(default_factory=datetime.now)
    ends_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=CLAN_WAR_DURATION_HOURS))
    winner_id: str = ""
    loot_amount: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["started_at"] = self.started_at.isoformat()
        data["ends_at"] = self.ends_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClanWar":
        data["status"] = ClanWarStatus(data.get("status", "pending"))
        data["started_at"] = datetime.fromisoformat(data["started_at"]) if isinstance(data.get("started_at"), str) else data.get("started_at", datetime.now())
        data["ends_at"] = datetime.fromisoformat(data["ends_at"]) if isinstance(data.get("ends_at"), str) else data.get("ends_at", datetime.now() + timedelta(hours=CLAN_WAR_DURATION_HOURS))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ TOURNAMENT
# ============================================================

@dataclass
class Tournament:
    tournament_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    tournament_type: TournamentType = TournamentType.POKER
    entry_fee: int = 0
    prize_pool: int = 0
    max_players: int = 32
    registered_players: List[int] = field(default_factory=list)
    status: TournamentStatus = TournamentStatus.REGISTRATION
    winner_id: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    starts_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=1))

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["tournament_type"] = self.tournament_type.value
        data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat()
        data["starts_at"] = self.starts_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tournament":
        data["tournament_type"] = TournamentType(data.get("tournament_type", "poker"))
        data["status"] = TournamentStatus(data.get("status", "registration"))
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["starts_at"] = datetime.fromisoformat(data["starts_at"]) if isinstance(data.get("starts_at"), str) else data.get("starts_at", datetime.now() + timedelta(hours=1))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ PET
# ============================================================

@dataclass
class Pet:
    pet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0
    name: str = ""
    species: str = ""
    rarity: PetRarity = PetRarity.COMMON
    level: int = 1
    experience: int = 0
    mood: PetMood = PetMood.NEUTRAL
    health: int = 100
    hunger: int = 0
    color: str = "default"
    mutation: str = ""
    generation: int = 1
    parents: List[str] = field(default_factory=list)
    last_fed: datetime = field(default_factory=datetime.now)
    last_played: datetime = field(default_factory=datetime.now)
    breeding_cooldown_until: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["rarity"] = self.rarity.value
        data["mood"] = self.mood.value
        data["last_fed"] = self.last_fed.isoformat()
        data["last_played"] = self.last_played.isoformat()
        data["breeding_cooldown_until"] = self.breeding_cooldown_until.isoformat() if self.breeding_cooldown_until else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pet":
        data["rarity"] = PetRarity(data.get("rarity", "common"))
        data["mood"] = PetMood(data.get("mood", "neutral"))
        data["last_fed"] = datetime.fromisoformat(data["last_fed"]) if isinstance(data.get("last_fed"), str) else data.get("last_fed", datetime.now())
        data["last_played"] = datetime.fromisoformat(data["last_played"]) if isinstance(data.get("last_played"), str) else data.get("last_played", datetime.now())
        data["breeding_cooldown_until"] = datetime.fromisoformat(data["breeding_cooldown_until"]) if data.get("breeding_cooldown_until") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ SHOPITEM
# ============================================================

@dataclass
class ShopItem:
    item_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    rarity: ItemRarity = ItemRarity.COMMON
    category: ItemCategory = ItemCategory.WORK_BOOSTER
    price: int = 0
    boost_percent: float = 0.0
    boost_duration_hours: int = 24
    stock: int = -1
    season_exclusive: bool = False
    min_level_required: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["rarity"] = self.rarity.value
        data["category"] = self.category.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ShopItem":
        data["rarity"] = ItemRarity(data.get("rarity", "common"))
        data["category"] = ItemCategory(data.get("category", "work_booster"))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ USERINVENTORY
# ============================================================

@dataclass
class UserInventory:
    user_id: int
    items: Dict[str, int] = field(default_factory=dict)
    active_boosters: Dict[str, datetime] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["active_boosters"] = {k: v.isoformat() for k, v in self.active_boosters.items()}
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserInventory":
        data["active_boosters"] = {k: datetime.fromisoformat(v) for k, v in data.get("active_boosters", {}).items()}
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ ACHIEVEMENT
# ============================================================

@dataclass
class Achievement:
    achievement_id: int
    name: str
    description: str
    category: AchievementCategory
    reward: int = 0
    hidden: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["category"] = self.category.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Achievement":
        data["category"] = AchievementCategory(data["category"])
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ TRANSACTION
# ============================================================

@dataclass
class Transaction:
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int = 0
    amount: int = 0
    transaction_type: TransactionType = TransactionType.WORK
    balance_after: int = 0
    description: str = ""
    related_user_id: Optional[int] = None
    related_item_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["transaction_type"] = self.transaction_type.value
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        data["transaction_type"] = TransactionType(data["transaction_type"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"]) if isinstance(data.get("timestamp"), str) else data.get("timestamp", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ GAMESESSION
# ============================================================

@dataclass
class GameSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    game_type: GameType = GameType.SLOTS
    user_id: int = 0
    bet_amount: int = 0
    result: Dict[str, Any] = field(default_factory=dict)
    win_amount: int = 0
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["game_type"] = self.game_type.value
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameSession":
        data["game_type"] = GameType(data["game_type"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"]) if isinstance(data.get("timestamp"), str) else data.get("timestamp", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ REPORT
# ============================================================

@dataclass
class Report:
    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reporter_id: int = 0
    target_id: int = 0
    chat_id: int = 0
    reason: str = ""
    status: str = "pending"
    handled_by: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Report":
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ GLOBALECONOMY
# ============================================================

@dataclass
class GlobalEconomy:
    inflation_rate: float = INFLATION_RATE_DEFAULT
    deflation_rate: float = DEFLATION_RATE_DEFAULT
    tax_rate: float = TAX_RATE_DEFAULT
    crisis_active: bool = False
    boom_active: bool = False
    last_crisis: Optional[datetime] = None
    last_boom: Optional[datetime] = None
    total_money_in_circulation: int = 0
    total_users: int = 0
    total_businesses: int = 0
    gdp_bot: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["last_crisis"] = self.last_crisis.isoformat() if self.last_crisis else None
        data["last_boom"] = self.last_boom.isoformat() if self.last_boom else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GlobalEconomy":
        data["last_crisis"] = datetime.fromisoformat(data["last_crisis"]) if data.get("last_crisis") else None
        data["last_boom"] = datetime.fromisoformat(data["last_boom"]) if data.get("last_boom") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ EARTH
# ============================================================

@dataclass
class Earth:
    earth_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    region: EarthRegion = EarthRegion.SPAWN
    owner_id: int = 0
    purchase_price: int = 0
    current_value: int = 0
    built_business_id: Optional[str] = None
    for_sale: bool = False
    sale_price: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["region"] = self.region.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Earth":
        data["region"] = EarthRegion(data.get("region", "spawn"))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ VEHICLE
# ============================================================

@dataclass
class Vehicle:
    vehicle_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0
    vehicle_type: str = "car"
    name: str = ""
    price: int = 0
    speed_bonus: float = 1.0
    income_bonus: float = 0.0
    for_sale: bool = False
    sale_price: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vehicle":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ HOUSE
# ============================================================

@dataclass
class House:
    house_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0
    house_type: str = "apartment"
    name: str = ""
    price: int = 0
    rooms: int = 1
    income_bonus: float = 0.0
    rentable: bool = False
    rent_price: int = 0
    tenant_id: Optional[int] = None
    for_sale: bool = False
    sale_price: int = 0
    mortgage_active: bool = False
    mortgage_amount: int = 0
    mortgage_due_date: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["mortgage_due_date"] = self.mortgage_due_date.isoformat() if self.mortgage_due_date else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "House":
        data["mortgage_due_date"] = datetime.fromisoformat(data["mortgage_due_date"]) if data.get("mortgage_due_date") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ INSURANCE
# ============================================================

@dataclass
class Insurance:
    insurance_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int = 0
    coverage_amount: int = 0
    premium_paid: int = 0
    active: bool = True
    purchased_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=INSURANCE_DURATION_DAYS))
    claims: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["purchased_at"] = self.purchased_at.isoformat()
        data["expires_at"] = self.expires_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Insurance":
        data["purchased_at"] = datetime.fromisoformat(data["purchased_at"]) if isinstance(data.get("purchased_at"), str) else data.get("purchased_at", datetime.now())
        data["expires_at"] = datetime.fromisoformat(data["expires_at"]) if isinstance(data.get("expires_at"), str) else data.get("expires_at", datetime.now() + timedelta(days=INSURANCE_DURATION_DAYS))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ BLACKLISTENTRY
# ============================================================

@dataclass
class BlacklistEntry:
    user_id: int
    reason: str = ""
    added_by: int = 0
    added_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["added_at"] = self.added_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlacklistEntry":
        data["added_at"] = datetime.fromisoformat(data["added_at"]) if isinstance(data.get("added_at"), str) else data.get("added_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ CHATSTATS
# ============================================================

@dataclass
class ChatStats:
    chat_id: int
    total_messages: int = 0
    total_users: int = 0
    active_users_today: int = 0
    messages_today: int = 0
    bans_today: int = 0
    mutes_today: int = 0
    kicks_today: int = 0
    warns_today: int = 0
    economy_activity_today: int = 0
    casino_activity_today: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["last_updated"] = self.last_updated.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatStats":
        data["last_updated"] = datetime.fromisoformat(data["last_updated"]) if isinstance(data.get("last_updated"), str) else data.get("last_updated", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# МОДЕЛЬ WORLDEVENT
# ============================================================

@dataclass
class WorldEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    affect_stocks: bool = False
    affect_crypto: bool = False
    affect_business: bool = False
    stock_impact_percent: float = 0.0
    crypto_impact_percent: float = 0.0
    business_impact_percent: float = 0.0
    duration_hours: int = 2
    active: bool = False
    started_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["started_at"] = self.started_at.isoformat() if self.started_at else None
        data["ends_at"] = self.ends_at.isoformat() if self.ends_at else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorldEvent":
        data["started_at"] = datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None
        data["ends_at"] = datetime.fromisoformat(data["ends_at"]) if data.get("ends_at") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def generate_id() -> str:
    return str(uuid.uuid4())

def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def validate_amount(amount: int, min_amount: int = 0, max_amount: int = MAX_BALANCE) -> Tuple[bool, str]:
    if not isinstance(amount, int):
        return False, "Сумма должна быть целым числом"
    if amount < min_amount:
        return False, f"Сумма не может быть меньше {min_amount}"
    if amount > max_amount:
        return False, f"Сумма не может быть больше {max_amount}"
    return True, ""

def validate_string_length(text: str, max_length: int = MAX_STRING_LENGTH) -> Tuple[bool, str]:
    if not isinstance(text, str):
        return False, "Текст должен быть строкой"
    if len(text) > max_length:
        return False, f"Длина текста не должна превышать {max_length} символов"
    return True, ""

def validate_duration_minutes(minutes: int) -> Tuple[bool, str]:
    if not isinstance(minutes, int):
        return False, "Длительность должна быть целым числом"
    if minutes < 1:
        return False, "Длительность не может быть меньше 1 минуты"
    if minutes > MAX_MUTE_DURATION_MINUTES:
        return False, f"Длительность не может быть больше {MAX_MUTE_DURATION_MINUTES} минут"
    return True, ""

def parse_duration(duration_str: str) -> Optional[int]:
    duration_str = duration_str.lower().strip()
    patterns = [
        (r"^(\d+)\s*м$", 1), (r"^(\d+)\s*мин$", 1), (r"^(\d+)\s*min$", 1),
        (r"^(\d+)\s*ч$", 60), (r"^(\d+)\s*час$", 60), (r"^(\d+)\s*h$", 60),
        (r"^(\d+)\s*д$", 1440), (r"^(\d+)\s*день$", 1440), (r"^(\d+)\s*дня$", 1440),
        (r"^(\d+)\s*дней$", 1440), (r"^(\d+)\s*d$", 1440),
        (r"^(\d+)\s*н$", 10080), (r"^(\d+)\s*нед$", 10080),
        (r"^(\d+)\s*неделя$", 10080), (r"^(\d+)\s*недели$", 10080),
        (r"^(\d+)\s*недель$", 10080), (r"^(\d+)\s*w$", 10080),
    ]
    for pattern, multiplier in patterns:
        match = re.match(pattern, duration_str)
        if match:
            value = int(match.group(1))
            result = value * multiplier
            if result > MAX_MUTE_DURATION_MINUTES:
                return MAX_MUTE_DURATION_MINUTES
            return result
    try:
        return int(duration_str)
    except ValueError:
        return None

def get_reputation_level(score: int) -> ReputationLevel:
    for level, data in REPUTATION_LEVELS.items():
        if data["min_score"] <= score <= data["max_score"]:
            return level
    return ReputationLevel.NEUTRAL

def calculate_business_income(business: Business) -> int:
    base_income = business.hourly_income
    employee_bonus = len(business.employees) * business.salary_per_employee * 0.1
    level_bonus = base_income * (business.level - 1) * 0.2
    total = int(base_income + employee_bonus + level_bonus)
    return max(total, base_income)

def calculate_miner_income(miner: Miner) -> int:
    config = MINER_CONFIG[miner.miner_type]
    base = config["base_income_per_hour"]
    efficiency = miner.efficiency
    electricity = base * MINER_ELECTRICITY_COST_PERCENT
    total = int((base * efficiency) - electricity)
    return max(total, 0)

def is_super_admin(user_id: int) -> bool:
    return user_id == SUPER_ADMIN_ID

def get_permissions_for_level(level: int) -> List[str]:
    if level <= 0:
        return []
    perms = set()
    for lvl in range(1, min(level, 10) + 1):
        perms.update(ADMIN_PERMISSIONS.get(lvl, []))
    return sorted(list(perms))

def has_permission(admin_level: int, required_permission: str) -> bool:
    if admin_level == SUPER_ADMIN_LEVEL:
        return True
    perms = get_permissions_for_level(admin_level)
    return required_permission in perms or "all" in perms or "all_chat_perms" in perms

print("✅ models.py загружен (ПОЛНАЯ ВЕРСИЯ!)")
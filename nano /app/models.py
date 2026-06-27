# ============================================================
# МОДЕЛИ ДАННЫХ (ПОЛНАЯ ВЕРСИЯ)
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
    "spawn": 0.5, "residential": 1.0, "suburban": 1.5,
    "business_center": 2.0, "industrial": 1.8,
    "entertainment": 2.5, "downtown": 3.0, "elite": 5.0,
}


# ============================================================
# ПЕРЕЧИСЛЕНИЯ
# ============================================================

class UserRole(Enum):
    USER = "user"; MODERATOR = "moderator"; ADMIN = "admin"
    SUPER_ADMIN = "super_admin"; CREATOR = "creator"

class ModActionType(Enum):
    WARN = "warn"; MUTE = "mute"; UNMUTE = "unmute"; KICK = "kick"
    BAN = "ban"; UNBAN = "unban"; CLEAR = "clear"; LOCK = "lock"
    UNLOCK = "unlock"; SLOWMODE = "slowmode"; GLOBAL_BAN = "global_ban"
    GLOBAL_UNBAN = "global_unban"; BLACKLIST_ADD = "blacklist_add"
    BLACKLIST_REMOVE = "blacklist_remove"

class BusinessStatus(Enum):
    ACTIVE = "active"; BANKRUPT = "bankrupt"; SOLD = "sold"; FROZEN = "frozen"

class OrderType(Enum):
    BUY = "buy"; SELL = "sell"

class AssetType(Enum):
    STOCK = "stock"; CRYPTO = "crypto"

class TransactionType(Enum):
    WORK = "work"; BONUS = "bonus"; TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"; BUSINESS_INCOME = "business_income"
    BUSINESS_UPGRADE = "business_upgrade"; BUSINESS_PURCHASE = "business_purchase"
    BUSINESS_SALE = "business_sale"; CRYPTO_BUY = "crypto_buy"
    CRYPTO_SELL = "crypto_sell"; STOCK_BUY = "stock_buy"
    STOCK_SELL = "stock_sell"; DIVIDEND = "dividend"
    BANK_DEPOSIT = "bank_deposit"; BANK_WITHDRAW = "bank_withdraw"
    LOAN_TAKE = "loan_take"; LOAN_REPAY = "loan_repay"
    CASINO_BET = "casino_bet"; CASINO_WIN = "casino_win"
    AUCTION_BID = "auction_bid"; AUCTION_SALE = "auction_sale"
    ROBBERY_LOOT = "robbery_loot"; ROBBERY_LOSS = "robbery_loss"
    TAX_AUDIT_FINE = "tax_audit_fine"; HOUSE_PURCHASE = "house_purchase"
    HOUSE_SALE = "house_sale"; VEHICLE_PURCHASE = "vehicle_purchase"
    VEHICLE_SALE = "vehicle_sale"; EARTH_PURCHASE = "earth_purchase"
    CLAN_CREATION = "clan_creation"; CLAN_DEPOSIT = "clan_deposit"
    CLAN_WAR_LOOT = "clan_war_loot"; MARRIAGE_COST = "marriage_cost"
    DIVORCE_COST = "divorce_cost"; INSURANCE_PURCHASE = "insurance_purchase"
    INSURANCE_PAYOUT = "insurance_payout"; ITEM_PURCHASE = "item_purchase"
    ITEM_SALE = "item_sale"; MINER_PURCHASE = "miner_purchase"
    MINER_SALE = "miner_sale"; MINER_REPAIR = "miner_repair"
    TOURNAMENT_ENTRY = "tournament_entry"; TOURNAMENT_PRIZE = "tournament_prize"
    ADMIN_GIFT = "admin_gift"; ADMIN_SEIZE = "admin_seize"
    SYSTEM_ADJUSTMENT = "system_adjustment"

class GameType(Enum):
    SLOTS = "slots"; POKER = "poker"; BLACKJACK = "blackjack"
    DICE = "dice"; ROULETTE = "roulette"; COINFLIP = "coinflip"
    DUEL = "duel"; RUSSIAN_ROULETTE = "russian_roulette"
    LOTTERY = "lottery"; WHEEL = "wheel"

class AuctionStatus(Enum):
    ACTIVE = "active"; ENDED = "ended"; CANCELLED = "cancelled"; SOLD = "sold"

class ClanWarStatus(Enum):
    PENDING = "pending"; ACTIVE = "active"; FINISHED = "finished"; DECLINED = "declined"

class MarriageStatus(Enum):
    SINGLE = "single"; MARRIED = "married"; DIVORCED = "divorced"

class InsuranceClaimReason(Enum):
    BUSINESS_BANKRUPTCY = "business_bankruptcy"; GLOBAL_CRISIS = "global_crisis"
    TAX_AUDIT = "tax_audit"; LOAN_DEFAULT = "loan_default"

class TournamentStatus(Enum):
    REGISTRATION = "registration"; IN_PROGRESS = "in_progress"
    FINISHED = "finished"; CANCELLED = "cancelled"

class TournamentType(Enum):
    SLOTS = "slots"; POKER = "poker"; DICE = "dice"
    BUSINESS_RACE = "business_race"; EARNINGS_RACE = "earnings_race"

class PetRarity(Enum):
    COMMON = "common"; UNCOMMON = "uncommon"; RARE = "rare"
    EPIC = "epic"; LEGENDARY = "legendary"

class PetMood(Enum):
    HAPPY = "happy"; NEUTRAL = "neutral"; SAD = "sad"; HUNGRY = "hungry"; SICK = "sick"

class EarthRegion(Enum):
    SPAWN = "spawn"; BUSINESS_CENTER = "business_center"
    RESIDENTIAL = "residential"; ELITE = "elite"; INDUSTRIAL = "industrial"
    ENTERTAINMENT = "entertainment"; SUBURBAN = "suburban"; DOWNTOWN = "downtown"

class ItemRarity(Enum):
    COMMON = "common"; UNCOMMON = "uncommon"; RARE = "rare"
    EPIC = "epic"; LEGENDARY = "legendary"; MYTHIC = "mythic"

class ItemCategory(Enum):
    WORK_BOOSTER = "work_booster"; BUSINESS_BOOSTER = "business_booster"
    CRYPTO_BOOSTER = "crypto_booster"; STOCK_BOOSTER = "stock_booster"
    CASINO_LUCK = "casino_luck"; ROBBERY_TOOL = "robbery_tool"
    REPUTATION_BOOST = "reputation_boost"; PET_FOOD = "pet_food"
    PET_TOY = "pet_toy"; COSMETIC = "cosmetic"
    INSURANCE_PREMIUM = "insurance_premium"; COLLECTIBLE = "collectible"

class MinerType(Enum):
    USB = "usb"; HOME_FARM = "home_farm"; GARAGE_FARM = "garage_farm"
    INDUSTRIAL = "industrial"; HOTEL = "hotel"

class ReputationLevel(Enum):
    HATED = "hated"; DISLIKED = "disliked"; NEUTRAL = "neutral"
    LIKED = "liked"; RESPECTED = "respected"; BELOVED = "beloved"
    LEGENDARY = "legendary"

class AchievementCategory(Enum):
    MONEY = "money"; BUSINESS = "business"; CRYPTO = "crypto"
    STOCKS = "stocks"; CASINO = "casino"; CRIME = "crime"
    CLAN = "clan"; SOCIAL = "social"; SPECIAL = "special"
    MODERATION = "moderation"

class StickerBlockMode(Enum):
    NONE = "none"; SPECIFIC = "specific"; PACK = "pack"; ALL = "all"

class GifBlockMode(Enum):
    NONE = "none"; KEYWORD = "keyword"; ALL = "all"

class IIModMode(Enum):
    ENABLED = "enabled"; DISABLED = "disabled"


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

    # РЕАЛИСТИЧНЫЕ ПОЛЯ
    age: int = 18
    hunger: int = 100
    sleep: int = 100
    stress: int = 0
    is_sick: bool = False
    sick_until: Optional[datetime] = None
    monthly_income: int = 0
    monthly_expenses: int = 0
    savings: int = 0
    debt: int = 0
    credit_history: float = 1.0
    has_ip: bool = False
    ip_name: str = ""
    ip_date: Optional[datetime] = None
    tax_debt: int = 0
    tax_history: List[Dict] = field(default_factory=list)
    children: int = 0
    family_expenses: int = 0
    job_title: str = ""
    job_experience: int = 0
    job_salary: int = 0
    is_employed: bool = False
    has_insurance: bool = False
    health_issues: List[str] = field(default_factory=list)
    last_doctor_visit: Optional[datetime] = None
    house_id: Optional[str] = None
    house_utilities: int = 0
    house_tax: int = 0
    car_id: Optional[str] = None
    car_fuel: int = 100
    car_insurance: bool = False
    car_fines: int = 0
    genes: Dict[str, float] = field(default_factory=dict)
    mutations: List[str] = field(default_factory=list)
    evolution_level: int = 0
    evolution_path: str = "Человек"
    survived_disasters: List[str] = field(default_factory=list)
    disaster_protection: bool = False
    quests: Dict[str, int] = field(default_factory=dict)
    daily_quests_done: bool = False
    total_work: int = 0
    total_casino_win: int = 0
    total_casino_lose: int = 0
    chat_activity: Dict[int, int] = field(default_factory=dict)
    bonus_streak: int = 0
    last_bonus_date: Optional[datetime] = None
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
# МОДЕЛЬ ChatConfig (ВАЖНО!)
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
# ОСТАЛЬНЫЕ МОДЕЛИ
# ============================================================

@dataclass
class AdminLevel:
    user_id: int; chat_id: int; level: int = 0; assigned_by: int = 0
    assigned_at: datetime = field(default_factory=datetime.now); is_creator: bool = False
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["assigned_at"] = self.assigned_at.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdminLevel":
        data["assigned_at"] = datetime.fromisoformat(data["assigned_at"]) if isinstance(data.get("assigned_at"), str) else data.get("assigned_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class ModLog:
    log_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    chat_id: int = 0; moderator_id: int = 0; target_id: int = 0
    action: ModActionType = ModActionType.WARN; reason: str = ""; comment: str = ""
    duration_minutes: int = 0; timestamp: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None; is_active: bool = True
    removed_by: Optional[int] = None; removed_at: Optional[datetime] = None
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["action"] = self.action.value; data["timestamp"] = self.timestamp.isoformat()
        data["expires_at"] = self.expires_at.isoformat() if self.expires_at else None
        data["removed_at"] = self.removed_at.isoformat() if self.removed_at else None; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModLog":
        data["action"] = ModActionType(data["action"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"]) if isinstance(data.get("timestamp"), str) else data.get("timestamp", datetime.now())
        data["expires_at"] = datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None
        data["removed_at"] = datetime.fromisoformat(data["removed_at"]) if data.get("removed_at") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Business:
    business_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0; name: str = ""; business_type: str = ""; level: int = 1
    status: BusinessStatus = BusinessStatus.ACTIVE; purchase_price: int = 0; current_value: int = 0
    hourly_income: int = 0; employees: List[int] = field(default_factory=list); max_employees: int = 5
    salary_per_employee: int = 100; franchise_available: bool = False; franchise_cost: int = 0
    sabotage_protection: bool = False; bankrupt_count: int = 0
    created_at: datetime = field(default_factory=datetime.now); last_collected: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat(); data["last_collected"] = self.last_collected.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Business":
        data["status"] = BusinessStatus(data.get("status", "active"))
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["last_collected"] = datetime.fromisoformat(data["last_collected"]) if isinstance(data.get("last_collected"), str) else data.get("last_collected", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class CryptoAsset:
    ticker: str; name: str; current_price: float; previous_price: float = 0.0
    change_percent: float = 0.0; all_time_high: float = 0.0; all_time_low: float = 0.0
    volume_24h: int = 0; last_updated: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["last_updated"] = self.last_updated.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CryptoAsset":
        data["last_updated"] = datetime.fromisoformat(data["last_updated"]) if isinstance(data.get("last_updated"), str) else data.get("last_updated", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class StockAsset:
    ticker: str; company_name: str; current_price: float; previous_price: float = 0.0
    change_percent: float = 0.0; dividend_yield: float = 0.01; sector: str = ""
    market_cap: int = 0; last_updated: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["last_updated"] = self.last_updated.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StockAsset":
        data["last_updated"] = datetime.fromisoformat(data["last_updated"]) if isinstance(data.get("last_updated"), str) else data.get("last_updated", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class UserPortfolio:
    user_id: int; crypto_holdings: Dict[str, float] = field(default_factory=dict)
    stock_holdings: Dict[str, int] = field(default_factory=dict)
    total_invested_crypto: int = 0; total_invested_stocks: int = 0; total_profit_loss: int = 0
    def to_dict(self) -> Dict[str, Any]: return asdict(self)
    @classmethod def from_dict(cls, data: Dict[str, Any]) -> "UserPortfolio":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Miner:
    miner_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0; miner_type: MinerType = MinerType.USB; efficiency: float = 1.0
    hours_mined: int = 0; total_mined_value: int = 0
    last_repair: datetime = field(default_factory=datetime.now); created_at: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["miner_type"] = self.miner_type.value
        data["last_repair"] = self.last_repair.isoformat(); data["created_at"] = self.created_at.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Miner":
        data["miner_type"] = MinerType(data.get("miner_type", "usb"))
        data["last_repair"] = datetime.fromisoformat(data["last_repair"]) if isinstance(data.get("last_repair"), str) else data.get("last_repair", datetime.now())
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Auction:
    auction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    seller_id: int = 0; item_type: str = ""; item_name: str = ""
    item_data: Dict[str, Any] = field(default_factory=dict); starting_price: int = 0
    current_bid: int = 0; current_bidder_id: int = 0; min_increment: int = AUCTION_BID_MIN_INCREMENT
    status: AuctionStatus = AuctionStatus.ACTIVE; created_at: datetime = field(default_factory=datetime.now)
    ends_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=AUCTION_DURATION_HOURS_DEFAULT))
    bids_history: List[Dict[str, Any]] = field(default_factory=list)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat(); data["ends_at"] = self.ends_at.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Auction":
        data["status"] = AuctionStatus(data.get("status", "active"))
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["ends_at"] = datetime.fromisoformat(data["ends_at"]) if isinstance(data.get("ends_at"), str) else data.get("ends_at", datetime.now() + timedelta(hours=AUCTION_DURATION_HOURS_DEFAULT))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Clan:
    clan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""; leader_id: int = 0; vice_leader_id: int = 0
    members: List[int] = field(default_factory=list); veteran_ids: List[int] = field(default_factory=list)
    treasury: int = 0; logo_emoji: str = "🏰"; wars_won: int = 0; wars_lost: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    war_debuff_until: Optional[datetime] = None
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["created_at"] = self.created_at.isoformat()
        data["war_debuff_until"] = self.war_debuff_until.isoformat() if self.war_debuff_until else None; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Clan":
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["war_debuff_until"] = datetime.fromisoformat(data["war_debuff_until"]) if data.get("war_debuff_until") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class ClanWar:
    war_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    attacker_clan_id: str = ""; defender_clan_id: str = ""
    attacker_score: int = 0; defender_score: int = 0
    status: ClanWarStatus = ClanWarStatus.PENDING
    started_at: datetime = field(default_factory=datetime.now)
    ends_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=CLAN_WAR_DURATION_HOURS))
    winner_id: str = ""; loot_amount: int = 0
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["status"] = self.status.value
        data["started_at"] = self.started_at.isoformat(); data["ends_at"] = self.ends_at.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClanWar":
        data["status"] = ClanWarStatus(data.get("status", "pending"))
        data["started_at"] = datetime.fromisoformat(data["started_at"]) if isinstance(data.get("started_at"), str) else data.get("started_at", datetime.now())
        data["ends_at"] = datetime.fromisoformat(data["ends_at"]) if isinstance(data.get("ends_at"), str) else data.get("ends_at", datetime.now() + timedelta(hours=CLAN_WAR_DURATION_HOURS))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Tournament:
    tournament_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""; tournament_type: TournamentType = TournamentType.POKER
    entry_fee: int = 0; prize_pool: int = 0; max_players: int = 32
    registered_players: List[int] = field(default_factory=list)
    status: TournamentStatus = TournamentStatus.REGISTRATION
    winner_id: int = 0; created_at: datetime = field(default_factory=datetime.now)
    starts_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=1))
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["tournament_type"] = self.tournament_type.value
        data["status"] = self.status.value; data["created_at"] = self.created_at.isoformat()
        data["starts_at"] = self.starts_at.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tournament":
        data["tournament_type"] = TournamentType(data.get("tournament_type", "poker"))
        data["status"] = TournamentStatus(data.get("status", "registration"))
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["starts_at"] = datetime.fromisoformat(data["starts_at"]) if isinstance(data.get("starts_at"), str) else data.get("starts_at", datetime.now() + timedelta(hours=1))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Pet:
    pet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0; name: str = ""; species: str = ""
    rarity: PetRarity = PetRarity.COMMON; level: int = 1; experience: int = 0
    mood: PetMood = PetMood.NEUTRAL; health: int = 100; hunger: int = 0
    color: str = "default"; mutation: str = ""; generation: int = 1
    parents: List[str] = field(default_factory=list)
    last_fed: datetime = field(default_factory=datetime.now); last_played: datetime = field(default_factory=datetime.now)
    breeding_cooldown_until: Optional[datetime] = None
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["rarity"] = self.rarity.value; data["mood"] = self.mood.value
        data["last_fed"] = self.last_fed.isoformat(); data["last_played"] = self.last_played.isoformat()
        data["breeding_cooldown_until"] = self.breeding_cooldown_until.isoformat() if self.breeding_cooldown_until else None; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pet":
        data["rarity"] = PetRarity(data.get("rarity", "common")); data["mood"] = PetMood(data.get("mood", "neutral"))
        data["last_fed"] = datetime.fromisoformat(data["last_fed"]) if isinstance(data.get("last_fed"), str) else data.get("last_fed", datetime.now())
        data["last_played"] = datetime.fromisoformat(data["last_played"]) if isinstance(data.get("last_played"), str) else data.get("last_played", datetime.now())
        data["breeding_cooldown_until"] = datetime.fromisoformat(data["breeding_cooldown_until"]) if data.get("breeding_cooldown_until") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class ShopItem:
    item_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""; description: str = ""; rarity: ItemRarity = ItemRarity.COMMON
    category: ItemCategory = ItemCategory.WORK_BOOSTER; price: int = 0
    boost_percent: float = 0.0; boost_duration_hours: int = 24
    stock: int = -1; season_exclusive: bool = False; min_level_required: int = 0
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["rarity"] = self.rarity.value; data["category"] = self.category.value; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ShopItem":
        data["rarity"] = ItemRarity(data.get("rarity", "common")); data["category"] = ItemCategory(data.get("category", "work_booster"))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class UserInventory:
    user_id: int; items: Dict[str, int] = field(default_factory=dict)
    active_boosters: Dict[str, datetime] = field(default_factory=dict)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["active_boosters"] = {k: v.isoformat() for k, v in self.active_boosters.items()}; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserInventory":
        data["active_boosters"] = {k: datetime.fromisoformat(v) for k, v in data.get("active_boosters", {}).items()}
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Achievement:
    achievement_id: int; name: str; description: str; category: AchievementCategory
    reward: int = 0; hidden: bool = False
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["category"] = self.category.value; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Achievement":
        data["category"] = AchievementCategory(data["category"])
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Transaction:
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int = 0; amount: int = 0; transaction_type: TransactionType = TransactionType.WORK
    balance_after: int = 0; description: str = ""
    related_user_id: Optional[int] = None; related_item_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["transaction_type"] = self.transaction_type.value; data["timestamp"] = self.timestamp.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        data["transaction_type"] = TransactionType(data["transaction_type"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"]) if isinstance(data.get("timestamp"), str) else data.get("timestamp", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class GameSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    game_type: GameType = GameType.SLOTS; user_id: int = 0; bet_amount: int = 0
    result: Dict[str, Any] = field(default_factory=dict); win_amount: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["game_type"] = self.game_type.value; data["timestamp"] = self.timestamp.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameSession":
        data["game_type"] = GameType(data["game_type"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"]) if isinstance(data.get("timestamp"), str) else data.get("timestamp", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Report:
    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reporter_id: int = 0; target_id: int = 0; chat_id: int = 0
    reason: str = ""; status: str = "pending"; handled_by: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["created_at"] = self.created_at.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Report":
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class GlobalEconomy:
    inflation_rate: float = INFLATION_RATE_DEFAULT; deflation_rate: float = DEFLATION_RATE_DEFAULT
    tax_rate: float = TAX_RATE_DEFAULT; crisis_active: bool = False; boom_active: bool = False
    last_crisis: Optional[datetime] = None; last_boom: Optional[datetime] = None
    total_money_in_circulation: int = 0; total_users: int = 0; total_businesses: int = 0; gdp_bot: int = 0
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["last_crisis"] = self.last_crisis.isoformat() if self.last_crisis else None
        data["last_boom"] = self.last_boom.isoformat() if self.last_boom else None; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GlobalEconomy":
        data["last_crisis"] = datetime.fromisoformat(data["last_crisis"]) if data.get("last_crisis") else None
        data["last_boom"] = datetime.fromisoformat(data["last_boom"]) if data.get("last_boom") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Earth:
    earth_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    region: EarthRegion = EarthRegion.SPAWN; owner_id: int = 0; purchase_price: int = 0
    current_value: int = 0; built_business_id: Optional[str] = None
    for_sale: bool = False; sale_price: int = 0
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["region"] = self.region.value; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Earth":
        data["region"] = EarthRegion(data.get("region", "spawn"))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Vehicle:
    vehicle_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0; vehicle_type: str = "car"; name: str = ""
    price: int = 0; speed_bonus: float = 1.0; income_bonus: float = 0.0
    for_sale: bool = False; sale_price: int = 0
    def to_dict(self) -> Dict[str, Any]: return asdict(self)
    @classmethod def from_dict(cls, data: Dict[str, Any]) -> "Vehicle":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class House:
    house_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: int = 0; house_type: str = "apartment"; name: str = ""
    price: int = 0; rooms: int = 1; income_bonus: float = 0.0
    rentable: bool = False; rent_price: int = 0; tenant_id: Optional[int] = None
    for_sale: bool = False; sale_price: int = 0
    mortgage_active: bool = False; mortgage_amount: int = 0
    mortgage_due_date: Optional[datetime] = None
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["mortgage_due_date"] = self.mortgage_due_date.isoformat() if self.mortgage_due_date else None; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "House":
        data["mortgage_due_date"] = datetime.fromisoformat(data["mortgage_due_date"]) if data.get("mortgage_due_date") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Insurance:
    insurance_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int = 0; coverage_amount: int = 0; premium_paid: int = 0
    active: bool = True; purchased_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=INSURANCE_DURATION_DAYS))
    claims: List[Dict[str, Any]] = field(default_factory=list)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["purchased_at"] = self.purchased_at.isoformat(); data["expires_at"] = self.expires_at.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Insurance":
        data["purchased_at"] = datetime.fromisoformat(data["purchased_at"]) if isinstance(data.get("purchased_at"), str) else data.get("purchased_at", datetime.now())
        data["expires_at"] = datetime.fromisoformat(data["expires_at"]) if isinstance(data.get("expires_at"), str) else data.get("expires_at", datetime.now() + timedelta(days=INSURANCE_DURATION_DAYS))
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class BlacklistEntry:
    user_id: int; reason: str = ""; added_by: int = 0
    added_at: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["added_at"] = self.added_at.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlacklistEntry":
        data["added_at"] = datetime.fromisoformat(data["added_at"]) if isinstance(data.get("added_at"), str) else data.get("added_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class ChatStats:
    chat_id: int; total_messages: int = 0; total_users: int = 0; active_users_today: int = 0
    messages_today: int = 0; bans_today: int = 0; mutes_today: int = 0
    kicks_today: int = 0; warns_today: int = 0; economy_activity_today: int = 0
    casino_activity_today: int = 0; last_updated: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["last_updated"] = self.last_updated.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatStats":
        data["last_updated"] = datetime.fromisoformat(data["last_updated"]) if isinstance(data.get("last_updated"), str) else data.get("last_updated", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class WorldEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""; description: str = ""; affect_stocks: bool = False
    affect_crypto: bool = False; affect_business: bool = False
    stock_impact_percent: float = 0.0; crypto_impact_percent: float = 0.0
    business_impact_percent: float = 0.0; duration_hours: int = 2
    active: bool = False; started_at: Optional[datetime] = None; ends_at: Optional[datetime] = None
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["started_at"] = self.started_at.isoformat() if self.started_at else None
        data["ends_at"] = self.ends_at.isoformat() if self.ends_at else None; return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorldEvent":
        data["started_at"] = datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None
        data["ends_at"] = datetime.fromisoformat(data["ends_at"]) if data.get("ends_at") else None
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# ============================================================
# КОНФИГУРАЦИИ
# ============================================================

BUSINESS_TYPES: List[Dict[str, Any]] = [
    {"type": "coffee_shop", "name": "Кофейня", "base_price": 150000, "base_income": 500, "max_employees": 3},
    {"type": "barbershop", "name": "Барбершоп", "base_price": 200000, "base_income": 700, "max_employees": 4},
    {"type": "grocery_store", "name": "Продуктовый магазин", "base_price": 300000, "base_income": 1000, "max_employees": 5},
    {"type": "pharmacy", "name": "Аптека", "base_price": 400000, "base_income": 1400, "max_employees": 5},
    {"type": "car_wash", "name": "Автомойка", "base_price": 180000, "base_income": 600, "max_employees": 3},
    {"type": "fitness_club", "name": "Фитнес-клуб", "base_price": 500000, "base_income": 1800, "max_employees": 6},
    {"type": "restaurant", "name": "Ресторан", "base_price": 600000, "base_income": 2200, "max_employees": 8},
    {"type": "clothing_store", "name": "Магазин одежды", "base_price": 250000, "base_income": 850, "max_employees": 4},
    {"type": "tech_repair", "name": "Ремонт техники", "base_price": 150000, "base_income": 500, "max_employees": 3},
    {"type": "beauty_salon", "name": "Салон красоты", "base_price": 280000, "base_income": 950, "max_employees": 5},
    {"type": "tire_service", "name": "Шиномонтаж", "base_price": 120000, "base_income": 400, "max_employees": 3},
    {"type": "bakery", "name": "Пекарня", "base_price": 200000, "base_income": 700, "max_employees": 4},
    {"type": "flower_shop", "name": "Цветочный магазин", "base_price": 100000, "base_income": 350, "max_employees": 2},
    {"type": "construction_company", "name": "Строительная компания", "base_price": 800000, "base_income": 3000, "max_employees": 10},
    {"type": "logistics_company", "name": "Логистическая компания", "base_price": 700000, "base_income": 2600, "max_employees": 8},
    {"type": "advertising_agency", "name": "Рекламное агентство", "base_price": 350000, "base_income": 1200, "max_employees": 5},
    {"type": "taxi_fleet", "name": "Таксопарк", "base_price": 450000, "base_income": 1600, "max_employees": 6},
    {"type": "hotel", "name": "Гостиница", "base_price": 900000, "base_income": 3500, "max_employees": 10},
    {"type": "car_dealership", "name": "Автосалон", "base_price": 1000000, "base_income": 4000, "max_employees": 8},
    {"type": "private_clinic", "name": "Частная клиника", "base_price": 1200000, "base_income": 5000, "max_employees": 12},
    {"type": "law_firm", "name": "Юридическая фирма", "base_price": 500000, "base_income": 1800, "max_employees": 6},
    {"type": "software_company", "name": "IT-компания", "base_price": 1500000, "base_income": 6000, "max_employees": 15},
    {"type": "jewelry_store", "name": "Ювелирный магазин", "base_price": 750000, "base_income": 2800, "max_employees": 5},
    {"type": "real_estate_agency", "name": "Агентство недвижимости", "base_price": 600000, "base_income": 2200, "max_employees": 7},
    {"type": "gas_station", "name": "АЗС", "base_price": 350000, "base_income": 1200, "max_employees": 4},
]

CRYPTO_ASSETS_CONFIG: List[Dict[str, Any]] = [
    {"ticker": "FABC", "name": "ФаблКоин", "base_price": 10.0, "volatility": 0.15},
    {"ticker": "GRTK", "name": "ГрокТокен", "base_price": 50.0, "volatility": 0.20},
    {"ticker": "DPCN", "name": "ДипЧейн", "base_price": 25.0, "volatility": 0.18},
    {"ticker": "MNET", "name": "МайнНет", "base_price": 100.0, "volatility": 0.12},
    {"ticker": "CSNC", "name": "КазиноКоин", "base_price": 5.0, "volatility": 0.30},
    {"ticker": "BLNC", "name": "БалансКоин", "base_price": 75.0, "volatility": 0.22},
    {"ticker": "RBLX", "name": "РоблКоикс", "base_price": 30.0, "volatility": 0.25},
    {"ticker": "NEFT", "name": "НефтьТокен", "base_price": 200.0, "volatility": 0.10},
    {"ticker": "GLDN", "name": "Золотой", "base_price": 500.0, "volatility": 0.08},
    {"ticker": "CLAN", "name": "КланТокен", "base_price": 15.0, "volatility": 0.28},
]

STOCK_ASSETS_CONFIG: List[Dict[str, Any]] = [
    {"ticker": "FBLK", "company_name": "ФабликТех", "base_price": 500.0, "sector": "tech", "dividend_yield": 0.02},
    {"ticker": "GRKC", "company_name": "ГрокКорп", "base_price": 1200.0, "sector": "tech", "dividend_yield": 0.015},
    {"ticker": "DPSK", "company_name": "ДипСикИнк", "base_price": 800.0, "sector": "tech", "dividend_yield": 0.018},
    {"ticker": "NGPT", "company_name": "НефтьГазПром", "base_price": 3000.0, "sector": "energy", "dividend_yield": 0.05},
    {"ticker": "RDMT", "company_name": "РудаМеталл", "base_price": 1500.0, "sector": "mining", "dividend_yield": 0.04},
    {"ticker": "AGRM", "company_name": "АгроМир", "base_price": 600.0, "sector": "agriculture", "dividend_yield": 0.03},
    {"ticker": "MDHL", "company_name": "МедиаХолд", "base_price": 900.0, "sector": "media", "dividend_yield": 0.025},
    {"ticker": "CRPB", "company_name": "КриптоБанк", "base_price": 2500.0, "sector": "finance", "dividend_yield": 0.035},
    {"ticker": "TRLG", "company_name": "ТрансЛог", "base_price": 1100.0, "sector": "logistics", "dividend_yield": 0.028},
    {"ticker": "ENRG", "company_name": "ЭнергоСеть", "base_price": 2000.0, "sector": "energy", "dividend_yield": 0.045},
]

MINER_CONFIG: Dict[MinerType, Dict[str, Any]] = {
    MinerType.USB: {"name": "USB-майнер", "price": 5000, "base_income_per_hour": 50},
    MinerType.HOME_FARM: {"name": "Домашняя ферма", "price": 25000, "base_income_per_hour": 300},
    MinerType.GARAGE_FARM: {"name": "Гаражная ферма", "price": 100000, "base_income_per_hour": 1500},
    MinerType.INDUSTRIAL: {"name": "Промышленный цех", "price": 500000, "base_income_per_hour": 8000},
    MinerType.HOTEL: {"name": "Майнинг-отель", "price": 2500000, "base_income_per_hour": 50000},
}

HOUSE_CONFIG: List[Dict[str, Any]] = [
    {"type": "apartment", "name": "Квартира-студия", "price": 100000, "rooms": 1, "income_bonus": 0.02},
    {"type": "apartment", "name": "Однокомнатная квартира", "price": 200000, "rooms": 1, "income_bonus": 0.03},
    {"type": "apartment", "name": "Двухкомнатная квартира", "price": 350000, "rooms": 2, "income_bonus": 0.05},
    {"type": "house", "name": "Дача", "price": 150000, "rooms": 2, "income_bonus": 0.02},
    {"type": "house", "name": "Частный дом", "price": 500000, "rooms": 3, "income_bonus": 0.07},
    {"type": "house", "name": "Коттедж", "price": 1000000, "rooms": 5, "income_bonus": 0.10},
    {"type": "villa", "name": "Вилла у моря", "price": 2500000, "rooms": 7, "income_bonus": 0.15},
    {"type": "mansion", "name": "Особняк", "price": 5000000, "rooms": 10, "income_bonus": 0.20},
    {"type": "castle", "name": "Замок", "price": 10000000, "rooms": 20, "income_bonus": 0.30},
    {"type": "apartment", "name": "Пентхаус", "price": 8000000, "rooms": 8, "income_bonus": 0.25},
]

VEHICLE_CONFIG: List[Dict[str, Any]] = [
    {"type": "car", "name": "Лада Гранта", "price": 50000, "speed_bonus": 1.1, "income_bonus": 0.01},
    {"type": "car", "name": "Toyota Camry", "price": 200000, "speed_bonus": 1.2, "income_bonus": 0.02},
    {"type": "car", "name": "BMW X5", "price": 500000, "speed_bonus": 1.3, "income_bonus": 0.03},
    {"type": "car", "name": "Mercedes S-Class", "price": 800000, "speed_bonus": 1.4, "income_bonus": 0.04},
    {"type": "car", "name": "Lamborghini Huracan", "price": 2000000, "speed_bonus": 1.6, "income_bonus": 0.06},
    {"type": "car", "name": "Rolls-Royce Phantom", "price": 3000000, "speed_bonus": 1.5, "income_bonus": 0.08},
    {"type": "car", "name": "Bugatti Chiron", "price": 5000000, "speed_bonus": 2.0, "income_bonus": 0.10},
    {"type": "yacht", "name": "Катер", "price": 300000, "speed_bonus": 1.0, "income_bonus": 0.03},
    {"type": "yacht", "name": "Яхта класса Люкс", "price": 1500000, "speed_bonus": 1.2, "income_bonus": 0.07},
    {"type": "yacht", "name": "Суперъяхта", "price": 5000000, "speed_bonus": 1.3, "income_bonus": 0.12},
    {"type": "plane", "name": "Частный самолёт", "price": 3000000, "speed_bonus": 2.5, "income_bonus": 0.10},
    {"type": "plane", "name": "Бизнес-джет", "price": 8000000, "speed_bonus": 3.0, "income_bonus": 0.15},
    {"type": "helicopter", "name": "Вертолёт", "price": 2000000, "speed_bonus": 2.0, "income_bonus": 0.08},
]

SHOP_ITEMS_CONFIG: List[Dict[str, Any]] = [
    {"item_id": "work_booster_1", "name": "Энергетик", "description": "Увеличивает доход с работы на 25% на 24 часа", "rarity": ItemRarity.COMMON, "category": ItemCategory.WORK_BOOSTER, "price": 500, "boost_percent": 25.0, "boost_duration_hours": 24},
    {"item_id": "work_booster_2", "name": "Кофе тройной", "description": "Увеличивает доход с работы на 50% на 12 часов", "rarity": ItemRarity.UNCOMMON, "category": ItemCategory.WORK_BOOSTER, "price": 1500, "boost_percent": 50.0, "boost_duration_hours": 12},
    {"item_id": "work_booster_3", "name": "Амфетамин", "description": "Увеличивает доход с работы на 100% на 6 часов", "rarity": ItemRarity.RARE, "category": ItemCategory.WORK_BOOSTER, "price": 5000, "boost_percent": 100.0, "boost_duration_hours": 6},
    {"item_id": "business_booster_1", "name": "Бизнес-план", "description": "Увеличивает прибыль бизнеса на 30% на 48 часов", "rarity": ItemRarity.RARE, "category": ItemCategory.BUSINESS_BOOSTER, "price": 10000, "boost_percent": 30.0, "boost_duration_hours": 48},
    {"item_id": "business_booster_2", "name": "Консалтинг", "description": "Увеличивает прибыль бизнеса на 60% на 24 часа", "rarity": ItemRarity.EPIC, "category": ItemCategory.BUSINESS_BOOSTER, "price": 25000, "boost_percent": 60.0, "boost_duration_hours": 24},
    {"item_id": "crypto_booster_1", "name": "Инсайдерская информация", "description": "Следующая сделка с криптой гарантированно в плюс на 20%", "rarity": ItemRarity.EPIC, "category": ItemCategory.CRYPTO_BOOSTER, "price": 15000, "boost_percent": 20.0, "boost_duration_hours": 1},
    {"item_id": "stock_booster_1", "name": "Прогноз аналитика", "description": "Следующая сделка с акциями гарантированно в плюс на 15%", "rarity": ItemRarity.EPIC, "category": ItemCategory.STOCK_BOOSTER, "price": 15000, "boost_percent": 15.0, "boost_duration_hours": 1},
    {"item_id": "casino_luck_1", "name": "Кроличья лапка", "description": "Увеличивает шанс выигрыша в казино на 10% на 1 час", "rarity": ItemRarity.RARE, "category": ItemCategory.CASINO_LUCK, "price": 3000, "boost_percent": 10.0, "boost_duration_hours": 1},
    {"item_id": "casino_luck_2", "name": "Подкова удачи", "description": "Увеличивает шанс выигрыша в казино на 25% на 30 минут", "rarity": ItemRarity.EPIC, "category": ItemCategory.CASINO_LUCK, "price": 10000, "boost_percent": 25.0, "boost_duration_hours": 0.5},
    {"item_id": "robbery_tool_1", "name": "Отмычка", "description": "Увеличивает шанс ограбления на 15%", "rarity": ItemRarity.RARE, "category": ItemCategory.ROBBERY_TOOL, "price": 8000, "boost_percent": 15.0, "boost_duration_hours": 1},
    {"item_id": "robbery_tool_2", "name": "Набор медвежатника", "description": "Увеличивает шанс ограбления на 30%", "rarity": ItemRarity.EPIC, "category": ItemCategory.ROBBERY_TOOL, "price": 20000, "boost_percent": 30.0, "boost_duration_hours": 1},
    {"item_id": "reputation_boost_1", "name": "Букет цветов", "description": "Мгновенно +5 к репутации", "rarity": ItemRarity.COMMON, "category": ItemCategory.REPUTATION_BOOST, "price": 1000, "boost_percent": 0, "boost_duration_hours": 0},
    {"item_id": "pet_food_1", "name": "Корм для питомца", "description": "Восстанавливает сытость питомца", "rarity": ItemRarity.COMMON, "category": ItemCategory.PET_FOOD, "price": 100, "boost_percent": 0, "boost_duration_hours": 0},
    {"item_id": "pet_toy_1", "name": "Игрушка-пищалка", "description": "Поднимает настроение питомца", "rarity": ItemRarity.COMMON, "category": ItemCategory.PET_TOY, "price": 200, "boost_percent": 0, "boost_duration_hours": 0},
    {"item_id": "cosmetic_title_1", "name": "Титул: Король", "description": "Отображается в профиле", "rarity": ItemRarity.RARE, "category": ItemCategory.COSMETIC, "price": 50000, "boost_percent": 0, "boost_duration_hours": 0},
    {"item_id": "cosmetic_frame_1", "name": "Золотая рамка", "description": "Золотая рамка профиля", "rarity": ItemRarity.EPIC, "category": ItemCategory.COSMETIC, "price": 100000, "boost_percent": 0, "boost_duration_hours": 0},
    {"item_id": "collectible_1", "name": "Карточка: Сатоши", "description": "Коллекционная карточка #1", "rarity": ItemRarity.LEGENDARY, "category": ItemCategory.COLLECTIBLE, "price": 500000, "boost_percent": 0, "boost_duration_hours": 0},
    {"item_id": "collectible_2", "name": "Карточка: Виталик", "description": "Коллекционная карточка #2", "rarity": ItemRarity.LEGENDARY, "category": ItemCategory.COLLECTIBLE, "price": 500000, "boost_percent": 0, "boost_duration_hours": 0},
    {"item_id": "insurance_premium_1", "name": "Премиум-страховка", "description": "Увеличивает возврат при банкротстве до 35%", "rarity": ItemRarity.EPIC, "category": ItemCategory.INSURANCE_PREMIUM, "price": 25000, "boost_percent": 35.0, "boost_duration_hours": 720},
]

ACHIEVEMENTS_CONFIG: List[Dict[str, Any]] = [
    {"achievement_id": 1, "name": "Первый заработок", "description": "Заработать 100 монет", "category": AchievementCategory.MONEY, "reward": 50},
    {"achievement_id": 2, "name": "Сотка", "description": "Накопить 100 000", "category": AchievementCategory.MONEY, "reward": 1000},
    {"achievement_id": 3, "name": "Миллионер", "description": "Накопить 1 000 000", "category": AchievementCategory.MONEY, "reward": 10000},
    {"achievement_id": 4, "name": "Миллиардер", "description": "Накопить 1 000 000 000", "category": AchievementCategory.MONEY, "reward": 100000, "hidden": True},
    {"achievement_id": 5, "name": "Гол как сокол", "description": "Баланс 0 монет", "category": AchievementCategory.MONEY, "reward": 100},
    {"achievement_id": 6, "name": "Банкрот", "description": "Обанкротить бизнес", "category": AchievementCategory.BUSINESS, "reward": 500},
    {"achievement_id": 7, "name": "Кредитная история", "description": "Взять и погасить 5 кредитов", "category": AchievementCategory.MONEY, "reward": 2000},
    {"achievement_id": 8, "name": "Щедрая душа", "description": "Перевести 100 000 другому", "category": AchievementCategory.SOCIAL, "reward": 1000},
    {"achievement_id": 9, "name": "Копилка", "description": "Не тратить монеты 7 дней", "category": AchievementCategory.MONEY, "reward": 500},
    {"achievement_id": 10, "name": "Транжира", "description": "Потратить 500 000 за день", "category": AchievementCategory.MONEY, "reward": 2000},
    {"achievement_id": 11, "name": "Стартапер", "description": "Создать первый бизнес", "category": AchievementCategory.BUSINESS, "reward": 500},
    {"achievement_id": 12, "name": "Империя", "description": "Владеть 5 бизнесами", "category": AchievementCategory.BUSINESS, "reward": 5000},
    {"achievement_id": 13, "name": "Монополист", "description": "Владеть 10 бизнесами", "category": AchievementCategory.BUSINESS, "reward": 20000},
    {"achievement_id": 14, "name": "Работодатель года", "description": "Нанять 20 сотрудников", "category": AchievementCategory.BUSINESS, "reward": 3000},
    {"achievement_id": 15, "name": "Золотые руки", "description": "Прокачать бизнес до макс уровня", "category": AchievementCategory.BUSINESS, "reward": 10000},
    {"achievement_id": 16, "name": "Слияние", "description": "Купить чужой бизнес", "category": AchievementCategory.BUSINESS, "reward": 2000},
    {"achievement_id": 17, "name": "Франчайзи", "description": "Продать франшизу", "category": AchievementCategory.BUSINESS, "reward": 5000},
    {"achievement_id": 18, "name": "Криптоэнтузиаст", "description": "Купить первую крипту", "category": AchievementCategory.CRYPTO, "reward": 200},
    {"achievement_id": 19, "name": "Ходлер", "description": "Держать крипту 30 дней", "category": AchievementCategory.CRYPTO, "reward": 10000},
    {"achievement_id": 20, "name": "Трейдер", "description": "Совершить 100 сделок", "category": AchievementCategory.STOCKS, "reward": 5000},
    {"achievement_id": 21, "name": "Точный прогноз", "description": "Заработать 50 000 на лонге/шорте", "category": AchievementCategory.STOCKS, "reward": 5000},
    {"achievement_id": 22, "name": "Кит", "description": "Купить акций на 1 000 000 за раз", "category": AchievementCategory.STOCKS, "reward": 10000},
    {"achievement_id": 23, "name": "Дивидендный рантье", "description": "Получить 10 выплат дивидендов", "category": AchievementCategory.STOCKS, "reward": 3000},
    {"achievement_id": 24, "name": "Новичок казино", "description": "Сыграть 10 раз", "category": AchievementCategory.CASINO, "reward": 500},
    {"achievement_id": 25, "name": "Счастливчик", "description": "Выиграть джекпот в слотах", "category": AchievementCategory.CASINO, "reward": 50000, "hidden": True},
    {"achievement_id": 26, "name": "Хайроллер", "description": "Поставить 100 000 за игру", "category": AchievementCategory.CASINO, "reward": 5000},
    {"achievement_id": 27, "name": "Стрик удачи", "description": "Выиграть 5 раз подряд", "category": AchievementCategory.CASINO, "reward": 10000},
    {"achievement_id": 28, "name": "Русская рулетка", "description": "Выжить в русской рулетке", "category": AchievementCategory.CASINO, "reward": 20000},
    {"achievement_id": 29, "name": "Покерфейс", "description": "Выиграть в покер с каре", "category": AchievementCategory.CASINO, "reward": 15000},
    {"achievement_id": 30, "name": "Дуэлянт", "description": "Выиграть 10 дуэлей", "category": AchievementCategory.CASINO, "reward": 5000},
    {"achievement_id": 31, "name": "Медвежатник", "description": "Ограбить банк", "category": AchievementCategory.CRIME, "reward": 50000},
    {"achievement_id": 32, "name": "Сорвиголова", "description": "Ограбить казино", "category": AchievementCategory.CRIME, "reward": 100000, "hidden": True},
    {"achievement_id": 33, "name": "Карманник", "description": "Ограбить 5 игроков", "category": AchievementCategory.CRIME, "reward": 5000},
    {"achievement_id": 34, "name": "Неудачник", "description": "Сесть в тюрьму", "category": AchievementCategory.CRIME, "reward": 500},
    {"achievement_id": 35, "name": "Рецидивист", "description": "Сесть в тюрьму 5 раз", "category": AchievementCategory.CRIME, "reward": 5000},
    {"achievement_id": 36, "name": "Чист перед законом", "description": "30 дней без тюрьмы", "category": AchievementCategory.CRIME, "reward": 10000},
    {"achievement_id": 37, "name": "Вместе сила", "description": "Вступить в клан", "category": AchievementCategory.CLAN, "reward": 500},
    {"achievement_id": 38, "name": "Глава клана", "description": "Создать клан", "category": AchievementCategory.CLAN, "reward": 5000},
    {"achievement_id": 39, "name": "Клановая война", "description": "Участвовать в войне", "category": AchievementCategory.CLAN, "reward": 2000},
    {"achievement_id": 40, "name": "Победитель", "description": "Выиграть войну кланов", "category": AchievementCategory.CLAN, "reward": 20000},
    {"achievement_id": 41, "name": "Семьянин", "description": "Вступить в брак", "category": AchievementCategory.SOCIAL, "reward": 1000},
    {"achievement_id": 42, "name": "Свобода", "description": "Развестись", "category": AchievementCategory.SOCIAL, "reward": 2000},
    {"achievement_id": 43, "name": "Медовый месяц", "description": "30 дней в браке", "category": AchievementCategory.SOCIAL, "reward": 10000},
    {"achievement_id": 44, "name": "Друг", "description": "Отправить 100 сообщений", "category": AchievementCategory.SOCIAL, "reward": 500},
    {"achievement_id": 45, "name": "Душа компании", "description": "Отправить 1000 сообщений", "category": AchievementCategory.SOCIAL, "reward": 2000},
    {"achievement_id": 46, "name": "Коллекционер", "description": "Купить редкий предмет", "category": AchievementCategory.SPECIAL, "reward": 5000},
    {"achievement_id": 47, "name": "Фартовый", "description": "Найти находку", "category": AchievementCategory.SPECIAL, "reward": 1000},
    {"achievement_id": 48, "name": "Кармический", "description": "Накопить 1000 кармы", "category": AchievementCategory.SPECIAL, "reward": 10000},
    {"achievement_id": 49, "name": "Проверка пройдена", "description": "Пережить проверку без штрафа", "category": AchievementCategory.SPECIAL, "reward": 5000},
    {"achievement_id": 50, "name": "Турнирный боец", "description": "Занять призовое место", "category": AchievementCategory.SPECIAL, "reward": 25000},
]

PET_SPECIES: List[Dict[str, Any]] = [
    {"species": "cat", "name": "Кот", "base_rarity": PetRarity.COMMON},
    {"species": "dog", "name": "Собака", "base_rarity": PetRarity.COMMON},
    {"species": "dragon", "name": "Дракон", "base_rarity": PetRarity.LEGENDARY},
    {"species": "unicorn", "name": "Единорог", "base_rarity": PetRarity.EPIC},
    {"species": "hamster", "name": "Хомяк", "base_rarity": PetRarity.COMMON},
    {"species": "parrot", "name": "Попугай", "base_rarity": PetRarity.UNCOMMON},
    {"species": "fox", "name": "Лис", "base_rarity": PetRarity.RARE},
    {"species": "phoenix", "name": "Феникс", "base_rarity": PetRarity.LEGENDARY},
]

PROFESSIONS: List[Dict[str, Any]] = [
    {"name": "Курьер", "min_level": 1, "base_income": 50, "cooldown_minutes": 60, "max_level": 10},
    {"name": "Таксист", "min_level": 2, "base_income": 100, "cooldown_minutes": 60, "max_level": 10},
    {"name": "Программист", "min_level": 5, "base_income": 250, "cooldown_minutes": 60, "max_level": 10},
    {"name": "Врач", "min_level": 7, "base_income": 400, "cooldown_minutes": 60, "max_level": 10},
    {"name": "Юрист", "min_level": 8, "base_income": 600, "cooldown_minutes": 60, "max_level": 10},
    {"name": "Бизнесмен", "min_level": 10, "base_income": 1000, "cooldown_minutes": 60, "max_level": 10},
    {"name": "Брокер", "min_level": 12, "base_income": 1500, "cooldown_minutes": 60, "max_level": 10},
    {"name": "Криптотрейдер", "min_level": 15, "base_income": 2500, "cooldown_minutes": 60, "max_level": 10},
    {"name": "Магнат", "min_level": 18, "base_income": 5000, "cooldown_minutes": 60, "max_level": 10},
    {"name": "Олигарх", "min_level": 20, "base_income": 10000, "cooldown_minutes": 60, "max_level": 10},
]

WORLD_EVENTS_POOL: List[Dict[str, Any]] = [
    {"name": "Кризис недвижимости", "affect_stocks": True, "affect_crypto": True, "affect_business": True, "stock_impact": -20, "crypto_impact": -15, "business_impact": -25, "duration_hours": 4},
    {"name": "Технологический бум", "affect_stocks": True, "affect_crypto": True, "affect_business": True, "stock_impact": 25, "crypto_impact": 20, "business_impact": 15, "duration_hours": 6},
    {"name": "Нефтяной кризис", "affect_stocks": True, "affect_crypto": False, "affect_business": True, "stock_impact": -30, "crypto_impact": 0, "business_impact": -15, "duration_hours": 3},
    {"name": "Прорыв в AI", "affect_stocks": True, "affect_crypto": True, "affect_business": False, "stock_impact": 15, "crypto_impact": 10, "business_impact": 0, "duration_hours": 8},
    {"name": "Пандемия", "affect_stocks": True, "affect_crypto": True, "affect_business": True, "stock_impact": -35, "crypto_impact": -25, "business_impact": -40, "duration_hours": 12},
    {"name": "Золотая лихорадка", "affect_stocks": True, "affect_crypto": True, "affect_business": False, "stock_impact": 10, "crypto_impact": 30, "business_impact": 0, "duration_hours": 5},
    {"name": "Банковский кризис", "affect_stocks": True, "affect_crypto": True, "affect_business": True, "stock_impact": -25, "crypto_impact": 15, "business_impact": -20, "duration_hours": 6},
    {"name": "Зелёная энергия", "affect_stocks": True, "affect_crypto": False, "affect_business": True, "stock_impact": 20, "crypto_impact": 0, "business_impact": 10, "duration_hours": 4},
]

REPUTATION_LEVELS: Dict[ReputationLevel, Dict[str, Any]] = {
    ReputationLevel.HATED: {"min_score": -9999, "max_score": -50, "color": "dark_red", "title": "Изгой"},
    ReputationLevel.DISLIKED: {"min_score": -49, "max_score": -10, "color": "red", "title": "Недоброжелатель"},
    ReputationLevel.NEUTRAL: {"min_score": -9, "max_score": 9, "color": "gray", "title": "Нейтрал"},
    ReputationLevel.LIKED: {"min_score": 10, "max_score": 49, "color": "green", "title": "Приятный"},
    ReputationLevel.RESPECTED: {"min_score": 50, "max_score": 199, "color": "blue", "title": "Уважаемый"},
    ReputationLevel.BELOVED: {"min_score": 200, "max_score": 999, "color": "purple", "title": "Любимчик"},
    ReputationLevel.LEGENDARY: {"min_score": 1000, "max_score": 99999, "color": "gold", "title": "Легенда"},
}

ADMIN_PERMISSIONS: Dict[int, List[str]] = {
    1: ["balance", "work", "casino", "profile"],
    2: ["balance", "work", "casino", "profile", "report"],
    3: ["balance", "work", "casino", "profile", "report", "warn"],
    4: ["balance", "work", "casino", "profile", "report", "warn", "mute"],
    5: ["balance", "work", "casino", "profile", "report", "warn", "mute", "kick", "clear_chat"],
    6: ["balance", "work", "casino", "profile", "report", "warn", "mute", "kick", "clear_chat", "chat_settings"],
    7: ["balance", "work", "casino", "profile", "report", "warn", "mute", "kick", "clear_chat", "chat_settings", "assign_admin"],
    8: ["balance", "work", "casino", "profile", "report", "warn", "mute", "kick", "clear_chat", "chat_settings", "assign_admin", "ii_mod"],
    9: ["balance", "work", "casino", "profile", "report", "warn", "mute", "kick", "clear_chat", "chat_settings", "assign_admin", "ii_mod", "antibot"],
    10: ["balance", "work", "casino", "profile", "report", "warn", "mute", "kick", "clear_chat", "chat_settings", "assign_admin", "ii_mod", "antibot", "ban", "all_chat_perms"],
}

SUPER_ADMIN_PERMISSIONS: List[str] = [
    "all", "global_ban", "global_unban", "blacklist", "broadcast", "economy_control",
    "reset_users", "view_all_stats", "global_crisis", "global_boom", "stop_bot",
    "restart_bot", "export_data", "import_data", "sudo"
]

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
    level_bonus = base_income * (business.level - 1) * 0.2    total = int(base_income + employee_bonus + level_bonus)
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

print("✅ models.py загружен (полная версия)")
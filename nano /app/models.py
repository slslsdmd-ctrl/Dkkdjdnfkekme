from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from enum import Enum, auto
from datetime import datetime, timedelta
import json, uuid, hashlib, re

SUPER_ADMIN_ID = 8039111975
SUPER_ADMIN_LEVEL = 10
DEFAULT_STARTING_BALANCE = 100
MAX_BALANCE = 999_999_999_999
BOT_NAME = "фабле"
MAX_WARNS_BEFORE_BAN = 5
MAX_CLAN_MEMBERS = 50
CLAN_CREATION_COST = 50000
MARRIAGE_COST = 5000
DIVORCE_COST = 5000
MAX_BUSINESSES_PER_USER = 25
MAX_BUSINESS_LEVEL = 10
CASINO_MIN_BET = 10
CASINO_MAX_BET = 1_000_000
INSURANCE_DURATION_DAYS = 30
MAX_PET_LEVEL = 100
AUCTION_DURATION_HOURS_DEFAULT = 24
AUCTION_BID_MIN_INCREMENT = 10
MIN_DEPOSIT_AMOUNT = 100
MAX_DEPOSIT_AMOUNT = 10_000_000
MIN_LOAN_AMOUNT = 1000
MAX_LOAN_AMOUNT = 5_000_000
LOAN_INTEREST_RATE = 0.15
LOAN_DEFAULT_DURATION_DAYS = 30
BONUS_COOLDOWN_HOURS = 3
DEFAULT_MUTE_DURATION_MINUTES = 60
MAX_MUTE_DURATION_MINUTES = 43200
MIN_BALANCE = 0
BUSINESS_CREATION_COST = 5000

class UserRole(Enum):
    USER = "user"; MODERATOR = "moderator"; ADMIN = "admin"; SUPER_ADMIN = "super_admin"; CREATOR = "creator"

class ModActionType(Enum):
    WARN = "warn"; MUTE = "mute"; UNMUTE = "unmute"; KICK = "kick"; BAN = "ban"; UNBAN = "unban"; CLEAR = "clear"; LOCK = "lock"; UNLOCK = "unlock"; SLOWMODE = "slowmode"

class BusinessStatus(Enum):
    ACTIVE = "active"; BANKRUPT = "bankrupt"; SOLD = "sold"; FROZEN = "frozen"

class TransactionType(Enum):
    WORK = "work"; BONUS = "bonus"; TRANSFER_IN = "transfer_in"; TRANSFER_OUT = "transfer_out"
    BUSINESS_INCOME = "business_income"; BUSINESS_UPGRADE = "business_upgrade"; BUSINESS_PURCHASE = "business_purchase"; BUSINESS_SALE = "business_sale"
    CRYPTO_BUY = "crypto_buy"; CRYPTO_SELL = "crypto_sell"; STOCK_BUY = "stock_buy"; STOCK_SELL = "stock_sell"; DIVIDEND = "dividend"
    BANK_DEPOSIT = "bank_deposit"; BANK_WITHDRAW = "bank_withdraw"; LOAN_TAKE = "loan_take"; LOAN_REPAY = "loan_repay"
    CASINO_BET = "casino_bet"; CASINO_WIN = "casino_win"; AUCTION_BID = "auction_bid"; AUCTION_SALE = "auction_sale"
    ROBBERY_LOOT = "robbery_loot"; ROBBERY_LOSS = "robbery_loss"; TAX_AUDIT_FINE = "tax_audit_fine"
    CLAN_CREATION = "clan_creation"; CLAN_DEPOSIT = "clan_deposit"; CLAN_WAR_LOOT = "clan_war_loot"
    MARRIAGE_COST = "marriage_cost"; DIVORCE_COST = "divorce_cost"; INSURANCE_PURCHASE = "insurance_purchase"; INSURANCE_PAYOUT = "insurance_payout"
    ADMIN_GIFT = "admin_gift"; ADMIN_SEIZE = "admin_seize"; SYSTEM_ADJUSTMENT = "system_adjustment"

class GameType(Enum):
    SLOTS = "slots"; DICE = "dice"; COINFLIP = "coinflip"; DUEL = "duel"; RUSSIAN_ROULETTE = "russian_roulette"; WHEEL = "wheel"

class AuctionStatus(Enum):
    ACTIVE = "active"; ENDED = "ended"; CANCELLED = "cancelled"; SOLD = "sold"

class ClanWarStatus(Enum):
    PENDING = "pending"; ACTIVE = "active"; FINISHED = "finished"; DECLINED = "declined"

class MarriageStatus(Enum):
    SINGLE = "single"; MARRIED = "married"; DIVORCED = "divorced"

class PetRarity(Enum):
    COMMON = "common"; UNCOMMON = "uncommon"; RARE = "rare"; EPIC = "epic"; LEGENDARY = "legendary"

class PetMood(Enum):
    HAPPY = "happy"; NEUTRAL = "neutral"; SAD = "sad"; HUNGRY = "hungry"; SICK = "sick"

class ItemRarity(Enum):
    COMMON = "common"; UNCOMMON = "uncommon"; RARE = "rare"; EPIC = "epic"; LEGENDARY = "legendary"; MYTHIC = "mythic"

class ItemCategory(Enum):
    WORK_BOOSTER = "work_booster"; BUSINESS_BOOSTER = "business_booster"; CASINO_LUCK = "casino_luck"; ROBBERY_TOOL = "robbery_tool"; COSMETIC = "cosmetic"; COLLECTIBLE = "collectible"

class MinerType(Enum):
    USB = "usb"; HOME_FARM = "home_farm"; GARAGE_FARM = "garage_farm"; INDUSTRIAL = "industrial"; HOTEL = "hotel"

class ReputationLevel(Enum):
    HATED = "hated"; DISLIKED = "disliked"; NEUTRAL = "neutral"; LIKED = "liked"; RESPECTED = "respected"; BELOVED = "beloved"; LEGENDARY = "legendary"

class AchievementCategory(Enum):
    MONEY = "money"; BUSINESS = "business"; CRYPTO = "crypto"; STOCKS = "stocks"; CASINO = "casino"; CRIME = "crime"; CLAN = "clan"; SOCIAL = "social"; SPECIAL = "special"

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
    reputation_score: int = 0
    karma: int = 0
    marriage_status: MarriageStatus = MarriageStatus.SINGLE
    spouse_id: Optional[int] = None
    achievements: Set[int] = field(default_factory=set)
    last_seen: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    global_blacklisted: bool = False
    muted_until: Optional[datetime] = None
    jailed_until: Optional[datetime] = None
    house_id: Optional[str] = None
    health: int = 100
    stress: int = 0
    is_sick: bool = False
    has_ip: bool = False
    ip_name: str = ""
    car_id: Optional[str] = None
    car_fuel: int = 100
    is_employed: bool = False
    job_salary: int = 0
    has_insurance: bool = False
    credit_history: float = 1.0
    loan_blocked: bool = False
    work_blocked: bool = False
    tax_debt: int = 0
    quests: Dict[str, int] = field(default_factory=dict)
    bonus_streak: int = 0
    last_bonus_date: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["achievements"] = list(self.achievements)
        data["last_bonus_time"] = self.last_bonus_time.isoformat() if self.last_bonus_time else None
        data["loan_due_date"] = self.loan_due_date.isoformat() if self.loan_due_date else None
        data["jailed_until"] = self.jailed_until.isoformat() if self.jailed_until else None
        data["last_seen"] = self.last_seen.isoformat()
        data["created_at"] = self.created_at.isoformat()
        data["muted_until"] = self.muted_until.isoformat() if self.muted_until else None
        data["marriage_status"] = self.marriage_status.value
        data["last_bonus_date"] = self.last_bonus_date.isoformat() if self.last_bonus_date else None
        data["quests"] = self.quests
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        data["achievements"] = set(data.get("achievements", []))
        data["last_bonus_time"] = datetime.fromisoformat(data["last_bonus_time"]) if data.get("last_bonus_time") else None
        data["loan_due_date"] = datetime.fromisoformat(data["loan_due_date"]) if data.get("loan_due_date") else None
        data["jailed_until"] = datetime.fromisoformat(data["jailed_until"]) if data.get("jailed_until") else None
        data["last_seen"] = datetime.fromisoformat(data["last_seen"]) if isinstance(data.get("last_seen"), str) else data.get("last_seen", datetime.now())
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        data["muted_until"] = datetime.fromisoformat(data["muted_until"]) if data.get("muted_until") else None
        data["marriage_status"] = MarriageStatus(data.get("marriage_status", "single"))
        data["last_bonus_date"] = datetime.fromisoformat(data["last_bonus_date"]) if data.get("last_bonus_date") else None
        data["quests"] = data.get("quests", {})
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class ChatConfig:
    chat_id: int
    chat_title: str = ""
    rules: str = ""
    slowmode_seconds: int = 0
    is_locked: bool = False
    antispam_enabled: bool = False
    welcome_message: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatConfig":
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

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

@dataclass
class CryptoAsset:
    ticker: str; name: str; current_price: float; previous_price: float = 0.0
    change_percent: float = 0.0; last_updated: datetime = field(default_factory=datetime.now)
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
    last_updated: datetime = field(default_factory=datetime.now)
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
    total_invested_crypto: int = 0; total_invested_stocks: int = 0
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
class Clan:
    clan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""; leader_id: int = 0; members: List[int] = field(default_factory=list)
    treasury: int = 0; logo_emoji: str = "🏰"; wars_won: int = 0; wars_lost: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["created_at"] = self.created_at.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Clan":
        data["created_at"] = datetime.fromisoformat(data["created_at"]) if isinstance(data.get("created_at"), str) else data.get("created_at", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class Transaction:
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int = 0; amount: int = 0
    transaction_type: TransactionType = TransactionType.WORK
    balance_after: int = 0; description: str = ""
    related_user_id: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self); data["transaction_type"] = self.transaction_type.value; data["timestamp"] = self.timestamp.isoformat(); return data
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        data["transaction_type"] = TransactionType(data["transaction_type"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"]) if isinstance(data.get("timestamp"), str) else data.get("timestamp", datetime.now())
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

def generate_id() -> str: return str(uuid.uuid4())
def is_super_admin(user_id: int) -> bool: return user_id == SUPER_ADMIN_ID

print("✅ models.py загружен")
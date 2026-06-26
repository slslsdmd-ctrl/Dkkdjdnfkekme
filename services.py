
# Часть 2: Основные сервисы/классы (ядро)
# Модуль: services.py

from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from datetime import datetime, timedelta
import random
import json
import asyncio
import logging
from dataclasses import asdict

# Импорты из models.py
from models import (
    User, ChatConfig, AdminLevel, ModLog, Business, CryptoAsset,
    StockAsset, UserPortfolio, Miner, Auction, Clan, ClanWar,
    Tournament, Pet, ShopItem, UserInventory, Achievement,
    Transaction, GameSession, Report, GlobalEconomy, Earth,
    Vehicle, House, Insurance, BlacklistEntry, ChatStats,
    WorldEvent, UserRole, ModActionType, BusinessStatus,
    OrderType, AssetType, TransactionType, GameType,
    AuctionStatus, ClanWarStatus, MarriageStatus,
    InsuranceClaimReason, TournamentStatus, TournamentType,
    PetRarity, PetMood, EarthRegion, ItemRarity, ItemCategory,
    MinerType, ReputationLevel, AchievementCategory,
    StickerBlockMode, GifBlockMode, IIModMode,
    DEFAULT_STARTING_BALANCE, MIN_BALANCE, MAX_BALANCE,
    BONUS_COOLDOWN_HOURS, BONUS_AMOUNT_PER_MESSAGE,
    BONUS_PER_MESSAGE_AFTER, BANK_INTEREST_RATE_PER_HOUR,
    MAX_DEPOSIT_AMOUNT, MIN_DEPOSIT_AMOUNT, MAX_LOAN_AMOUNT,
    MIN_LOAN_AMOUNT, LOAN_INTEREST_RATE, LOAN_DEFAULT_DURATION_DAYS,
    BUSINESS_CREATION_COST, MAX_BUSINESSES_PER_USER,
    MAX_BUSINESS_LEVEL, BUSINESS_UPGRADE_COST_MULTIPLIER,
    CRYPTO_UPDATE_INTERVAL_MINUTES, STOCK_UPDATE_INTERVAL_MINUTES,
    DIVIDEND_INTERVAL_HOURS, CASINO_MIN_BET, CASINO_MAX_BET,
    SLOTS_SYMBOLS, ROBBERY_SUCCESS_RATE_BANK,
    ROBBERY_SUCCESS_RATE_CASINO, ROBBERY_SUCCESS_RATE_PLAYER,
    ROBBERY_JAIL_HOURS, ROBBERY_MAX_LOOT_PERCENT,
    TAX_AUDIT_CHANCE, TAX_AUDIT_FINE_PERCENT,
    MAX_WARNS_BEFORE_BAN, WARN_EXPIRATION_DAYS,
    DEFAULT_MUTE_DURATION_MINUTES, MAX_MUTE_DURATION_MINUTES,
    MAX_CLAN_MEMBERS, CLAN_CREATION_COST,
    CLAN_WAR_DURATION_HOURS, CLAN_WAR_LOOT_PERCENT,
    MARRIAGE_COST, DIVORCE_COST, MARRIAGE_INCOME_BONUS,
    INSURANCE_COST_PERCENT, INSURANCE_RETURN_PERCENT,
    INSURANCE_DURATION_DAYS, INSURANCE_MIN_BALANCE,
    REPUTATION_VOTE_COOLDOWN_HOURS,
    REPUTATION_MUTUAL_LIMIT_PER_WEEK, REPUTATION_LOW_THRESHOLD,
    MAX_PET_LEVEL, PET_EVOLUTION_LEVEL,
    PET_BREEDING_COOLDOWN_DAYS, PET_MUTATION_CHANCE,
    ACHIEVEMENTS_COUNT, MINER_TYPES,
    MINER_EFFICIENCY_DECAY_WEEKLY,
    MINER_ELECTRICITY_COST_PERCENT,
    MINER_REPAIR_COST_PERCENT,
    ITEM_RARITY_LEVELS, RARE_ITEM_DROP_CHANCE,
    LEGENDARY_ITEM_DROP_CHANCE,
    TOURNAMENT_MIN_PLAYERS, TOURNAMENT_MAX_PLAYERS,
    TOURNAMENT_ENTRY_FEE_MIN, TOURNAMENT_PRIZE_POOL_PERCENT,
    EARTH_REGIONS, VEHICLE_TYPES, HOUSE_TYPES,
    STICKER_BLOCK_MODE, GIF_BLOCK_MODE,
    SUPER_ADMIN_ID, SUPER_ADMIN_LEVEL,
    BUSINESS_TYPES, CRYPTO_ASSETS_CONFIG,
    STOCK_ASSETS_CONFIG, MINER_CONFIG,
    HOUSE_CONFIG, VEHICLE_CONFIG, SHOP_ITEMS_CONFIG,
    ACHIEVEMENTS_CONFIG, PET_SPECIES, PROFESSIONS,
    WORLD_EVENTS_POOL, REPUTATION_LEVELS,
    ADMIN_PERMISSIONS, SUPER_ADMIN_PERMISSIONS,
    generate_id, validate_amount, validate_string_length,
    validate_duration_minutes, parse_duration,
    get_reputation_level, calculate_business_income,
    calculate_miner_income, is_super_admin,
    get_permissions_for_level, has_permission,
)


# ============================================================
# ХРАНИЛИЩЕ ДАННЫХ (IN-MEMORY С ПЕРСИСТЕНТНОСТЬЮ)
# ============================================================

class DataStore:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.chats: Dict[int, ChatConfig] = {}
        self.admin_levels: Dict[Tuple[int, int], AdminLevel] = {}
        self.mod_logs: List[ModLog] = []
        self.businesses: Dict[str, Business] = {}
        self.crypto_assets: Dict[str, CryptoAsset] = {}
        self.stock_assets: Dict[str, StockAsset] = {}
        self.portfolios: Dict[int, UserPortfolio] = {}
        self.miners: Dict[str, Miner] = {}
        self.auctions: Dict[str, Auction] = {}
        self.clans: Dict[str, Clan] = {}
        self.clan_wars: Dict[str, ClanWar] = {}
        self.tournaments: Dict[str, Tournament] = {}
        self.pets: Dict[str, Pet] = {}
        self.shop_items: Dict[str, ShopItem] = {}
        self.inventories: Dict[int, UserInventory] = {}
        self.achievements: Dict[int, Achievement] = {}
        self.transactions: List[Transaction] = []
        self.game_sessions: List[GameSession] = []
        self.reports: List[Report] = []
        self.global_economy: GlobalEconomy = GlobalEconomy()
        self.earths: Dict[str, Earth] = {}
        self.vehicles: Dict[str, Vehicle] = {}
        self.houses: Dict[str, House] = {}
        self.insurances: Dict[str, Insurance] = {}
        self.blacklist: Dict[int, BlacklistEntry] = {}
        self.chat_stats: Dict[int, ChatStats] = {}
        self.world_events: Dict[str, WorldEvent] = {}
        self.user_clans: Dict[int, str] = {}
        self.user_businesses: Dict[int, List[str]] = {}
        self.user_miners: Dict[int, List[str]] = {}
        self.user_earth: Dict[int, List[str]] = {}
        self.user_vehicles: Dict[int, List[str]] = {}
        self.user_houses: Dict[int, List[str]] = {}
        self.user_pets: Dict[int, List[str]] = {}
        self.active_games: Dict[int, List[str]] = {}
        self.command_cooldowns: Dict[int, Dict[str, datetime]] = {}
        self.message_counters: Dict[int, Dict[str, int]] = {}

    def get_user(self, user_id: int) -> User:
        if user_id not in self.users:
            self.users[user_id] = User(user_id=user_id)
        return self.users[user_id]

    def get_chat(self, chat_id: int) -> ChatConfig:
        if chat_id not in self.chats:
            self.chats[chat_id] = ChatConfig(chat_id=chat_id)
        return self.chats[chat_id]

    def get_admin_level(self, user_id: int, chat_id: int) -> int:
        if is_super_admin(user_id):
            return SUPER_ADMIN_LEVEL
        key = (user_id, chat_id)
        if key in self.admin_levels:
            return self.admin_levels[key].level
        return 0

    def set_admin_level(self, user_id: int, chat_id: int, level: int, assigned_by: int = 0, is_creator: bool = False) -> AdminLevel:
        key = (user_id, chat_id)
        admin_level = AdminLevel(
            user_id=user_id,
            chat_id=chat_id,
            level=level,
            assigned_by=assigned_by,
            is_creator=is_creator,
        )
        self.admin_levels[key] = admin_level
        return admin_level

    def remove_admin_level(self, user_id: int, chat_id: int) -> None:
        key = (user_id, chat_id)
        if key in self.admin_levels:
            del self.admin_levels[key]

    def add_mod_log(self, log: ModLog) -> None:
        self.mod_logs.append(log)

    def get_mod_logs_for_user(self, user_id: int, chat_id: int = 0) -> List[ModLog]:
        result = []
        for log in self.mod_logs:
            if log.target_id == user_id:
                if chat_id == 0 or log.chat_id == chat_id:
                    result.append(log)
        return result

    def get_active_warns(self, user_id: int, chat_id: int) -> List[ModLog]:
        result = []
        for log in self.mod_logs:
            if (log.target_id == user_id and log.chat_id == chat_id
                    and log.action == ModActionType.WARN and log.is_active):
                if log.expires_at is None or log.expires_at > datetime.now():
                    result.append(log)
                else:
                    log.is_active = False
        return result

    def get_active_mutes(self, user_id: int, chat_id: int) -> List[ModLog]:
        result = []
        for log in self.mod_logs:
            if (log.target_id == user_id and log.chat_id == chat_id
                    and log.action == ModActionType.MUTE and log.is_active):
                if log.expires_at is not None and log.expires_at > datetime.now():
                    result.append(log)
                else:
                    log.is_active = False
        return result

    def get_business(self, business_id: str) -> Optional[Business]:
        return self.businesses.get(business_id)

    def get_user_businesses(self, user_id: int) -> List[Business]:
        ids = self.user_businesses.get(user_id, [])
        return [self.businesses[bid] for bid in ids if bid in self.businesses]

    def add_business(self, business: Business) -> None:
        self.businesses[business.business_id] = business
        if business.owner_id not in self.user_businesses:
            self.user_businesses[business.owner_id] = []
        self.user_businesses[business.owner_id].append(business.business_id)

    def remove_business(self, business_id: str) -> None:
        if business_id in self.businesses:
            business = self.businesses[business_id]
            if business.owner_id in self.user_businesses:
                self.user_businesses[business.owner_id] = [
                    bid for bid in self.user_businesses[business.owner_id] if bid != business_id
                ]
            del self.businesses[business_id]

    def get_crypto_asset(self, ticker: str) -> Optional[CryptoAsset]:
        return self.crypto_assets.get(ticker.upper())

    def get_all_crypto_assets(self) -> List[CryptoAsset]:
        return list(self.crypto_assets.values())

    def get_stock_asset(self, ticker: str) -> Optional[StockAsset]:
        return self.stock_assets.get(ticker.upper())

    def get_all_stock_assets(self) -> List[StockAsset]:
        return list(self.stock_assets.values())

    def get_portfolio(self, user_id: int) -> UserPortfolio:
        if user_id not in self.portfolios:
            self.portfolios[user_id] = UserPortfolio(user_id=user_id)
        return self.portfolios[user_id]

    def get_miner(self, miner_id: str) -> Optional[Miner]:
        return self.miners.get(miner_id)

    def get_user_miners(self, user_id: int) -> List[Miner]:
        ids = self.user_miners.get(user_id, [])
        return [self.miners[mid] for mid in ids if mid in self.miners]

    def add_miner(self, miner: Miner) -> None:
        self.miners[miner.miner_id] = miner
        if miner.owner_id not in self.user_miners:
            self.user_miners[miner.owner_id] = []
        self.user_miners[miner.owner_id].append(miner.miner_id)

    def remove_miner(self, miner_id: str) -> None:
        if miner_id in self.miners:
            miner = self.miners[miner_id]
            if miner.owner_id in self.user_miners:
                self.user_miners[miner.owner_id] = [
                    mid for mid in self.user_miners[miner.owner_id] if mid != miner_id
                ]
            del self.miners[miner_id]

    def get_auction(self, auction_id: str) -> Optional[Auction]:
        return self.auctions.get(auction_id)

    def get_active_auctions(self) -> List[Auction]:
        return [a for a in self.auctions.values() if a.status == AuctionStatus.ACTIVE]

    def get_clan(self, clan_id: str) -> Optional[Clan]:
        return self.clans.get(clan_id)

    def get_clan_by_name(self, name: str) -> Optional[Clan]:
        for clan in self.clans.values():
            if clan.name.lower() == name.lower():
                return clan
        return None

    def get_user_clan(self, user_id: int) -> Optional[Clan]:
        clan_id = self.user_clans.get(user_id)
        if clan_id:
            return self.clans.get(clan_id)
        return None

    def add_clan_member(self, clan_id: str, user_id: int) -> None:
        clan = self.clans.get(clan_id)
        if clan and user_id not in clan.members:
            clan.members.append(user_id)
            self.user_clans[user_id] = clan_id

    def remove_clan_member(self, clan_id: str, user_id: int) -> None:
        clan = self.clans.get(clan_id)
        if clan and user_id in clan.members:
            clan.members.remove(user_id)
            if user_id in self.user_clans:
                del self.user_clans[user_id]

    def get_clan_war(self, war_id: str) -> Optional[ClanWar]:
        return self.clan_wars.get(war_id)

    def get_active_clan_wars(self) -> List[ClanWar]:
        return [w for w in self.clan_wars.values() if w.status == ClanWarStatus.ACTIVE]

    def get_tournament(self, tournament_id: str) -> Optional[Tournament]:
        return self.tournaments.get(tournament_id)

    def get_active_tournaments(self) -> List[Tournament]:
        return [t for t in self.tournaments.values() if t.status in (TournamentStatus.REGISTRATION, TournamentStatus.IN_PROGRESS)]

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        return self.pets.get(pet_id)

    def get_user_pets(self, user_id: int) -> List[Pet]:
        ids = self.user_pets.get(user_id, [])
        return [self.pets[pid] for pid in ids if pid in self.pets]

    def add_pet(self, pet: Pet) -> None:
        self.pets[pet.pet_id] = pet
        if pet.owner_id not in self.user_pets:
            self.user_pets[pet.owner_id] = []
        self.user_pets[pet.owner_id].append(pet.pet_id)

    def remove_pet(self, pet_id: str) -> None:
        if pet_id in self.pets:
            pet = self.pets[pet_id]
            if pet.owner_id in self.user_pets:
                self.user_pets[pet.owner_id] = [
                    pid for pid in self.user_pets[pet.owner_id] if pid != pet_id
                ]
            del self.pets[pet_id]

    def get_shop_item(self, item_id: str) -> Optional[ShopItem]:
        return self.shop_items.get(item_id)

    def get_all_shop_items(self) -> List[ShopItem]:
        return list(self.shop_items.values())

    def get_inventory(self, user_id: int) -> UserInventory:
        if user_id not in self.inventories:
            self.inventories[user_id] = UserInventory(user_id=user_id)
        return self.inventories[user_id]

    def get_achievement(self, achievement_id: int) -> Optional[Achievement]:
        return self.achievements.get(achievement_id)

    def get_all_achievements(self) -> List[Achievement]:
        return list(self.achievements.values())

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def get_user_transactions(self, user_id: int, limit: int = 20) -> List[Transaction]:
        result = [t for t in self.transactions if t.user_id == user_id]
        result.sort(key=lambda x: x.timestamp, reverse=True)
        return result[:limit]

    def add_game_session(self, session: GameSession) -> None:
        self.game_sessions.append(session)

    def get_user_game_sessions(self, user_id: int, game_type: Optional[GameType] = None) -> List[GameSession]:
        result = [s for s in self.game_sessions if s.user_id == user_id]
        if game_type:
            result = [s for s in result if s.game_type == game_type]
        result.sort(key=lambda x: x.timestamp, reverse=True)
        return result

    def add_report(self, report: Report) -> None:
        self.reports.append(report)

    def get_pending_reports(self, chat_id: int = 0) -> List[Report]:
        result = [r for r in self.reports if r.status == "pending"]
        if chat_id > 0:
            result = [r for r in result if r.chat_id == chat_id]
        return result

    def get_earth(self, earth_id: str) -> Optional[Earth]:
        return self.earths.get(earth_id)

    def get_user_earth(self, user_id: int) -> List[Earth]:
        ids = self.user_earth.get(user_id, [])
        return [self.earths[eid] for eid in ids if eid in self.earths]

    def add_earth(self, earth: Earth) -> None:
        self.earths[earth.earth_id] = earth
        if earth.owner_id not in self.user_earth:
            self.user_earth[earth.owner_id] = []
        self.user_earth[earth.owner_id].append(earth.earth_id)

    def remove_earth(self, earth_id: str) -> None:
        if earth_id in self.earths:
            earth = self.earths[earth_id]
            if earth.owner_id in self.user_earth:
                self.user_earth[earth.owner_id] = [
                    eid for eid in self.user_earth[earth.owner_id] if eid != earth_id
                ]
            del self.earths[earth_id]

    def get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]:
        return self.vehicles.get(vehicle_id)

    def get_user_vehicles(self, user_id: int) -> List[Vehicle]:
        ids = self.user_vehicles.get(user_id, [])
        return [self.vehicles[vid] for vid in ids if vid in self.vehicles]

    def add_vehicle(self, vehicle: Vehicle) -> None:
        self.vehicles[vehicle.vehicle_id] = vehicle
        if vehicle.owner_id not in self.user_vehicles:
            self.user_vehicles[vehicle.owner_id] = []
        self.user_vehicles[vehicle.owner_id].append(vehicle.vehicle_id)

    def remove_vehicle(self, vehicle_id: str) -> None:
        if vehicle_id in self.vehicles:
            vehicle = self.vehicles[vehicle_id]
            if vehicle.owner_id in self.user_vehicles:
                self.user_vehicles[vehicle.owner_id] = [
                    vid for vid in self.user_vehicles[vehicle.owner_id] if vid != vehicle_id
                ]
            del self.vehicles[vehicle_id]

    def get_house(self, house_id: str) -> Optional[House]:
        return self.houses.get(house_id)

    def get_user_houses(self, user_id: int) -> List[House]:
        ids = self.user_houses.get(user_id, [])
        return [self.houses[hid] for hid in ids if hid in self.houses]

    def add_house(self, house: House) -> None:
        self.houses[house.house_id] = house
        if house.owner_id not in self.user_houses:
            self.user_houses[house.owner_id] = []
        self.user_houses[house.owner_id].append(house.house_id)

    def remove_house(self, house_id: str) -> None:
        if house_id in self.houses:
            house = self.houses[house_id]
            if house.owner_id in self.user_houses:
                self.user_houses[house.owner_id] = [
                    hid for hid in self.user_houses[house.owner_id] if hid != house_id
                ]
            del self.houses[house_id]

    def get_insurance(self, insurance_id: str) -> Optional[Insurance]:
        return self.insurances.get(insurance_id)

    def get_user_active_insurance(self, user_id: int) -> Optional[Insurance]:
        for insurance in self.insurances.values():
            if insurance.user_id == user_id and insurance.active:
                if insurance.expires_at > datetime.now():
                    return insurance
                else:
                    insurance.active = False
        return None

    def is_blacklisted(self, user_id: int) -> bool:
        return user_id in self.blacklist

    def add_blacklist(self, entry: BlacklistEntry) -> None:
        self.blacklist[entry.user_id] = entry

    def remove_blacklist(self, user_id: int) -> None:
        if user_id in self.blacklist:
            del self.blacklist[user_id]

    def get_chat_stats(self, chat_id: int) -> ChatStats:
        if chat_id not in self.chat_stats:
            self.chat_stats[chat_id] = ChatStats(chat_id=chat_id)
        return self.chat_stats[chat_id]

    def get_world_event(self, event_id: str) -> Optional[WorldEvent]:
        return self.world_events.get(event_id)

    def get_active_world_events(self) -> List[WorldEvent]:
        return [e for e in self.world_events.values() if e.active]

    def set_command_cooldown(self, user_id: int, command: str, cooldown_minutes: int) -> None:
        if user_id not in self.command_cooldowns:
            self.command_cooldowns[user_id] = {}
        self.command_cooldowns[user_id][command] = datetime.now() + timedelta(minutes=cooldown_minutes)

    def is_on_cooldown(self, user_id: int, command: str) -> bool:
        if user_id in self.command_cooldowns:
            if command in self.command_cooldowns[user_id]:
                return datetime.now() < self.command_cooldowns[user_id][command]
        return False

    def get_cooldown_remaining(self, user_id: int, command: str) -> int:
        if self.is_on_cooldown(user_id, command):
            remaining = self.command_cooldowns[user_id][command] - datetime.now()
            return max(0, int(remaining.total_seconds()))
        return 0

    def increment_message_counter(self, user_id: int, counter_type: str) -> int:
        if user_id not in self.message_counters:
            self.message_counters[user_id] = {}
        if counter_type not in self.message_counters[user_id]:
            self.message_counters[user_id][counter_type] = 0
        self.message_counters[user_id][counter_type] += 1
        return self.message_counters[user_id][counter_type]

    def get_message_counter(self, user_id: int, counter_type: str) -> int:
        if user_id in self.message_counters:
            return self.message_counters[user_id].get(counter_type, 0)
        return 0

    def reset_message_counter(self, user_id: int, counter_type: str) -> None:
        if user_id in self.message_counters:
            if counter_type in self.message_counters[user_id]:
                self.message_counters[user_id][counter_type] = 0

    def can_user_start_game(self, user_id: int) -> bool:
        active = self.active_games.get(user_id, [])
        return len(active) < 3

    def register_game_start(self, user_id: int, session_id: str) -> None:
        if user_id not in self.active_games:
            self.active_games[user_id] = []
        self.active_games[user_id].append(session_id)

    def register_game_end(self, user_id: int, session_id: str) -> None:
        if user_id in self.active_games:
            if session_id in self.active_games[user_id]:
                self.active_games[user_id].remove(session_id)

    def get_total_users(self) -> int:
        return len(self.users)

    def get_total_chats(self) -> int:
        return len(self.chats)

    def get_active_users_today(self) -> int:
        today = datetime.now().date()
        count = 0
        for user in self.users.values():
            if user.last_seen.date() == today:
                count += 1
        return count

    def get_total_money_in_circulation(self) -> int:
        total = sum(user.balance + user.bank_balance for user in self.users.values())
        return total

    def save_to_disk(self, filepath: str) -> None:
        try:
            data = {
                "users": {str(k): v.to_dict() for k, v in self.users.items()},
                "chats": {str(k): v.to_dict() for k, v in self.chats.items()},
                "admin_levels": {f"{k[0]}_{k[1]}": v.to_dict() for k, v in self.admin_levels.items()},
                "mod_logs": [log.to_dict() for log in self.mod_logs],
                "businesses": {k: v.to_dict() for k, v in self.businesses.items()},
                "crypto_assets": {k: v.to_dict() for k, v in self.crypto_assets.items()},
                "stock_assets": {k: v.to_dict() for k, v in self.stock_assets.items()},
                "portfolios": {str(k): v.to_dict() for k, v in self.portfolios.items()},
                "miners": {k: v.to_dict() for k, v in self.miners.items()},
                "auctions": {k: v.to_dict() for k, v in self.auctions.items()},
                "clans": {k: v.to_dict() for k, v in self.clans.items()},
                "clan_wars": {k: v.to_dict() for k, v in self.clan_wars.items()},
                "tournaments": {k: v.to_dict() for k, v in self.tournaments.items()},
                "pets": {k: v.to_dict() for k, v in self.pets.items()},
                "inventories": {str(k): v.to_dict() for k, v in self.inventories.items()},
                "transactions": [t.to_dict() for t in self.transactions[-10000:]],
                "reports": [r.to_dict() for r in self.reports],
                "global_economy": self.global_economy.to_dict(),
                "earths": {k: v.to_dict() for k, v in self.earths.items()},
                "vehicles": {k: v.to_dict() for k, v in self.vehicles.items()},
                "houses": {k: v.to_dict() for k, v in self.houses.items()},
                "insurances": {k: v.to_dict() for k, v in self.insurances.items()},
                "blacklist": {str(k): v.to_dict() for k, v in self.blacklist.items()},
                "chat_stats": {str(k): v.to_dict() for k, v in self.chat_stats.items()},
                "user_clans": {str(k): v for k, v in self.user_clans.items()},
                "user_businesses": {str(k): v for k, v in self.user_businesses.items()},
                "user_miners": {str(k): v for k, v in self.user_miners.items()},
                "user_earth": {str(k): v for k, v in self.user_earth.items()},
                "user_vehicles": {str(k): v for k, v in self.user_vehicles.items()},
                "user_houses": {str(k): v for k, v in self.user_houses.items()},
                "user_pets": {str(k): v for k, v in self.user_pets.items()},
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Ошибка сохранения данных: {e}")

    def load_from_disk(self, filepath: str) -> bool:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.users = {int(k): User.from_dict(v) for k, v in data.get("users", {}).items()}
            self.chats = {int(k): ChatConfig.from_dict(v) for k, v in data.get("chats", {}).items()}
            self.admin_levels = {}
            for k, v in data.get("admin_levels", {}).items():
                parts = k.split("_")
                if len(parts) == 2:
                    self.admin_levels[(int(parts[0]), int(parts[1]))] = AdminLevel.from_dict(v)
            self.mod_logs = [ModLog.from_dict(v) for v in data.get("mod_logs", [])]
            self.businesses = {k: Business.from_dict(v) for k, v in data.get("businesses", {}).items()}
            self.crypto_assets = {k: CryptoAsset.from_dict(v) for k, v in data.get("crypto_assets", {}).items()}
            self.stock_assets = {k: StockAsset.from_dict(v) for k, v in data.get("stock_assets", {}).items()}
            self.portfolios = {int(k): UserPortfolio.from_dict(v) for k, v in data.get("portfolios", {}).items()}
            self.miners = {k: Miner.from_dict(v) for k, v in data.get("miners", {}).items()}
            self.auctions = {k: Auction.from_dict(v) for k, v in data.get("auctions", {}).items()}
            self.clans = {k: Clan.from_dict(v) for k, v in data.get("clans", {}).items()}
            self.clan_wars = {k: ClanWar.from_dict(v) for k, v in data.get("clan_wars", {}).items()}
            self.tournaments = {k: Tournament.from_dict(v) for k, v in data.get("tournaments", {}).items()}
            self.pets = {k: Pet.from_dict(v) for k, v in data.get("pets", {}).items()}
            self.inventories = {int(k): UserInventory.from_dict(v) for k, v in data.get("inventories", {}).items()}
            self.transactions = [Transaction.from_dict(v) for v in data.get("transactions", [])]
            self.reports = [Report.from_dict(v) for v in data.get("reports", [])]
            if "global_economy" in data:
                self.global_economy = GlobalEconomy.from_dict(data["global_economy"])
            self.earths = {k: Earth.from_dict(v) for k, v in data.get("earths", {}).items()}
            self.vehicles = {k: Vehicle.from_dict(v) for k, v in data.get("vehicles", {}).items()}
            self.houses = {k: House.from_dict(v) for k, v in data.get("houses", {}).items()}
            self.insurances = {k: Insurance.from_dict(v) for k, v in data.get("insurances", {}).items()}
            self.blacklist = {int(k): BlacklistEntry.from_dict(v) for k, v in data.get("blacklist", {}).items()}
            self.chat_stats = {int(k): ChatStats.from_dict(v) for k, v in data.get("chat_stats", {}).items()}
            self.user_clans = {int(k): v for k, v in data.get("user_clans", {}).items()}
            self.user_businesses = {int(k): v for k, v in data.get("user_businesses", {}).items()}
            self.user_miners = {int(k): v for k, v in data.get("user_miners", {}).items()}
            self.user_earth = {int(k): v for k, v in data.get("user_earth", {}).items()}
            self.user_vehicles = {int(k): v for k, v in data.get("user_vehicles", {}).items()}
            self.user_houses = {int(k): v for k, v in data.get("user_houses", {}).items()}
            self.user_pets = {int(k): v for k, v in data.get("user_pets", {}).items()}
            return True
        except Exception as e:
            logging.error(f"Ошибка загрузки данных: {e}")
            return False


# ============================================================
# СЕРВИС ЭКОНОМИКИ
# ============================================================

class EconomyService:
    def __init__(self, store: DataStore):
        self.store = store

    def get_balance(self, user_id: int) -> int:
        user = self.store.get_user(user_id)
        return user.balance

    def add_money(self, user_id: int, amount: int, transaction_type: TransactionType,
                   description: str = "", related_user_id: Optional[int] = None) -> Tuple[bool, str, int]:
        valid, error = validate_amount(amount, 1, MAX_BALANCE)
        if not valid:
            return False, error, 0

        user = self.store.get_user(user_id)
        if user.balance + amount > MAX_BALANCE:
            return False, f"Баланс не может превышать {MAX_BALANCE}", 0

        user.balance += amount
        balance_after = user.balance

        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
            balance_after=balance_after,
            description=description,
            related_user_id=related_user_id,
        )
        self.store.add_transaction(transaction)
        return True, f"Получено {amount} монет", balance_after

    def remove_money(self, user_id: int, amount: int, transaction_type: TransactionType,
                      description: str = "", related_user_id: Optional[int] = None) -> Tuple[bool, str, int]:
        valid, error = validate_amount(amount, 1, MAX_BALANCE)
        if not valid:
            return False, error, 0

        user = self.store.get_user(user_id)
        if user.balance < amount:
            return False, f"Недостаточно средств. Баланс: {user.balance}", user.balance

        user.balance -= amount
        balance_after = user.balance

        transaction = Transaction(
            user_id=user_id,
            amount=-amount,
            transaction_type=transaction_type,
            balance_after=balance_after,
            description=description,
            related_user_id=related_user_id,
        )
        self.store.add_transaction(transaction)
        return True, f"Списано {amount} монет", balance_after

    def transfer_money(self, sender_id: int, receiver_id: int, amount: int) -> Tuple[bool, str]:
        if sender_id == receiver_id:
            return False, "Нельзя перевести деньги самому себе"

        success, error, _ = self.remove_money(
            sender_id, amount,
            TransactionType.TRANSFER_OUT,
            f"Перевод пользователю {receiver_id}",
            receiver_id
        )
        if not success:
            return False, error

        success, error, _ = self.add_money(
            receiver_id, amount,
            TransactionType.TRANSFER_IN,
            f"Перевод от пользователя {sender_id}",
            sender_id
        )
        if not success:
            self.add_money(
                sender_id, amount,
                TransactionType.TRANSFER_IN,
                f"Возврат перевода (ошибка зачисления)",
                receiver_id
            )
            return False, error

        return True, f"Переведено {amount} монет"

    def process_work(self, user_id: int) -> Tuple[bool, str, int]:
        user = self.store.get_user(user_id)

        if self.store.is_on_cooldown(user_id, "work"):
            remaining = self.store.get_cooldown_remaining(user_id, "work")
            return False, f"Работать можно раз в час. Осталось {remaining // 60} мин {remaining % 60} сек", 0

        profession = None
        for prof in reversed(PROFESSIONS):
            if user.level >= prof["min_level"]:
                profession = prof
                break

        if profession is None:
            return False, "Нет доступных профессий", 0

        base_income = profession["base_income"]
        level_bonus = base_income * (user.level - 1) * 0.05
        total = int(base_income + level_bonus)

        inventory = self.store.get_inventory(user_id)
        for item_id, expires_str in list(inventory.active_boosters.items()):
            if datetime.now() < datetime.fromisoformat(expires_str) if isinstance(expires_str, str) else expires_str:
                item = self.store.get_shop_item(item_id)
                if item and item.category == ItemCategory.WORK_BOOSTER:
                    total = int(total * (1 + item.boost_percent / 100))

        self.store.set_command_cooldown(user_id, "work", 60)

        success, error, balance = self.add_money(
            user_id, total,
            TransactionType.WORK,
            f"Работа: {profession['name']}"
        )

        if success:
            return True, f"Вы заработали {total} монет как {profession['name']}. Баланс: {balance}", total
        return False, error, 0

    def process_bonus(self, user_id: int) -> Tuple[bool, str, int]:
        user = self.store.get_user(user_id)

        if user.last_bonus_time:
            hours_passed = (datetime.now() - user.last_bonus_time).total_seconds() / 3600
            if hours_passed < BONUS_COOLDOWN_HOURS:
                remaining = BONUS_COOLDOWN_HOURS - hours_passed
                return False, f"Бонус доступен через {int(remaining)} ч {int((remaining % 1) * 60)} мин", 0

        msg_count = self.store.get_message_counter(user_id, "bonus_messages")
        if msg_count < 1:
            return False, "Напишите хотя бы 1 сообщение для бонуса", 0

        bonus_amount = BONUS_AMOUNT_PER_MESSAGE + (msg_count - 1) * BONUS_PER_MESSAGE_AFTER
        bonus_amount = min(bonus_amount, 1000)

        user.last_bonus_time = datetime.now()
        self.store.reset_message_counter(user_id, "bonus_messages")

        success, error, balance = self.add_money(
            user_id, bonus_amount,
            TransactionType.BONUS,
            f"Бонус за {msg_count} сообщений"
        )

        if success:
            return True, f"Бонус: {bonus_amount} монет за {msg_count} сообщений. Баланс: {balance}", bonus_amount
        return False, error, 0

    def get_top_balances(self, limit: int = 10, chat_id: Optional[int] = None) -> List[Tuple[int, int, str]]:
        users = sorted(self.store.users.values(), key=lambda u: u.balance, reverse=True)
        result = []
        for user in users:
            if len(result) >= limit:
                break
            name = user.first_name or user.username or str(user.user_id)
            result.append((user.user_id, user.balance, name))
        return result


# ============================================================
# СЕРВИС БАНКА
# ============================================================

class BankService:
    def __init__(self, store: DataStore):
        self.store = store

    def deposit(self, user_id: int, amount: int) -> Tuple[bool, str, int]:
        valid, error = validate_amount(amount, MIN_DEPOSIT_AMOUNT, MAX_DEPOSIT_AMOUNT)
        if not valid:
            return False, error, 0

        user = self.store.get_user(user_id)
        if user.balance < amount:
            return False, f"Недостаточно средств. Баланс: {user.balance}", user.balance

        user.balance -= amount
        user.bank_balance += amount

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-amount,
            transaction_type=TransactionType.BANK_DEPOSIT,
            balance_after=user.balance,
            description=f"Вклад в банк: {amount}",
        ))

        return True, f"Вклад {amount} монет принят. На счету в банке: {user.bank_balance}", user.balance

    def withdraw(self, user_id: int, amount: int) -> Tuple[bool, str, int]:
        valid, error = validate_amount(amount, 1, MAX_DEPOSIT_AMOUNT)
        if not valid:
            return False, error, 0

        user = self.store.get_user(user_id)
        if user.bank_balance < amount:
            return False, f"Недостаточно средств в банке. На счету: {user.bank_balance}", user.balance

        user.bank_balance -= amount
        user.balance += amount

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.BANK_WITHDRAW,
            balance_after=user.balance,
            description=f"Снятие с банка: {amount}",
        ))

        return True, f"Снято {amount} монет. Баланс: {user.balance}", user.balance

    def process_interest(self, user_id: int) -> Tuple[bool, str, int]:
        user = self.store.get_user(user_id)
        if user.bank_balance <= 0:
            return False, "Нет средств для начисления процентов", 0

        interest = int(user.bank_balance * BANK_INTEREST_RATE_PER_HOUR)
        if interest <= 0:
            interest = 1

        user.bank_balance += interest

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=interest,
            transaction_type=TransactionType.BANK_DEPOSIT,
            balance_after=user.balance,
            description=f"Проценты по вкладу: {interest}",
        ))

        return True, f"Начислено {interest} монет процентов. В банке: {user.bank_balance}", interest

    def take_loan(self, user_id: int, amount: int) -> Tuple[bool, str, int]:
        valid, error = validate_amount(amount, MIN_LOAN_AMOUNT, MAX_LOAN_AMOUNT)
        if not valid:
            return False, error, 0

        user = self.store.get_user(user_id)
        if user.loan_amount > 0:
            return False, f"У вас уже есть непогашенный кредит: {user.loan_amount}", 0

        total_debt = int(amount * (1 + LOAN_INTEREST_RATE))
        user.loan_amount = total_debt
        user.loan_due_date = datetime.now() + timedelta(days=LOAN_DEFAULT_DURATION_DAYS)
        user.balance += amount

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.LOAN_TAKE,
            balance_after=user.balance,
            description=f"Кредит: {amount} (к оплате: {total_debt})",
        ))

        return True, f"Кредит {amount} выдан. Вернуть нужно {total_debt} до {user.loan_due_date.strftime('%d.%m.%Y')}", user.balance

    def repay_loan(self, user_id: int, amount: int = 0) -> Tuple[bool, str, int]:
        user = self.store.get_user(user_id)
        if user.loan_amount <= 0:
            return False, "У вас нет кредита", user.balance

        repay_amount = amount if amount > 0 else user.loan_amount
        repay_amount = min(repay_amount, user.loan_amount)

        if user.balance < repay_amount:
            return False, f"Недостаточно средств. Нужно: {repay_amount}, баланс: {user.balance}", user.balance

        user.balance -= repay_amount
        user.loan_amount -= repay_amount

        if user.loan_amount <= 0:
            user.loan_amount = 0
            user.loan_due_date = None

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-repay_amount,
            transaction_type=TransactionType.LOAN_REPAY,
            balance_after=user.balance,
            description=f"Погашение кредита: {repay_amount}",
        ))

        return True, f"Погашено {repay_amount}. Остаток кредита: {user.loan_amount}", user.balance


# ============================================================
# СЕРВИС БИЗНЕСА
# ============================================================

class BusinessService:
    def __init__(self, store: DataStore):
        self.store = store

    def create_business(self, user_id: int, business_type: str, name: str) -> Tuple[bool, str, Optional[Business]]:
        user = self.store.get_user(user_id)
        current_businesses = self.store.get_user_businesses(user_id)

        if len(current_businesses) >= MAX_BUSINESSES_PER_USER:
            return False, f"Максимум {MAX_BUSINESSES_PER_USER} бизнесов", None

        config = None
        for bt in BUSINESS_TYPES:
            if bt["type"] == business_type or bt["name"].lower() == business_type.lower():
                config = bt
                break

        if config is None:
            return False, "Тип бизнеса не найден", None

        cost = config["base_price"]
        if user.balance < cost:
            return False, f"Недостаточно средств. Нужно: {cost}, баланс: {user.balance}", None

        user.balance -= cost

        business = Business(
            owner_id=user_id,
            name=name if name else config["name"],
            business_type=config["type"],
            purchase_price=cost,
            current_value=cost,
            hourly_income=config["base_income"],
            max_employees=config["max_employees"],
            franchise_cost=config["franchise_cost"],
        )
        self.store.add_business(business)

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-cost,
            transaction_type=TransactionType.BUSINESS_PURCHASE,
            balance_after=user.balance,
            description=f"Создание бизнеса: {business.name}",
            related_item_id=business.business_id,
        ))

        return True, f"Бизнес '{business.name}' создан за {cost} монет", business

    def collect_income(self, user_id: int, business_id: str) -> Tuple[bool, str, int]:
        business = self.store.get_business(business_id)
        if business is None:
            return False, "Бизнес не найден", 0
        if business.owner_id != user_id:
            return False, "Это не ваш бизнес", 0
        if business.status != BusinessStatus.ACTIVE:
            return False, f"Бизнес в статусе: {business.status.value}", 0

        income = calculate_business_income(business)
        inventory = self.store.get_inventory(user_id)
        for item_id, expires_str in list(inventory.active_boosters.items()):
            if datetime.now() < datetime.fromisoformat(expires_str) if isinstance(expires_str, str) else expires_str:
                item = self.store.get_shop_item(item_id)
                if item and item.category == ItemCategory.BUSINESS_BOOSTER:
                    income = int(income * (1 + item.boost_percent / 100))

        user = self.store.get_user(user_id)
        user.balance += income
        business.last_collected = datetime.now()

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=income,
            transaction_type=TransactionType.BUSINESS_INCOME,
            balance_after=user.balance,
            description=f"Прибыль бизнеса: {business.name}",
            related_item_id=business_id,
        ))

        return True, f"Собрано {income} монет с бизнеса '{business.name}'", income

    def upgrade_business(self, user_id: int, business_id: str) -> Tuple[bool, str, Optional[Business]]:
        business = self.store.get_business(business_id)
        if business is None:
            return False, "Бизнес не найден", None
        if business.owner_id != user_id:
            return False, "Это не ваш бизнес", None
        if business.level >= MAX_BUSINESS_LEVEL:
            return False, "Бизнес максимального уровня", None

        upgrade_cost = int(business.purchase_price * business.level * BUSINESS_UPGRADE_COST_MULTIPLIER)
        user = self.store.get_user(user_id)
        if user.balance < upgrade_cost:
            return False, f"Недостаточно средств. Нужно: {upgrade_cost}", None

        user.balance -= upgrade_cost
        business.level += 1
        business.hourly_income = int(business.hourly_income * 1.5)
        business.current_value += upgrade_cost

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-upgrade_cost,
            transaction_type=TransactionType.BUSINESS_UPGRADE,
            balance_after=user.balance,
            description=f"Прокачка бизнеса {business.name} до уровня {business.level}",
            related_item_id=business_id,
        ))

        return True, f"Бизнес '{business.name}' прокачан до уровня {business.level}", business

    def sell_business(self, user_id: int, business_id: str) -> Tuple[bool, str, int]:
        business = self.store.get_business(business_id)
        if business is None:
            return False, "Бизнес не найден", 0
        if business.owner_id != user_id:
            return False, "Это не ваш бизнес", 0

        sale_price = business.current_value
        if business.employees:
            severance = len(business.employees) * business.salary_per_employee * 2
            sale_price -= severance
            sale_price = max(sale_price, 0)

        user = self.store.get_user(user_id)
        user.balance += sale_price
        self.store.remove_business(business_id)

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=sale_price,
            transaction_type=TransactionType.BUSINESS_SALE,
            balance_after=user.balance,
            description=f"Продажа бизнеса {business.name}",
            related_item_id=business_id,
        ))

        return True, f"Бизнес продан за {sale_price} монет", sale_price

    def hire_employee(self, owner_id: int, business_id: str, employee_id: int) -> Tuple[bool, str]:
        business = self.store.get_business(business_id)
        if business is None:
            return False, "Бизнес не найден"
        if business.owner_id != owner_id:
            return False, "Это не ваш бизнес"
        if len(business.employees) >= business.max_employees:
            return False, f"Максимум {business.max_employees} сотрудников"
        if employee_id in business.employees:
            return False, "Этот пользователь уже работает у вас"

        business.employees.append(employee_id)
        return True, f"Сотрудник нанят. Всего: {len(business.employees)}"

    def fire_employee(self, owner_id: int, business_id: str, employee_id: int) -> Tuple[bool, str]:
        business = self.store.get_business(business_id)
        if business is None:
            return False, "Бизнес не найден"
        if business.owner_id != owner_id:
            return False, "Это не ваш бизнес"
        if employee_id not in business.employees:
            return False, "Этот пользователь не работает у вас"

        business.employees.remove(employee_id)
        return True, f"Сотрудник уволен. Осталось: {len(business.employees)}"


# ============================================================
# СЕРВИС КРИПТОВАЛЮТ И АКЦИЙ
# ============================================================

class MarketService:
    def __init__(self, store: DataStore):
        self.store = store

    def initialize_crypto_assets(self) -> None:
        for config in CRYPTO_ASSETS_CONFIG:
            asset = CryptoAsset(
                ticker=config["ticker"],
                name=config["name"],
                current_price=config["base_price"],
                previous_price=config["base_price"],
                all_time_high=config["base_price"],
                all_time_low=config["base_price"],
            )
            self.store.crypto_assets[asset.ticker] = asset

    def initialize_stock_assets(self) -> None:
        for config in STOCK_ASSETS_CONFIG:
            asset = StockAsset(
                ticker=config["ticker"],
                company_name=config["company_name"],
                current_price=config["base_price"],
                previous_price=config["base_price"],
                dividend_yield=config["dividend_yield"],
                sector=config["sector"],
            )
            self.store.stock_assets[asset.ticker] = asset

    def update_crypto_prices(self) -> None:
        events = self.store.get_active_world_events()
        event_impact = 0.0
        for event in events:
            if event.affect_crypto:
                event_impact += event.crypto_impact_percent / 100.0

        for ticker, asset in self.store.crypto_assets.items():
            config = next((c for c in CRYPTO_ASSETS_CONFIG if c["ticker"] == ticker), None)
            if config is None:
                continue

            volatility = config["volatility"]
            change = random.uniform(-volatility, volatility)
            change += event_impact

            asset.previous_price = asset.current_price
            new_price = asset.current_price * (1 + change)
            new_price = max(new_price, 0.01)
            asset.current_price = round(new_price, 2)
            asset.change_percent = round(change * 100, 2)
            asset.last_updated = datetime.now()

            if asset.current_price > asset.all_time_high:
                asset.all_time_high = asset.current_price
            if asset.current_price < asset.all_time_low:
                asset.all_time_low = asset.current_price

    def update_stock_prices(self) -> None:
        events = self.store.get_active_world_events()
        event_impact = 0.0
        for event in events:
            if event.affect_stocks:
                event_impact += event.stock_impact_percent / 100.0

        for ticker, asset in self.store.stock_assets.items():
            change = random.uniform(-0.15, 0.20)
            change += event_impact

            asset.previous_price = asset.current_price
            new_price = asset.current_price * (1 + change)
            new_price = max(new_price, 1.0)
            asset.current_price = round(new_price, 2)
            asset.change_percent = round(change * 100, 2)
            asset.last_updated = datetime.now()

    def buy_crypto(self, user_id: int, ticker: str, quantity: float) -> Tuple[bool, str, float]:
        asset = self.store.get_crypto_asset(ticker)
        if asset is None:
            return False, "Криптовалюта не найдена", 0

        cost = int(asset.current_price * quantity)
        if cost <= 0:
            return False, "Сумма покупки слишком мала", 0

        user = self.store.get_user(user_id)
        if user.balance < cost:
            return False, f"Недостаточно средств. Нужно: {cost}", 0

        user.balance -= cost

        portfolio = self.store.get_portfolio(user_id)
        if ticker not in portfolio.crypto_holdings:
            portfolio.crypto_holdings[ticker] = 0.0
        portfolio.crypto_holdings[ticker] += quantity
        portfolio.total_invested_crypto += cost

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-cost,
            transaction_type=TransactionType.CRYPTO_BUY,
            balance_after=user.balance,
            description=f"Покупка {quantity} {ticker} по {asset.current_price}",
        ))

        return True, f"Куплено {quantity} {ticker} за {cost} монет", quantity

    def sell_crypto(self, user_id: int, ticker: str, quantity: float) -> Tuple[bool, str, int]:
        asset = self.store.get_crypto_asset(ticker)
        if asset is None:
            return False, "Криптовалюта не найдена", 0

        portfolio = self.store.get_portfolio(user_id)
        if ticker not in portfolio.crypto_holdings or portfolio.crypto_holdings[ticker] < quantity:
            return False, f"Недостаточно {ticker} в портфеле", 0

        revenue = int(asset.current_price * quantity)
        portfolio.crypto_holdings[ticker] -= quantity
        if portfolio.crypto_holdings[ticker] <= 0:
            del portfolio.crypto_holdings[ticker]

        user = self.store.get_user(user_id)
        user.balance += revenue

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=revenue,
            transaction_type=TransactionType.CRYPTO_SELL,
            balance_after=user.balance,
            description=f"Продажа {quantity} {ticker} по {asset.current_price}",
        ))

        return True, f"Продано {quantity} {ticker} за {revenue} монет", revenue

    def buy_stock(self, user_id: int, ticker: str, quantity: int) -> Tuple[bool, str, int]:
        asset = self.store.get_stock_asset(ticker)
        if asset is None:
            return False, "Акция не найдена", 0

        cost = int(asset.current_price * quantity)
        if cost <= 0:
            return False, "Сумма покупки слишком мала", 0

        user = self.store.get_user(user_id)
        if user.balance < cost:
            return False, f"Недостаточно средств. Нужно: {cost}", 0

        user.balance -= cost

        portfolio = self.store.get_portfolio(user_id)
        if ticker not in portfolio.stock_holdings:
            portfolio.stock_holdings[ticker] = 0
        portfolio.stock_holdings[ticker] += quantity
        portfolio.total_invested_stocks += cost

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-cost,
            transaction_type=TransactionType.STOCK_BUY,
            balance_after=user.balance,
            description=f"Покупка {quantity} акций {ticker} по {asset.current_price}",
        ))

        return True, f"Куплено {quantity} акций {ticker} за {cost} монет", cost

    def sell_stock(self, user_id: int, ticker: str, quantity: int) -> Tuple[bool, str, int]:
        asset = self.store.get_stock_asset(ticker)
        if asset is None:
            return False, "Акция не найдена", 0

        portfolio = self.store.get_portfolio(user_id)
        if ticker not in portfolio.stock_holdings or portfolio.stock_holdings[ticker] < quantity:
            return False, f"Недостаточно акций {ticker} в портфеле", 0

        revenue = int(asset.current_price * quantity)
        portfolio.stock_holdings[ticker] -= quantity
        if portfolio.stock_holdings[ticker] <= 0:
            del portfolio.stock_holdings[ticker]

        user = self.store.get_user(user_id)
        user.balance += revenue

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=revenue,
            transaction_type=TransactionType.STOCK_SELL,
            balance_after=user.balance,
            description=f"Продажа {quantity} акций {ticker} по {asset.current_price}",
        ))

        return True, f"Продано {quantity} акций {ticker} за {revenue} монет", revenue

    def process_dividends(self, user_id: int) -> Tuple[bool, str, int]:
        portfolio = self.store.get_portfolio(user_id)
        total_dividends = 0

        for ticker, quantity in list(portfolio.stock_holdings.items()):
            asset = self.store.get_stock_asset(ticker)
            if asset:
                dividend_per_share = int(asset.current_price * asset.dividend_yield)
                total_dividends += dividend_per_share * quantity

        if total_dividends <= 0:
            return False, "Нет дивидендов для выплаты", 0

        user = self.store.get_user(user_id)
        user.balance += total_dividends

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=total_dividends,
            transaction_type=TransactionType.DIVIDEND,
            balance_after=user.balance,
            description=f"Дивиденды по акциям",
        ))

        return True, f"Выплачены дивиденды: {total_dividends} монет", total_dividends

    def process_mining(self, user_id: int) -> Tuple[bool, str, int]:
        miners = self.store.get_user_miners(user_id)
        if not miners:
            return False, "У вас нет майнеров", 0

        total_income = 0
        for miner in miners:
            income = calculate_miner_income(miner)
            miner.hours_mined += 1
            miner.total_mined_value += income
            total_income += income

            if miner.hours_mined % 168 == 0 and miner.hours_mined > 0:
                miner.efficiency = max(0.1, miner.efficiency - MINER_EFFICIENCY_DECAY_WEEKLY)

        if total_income <= 0:
            return False, "Майнеры не принесли доход", 0

        user = self.store.get_user(user_id)
        user.balance += total_income

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=total_income,
            transaction_type=TransactionType.MINER_PURCHASE,
            balance_after=user.balance,
            description=f"Доход от майнинга ({len(miners)} майнеров)",
        ))

        return True, f"Майнинг принёс {total_income} монет", total_income

    def buy_miner(self, user_id: int, miner_type: str, quantity: int = 1) -> Tuple[bool, str, int]:
        mtype = None
        for mt in MinerType:
            if mt.value == miner_type:
                mtype = mt
                break

        if mtype is None:
            return False, "Тип майнера не найден", 0

        config = MINER_CONFIG[mtype]
        total_cost = config["price"] * quantity

        user = self.store.get_user(user_id)
        if user.balance < total_cost:
            return False, f"Недостаточно средств. Нужно: {total_cost}", 0

        user.balance -= total_cost

        for _ in range(quantity):
            miner = Miner(
                owner_id=user_id,
                miner_type=mtype,
            )
            self.store.add_miner(miner)

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-total_cost,
            transaction_type=TransactionType.MINER_PURCHASE,
            balance_after=user.balance,
            description=f"Покупка {quantity} x {config['name']}",
        ))

        return True, f"Куплено {quantity} x {config['name']} за {total_cost} монет", total_cost

    def sell_miner(self, user_id: int, miner_id: str) -> Tuple[bool, str, int]:
        miner = self.store.get_miner(miner_id)
        if miner is None:
            return False, "Майнер не найден", 0
        if miner.owner_id != user_id:
            return False, "Это не ваш майнер", 0

        config = MINER_CONFIG[miner.miner_type]
        sale_price = int(config["price"] * 0.7)

        user = self.store.get_user(user_id)
        user.balance += sale_price
        self.store.remove_miner(miner_id)

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=sale_price,
            transaction_type=TransactionType.MINER_SALE,
            balance_after=user.balance,
            description=f"Продажа {config['name']}",
        ))

        return True, f"Майнер продан за {sale_price} монет", sale_price

    def repair_miner(self, user_id: int, miner_id: str) -> Tuple[bool, str]:
        miner = self.store.get_miner(miner_id)
        if miner is None:
            return False, "Майнер не найден"
        if miner.owner_id != user_id:
            return False, "Это не ваш майнер"
        if miner.efficiency >= 1.0:
            return False, "Майнер не требует ремонта"

        config = MINER_CONFIG[miner.miner_type]
        repair_cost = int(config["price"] * MINER_REPAIR_COST_PERCENT)

        user = self.store.get_user(user_id)
        if user.balance < repair_cost:
            return False, f"Недостаточно средств. Нужно: {repair_cost}"

        user.balance -= repair_cost
        miner.efficiency = min(1.0, miner.efficiency + 0.5)
        miner.last_repair = datetime.now()

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-repair_cost,
            transaction_type=TransactionType.MINER_REPAIR,
            balance_after=user.balance,
            description=f"Ремонт майнера",
        ))

        return True, f"Майнер отремонтирован. Эффективность: {miner.efficiency:.0%}"


print("Основные сервисы/классы (ядро) загружены успешно.")
print(f"DataStore: 40+ методов")
print(f"EconomyService: 5 методов")
print(f"BankService: 4 метода")
print(f"BusinessService: 6 методов")
print(f"MarketService: 12 методов")



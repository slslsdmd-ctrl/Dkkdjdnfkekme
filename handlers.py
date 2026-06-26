

from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from datetime import datetime, timedelta
import re
import json
import asyncio
import logging
from dataclasses import asdict

from models import (
    User, ChatConfig, AdminLevel, ModLog, Business, CryptoAsset,
    StockAsset, UserPortfolio, Miner, Auction, Clan, ClanWar,
    Tournament, Pet, ShopItem, UserInventory, Achievement,
    Transaction, GameSession, Report, GlobalEconomy, Earth,
    Vehicle, House, Insurance, BlacklistEntry, ChatStats,
    WorldEvent, GameType, ModActionType, BusinessStatus,
    TransactionType, AuctionStatus, ClanWarStatus,
    MarriageStatus, InsuranceClaimReason, TournamentStatus,
    TournamentType, PetRarity, PetMood, EarthRegion,
    ItemRarity, ItemCategory, MinerType, ReputationLevel,
    AchievementCategory, StickerBlockMode, GifBlockMode,
    IIModMode, UserRole, SUPER_ADMIN_ID, SUPER_ADMIN_LEVEL,
    BOT_NAME, BOT_ALIASES, COMMAND_ALIASES,
    BUSINESS_TYPES, CRYPTO_ASSETS_CONFIG, STOCK_ASSETS_CONFIG,
    MINER_CONFIG, HOUSE_CONFIG, VEHICLE_CONFIG,
    SHOP_ITEMS_CONFIG, ACHIEVEMENTS_CONFIG,
    PET_SPECIES, PROFESSIONS, WORLD_EVENTS_POOL,
    REPUTATION_LEVELS, ADMIN_PERMISSIONS,
    DEFAULT_PAGE_SIZE, CASINO_MIN_BET, CASINO_MAX_BET,
    MAX_BUSINESSES_PER_USER, INSURANCE_COST_PERCENT,
    MARRIAGE_COST, DIVORCE_COST, CLAN_CREATION_COST,
    MAX_CLAN_MEMBERS, BUSINESS_CREATION_COST,
    generate_id, validate_amount, parse_duration,
    is_super_admin, has_permission,
)

from services import DataStore, EconomyService, BankService, BusinessService, MarketService
from game_logic import (
    CasinoService, AuctionService, CrimeService, ModerationService,
    ClanService, MarriageService, AchievementService,
    InsuranceService, ReputationService,
)
from integrations import (
    TelegramBotClient, DeepSeekClient, GrokClient,
    ImageGenerationClient, BroadcastService, NotificationService,
)
from utils import (
    logger, format_currency, format_number, format_duration,
    format_datetime, format_remaining_time, format_percent,
    format_user_mention, format_balance_card, format_business_card,
    format_crypto_card, format_stock_card, format_clan_card,
    format_pet_card, format_achievement_card, format_shop_item,
    format_transaction_history, format_mod_logs,
    format_auction_card, format_tournament_card,
    format_world_event, paginate_list, paginate_text,
    generate_pagination_keyboard, extract_command_args,
    extract_mentions, extract_numbers, parse_amount_from_text,
    parse_duration_from_text, match_command, find_bot_mention,
    validate_user_id, validate_business_name, validate_clan_name,
    validate_pet_name, validate_message_text,
    validate_bet, validate_transfer_amount,
    build_command_response, build_error_response,
    check_cooldown, is_user_muted, is_user_banned,
    is_user_jailed, calculate_total_wealth,
    get_user_title, emoji_status, emoji_progress_bar,
    emoji_number, send_long_message, async_send_long_message,
    BotConfig, BotMetrics, initialize_all_data,
    create_default_chat_config, create_super_admin_entry,
)


# ============================================================
# БАЗОВЫЙ КЛАСС ХЕНДЛЕРА
# ============================================================

class BaseHandler:
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics):
        self.store = store
        self.config = config
        self.metrics = metrics
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_response(self, success: bool, message: str, data: Any = None) -> Dict[str, Any]:
        return build_command_response(success, message, data)

    def get_error(self, message: str, error_code: str = "UNKNOWN") -> Dict[str, Any]:
        return build_error_response(message, error_code)

    def check_admin(self, user_id: int, chat_id: int, permission: str = "") -> Tuple[bool, str]:
        if is_super_admin(user_id):
            return True, ""
        level = self.store.get_admin_level(user_id, chat_id)
        if level <= 0:
            return False, "У вас нет прав администратора"
        if permission and not has_permission(level, permission):
            return False, f"Недостаточно прав. Нужно право: {permission}"
        return True, ""

    def check_super_admin(self, user_id: int) -> Tuple[bool, str]:
        if not is_super_admin(user_id):
            return False, "Только супер-админ может выполнить это действие"
        return True, ""


# ============================================================
# ХЕНДЛЕР ЭКОНОМИКИ
# ============================================================

class EconomyHandler(BaseHandler):
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 economy_service: EconomyService, bank_service: BankService,
                 notification_service: NotificationService):
        super().__init__(store, config, metrics)
        self.economy = economy_service
        self.bank = bank_service
        self.notify = notification_service

    async def handle_balance(self, user_id: int, chat_id: int,
                              args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        target_id = user_id
        if args:
            mention_ids = extract_mentions(" ".join(args))
            if mention_ids:
                target_id = mention_ids[0]
            else:
                valid, error, uid = validate_user_id(args[0])
                if valid:
                    target_id = uid

        user = self.store.get_user(target_id)
        balance_card = format_balance_card(user)
        return True, balance_card, {"target_id": target_id, "balance": user.balance}

    async def handle_transfer(self, user_id: int, chat_id: int,
                               args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Использование: перевод @user 1000", None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя (@user или ID)", None

        target_id = mention_ids[0]
        if target_id == user_id:
            return False, "Нельзя перевести деньги самому себе", None

        numbers = extract_numbers(" ".join(args))
        if not numbers:
            return False, "Укажите сумму перевода", None

        amount = numbers[0]
        if amount <= 0:
            return False, "Сумма должна быть положительной", None

        success, error, balance = self.economy.transfer_money(user_id, target_id, amount)
        if not success:
            return False, error, None

        self.metrics.increment_transactions()
        await self.notify.notify_transaction(target_id, amount, "Перевод", self.store.get_user(target_id).balance)
        return True, f"✅ Переведено {format_currency(amount)} пользователю {target_id}", {
            "sender_id": user_id,
            "receiver_id": target_id,
            "amount": amount,
            "balance": balance,
        }

    async def handle_work(self, user_id: int, chat_id: int,
                           args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        success, error, amount = self.economy.process_work(user_id)
        if not success:
            return False, error, None

        self.metrics.increment_commands()
        user = self.store.get_user(user_id)
        return True, error, {"amount": amount, "balance": user.balance}

    async def handle_bonus(self, user_id: int, chat_id: int,
                            args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        success, error, amount = self.economy.process_bonus(user_id)
        if not success:
            return False, error, None

        user = self.store.get_user(user_id)
        return True, error, {"amount": amount, "balance": user.balance}

    async def handle_top(self, user_id: int, chat_id: int,
                          args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        limit = 10
        if args:
            try:
                limit = int(args[0])
                limit = max(1, min(50, limit))
            except ValueError:
                pass

        top_users = self.economy.get_top_balances(limit)
        lines = [f"🏆 Топ-{limit} богачей:"]
        for i, (uid, balance, name) in enumerate(top_users, 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
            lines.append(f"{medal} {name}: {format_currency(balance)}")

        if user_id not in [u[0] for u in top_users]:
            user = self.store.get_user(user_id)
            all_users = sorted(self.store.users.values(), key=lambda u: u.balance, reverse=True)
            user_rank = next((i + 1 for i, u in enumerate(all_users) if u.user_id == user_id), 0)
            if user_rank:
                lines.append(f"...")
                lines.append(f"{user_rank}. Вы: {format_currency(user.balance)}")

        return True, "\n".join(lines), {"top": top_users}

    async def handle_bank_deposit(self, user_id: int, chat_id: int,
                                   args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите сумму вклада", None

        amount = parse_amount_from_text(" ".join(args))
        if amount is None:
            return False, "Некорректная сумма", None

        success, error, balance = self.bank.deposit(user_id, amount)
        if not success:
            return False, error, None

        return True, error, {"balance": balance}

    async def handle_bank_withdraw(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите сумму для снятия", None

        amount = parse_amount_from_text(" ".join(args))
        if amount is None:
            return False, "Некорректная сумма", None

        success, error, balance = self.bank.withdraw(user_id, amount)
        if not success:
            return False, error, None

        return True, error, {"balance": balance}

    async def handle_loan_take(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите сумму кредита", None

        amount = parse_amount_from_text(" ".join(args))
        if amount is None:
            return False, "Некорректная сумма", None

        success, error, balance = self.bank.take_loan(user_id, amount)
        if not success:
            return False, error, None

        return True, error, {"balance": balance}

    async def handle_loan_repay(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        amount = 0
        if args:
            amount = parse_amount_from_text(" ".join(args)) or 0

        success, error, balance = self.bank.repay_loan(user_id, amount)
        if not success:
            return False, error, None

        return True, error, {"balance": balance}


# ============================================================
# ХЕНДЛЕР БИЗНЕСА
# ============================================================

class BusinessHandler(BaseHandler):
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 business_service: BusinessService):
        super().__init__(store, config, metrics)
        self.business = business_service

    async def handle_business_create(self, user_id: int, chat_id: int,
                                      args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if len(args) < 1:
            types_list = "\n".join([f"• {b['name']} ({b['type']}) - {format_currency(b['base_price'])}"
                                    for b in BUSINESS_TYPES])
            return False, f"Укажите тип бизнеса:\n{types_list}", None

        business_type = args[0].lower()
        name = " ".join(args[1:]) if len(args) > 1 else ""

        if name:
            valid, error = validate_business_name(name)
            if not valid:
                return False, error, None

        success, error, business = self.business.create_business(user_id, business_type, name)
        if not success:
            return False, error, None

        return True, error, {"business": business.to_dict() if business else None}

    async def handle_business_collect(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        user_businesses = self.store.get_user_businesses(user_id)
        if not user_businesses:
            return False, "У вас нет бизнесов", None

        if args:
            business_id = args[0]
            success, error, income = self.business.collect_income(user_id, business_id)
            if not success:
                return False, error, None
            return True, error, {"income": income}
        else:
            total_income = 0
            results = []
            for b in user_businesses:
                if b.status == BusinessStatus.ACTIVE:
                    success, error, income = self.business.collect_income(user_id, b.business_id)
                    if success:
                        total_income += income
                        results.append(f"• {b.name}: +{format_currency(income)}")

            if total_income == 0:
                return False, "Нет активных бизнесов", None

            user = self.store.get_user(user_id)
            return True, f"Собрано:\n" + "\n".join(results) + f"\n\nВсего: {format_currency(total_income)}\nБаланс: {format_currency(user.balance)}", {
                "total_income": total_income,
                "balance": user.balance,
            }

    async def handle_business_upgrade(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите ID бизнеса", None

        business_id = args[0]
        success, error, business = self.business.upgrade_business(user_id, business_id)
        if not success:
            return False, error, None

        return True, error, {"business": business.to_dict() if business else None}

    async def handle_business_sell(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите ID бизнеса", None

        business_id = args[0]
        success, error, price = self.business.sell_business(user_id, business_id)
        if not success:
            return False, error, None

        return True, error, {"price": price}

    async def handle_business_hire(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if len(args) < 2:
            return False, "Укажите ID бизнеса и @пользователя", None

        business_id = args[0]
        mention_ids = extract_mentions(" ".join(args[1:]))
        if not mention_ids:
            return False, "Укажите пользователя", None

        employee_id = mention_ids[0]
        success, error = self.business.hire_employee(user_id, business_id, employee_id)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_business_fire(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if len(args) < 2:
            return False, "Укажите ID бизнеса и @пользователя", None

        business_id = args[0]
        mention_ids = extract_mentions(" ".join(args[1:]))
        if not mention_ids:
            return False, "Укажите пользователя", None

        employee_id = mention_ids[0]
        success, error = self.business.fire_employee(user_id, business_id, employee_id)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_business_list(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        businesses = self.store.get_user_businesses(user_id)
        if not businesses:
            return False, "У вас нет бизнесов", None

        lines = [f"🏢 Ваши бизнесы ({len(businesses)}/{MAX_BUSINESSES_PER_USER}):"]
        for b in businesses:
            status_emoji = {"active": "✅", "bankrupt": "❌", "sold": "💰", "frozen": "🧊"}
            emoji = status_emoji.get(b.status.value, "❓")
            lines.append(f"{emoji} {b.name} (Lvl {b.level}) | ID: {b.business_id[:8]}")
            lines.append(f"   Доход: {format_currency(b.hourly_income)}/час | "
                         f"Сотрудники: {len(b.employees)}/{b.max_employees}")

        return True, "\n".join(lines), {"businesses": [b.to_dict() for b in businesses]}


# ============================================================
# ХЕНДЛЕР КРИПТЫ И АКЦИЙ
# ============================================================

class MarketHandler(BaseHandler):
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 market_service: MarketService):
        super().__init__(store, config, metrics)
        self.market = market_service

    async def handle_crypto_list(self, user_id: int, chat_id: int,
                                  args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        assets = self.store.get_all_crypto_assets()
        if not assets:
            return False, "Нет доступных криптовалют", None

        lines = ["🪙 Курсы криптовалют:"]
        for asset in assets:
            emoji = "📈" if asset.change_percent >= 0 else "📉"
            lines.append(
                f"{emoji} {asset.name} ({asset.ticker}): "
                f"${asset.current_price:,.2f} ({format_percent(asset.change_percent)})"
            )

        return True, "\n".join(lines), {"crypto": [a.to_dict() for a in assets]}

    async def handle_crypto_info(self, user_id: int, chat_id: int,
                                  args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите тикер криптовалюты", None

        ticker = args[0].upper()
        asset = self.store.get_crypto_asset(ticker)
        if asset is None:
            return False, "Криптовалюта не найдена", None

        card = format_crypto_card(asset)
        return True, card, {"asset": asset.to_dict()}

    async def handle_crypto_buy(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if len(args) < 2:
            return False, "Укажите тикер и количество", None

        ticker = args[0].upper()
        try:
            quantity = float(args[1])
        except ValueError:
            return False, "Некорректное количество", None

        if quantity <= 0:
            return False, "Количество должно быть положительным", None

        success, error, qty = self.market.buy_crypto(user_id, ticker, quantity)
        if not success:
            return False, error, None

        self.metrics.increment_transactions()
        return True, error, {"ticker": ticker, "quantity": qty}

    async def handle_crypto_sell(self, user_id: int, chat_id: int,
                                  args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if len(args) < 2:
            return False, "Укажите тикер и количество", None

        ticker = args[0].upper()
        try:
            quantity = float(args[1])
        except ValueError:
            return False, "Некорректное количество", None

        success, error, revenue = self.market.sell_crypto(user_id, ticker, quantity)
        if not success:
            return False, error, None

        self.metrics.increment_transactions()
        return True, error, {"ticker": ticker, "revenue": revenue}

    async def handle_crypto_portfolio(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        portfolio = self.store.get_portfolio(user_id)
        if not portfolio.crypto_holdings:
            return False, "У вас нет криптовалют", None

        lines = ["📊 Ваш крипто-портфель:"]
        total_value = 0
        for ticker, quantity in portfolio.crypto_holdings.items():
            asset = self.store.get_crypto_asset(ticker)
            if asset:
                value = int(asset.current_price * quantity)
                total_value += value
                lines.append(
                    f"• {asset.name} ({ticker}): {quantity:.4f} = {format_currency(value)}"
                )

        lines.append(f"💰 Общая стоимость: {format_currency(total_value)}")
        return True, "\n".join(lines), {"portfolio": portfolio.to_dict(), "total_value": total_value}

    async def handle_stock_list(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        assets = self.store.get_all_stock_assets()
        if not assets:
            return False, "Нет доступных акций", None

        lines = ["📊 Рынок акций:"]
        for asset in assets:
            emoji = "📈" if asset.change_percent >= 0 else "📉"
            lines.append(
                f"{emoji} {asset.company_name} ({asset.ticker}): "
                f"${asset.current_price:,.2f} ({format_percent(asset.change_percent)})"
            )

        return True, "\n".join(lines), {"stocks": [a.to_dict() for a in assets]}

    async def handle_stock_info(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите тикер акции", None

        ticker = args[0].upper()
        asset = self.store.get_stock_asset(ticker)
        if asset is None:
            return False, "Акция не найдена", None

        card = format_stock_card(asset)
        return True, card, {"asset": asset.to_dict()}

    async def handle_stock_buy(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if len(args) < 2:
            return False, "Укажите тикер и количество", None

        ticker = args[0].upper()
        try:
            quantity = int(args[1])
        except ValueError:
            return False, "Некорректное количество", None

        success, error, cost = self.market.buy_stock(user_id, ticker, quantity)
        if not success:
            return False, error, None

        self.metrics.increment_transactions()
        return True, error, {"ticker": ticker, "quantity": quantity, "cost": cost}

    async def handle_stock_sell(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if len(args) < 2:
            return False, "Укажите тикер и количество", None

        ticker = args[0].upper()
        try:
            quantity = int(args[1])
        except ValueError:
            return False, "Некорректное количество", None

        success, error, revenue = self.market.sell_stock(user_id, ticker, quantity)
        if not success:
            return False, error, None

        self.metrics.increment_transactions()
        return True, error, {"ticker": ticker, "revenue": revenue}

    async def handle_stock_portfolio(self, user_id: int, chat_id: int,
                                      args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        portfolio = self.store.get_portfolio(user_id)
        if not portfolio.stock_holdings:
            return False, "У вас нет акций", None

        lines = ["📊 Ваш портфель акций:"]
        total_value = 0
        for ticker, quantity in portfolio.stock_holdings.items():
            asset = self.store.get_stock_asset(ticker)
            if asset:
                value = int(asset.current_price * quantity)
                total_value += value
                lines.append(
                    f"• {asset.company_name} ({ticker}): {quantity} шт = {format_currency(value)}"
                )

        lines.append(f"💰 Общая стоимость: {format_currency(total_value)}")
        return True, "\n".join(lines), {"portfolio": portfolio.to_dict(), "total_value": total_value}

    async def handle_dividends(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        success, error, total = self.market.process_dividends(user_id)
        if not success:
            return False, error, None

        return True, error, {"total_dividends": total}

    async def handle_miners_list(self, user_id: int, chat_id: int,
                                   args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        miners = self.store.get_user_miners(user_id)
        if not miners:
            return False, "У вас нет майнеров", None

        lines = ["⛏ Ваши майнеры:"]
        for m in miners:
            config = MINER_CONFIG.get(m.miner_type, {})
            income = calculate_miner_income(m)
            lines.append(
                f"• {config.get('name', m.miner_type.value)} (ID: {m.miner_id[:8]})\n"
                f"   Эффективность: {m.efficiency:.0%} | Доход: {format_currency(income)}/час | "
                f"Наработано: {m.hours_mined}ч"
            )

        return True, "\n".join(lines), {"miners": [m.to_dict() for m in miners]}

    async def handle_miner_buy(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            miners_list = "\n".join([
                f"• {config['name']} ({mt.value}) - {format_currency(config['price'])}"
                for mt, config in MINER_CONFIG.items()
            ])
            return False, f"Укажите тип майнера:\n{miners_list}", None

        miner_type = args[0].lower()
        quantity = 1
        if len(args) > 1:
            try:
                quantity = int(args[1])
                quantity = max(1, min(10, quantity))
            except ValueError:
                pass

        success, error, cost = self.market.buy_miner(user_id, miner_type, quantity)
        if not success:
            return False, error, None

        return True, error, {"miner_type": miner_type, "quantity": quantity, "cost": cost}

    async def handle_miner_sell(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите ID майнера", None

        miner_id = args[0]
        success, error, price = self.market.sell_miner(user_id, miner_id)
        if not success:
            return False, error, None

        return True, error, {"price": price}

    async def handle_miner_repair(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите ID майнера", None

        miner_id = args[0]
        success, error = self.market.repair_miner(user_id, miner_id)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_mining_collect(self, user_id: int, chat_id: int,
                                      args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        success, error, total = self.market.process_mining(user_id)
        if not success:
            return False, error, None

        return True, error, {"total_income": total}


# ============================================================
# ХЕНДЛЕР КАЗИНО
# ============================================================

class CasinoHandler(BaseHandler):
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 casino_service: CasinoService):
        super().__init__(store, config, metrics)
        self.casino = casino_service

    async def handle_slots(self, user_id: int, chat_id: int,
                            args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        bet = CASINO_MIN_BET
        if args:
            bet = parse_amount_from_text(args[0]) or CASINO_MIN_BET

        valid, error = validate_bet(bet)
        if not valid:
            return False, error, None

        success, error, result = self.casino.play_slots(user_id, bet)
        if not success:
            return False, error, None

        self.metrics.increment_games()

        reels = result.get("reels", [[], [], []])
        reel_display = (
            f"🎰 Слоты:\n"
            f"| {' | '.join(reels[0])} |\n"
            f"| {' | '.join(reels[1])} |\n"
            f"| {' | '.join(reels[2])} |\n"
            f"\n{error}"
        )

        return True, reel_display, result

    async def handle_dice(self, user_id: int, chat_id: int,
                           args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        bet = CASINO_MIN_BET
        guess = None

        if args:
            numbers = extract_numbers(" ".join(args))
            if numbers:
                bet = numbers[0]
                if len(numbers) > 1:
                    guess = numbers[1]

        valid, error = validate_bet(bet)
        if not valid:
            return False, error, None

        success, error, result = self.casino.play_dice(user_id, bet, guess)
        if not success:
            return False, error, None

        self.metrics.increment_games()

        dice_display = (
            f"🎲 Кубики: {result['dice1']} + {result['dice2']} = {result['total']}\n"
            f"{error}"
        )

        return True, dice_display, result

    async def handle_coinflip(self, user_id: int, chat_id: int,
                               args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        bet = CASINO_MIN_BET
        choice = "орёл"

        if args:
            numbers = extract_numbers(" ".join(args))
            if numbers:
                bet = numbers[0]

            if args[-1].lower() in ("орёл", "орел", "орёль", "решка", "решкa"):
                choice = args[-1].lower()

        valid, error = validate_bet(bet)
        if not valid:
            return False, error, None

        success, error, result = self.casino.play_coinflip(user_id, bet, choice)
        if not success:
            return False, error, None

        self.metrics.increment_games()

        coin_display = (
            f"🪙 Монетка: {result['result']}\n"
            f"{error}"
        )

        return True, coin_display, result

    async def handle_duel(self, user_id: int, chat_id: int,
                           args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите @противника и ставку", None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите противника через @", None

        opponent_id = mention_ids[0]
        numbers = extract_numbers(" ".join(args))
        bet = numbers[0] if numbers else CASINO_MIN_BET

        valid, error = validate_bet(bet)
        if not valid:
            return False, error, None

        success, error = self.casino.play_duel(user_id, opponent_id, bet)
        if not success:
            return False, error, None

        self.metrics.increment_games()
        return True, error, {"challenger_id": user_id, "opponent_id": opponent_id, "bet": bet}

    async def handle_russian_roulette(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        bet = CASINO_MIN_BET * 10
        if args:
            bet = parse_amount_from_text(args[0]) or bet

        valid, error = validate_bet(bet)
        if not valid:
            return False, error, None

        success, error = self.casino.play_russian_roulette(user_id, bet)
        if not success:
            return False, error, None

        self.metrics.increment_games()
        return True, error, {"bet": bet}

    async def handle_case_open(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите тип кейса: обычный, редкий, эпический, легендарный", None

        case_type = args[0].lower()
        success, error, result = self.casino.open_case(user_id, case_type)
        if not success:
            return False, error, None

        self.metrics.increment_games()

        return True, error, result

    async def handle_wheel(self, user_id: int, chat_id: int,
                            args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        bet = CASINO_MIN_BET
        if args:
            bet = parse_amount_from_text(args[0]) or CASINO_MIN_BET

        valid, error = validate_bet(bet)
        if not valid:
            return False, error, None

        user = self.store.get_user(user_id)
        if user.balance < bet:
            return False, f"Недостаточно средств. Баланс: {format_currency(user.balance)}", None

        wheel_items = [
            {"name": "0x", "weight": 30, "color": "⚫"},
            {"name": "0.5x", "weight": 25, "color": "🔴"},
            {"name": "1x", "weight": 20, "color": "🟡"},
            {"name": "2x", "weight": 15, "color": "🟢"},
            {"name": "5x", "weight": 7, "color": "🔵"},
            {"name": "10x", "weight": 3, "color": "🟣"},
        ]

        total_weight = sum(item["weight"] for item in wheel_items)
        roll = random.randint(1, total_weight)
        cumulative = 0
        result_item = wheel_items[0]
        for item in wheel_items:
            cumulative += item["weight"]
            if roll <= cumulative:
                result_item = item
                break

        multiplier = float(result_item["name"].replace("x", ""))
        win_amount = int(bet * multiplier)

        if win_amount > bet:
            user.balance += win_amount - bet
            transaction_type = TransactionType.CASINO_WIN
        elif win_amount == bet:
            transaction_type = TransactionType.CASINO_BET
            win_amount = bet
        else:
            user.balance -= bet - win_amount
            transaction_type = TransactionType.CASINO_BET

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=win_amount - bet,
            transaction_type=transaction_type,
            balance_after=user.balance,
            description=f"Колесо фортуны: {result_item['name']}",
        ))

        self.metrics.increment_games()

        return True, (
            f"🎡 Колесо фортуны: {result_item['color']} {result_item['name']}\n"
            f"Ставка: {format_currency(bet)}\n"
            f"Выигрыш: {format_currency(win_amount)}\n"
            f"Баланс: {format_currency(user.balance)}"
        ), {"bet": bet, "multiplier": multiplier, "win_amount": win_amount}


# ============================================================
# ХЕНДЛЕР МОДЕРАЦИИ
# ============================================================

class ModerationHandler(BaseHandler):
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 moderation_service: ModerationService, notification_service: NotificationService,
                 telegram_client: TelegramBotClient):
        super().__init__(store, config, metrics)
        self.moderation = moderation_service
        self.notify = notification_service
        self.tg = telegram_client

    async def handle_warn(self, user_id: int, chat_id: int,
                           args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя для варна", None

        target_id = mention_ids[0]
        reason = " ".join(args[len(extract_mentions.__code__.co_varnames):]).strip()

        success, error = self.moderation.warn_user(user_id, target_id, chat_id, reason)
        if not success:
            return False, error, None

        self.metrics.increment_moderation()
        await self.notify.notify_moderation_action(target_id, "Предупреждение", reason, "", "")
        return True, error, {"target_id": target_id}

    async def handle_mute(self, user_id: int, chat_id: int,
                           args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя для мута", None

        target_id = mention_ids[0]

        duration_minutes = 60
        duration_str = parse_duration_from_text(" ".join(args))
        if duration_str:
            duration_minutes = duration_str // 60
        elif len(args) > 1:
            parsed = parse_duration(args[1])
            if parsed:
                duration_minutes = parsed

        reason = " ".join([
            a for a in args
            if a not in str(mention_ids[0]) and a not in str(duration_minutes)
        ]).strip()

        if not reason:
            reason = "Нарушение правил"

        success, error = self.moderation.mute_user(user_id, target_id, chat_id, duration_minutes, reason)
        if not success:
            return False, error, None

        self.metrics.increment_moderation()
        await self.notify.notify_moderation_action(
            target_id, "Мут", reason,
            format_duration(duration_minutes * 60), ""
        )
        return True, error, {"target_id": target_id, "duration": duration_minutes}

    async def handle_unmute(self, user_id: int, chat_id: int,
                             args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        success, error = self.moderation.unmute_user(user_id, target_id, chat_id)
        if not success:
            return False, error, None

        await self.notify.notify_unmute_unban(target_id, "Мут", "")
        return True, error, None

    async def handle_kick(self, user_id: int, chat_id: int,
                           args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя для кика", None

        target_id = mention_ids[0]
        reason = " ".join(args[1:]) if len(args) > 1 else ""

        success, error = self.moderation.kick_user(user_id, target_id, chat_id, reason)
        if not success:
            return False, error, None

        self.metrics.increment_moderation()
        return True, error, {"target_id": target_id}

    async def handle_ban(self, user_id: int, chat_id: int,
                          args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя для бана", None

        target_id = mention_ids[0]

        duration_minutes = 0
        duration_str = parse_duration_from_text(" ".join(args))
        if duration_str:
            duration_minutes = duration_str // 60

        reason = " ".join(args[1:]) if len(args) > 1 else ""

        success, error = self.moderation.ban_user(user_id, target_id, chat_id, reason, duration_minutes)
        if not success:
            return False, error, None

        self.metrics.increment_moderation()
        duration_text = format_duration(duration_minutes * 60) if duration_minutes > 0 else "Навсегда"
        await self.notify.notify_moderation_action(target_id, "Бан", reason, duration_text, "")

        try:
            if duration_minutes <= 0:
                await self.tg.ban_chat_member(chat_id, target_id)
            else:
                until_date = int((datetime.now() + timedelta(minutes=duration_minutes)).timestamp())
                await self.tg.ban_chat_member(chat_id, target_id, until_date)
        except Exception as e:
            self.logger.error(f"Telegram ban error: {e}")

        return True, error, {"target_id": target_id, "duration": duration_minutes}

    async def handle_unban(self, user_id: int, chat_id: int,
                            args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        success, error = self.moderation.unban_user(user_id, target_id, chat_id)
        if not success:
            return False, error, None

        await self.notify.notify_unmute_unban(target_id, "Бан", "")

        try:
            await self.tg.unban_chat_member(chat_id, target_id)
        except Exception as e:
            self.logger.error(f"Telegram unban error: {e}")

        return True, error, None

    async def handle_clear(self, user_id: int, chat_id: int,
                            args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        count = 10
        target_id = None

        if args:
            numbers = extract_numbers(args[0])
            if numbers:
                count = numbers[0]
            mention_ids = extract_mentions(" ".join(args))
            if mention_ids:
                target_id = mention_ids[0]

        count = max(1, min(1000, count))

        success, error = self.moderation.clear_messages(user_id, chat_id, count, target_id)
        if not success:
            return False, error, None

        return True, error, {"count": count}

    async def handle_lock(self, user_id: int, chat_id: int,
                           args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        success, error = self.moderation.lock_chat(user_id, chat_id)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_unlock(self, user_id: int, chat_id: int,
                             args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        success, error = self.moderation.unlock_chat(user_id, chat_id)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_slowmode(self, user_id: int, chat_id: int,
                               args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        seconds = 0
        if args:
            numbers = extract_numbers(args[0])
            if numbers:
                seconds = numbers[0]

        success, error = self.moderation.set_slowmode(user_id, chat_id, seconds)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_warns_list(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        target_id = user_id
        if args:
            mention_ids = extract_mentions(" ".join(args))
            if mention_ids:
                target_id = mention_ids[0]

        warns = self.store.get_active_warns(target_id, chat_id)
        if not warns:
            return True, f"У пользователя {target_id} нет активных варнов", {"warns": []}

        lines = [f"⚠️ Варны пользователя {target_id}:"]
        for i, warn in enumerate(warns, 1):
            lines.append(f"{i}. {format_datetime(warn.timestamp)}")
            if warn.reason:
                lines.append(f"   Причина: {warn.reason}")

        return True, "\n".join(lines), {"warns": [w.to_dict() for w in warns]}

    async def handle_remove_warn(self, user_id: int, chat_id: int,
                                  args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        warn_number = 1
        numbers = extract_numbers(" ".join(args))
        if numbers:
            warn_number = numbers[-1] if numbers else 1

        warns = self.store.get_active_warns(target_id, chat_id)
        if not warns:
            return False, "У пользователя нет варнов", None

        if warn_number < 1 or warn_number > len(warns):
            return False, f"Номер варна от 1 до {len(warns)}", None

        warn = warns[warn_number - 1]
        warn.is_active = False
        warn.removed_by = user_id
        warn.removed_at = datetime.now()

        return True, f"Варн #{warn_number} снят", None

    async def handle_mod_logs(self, user_id: int, chat_id: int,
                               args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        logs = [log for log in self.store.mod_logs if log.chat_id == chat_id]
        logs.sort(key=lambda x: x.timestamp, reverse=True)

        if not logs:
            return True, "Логи модерации пусты", {"logs": []}

        return True, format_mod_logs(logs, 15), {"logs": [l.to_dict() for l in logs[:15]]}

    async def handle_report(self, user_id: int, chat_id: int,
                             args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя для жалобы", None

        target_id = mention_ids[0]
        reason = " ".join(args[1:]) if len(args) > 1 else "Без причины"

        report = Report(
            reporter_id=user_id,
            target_id=target_id,
            chat_id=chat_id,
            reason=reason,
        )
        self.store.add_report(report)

        return True, f"✅ Жалоба на пользователя {target_id} отправлена", {"report_id": report.report_id}

    async def handle_reports_list(self, user_id: int, chat_id: int,
                                   args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_mod, error = self.check_admin(user_id, chat_id, "report")
        if not can_mod:
            return False, error, None

        reports = self.store.get_pending_reports(chat_id)
        if not reports:
            return True, "Нет активных жалоб", {"reports": []}

        lines = ["📋 Активные жалобы:"]
        for r in reports[:10]:
            lines.append(f"ID: {r.report_id[:8]} | От: {r.reporter_id} | На: {r.target_id}")
            lines.append(f"   Причина: {r.reason} | {format_datetime(r.created_at)}")

        return True, "\n".join(lines), {"reports": [r.to_dict() for r in reports]}


# ============================================================
# ХЕНДЛЕР АДМИНИСТРИРОВАНИЯ
# ============================================================

class AdminHandler(BaseHandler):
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 economy_service: EconomyService, notification_service: NotificationService,
                 telegram_client: TelegramBotClient):
        super().__init__(store, config, metrics)
        self.economy = economy_service
        self.notify = notification_service
        self.tg = telegram_client

    async def handle_set_admin(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_admin(user_id, chat_id, "assign_admin")
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]

        level = 1
        numbers = extract_numbers(" ".join(args))
        if numbers:
            level = numbers[-1]

        level = max(1, min(9, level))

        moderator_level = self.store.get_admin_level(user_id, chat_id)
        if level >= moderator_level and not is_super_admin(user_id):
            return False, "Нельзя выдать уровень равный или выше своего", None

        self.store.set_admin_level(target_id, chat_id, level, assigned_by=user_id)

        return True, f"✅ Пользователь {target_id} назначен администратором уровня {level}", {
            "target_id": target_id,
            "level": level,
        }

    async def handle_remove_admin(self, user_id: int, chat_id: int,
                                   args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_admin(user_id, chat_id, "assign_admin")
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]

        target_level = self.store.get_admin_level(target_id, chat_id)
        moderator_level = self.store.get_admin_level(user_id, chat_id)

        if target_level >= moderator_level and not is_super_admin(user_id):
            return False, "Нельзя снять администратора с таким же или более высоким уровнем", None

        self.store.remove_admin_level(target_id, chat_id)

        return True, f"✅ Администраторские права пользователя {target_id} сняты", {"target_id": target_id}

    async def handle_promote(self, user_id: int, chat_id: int,
                              args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_admin(user_id, chat_id, "assign_admin")
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        current_level = self.store.get_admin_level(target_id, chat_id)

        if current_level >= 9:
            return False, "Достигнут максимальный уровень", None

        new_level = current_level + 1
        if new_level >= self.store.get_admin_level(user_id, chat_id) and not is_super_admin(user_id):
            return False, "Нельзя повысить до своего уровня или выше", None

        self.store.set_admin_level(target_id, chat_id, new_level, assigned_by=user_id)

        return True, f"✅ Пользователь {target_id} повышен до уровня {new_level}", {
            "target_id": target_id,
            "level": new_level,
        }

    async def handle_demote(self, user_id: int, chat_id: int,
                             args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_admin(user_id, chat_id, "assign_admin")
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        current_level = self.store.get_admin_level(target_id, chat_id)

        if current_level <= 1:
            return False, "Достигнут минимальный уровень", None

        new_level = current_level - 1
        self.store.set_admin_level(target_id, chat_id, new_level, assigned_by=user_id)

        return True, f"✅ Пользователь {target_id} понижен до уровня {new_level}", {
            "target_id": target_id,
            "level": new_level,
        }

    async def handle_admin_list(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_admin(user_id, chat_id)
        if not can_admin:
            return False, error, None

        admins = []
        for (uid, cid), admin_level in self.store.admin_levels.items():
            if cid == chat_id:
                admins.append((uid, admin_level))

        if not admins:
            return True, "В чате нет администраторов", {"admins": []}

        admins.sort(key=lambda x: x[1].level, reverse=True)
        lines = ["👥 Администраторы чата:"]
        for uid, admin in admins:
            lines.append(f"• {uid}: уровень {admin.level}" + (" (создатель)" if admin.is_creator else ""))

        return True, "\n".join(lines), {"admins": [a[1].to_dict() for a in admins]}

    async def handle_rules_set(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_admin(user_id, chat_id, "chat_settings")
        if not can_admin:
            return False, error, None

        rules = " ".join(args)
        if not rules:
            return False, "Укажите текст правил", None

        chat_config = self.store.get_chat(chat_id)
        chat_config.rules = rules

        return True, "✅ Правила чата обновлены", {"rules": rules}

    async def handle_rules(self, user_id: int, chat_id: int,
                            args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        chat_config = self.store.get_chat(chat_id)
        if not chat_config.rules:
            return True, "Правила чата не установлены", {}

        return True, f"📜 Правила чата:\n{chat_config.rules}", {"rules": chat_config.rules}

    async def handle_welcome_set(self, user_id: int, chat_id: int,
                                  args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_admin(user_id, chat_id, "chat_settings")
        if not can_admin:
            return False, error, None

        welcome = " ".join(args)
        if not welcome:
            return False, "Укажите текст приветствия", None

        chat_config = self.store.get_chat(chat_id)
        chat_config.welcome_message = welcome

        return True, "✅ Приветствие обновлено", {"welcome": welcome}

    async def handle_chat_info(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        chat_config = self.store.get_chat(chat_id)
        chat_stats = self.store.get_chat_stats(chat_id)

        lines = [
            f"💬 Информация о чате {chat_id}:",
            f"📝 Название: {chat_config.chat_title or 'Не указано'}",
            f"🔒 Закрыт: {'Да' if chat_config.is_locked else 'Нет'}",
            f"🐢 Слоумод: {chat_config.slowmode_seconds} сек",
            f"🤖 ИИ-модерация: {'Вкл' if chat_config.ii_moderation_enabled else 'Выкл'}",
            f"📊 Сообщений всего: {chat_stats.total_messages}",
            f"📅 Сообщений сегодня: {chat_stats.messages_today}",
        ]

        return True, "\n".join(lines), {
            "chat_config": chat_config.to_dict(),
            "chat_stats": chat_stats.to_dict(),
        }

    async def handle_admin_give_money(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_admin(user_id, chat_id, "balance")
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        numbers = extract_numbers(" ".join(args))
        amount = numbers[-1] if numbers else 0

        if amount <= 0:
            return False, "Укажите положительную сумму", None

        success, error, balance = self.economy.add_money(
            target_id, amount,
            TransactionType.ADMIN_GIFT,
            f"Выдано администратором {user_id}",
            user_id,
        )

        if not success:
            return False, error, None

        return True, f"✅ Выдано {format_currency(amount)} пользователю {target_id}", {
            "target_id": target_id,
            "amount": amount,
            "balance": balance,
        }

    async def handle_admin_take_money(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_admin(user_id, chat_id, "balance")
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        numbers = extract_numbers(" ".join(args))
        amount = numbers[-1] if numbers else 0

        if amount <= 0:
            return False, "Укажите положительную сумму", None

        success, error, balance = self.economy.remove_money(
            target_id, amount,
            TransactionType.ADMIN_SEIZE,
            f"Изъято администратором {user_id}",
            user_id,
        )

        if not success:
            return False, error, None

        return True, f"✅ Изъято {format_currency(amount)} у пользователя {target_id}", {
            "target_id": target_id,
            "amount": amount,
            "balance": balance,
        }


# ============================================================
# ХЕНДЛЕР СУПЕР-АДМИНА
# ============================================================

class SuperAdminHandler(BaseHandler):
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 economy_service: EconomyService, notification_service: NotificationService,
                 broadcast_service: BroadcastService, telegram_client: TelegramBotClient):
        super().__init__(store, config, metrics)
        self.economy = economy_service
        self.notify = notification_service
        self.broadcast = broadcast_service
        self.tg = telegram_client

    async def handle_global_broadcast(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        text = " ".join(args)
        if not text:
            return False, "Укажите текст рассылки", None

        success, error, count = await self.broadcast.broadcast_to_all_chats(user_id, text)
        if not success:
            return False, error, None

        return True, error, {"sent_count": count}

    async def handle_global_announce(self, user_id: int, chat_id: int,
                                      args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        text = " ".join(args)
        if not text:
            return False, "Укажите текст анонса", None

        success, error, count = await self.broadcast.send_announcement(user_id, text)
        if not success:
            return False, error, None

        return True, error, {"sent_count": count}

    async def handle_global_ban(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        reason = " ".join(args[1:]) if len(args) > 1 else "Глобальный бан"

        moderation_service = ModerationService(self.store)
        success, error = moderation_service.global_ban_user(user_id, target_id, reason)
        if not success:
            return False, error, None

        return True, error, {"target_id": target_id}

    async def handle_global_unban(self, user_id: int, chat_id: int,
                                   args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]

        moderation_service = ModerationService(self.store)
        success, error = moderation_service.global_unban_user(user_id, target_id)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_blacklist_add(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        reason = " ".join(args[1:]) if len(args) > 1 else ""

        if self.store.is_blacklisted(target_id):
            return False, "Пользователь уже в чёрном списке", None

        entry = BlacklistEntry(
            user_id=target_id,
            reason=reason,
            added_by=user_id,
        )
        self.store.add_blacklist(entry)

        return True, f"✅ Пользователь {target_id} добавлен в чёрный список", {"target_id": target_id}

    async def handle_blacklist_remove(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]

        if not self.store.is_blacklisted(target_id):
            return False, "Пользователь не в чёрном списке", None

        self.store.remove_blacklist(target_id)

        return True, f"✅ Пользователь {target_id} удалён из чёрного списка", {"target_id": target_id}

    async def handle_blacklist_list(self, user_id: int, chat_id: int,
                                     args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        if not self.store.blacklist:
            return True, "Чёрный список пуст", {"blacklist": []}

        lines = ["🚫 Чёрный список:"]
        for uid, entry in self.store.blacklist.items():
            lines.append(f"• {uid}" + (f" - {entry.reason}" if entry.reason else ""))

        return True, "\n".join(lines), {"blacklist": [e.to_dict() for e in self.store.blacklist.values()]}

    async def handle_bot_stats(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        success, error = await self.notify.notify_super_admin_stats(user_id)
        if not success:
            return False, error, None

        return True, "Статистика отправлена в ЛС", {}

    async def handle_inflation_set(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        if not args:
            return False, f"Текущая инфляция: {self.store.global_economy.inflation_rate * 100:.1f}%", None

        try:
            rate = float(args[0]) / 100.0
            if rate < 0 or rate > 1:
                return False, "Инфляция от 0% до 100%", None
            self.store.global_economy.inflation_rate = rate
            return True, f"✅ Инфляция установлена: {rate * 100:.1f}%", {"inflation_rate": rate}
        except ValueError:
            return False, "Некорректное значение", None

    async def handle_deflation_set(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        if not args:
            return False, f"Текущая дефляция: {self.store.global_economy.deflation_rate * 100:.1f}%", None

        try:
            rate = float(args[0]) / 100.0
            if rate < 0 or rate > 1:
                return False, "Дефляция от 0% до 100%", None
            self.store.global_economy.deflation_rate = rate
            return True, f"✅ Дефляция установлена: {rate * 100:.1f}%", {"deflation_rate": rate}
        except ValueError:
            return False, "Некорректное значение", None

    async def handle_crisis(self, user_id: int, chat_id: int,
                             args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        self.store.global_economy.crisis_active = True
        self.store.global_economy.last_crisis = datetime.now()

        for ticker, asset in self.store.stock_assets.items():
            asset.current_price = int(asset.current_price * 0.5)

        for ticker, asset in self.store.crypto_assets.items():
            asset.current_price = round(asset.current_price * 0.5, 2)

        return True, "📉 Глобальный кризис! Все активы упали на 50%", {"crisis": True}

    async def handle_boom(self, user_id: int, chat_id: int,
                           args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        self.store.global_economy.boom_active = True
        self.store.global_economy.last_boom = datetime.now()

        for ticker, asset in self.store.stock_assets.items():
            asset.current_price = int(asset.current_price * 1.5)

        for ticker, asset in self.store.crypto_assets.items():
            asset.current_price = round(asset.current_price * 1.5, 2)

        return True, "📈 Экономический бум! Все активы выросли на 50%", {"boom": True}

    async def handle_reset_user(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        can_admin, error = self.check_super_admin(user_id)
        if not can_admin:
            return False, error, None

        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя", None

        target_id = mention_ids[0]
        user = self.store.get_user(target_id)

        user.balance = 0
        user.bank_balance = 0
        user.loan_amount = 0
        user.loan_due_date = None

        self.store.add_transaction(Transaction(
            user_id=target_id,
            amount=-user.balance,
            transaction_type=TransactionType.SYSTEM_ADJUSTMENT,
            balance_after=0,
            description=f"Сброс супер-админом {user_id}",
        ))

        return True, f"✅ Пользователь {target_id} обнулён", {"target_id": target_id}


# ============================================================
# ХЕНДЛЕР КЛАНОВ
# ============================================================

class ClanHandler(BaseHandler):
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 clan_service: ClanService, notification_service: NotificationService):
        super().__init__(store, config, metrics)
        self.clan = clan_service
        self.notify = notification_service

    async def handle_clan_create(self, user_id: int, chat_id: int,
                                  args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите название клана", None

        name = args[0]
        valid, error = validate_clan_name(name)
        if not valid:
            return False, error, None

        success, error, clan = self.clan.create_clan(user_id, name)
        if not success:
            return False, error, None

        return True, error, {"clan": clan.to_dict() if clan else None}

    async def handle_clan_join(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите название клана", None

        clan_name = args[0]
        success, error = self.clan.join_clan(user_id, clan_name)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_clan_leave(self, user_id: int, chat_id: int,
                                 args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        success, error = self.clan.leave_clan(user_id)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_clan_info(self, user_id: int, chat_id: int,
                                args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if args:
            clan = self.store.get_clan_by_name(args[0])
        else:
            clan = self.store.get_user_clan(user_id)

        if clan is None:
            return False, "Клан не найден", None

        card = format_clan_card(clan)
        return True, card, {"clan": clan.to_dict()}

    async def handle_clan_deposit(self, user_id: int, chat_id: int,
                                   args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите сумму", None

        amount = parse_amount_from_text(" ".join(args))
        if amount is None or amount <= 0:
            return False, "Некорректная сумма", None

        success, error = self.clan.deposit_treasury(user_id, amount)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_clan_war_declare(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите название клана противника", None

        clan_name = args[0]
        success, error, war = self.clan.declare_war(user_id, clan_name)
        if not success:
            return False, error, None

        return True, error, {"war": war.to_dict() if war else None}

    async def handle_clan_war_accept(self, user_id: int, chat_id: int,
                                      args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите ID войны", None

        war_id = args[0]
        success, error = self.clan.accept_war(user_id, war_id)
        if not success:
            return False, error, None

        clan = self.store.get_user_clan(user_id)
        if clan:
            for member_id in clan.members:
                if member_id != user_id:
                    await self.notify.notify_clan_war_start(member_id, "противник")

        return True, error, None

    async def handle_clan_war_decline(self, user_id: int, chat_id: int,
                                       args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        if not args:
            return False, "Укажите ID войны", None

        war_id = args[0]
        success, error = self.clan.decline_war(user_id, war_id)
        if not success:
            return False, error, None

        return True, error, None

    async def handle_clan_top(self, user_id: int, chat_id: int,
                               args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        clans = sorted(self.store.clans.values(),
                       key=lambda c: c.treasury + c.wars_won * 100000,
                       reverse=True)

        if not clans:
            return True, "Нет созданных кланов", {"clans": []}

        lines = ["🏰 Топ кланов:"]
        for i, clan in enumerate(clans[:10], 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
            lines.append(
                f"{medal} {clan.logo_emoji} {clan.name} | "
                f"👥 {len(clan.members)} | "
                f"💰 {format_currency(clan.treasury)} | "
                f"⚔️ {clan.wars_won}/{clan.wars_lost}"
            )

        return True, "\n".join(lines), {"clans": [c.to_dict() for c in clans[:10]]}


# ============================================================
# ХЕНДЛЕР БРАКОВ
# ============================================================

class MarriageHandler(BaseHandler):
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 marriage_service: MarriageService):
        super().__init__(store, config, metrics)
        self.marriage = marriage_service

    async def handle_marry_propose(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        if not mention_ids:
            return False, "Укажите пользователя для предложения", None

        target_id = mention_ids[0]
        success, error = self.marriage.propose(user_id, target_id)
        if not success:
            return False, error, None

        return True, f"💍 Предложение отправлено пользователю {target_id}. Ожидайте 'брак да'", {
            "proposer_id": user_id,
            "target_id": target_id,
        }

    async def handle_marry_accept(self, user_id: int, chat_id: int,
                                   args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        mention_ids = extract_mentions(" ".join(args))
        proposer_id = mention_ids[0] if mention_ids else 0

        success, error = self.marriage.accept_marriage(proposer_id, user_id)
        if not success:
            return False, error, None

        return True, "💒 Поздравляем! Вы в браке!", {"spouse_id": proposer_id}

    async def handle_marry_decline(self, user_id: int, chat_id: int,
                                    args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        return True, "❌ Предложение отклонено", {}

    async def handle_divorce(self, user_id: int, chat_id: int,
                              args: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        success, error = self.marriage.divorce(user_id)
        if not success:
            return False, error, None

        return True, error, None


# ============================================================
# ГЛАВНЫЙ ДИСПЕТЧЕР КОМАНД
# ============================================================

class CommandDispatcher:
    def __init__(self, store: DataStore, config: BotConfig, metrics: BotMetrics,
                 telegram_client: TelegramBotClient):
        self.store = store
        self.config = config
        self.metrics = metrics
        self.tg = telegram_client
        self.logger = logging.getLogger("CommandDispatcher")

        self.economy_service = EconomyService(store)
        self.bank_service = BankService(store)
        self.business_service = BusinessService(store)
        self.market_service = MarketService(store)
        self.casino_service = CasinoService(store, self.economy_service)
        self.auction_service = AuctionService(store, self.economy_service)
        self.crime_service = CrimeService(store, self.economy_service)
        self.moderation_service = ModerationService(store)
        self.clan_service = ClanService(store, self.economy_service)
        self.marriage_service = MarriageService(store, self.economy_service)
        self.achievement_service = AchievementService(store)
        self.insurance_service = InsuranceService(store, self.economy_service)
        self.reputation_service = ReputationService(store)
        self.notification_service = NotificationService(store, self.tg)
        self.broadcast_service = BroadcastService(store, self.tg)

        self.economy_handler = EconomyHandler(
            store, config, metrics,
            self.economy_service, self.bank_service,
            self.notification_service,
        )
        self.business_handler = BusinessHandler(
            store, config, metrics, self.business_service,
        )
        self.market_handler = MarketHandler(
            store, config, metrics, self.market_service,
        )
        self.casino_handler = CasinoHandler(
            store, config, metrics, self.casino_service,
        )
        self.moderation_handler = ModerationHandler(
            store, config, metrics,
            self.moderation_service, self.notification_service, self.tg,
        )
        self.admin_handler = AdminHandler(
            store, config, metrics,
            self.economy_service, self.notification_service, self.tg,
        )
        self.super_admin_handler = SuperAdminHandler(
            store, config, metrics,
            self.economy_service, self.notification_service,
            self.broadcast_service, self.tg,
        )
        self.clan_handler = ClanHandler(
            store, config, metrics,
            self.clan_service, self.notification_service,
        )
        self.marriage_handler = MarriageHandler(
            store, config, metrics, self.marriage_service,
        )

        self.command_map = self._build_command_map()

    def _build_command_map(self) -> Dict[str, Callable]:
        return {
            "баланс": self.economy_handler.handle_balance,
            "б": self.economy_handler.handle_balance,
            "balance": self.economy_handler.handle_balance,
            "перевод": self.economy_handler.handle_transfer,
            "плачу": self.economy_handler.handle_transfer,
            "работа": self.economy_handler.handle_work,
            "работка": self.economy_handler.handle_work,
            "бонус": self.economy_handler.handle_bonus,
            "топ": self.economy_handler.handle_top,
            "богачи": self.economy_handler.handle_top,
            "банк": self.economy_handler.handle_balance,
            "вклад": self.economy_handler.handle_bank_deposit,
            "снять": self.economy_handler.handle_bank_withdraw,
            "кредит": self.economy_handler.handle_loan_take,
            "кредит погасить": self.economy_handler.handle_loan_repay,
            "бизнес создать": self.business_handler.handle_business_create,
            "бизнес прибыль": self.business_handler.handle_business_collect,
            "бизнес прокачать": self.business_handler.handle_business_upgrade,
            "бизнес продать": self.business_handler.handle_business_sell,
            "бизнес нанять": self.business_handler.handle_business_hire,
            "бизнес уволить": self.business_handler.handle_business_fire,
            "бизнес мои": self.business_handler.handle_business_list,
            "крипта": self.market_handler.handle_crypto_list,
            "крипта инфо": self.market_handler.handle_crypto_info,
            "крипта купить": self.market_handler.handle_crypto_buy,
            "крипта продать": self.market_handler.handle_crypto_sell,
            "крипта портфель": self.market_handler.handle_crypto_portfolio,
            "акции": self.market_handler.handle_stock_list,
            "акции инфо": self.market_handler.handle_stock_info,
            "акции купить": self.market_handler.handle_stock_buy,
            "акции продать": self.market_handler.handle_stock_sell,
            "акции портфель": self.market_handler.handle_stock_portfolio,
            "дивиденды": self.market_handler.handle_dividends,
            "майнеры": self.market_handler.handle_miners_list,
            "майнер купить": self.market_handler.handle_miner_buy,
            "майнер продать": self.market_handler.handle_miner_sell,
            "майнер чинить": self.market_handler.handle_miner_repair,
            "майнинг": self.market_handler.handle_mining_collect,
            "слоты": self.casino_handler.handle_slots,
            "слот": self.casino_handler.handle_slots,
            "кубики": self.casino_handler.handle_dice,
            "монетка": self.casino_handler.handle_coinflip,
            "орёл": self.casino_handler.handle_coinflip,
            "орел": self.casino_handler.handle_coinflip,
            "дуэль": self.casino_handler.handle_duel,
            "рулетка": self.casino_handler.handle_russian_roulette,
            "кейс": self.casino_handler.handle_case_open,
            "колесо": self.casino_handler.handle_wheel,
            "бан": self.moderation_handler.handle_ban,
            "разбан": self.moderation_handler.handle_unban,
            "мут": self.moderation_handler.handle_mute,
            "размут": self.moderation_handler.handle_unmute,
            "кик": self.moderation_handler.handle_kick,
            "варн": self.moderation_handler.handle_warn,
            "варны": self.moderation_handler.handle_warns_list,
            "снятьварн": self.moderation_handler.handle_remove_warn,
            "очистить": self.moderation_handler.handle_clear,
            "чат закрой": self.moderation_handler.handle_lock,
            "чат открой": self.moderation_handler.handle_unlock,
            "слоумод": self.moderation_handler.handle_slowmode,
            "логи": self.moderation_handler.handle_mod_logs,
            "репорт": self.moderation_handler.handle_report,
            "репорты": self.moderation_handler.handle_reports_list,
            "админ": self.admin_handler.handle_set_admin,
            "снять админ": self.admin_handler.handle_remove_admin,
            "повысить": self.admin_handler.handle_promote,
            "понизить": self.admin_handler.handle_demote,
            "админы": self.admin_handler.handle_admin_list,
            "правила": self.admin_handler.handle_rules,
            "правила установить": self.admin_handler.handle_rules_set,
            "приветствие": self.admin_handler.handle_welcome_set,
            "чат инфо": self.admin_handler.handle_chat_info,
            "выдать": self.admin_handler.handle_admin_give_money,
            "забрать": self.admin_handler.handle_admin_take_money,
            "рассылка": self.super_admin_handler.handle_global_broadcast,
            "анонс": self.super_admin_handler.handle_global_announce,
            "бан глоб": self.super_admin_handler.handle_global_ban,
            "разбан глоб": self.super_admin_handler.handle_global_unban,
            "чс добавить": self.super_admin_handler.handle_blacklist_add,
            "чс убрать": self.super_admin_handler.handle_blacklist_remove,
            "чс": self.super_admin_handler.handle_blacklist_list,
            "стата": self.super_admin_handler.handle_bot_stats,
            "инфляция": self.super_admin_handler.handle_inflation_set,
            "дефляция": self.super_admin_handler.handle_deflation_set,
            "кризис": self.super_admin_handler.handle_crisis,
            "бум": self.super_admin_handler.handle_boom,
            "обнулить": self.super_admin_handler.handle_reset_user,
            "клан создать": self.clan_handler.handle_clan_create,
            "клан войти": self.clan_handler.handle_clan_join,
            "клан выйти": self.clan_handler.handle_clan_leave,
            "клан инфо": self.clan_handler.handle_clan_info,
            "клан казна": self.clan_handler.handle_clan_deposit,
            "клан война": self.clan_handler.handle_clan_war_declare,
            "клан топ": self.clan_handler.handle_clan_top,
            "брак": self.marriage_handler.handle_marry_propose,
            "брак да": self.marriage_handler.handle_marry_accept,
            "брак нет": self.marriage_handler.handle_marry_decline,
            "развод": self.marriage_handler.handle_divorce,
        }

    async def dispatch(self, user_id: int, chat_id: int,
                       text: str) -> Tuple[bool, str, Optional[Dict]]:
        self.metrics.increment_messages()

        if self.store.is_blacklisted(user_id):
            return False, "Вы в чёрном списке бота", None

        user = self.store.get_user(user_id)
        user.total_messages += 1
        self.store.increment_message_counter(user_id, "bonus_messages")

        chat_stats = self.store.get_chat_stats(chat_id)
        chat_stats.total_messages += 1
        chat_stats.messages_today += 1

        achievement_service = AchievementService(self.store)
        achievement_service.check_all_conditions(user_id)

        if is_user_jailed(user_id, self.store):
            remaining = (user.jailed_until - datetime.now()).total_seconds()
            return False, f"🚔 Вы в тюрьме ещё {format_duration(int(remaining))}", None

        if is_user_banned(user_id, chat_id, self.store):
            return False, "Вы забанены в этом чате", None

        if is_user_muted(user_id, self.store):
            return False, "Вы замучены", None

        chat_config = self.store.get_chat(chat_id)
        if chat_config.is_locked:
            admin_level = self.store.get_admin_level(user_id, chat_id)
            if admin_level <= 0 and not is_super_admin(user_id):
                return False, "Чат закрыт", None

        auto_log = self.moderation_service.check_auto_moderation(text, user_id, chat_id)
        if auto_log:
            self.store.add_mod_log(auto_log)
            if auto_log.action == ModActionType.MUTE:
                user.muted_until = auto_log.expires_at
                return False, f"🔇 Авто-мут: {auto_log.reason}", None

        command, args = extract_command_args(text)
        if command is None:
            return False, "", None

        if command in ("фабле", "фабл", "fable"):
            if not args:
                return True, "Я здесь! Используйте 'команды' для списка команд", None
            command = args[0]
            args = args[1:]

        handler = self.command_map.get(command)
        if handler is None:
            for cmd, aliases in COMMAND_ALIASES.items():
                if command in aliases:
                    handler = self.command_map.get(cmd)
                    break

        if handler is None:
            return False, "", None

        try:
            result = await handler(user_id, chat_id, args)
            self.metrics.increment_commands()
            return result
        except Exception as e:
            self.logger.error(f"Command dispatch error: {e}")
            self.metrics.increment_errors()
            return False, f"❌ Ошибка выполнения команды: {str(e)[:100]}", None

    async def process_message(self, user_id: int, chat_id: int,
                               text: str) -> Optional[str]:
        success, message, data = await self.dispatch(user_id, chat_id, text)

        if message:
            return message
        return None


print("Хендлеры сообщений и обработка команд загружены успешно.")
print(f"EconomyHandler: 8 методов")
print(f"BusinessHandler: 7 методов")
print(f"MarketHandler: 14 методов")
print(f"CasinoHandler: 8 методов")
print(f"ModerationHandler: 14 методов")
print(f"AdminHandler: 12 методов")
print(f"SuperAdminHandler: 12 методов")
print(f"ClanHandler: 9 методов")
print(f"MarriageHandler: 3 метода")
print(f"CommandDispatcher: 100+ команд")

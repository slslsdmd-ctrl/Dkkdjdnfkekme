
# Часть 3: Логика обработки + бизнес-сценарии
# Модуль: game_logic.py

from typing import Any, Dict, List, Optional, Set, Tuple, Union
from datetime import datetime, timedelta
import random
import math
import logging
from dataclasses import asdict

from models import (
    User, ChatConfig, AdminLevel, ModLog, Business, CryptoAsset,
    StockAsset, UserPortfolio, Miner, Auction, Clan, ClanWar,
    Tournament, Pet, ShopItem, UserInventory, Achievement,
    Transaction, GameSession, Report, GlobalEconomy, Earth,
    Vehicle, House, Insurance, BlacklistEntry, ChatStats,
    WorldEvent, GameType, AuctionStatus, ClanWarStatus,
    MarriageStatus, InsuranceClaimReason, TournamentStatus,
    TournamentType, PetRarity, PetMood, EarthRegion,
    ItemRarity, ItemCategory, MinerType, ReputationLevel,
    AchievementCategory, ModActionType, BusinessStatus,
    TransactionType, generate_id, validate_amount,
    calculate_business_income, calculate_miner_income,
    get_reputation_level, has_permission, parse_duration,
    CASINO_MIN_BET, CASINO_MAX_BET, SLOTS_SYMBOLS,
    ROBBERY_SUCCESS_RATE_BANK, ROBBERY_SUCCESS_RATE_CASINO,
    ROBBERY_SUCCESS_RATE_PLAYER, ROBBERY_JAIL_HOURS,
    ROBBERY_MAX_LOOT_PERCENT, TAX_AUDIT_CHANCE,
    TAX_AUDIT_FINE_PERCENT, MAX_WARNS_BEFORE_BAN,
    WARN_EXPIRATION_DAYS, DEFAULT_MUTE_DURATION_MINUTES,
    MAX_MUTE_DURATION_MINUTES, MAX_CLAN_MEMBERS,
    CLAN_CREATION_COST, CLAN_WAR_DURATION_HOURS,
    CLAN_WAR_LOOT_PERCENT, MARRIAGE_COST, DIVORCE_COST,
    MARRIAGE_INCOME_BONUS, INSURANCE_COST_PERCENT,
    INSURANCE_RETURN_PERCENT, INSURANCE_DURATION_DAYS,
    INSURANCE_MIN_BALANCE, REPUTATION_VOTE_COOLDOWN_HOURS,
    REPUTATION_MUTUAL_LIMIT_PER_WEEK, REPUTATION_LOW_THRESHOLD,
    MAX_PET_LEVEL, PET_EVOLUTION_LEVEL,
    PET_BREEDING_COOLDOWN_DAYS, PET_MUTATION_CHANCE,
    TOURNAMENT_MIN_PLAYERS, TOURNAMENT_MAX_PLAYERS,
    TOURNAMENT_ENTRY_FEE_MIN, TOURNAMENT_PRIZE_POOL_PERCENT,
    ACHIEVEMENTS_CONFIG, SUPER_ADMIN_ID, SUPER_ADMIN_LEVEL,
)

from services import DataStore, EconomyService, BankService, BusinessService, MarketService


# ============================================================
# СЕРВИС КАЗИНО И ИГР
# ============================================================

class CasinoService:
    def __init__(self, store: DataStore, economy_service: EconomyService):
        self.store = store
        self.economy = economy_service

    def play_slots(self, user_id: int, bet: int) -> Tuple[bool, str, Dict[str, Any]]:
        if bet < CASINO_MIN_BET:
            return False, f"Минимальная ставка: {CASINO_MIN_BET}", {}
        if bet > CASINO_MAX_BET:
            return False, f"Максимальная ставка: {CASINO_MAX_BET}", {}

        user = self.store.get_user(user_id)
        if user.balance < bet:
            return False, f"Недостаточно средств. Баланс: {user.balance}", {}
        if not self.store.can_user_start_game(user_id):
            return False, "Слишком много активных игр", {}
        if user.jailed_until and user.jailed_until > datetime.now():
            remaining = int((user.jailed_until - datetime.now()).total_seconds() / 60)
            return False, f"Вы в тюрьме ещё {remaining} мин", {}

        session_id = generate_id()
        self.store.register_game_start(user_id, session_id)

        try:
            symbols_list = list(SLOTS_SYMBOLS)
            reels = []
            for _ in range(3):
                reel = [random.choice(symbols_list) for _ in range(3)]
                reels.append(reel)

            win_amount = 0
            win_description = ""

            row1 = [reels[0][0], reels[1][0], reels[2][0]]
            row2 = [reels[0][1], reels[1][1], reels[2][1]]
            row3 = [reels[0][2], reels[1][2], reels[2][2]]

            payouts = {"🍒": 2, "🍋": 3, "🍊": 5, "🍇": 10, "💎": 25, "7️⃣": 50, "🎰": 100}

            for row_num, row in enumerate([row1, row2, row3], 1):
                if row[0] == row[1] == row[2]:
                    symbol = row[0]
                    multiplier = payouts.get(symbol, 1)
                    win_amount += bet * multiplier
                    win_description += f"Линия {row_num}: {symbol}x{multiplier} "

            inventory = self.store.get_inventory(user_id)
            for item_id, expires_str in list(inventory.active_boosters.items()):
                if datetime.now() < datetime.fromisoformat(expires_str) if isinstance(expires_str, str) else expires_str:
                    item = self.store.get_shop_item(item_id)
                    if item and item.category == ItemCategory.CASINO_LUCK and win_amount > 0:
                        win_amount = int(win_amount * (1 + item.boost_percent / 100))

            if win_amount > 0:
                user.balance += win_amount - bet
                result_text = f"Выигрыш: {win_amount} монет! {win_description}"
                transaction_type = TransactionType.CASINO_WIN
            else:
                user.balance -= bet
                win_amount = -bet
                result_text = f"Проигрыш: {bet} монет"
                transaction_type = TransactionType.CASINO_BET

            balance_after = user.balance

            self.store.add_transaction(Transaction(
                user_id=user_id,
                amount=win_amount if win_amount > 0 else -bet,
                transaction_type=transaction_type,
                balance_after=balance_after,
                description=f"Слоты: ставка {bet}",
            ))

            session = GameSession(
                session_id=session_id,
                game_type=GameType.SLOTS,
                user_id=user_id,
                bet_amount=bet,
                result={"reels": reels, "win_amount": win_amount if win_amount > 0 else -bet},
                win_amount=win_amount if win_amount > 0 else -bet,
            )
            self.store.add_game_session(session)

            result_data = {
                "reels": reels,
                "win_amount": win_amount if win_amount > 0 else -bet,
                "balance": balance_after,
            }

            return True, result_text, result_data

        finally:
            self.store.register_game_end(user_id, session_id)

    def play_dice(self, user_id: int, bet: int, guess: Optional[int] = None) -> Tuple[bool, str, Dict[str, Any]]:
        if bet < CASINO_MIN_BET:
            return False, f"Минимальная ставка: {CASINO_MIN_BET}", {}
        if bet > CASINO_MAX_BET:
            return False, f"Максимальная ставка: {CASINO_MAX_BET}", {}

        user = self.store.get_user(user_id)
        if user.balance < bet:
            return False, f"Недостаточно средств. Баланс: {user.balance}", {}
        if not self.store.can_user_start_game(user_id):
            return False, "Слишком много активных игр", {}
        if user.jailed_until and user.jailed_until > datetime.now():
            return False, "Вы в тюрьме", {}

        session_id = generate_id()
        self.store.register_game_start(user_id, session_id)

        try:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            total = dice1 + dice2

            win_amount = 0
            if guess is not None:
                if total == guess:
                    win_amount = bet * 6
                elif abs(total - guess) <= 1:
                    win_amount = bet * 2
                else:
                    win_amount = -bet
            else:
                if total >= 7:
                    win_amount = bet
                else:
                    win_amount = -bet

            if win_amount > 0:
                user.balance += win_amount - bet
                result_text = f"Кубики: {dice1}+{dice2}={total}. Выигрыш: {win_amount}!"
                transaction_type = TransactionType.CASINO_WIN
            else:
                user.balance -= bet
                result_text = f"Кубики: {dice1}+{dice2}={total}. Проигрыш: {bet}"
                transaction_type = TransactionType.CASINO_BET

            balance_after = user.balance

            self.store.add_transaction(Transaction(
                user_id=user_id,
                amount=win_amount if win_amount > 0 else -bet,
                transaction_type=transaction_type,
                balance_after=balance_after,
                description=f"Кубики: ставка {bet}, результат {total}",
            ))

            result_data = {
                "dice1": dice1,
                "dice2": dice2,
                "total": total,
                "win_amount": win_amount,
                "balance": balance_after,
            }

            return True, result_text, result_data

        finally:
            self.store.register_game_end(user_id, session_id)

    def play_coinflip(self, user_id: int, bet: int, choice: str = "орёл") -> Tuple[bool, str, Dict[str, Any]]:
        if bet < CASINO_MIN_BET:
            return False, f"Минимальная ставка: {CASINO_MIN_BET}", {}
        if bet > CASINO_MAX_BET:
            return False, f"Максимальная ставка: {CASINO_MAX_BET}", {}

        user = self.store.get_user(user_id)
        if user.balance < bet:
            return False, f"Недостаточно средств. Баланс: {user.balance}", {}
        if not self.store.can_user_start_game(user_id):
            return False, "Слишком много активных игр", {}
        if user.jailed_until and user.jailed_until > datetime.now():
            return False, "Вы в тюрьме", {}

        session_id = generate_id()
        self.store.register_game_start(user_id, session_id)

        try:
            choice = choice.lower().strip()
            if choice in ["орел", "орёл", "орель", "o"]:
                choice = "орёл"
            elif choice in ["решка", "решка", "r"]:
                choice = "решка"
            else:
                return False, "Выберите 'орёл' или 'решка'", {}

            result = random.choice(["орёл", "решка"])
            win_amount = bet if choice == result else -bet

            if win_amount > 0:
                user.balance += win_amount
                result_text = f"Монетка: {result}. Выигрыш: {win_amount}!"
                transaction_type = TransactionType.CASINO_WIN
            else:
                user.balance -= bet
                result_text = f"Монетка: {result}. Проигрыш: {bet}"
                transaction_type = TransactionType.CASINO_BET

            balance_after = user.balance

            self.store.add_transaction(Transaction(
                user_id=user_id,
                amount=win_amount if win_amount > 0 else -bet,
                transaction_type=transaction_type,
                balance_after=balance_after,
                description=f"Монетка: {choice}, результат {result}",
            ))

            result_data = {
                "choice": choice,
                "result": result,
                "win_amount": win_amount,
                "balance": balance_after,
            }

            return True, result_text, result_data

        finally:
            self.store.register_game_end(user_id, session_id)

    def play_duel(self, challenger_id: int, opponent_id: int, bet: int) -> Tuple[bool, str]:
        if bet < CASINO_MIN_BET:
            return False, f"Минимальная ставка: {CASINO_MIN_BET}"
        if bet > CASINO_MAX_BET:
            return False, f"Максимальная ставка: {CASINO_MAX_BET}"

        if challenger_id == opponent_id:
            return False, "Нельзя вызвать на дуэль самого себя"

        challenger = self.store.get_user(challenger_id)
        opponent = self.store.get_user(opponent_id)

        if challenger.balance < bet:
            return False, f"У вас недостаточно средств. Баланс: {challenger.balance}"
        if opponent.balance < bet:
            return False, f"У противника недостаточно средств"
        if challenger.jailed_until and challenger.jailed_until > datetime.now():
            return False, "Вы в тюрьме"
        if opponent.jailed_until and opponent.jailed_until > datetime.now():
            return False, "Противник в тюрьме"

        challenger_score = random.randint(1, 100)
        opponent_score = random.randint(1, 100)

        if challenger_score > opponent_score:
            winner = challenger
            loser = opponent
            winner_id = challenger_id
            loser_id = challenger_id
        elif opponent_score > challenger_score:
            winner = opponent
            loser = challenger
            winner_id = opponent_id
            loser_id = challenger_id
        else:
            challenger.balance -= bet // 2
            opponent.balance -= bet // 2
            return True, f"Ничья! {challenger_score} - {opponent_score}. Каждый потерял {bet // 2}"

        loser.balance -= bet
        winner.balance += bet

        self.store.add_transaction(Transaction(
            user_id=winner_id,
            amount=bet,
            transaction_type=TransactionType.CASINO_WIN,
            balance_after=winner.balance,
            description=f"Дуэль: победа над {loser_id} ({winner_score} vs {opponent_score})",
        ))

        self.store.add_transaction(Transaction(
            user_id=loser_id,
            amount=-bet,
            transaction_type=TransactionType.CASINO_BET,
            balance_after=loser.balance,
            description=f"Дуэль: поражение от {winner_id} ({opponent_score} vs {winner_score})",
        ))

        return True, f"Дуэль: {winner_score} - {opponent_score}. Победитель: {winner_id}!"

    def play_russian_roulette(self, user_id: int, bet: int) -> Tuple[bool, str]:
        if bet < CASINO_MIN_BET:
            return False, f"Минимальная ставка: {CASINO_MIN_BET}"
        if bet > CASINO_MAX_BET:
            return False, f"Максимальная ставка: {CASINO_MAX_BET}"

        user = self.store.get_user(user_id)
        if user.balance < bet:
            return False, f"Недостаточно средств. Баланс: {user.balance}"
        if user.jailed_until and user.jailed_until > datetime.now():
            return False, "Вы в тюрьме"

        bullet_position = random.randint(1, 6)
        current_position = random.randint(1, 6)

        if current_position == bullet_position:
            user.balance -= bet
            self.store.add_transaction(Transaction(
                user_id=user_id,
                amount=-bet,
                transaction_type=TransactionType.CASINO_BET,
                balance_after=user.balance,
                description=f"Русская рулетка: проигрыш",
            ))
            return True, f"💀 БАХ! Вы проиграли {bet} монет"

        else:
            win_amount = bet * 5
            user.balance += win_amount
            self.store.add_transaction(Transaction(
                user_id=user_id,
                amount=win_amount,
                transaction_type=TransactionType.CASINO_WIN,
                balance_after=user.balance,
                description=f"Русская рулетка: выжил",
            ))
            return True, f"😅 Пронесло! Выигрыш: {win_amount} монет"

    def open_case(self, user_id: int, case_type: str) -> Tuple[bool, str, Dict[str, Any]]:
        cases = {
            "обычный": {"price": 500, "rewards": [100, 200, 300, 400, 500, 750, 1000, 1500]},
            "редкий": {"price": 2000, "rewards": [500, 1000, 1500, 2000, 3000, 5000, 7500, 10000]},
            "эпический": {"price": 10000, "rewards": [2000, 5000, 7500, 10000, 15000, 25000, 50000, 100000]},
            "легендарный": {"price": 50000, "rewards": [10000, 25000, 50000, 75000, 100000, 250000, 500000, 1000000]},
        }

        case_type = case_type.lower()
        if case_type not in cases:
            return False, f"Тип кейса не найден. Доступны: {', '.join(cases.keys())}", {}

        case = cases[case_type]
        user = self.store.get_user(user_id)
        if user.balance < case["price"]:
            return False, f"Недостаточно средств. Нужно: {case['price']}", {}

        user.balance -= case["price"]
        reward = random.choice(case["rewards"])

        if reward > case["price"]:
            user.balance += reward
            result_text = f"Открыт {case_type} кейс! Выпало: {reward} монет (+{reward - case['price']})"
        else:
            result_text = f"Открыт {case_type} кейс! Выпало: {reward} монет (-{case['price'] - reward})"

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=reward - case["price"],
            transaction_type=TransactionType.CASINO_WIN,
            balance_after=user.balance,
            description=f"Кейс {case_type}: {reward}",
        ))

        result_data = {
            "case_type": case_type,
            "cost": case["price"],
            "reward": reward,
            "balance": user.balance,
        }

        return True, result_text, result_data


# ============================================================
# СЕРВИС АУКЦИОНОВ
# ============================================================

class AuctionService:
    def __init__(self, store: DataStore, economy_service: EconomyService):
        self.store = store
        self.economy = economy_service

    def create_auction(self, seller_id: int, item_type: str, item_name: str,
                       starting_price: int, duration_hours: int = 24,
                       item_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str, Optional[Auction]]:
        valid, error = validate_amount(starting_price, 1, 100_000_000)
        if not valid:
            return False, error, None

        if duration_hours < 1 or duration_hours > 168:
            return False, "Длительность от 1 до 168 часов", None

        active_auctions = [a for a in self.store.get_active_auctions() if a.seller_id == seller_id]
        if len(active_auctions) >= 10:
            return False, "Максимум 10 активных аукционов", None

        auction = Auction(
            seller_id=seller_id,
            item_type=item_type,
            item_name=item_name,
            starting_price=starting_price,
            current_bid=starting_price,
            item_data=item_data or {},
            ends_at=datetime.now() + timedelta(hours=duration_hours),
        )
        self.store.auctions[auction.auction_id] = auction
        return True, f"Аукцион создан. ID: {auction.auction_id}", auction

    def place_bid(self, bidder_id: int, auction_id: str, bid_amount: int) -> Tuple[bool, str]:
        auction = self.store.get_auction(auction_id)
        if auction is None:
            return False, "Аукцион не найден"
        if auction.status != AuctionStatus.ACTIVE:
            return False, "Аукцион не активен"
        if auction.ends_at < datetime.now():
            auction.status = AuctionStatus.ENDED
            return False, "Аукцион завершён"
        if auction.seller_id == bidder_id:
            return False, "Нельзя ставить на свой аукцион"

        min_bid = auction.current_bid + auction.min_increment
        if bid_amount < min_bid:
            return False, f"Минимальная ставка: {min_bid}"

        user = self.store.get_user(bidder_id)
        if user.balance < bid_amount:
            return False, f"Недостаточно средств. Баланс: {user.balance}"

        if auction.current_bidder_id != 0:
            old_bidder = self.store.get_user(auction.current_bidder_id)
            old_bidder.balance += auction.current_bid
            self.store.add_transaction(Transaction(
                user_id=auction.current_bidder_id,
                amount=auction.current_bid,
                transaction_type=TransactionType.AUCTION_BID,
                balance_after=old_bidder.balance,
                description=f"Возврат ставки по аукциону {auction_id}",
            ))

        user.balance -= bid_amount
        auction.current_bid = bid_amount
        auction.current_bidder_id = bidder_id
        auction.bids_history.append({
            "bidder_id": bidder_id,
            "amount": bid_amount,
            "timestamp": datetime.now().isoformat(),
        })

        self.store.add_transaction(Transaction(
            user_id=bidder_id,
            amount=-bid_amount,
            transaction_type=TransactionType.AUCTION_BID,
            balance_after=user.balance,
            description=f"Ставка на аукцион {auction.item_name}",
            related_item_id=auction_id,
        ))

        return True, f"Ставка {bid_amount} принята. Вы лидируете"

    def finalize_auction(self, auction_id: str) -> Tuple[bool, str]:
        auction = self.store.get_auction(auction_id)
        if auction is None:
            return False, "Аукцион не найден"
        if auction.status != AuctionStatus.ACTIVE:
            return False, "Аукцион не активен"

        if auction.ends_at > datetime.now():
            return False, "Аукцион ещё не завершён"

        if auction.current_bidder_id == 0:
            auction.status = AuctionStatus.CANCELLED
            return True, "Аукцион отменён (нет ставок)"

        seller = self.store.get_user(auction.seller_id)
        commission = int(auction.current_bid * 0.05)
        revenue = auction.current_bid - commission
        seller.balance += revenue
        auction.status = AuctionStatus.SOLD

        self.store.add_transaction(Transaction(
            user_id=auction.seller_id,
            amount=revenue,
            transaction_type=TransactionType.AUCTION_SALE,
            balance_after=seller.balance,
            description=f"Продажа с аукциона: {auction.item_name}",
            related_item_id=auction_id,
        ))

        return True, f"Аукцион завершён. Продавец получил {revenue} монет (комиссия {commission})"


# ============================================================
# СЕРВИС КРИМИНАЛА
# ============================================================

class CrimeService:
    def __init__(self, store: DataStore, economy_service: EconomyService):
        self.store = store
        self.economy = economy_service

    def rob_bank(self, user_id: int) -> Tuple[bool, str, int]:
        user = self.store.get_user(user_id)
        if user.jailed_until and user.jailed_until > datetime.now():
            remaining = int((user.jailed_until - datetime.now()).total_seconds() / 60)
            return False, f"Вы в тюрьме ещё {remaining} мин", 0
        if user.karma < -50:
            return False, "Слишком низкая карма для ограбления", 0

        success_chance = ROBBERY_SUCCESS_RATE_BANK

        inventory = self.store.get_inventory(user_id)
        for item_id, expires_str in list(inventory.active_boosters.items()):
            if datetime.now() < datetime.fromisoformat(expires_str) if isinstance(expires_str, str) else expires_str:
                item = self.store.get_shop_item(item_id)
                if item and item.category == ItemCategory.ROBBERY_TOOL:
                    success_chance += item.boost_percent / 100.0

        if random.random() < success_chance:
            loot = random.randint(10000, 100000)
            user.balance += loot
            user.karma -= 30

            self.store.add_transaction(Transaction(
                user_id=user_id,
                amount=loot,
                transaction_type=TransactionType.ROBBERY_LOOT,
                balance_after=user.balance,
                description=f"Ограбление банка: +{loot}",
            ))
            return True, f"🎉 Банк ограблен! Добыча: {loot} монет", loot
        else:
            user.karma -= 10
            jail_time = ROBBERY_JAIL_HOURS
            user.jailed_until = datetime.now() + timedelta(hours=jail_time)

            self.store.add_mod_log(ModLog(
                chat_id=0,
                moderator_id=0,
                target_id=user_id,
                action=ModActionType.MUTE,
                reason="Неудачное ограбление банка",
                duration_minutes=jail_time * 60,
                expires_at=user.jailed_until,
            ))
            return False, f"🚔 Провал! Вы в тюрьме на {jail_time} час", 0

    def rob_casino(self, user_id: int) -> Tuple[bool, str, int]:
        user = self.store.get_user(user_id)
        if user.jailed_until and user.jailed_until > datetime.now():
            return False, "Вы в тюрьме", 0
        if user.karma < -100:
            return False, "Слишком низкая карма", 0
        if user.balance < 50000:
            return False, "Нужно минимум 50000 монет для подготовки", 0

        success_chance = ROBBERY_SUCCESS_RATE_CASINO

        inventory = self.store.get_inventory(user_id)
        for item_id, expires_str in list(inventory.active_boosters.items()):
            if datetime.now() < datetime.fromisoformat(expires_str) if isinstance(expires_str, str) else expires_str:
                item = self.store.get_shop_item(item_id)
                if item and item.category == ItemCategory.ROBBERY_TOOL:
                    success_chance += item.boost_percent / 100.0

        user.balance -= 50000

        if random.random() < success_chance:
            loot = random.randint(50000, 500000)
            user.balance += loot
            user.karma -= 50

            self.store.add_transaction(Transaction(
                user_id=user_id,
                amount=loot - 50000,
                transaction_type=TransactionType.ROBBERY_LOOT,
                balance_after=user.balance,
                description=f"Ограбление казино: +{loot}",
            ))
            return True, f"💰 Казино ограблено! Добыча: {loot} монет", loot
        else:
            user.karma -= 20
            jail_time = ROBBERY_JAIL_HOURS * 3
            user.jailed_until = datetime.now() + timedelta(hours=jail_time)
            return False, f"🚔 Спецназ! Вы в тюрьме на {jail_time} часов", 0

    def rob_player(self, robber_id: int, victim_id: int) -> Tuple[bool, str, int]:
        if robber_id == victim_id:
            return False, "Нельзя ограбить самого себя", 0

        robber = self.store.get_user(robber_id)
        victim = self.store.get_user(victim_id)

        if robber.jailed_until and robber.jailed_until > datetime.now():
            return False, "Вы в тюрьме", 0
        if robber.karma < -20:
            return False, "Слишком низкая карма", 0
        if victim.balance < 100:
            return False, "У жертвы слишком мало денег", 0

        success_chance = ROBBERY_SUCCESS_RATE_PLAYER

        inventory = self.store.get_inventory(robber_id)
        for item_id, expires_str in list(inventory.active_boosters.items()):
            if datetime.now() < datetime.fromisoformat(expires_str) if isinstance(expires_str, str) else expires_str:
                item = self.store.get_shop_item(item_id)
                if item and item.category == ItemCategory.ROBBERY_TOOL:
                    success_chance += item.boost_percent / 100.0

        if random.random() < success_chance:
            loot = int(victim.balance * random.uniform(0.05, ROBBERY_MAX_LOOT_PERCENT))
            victim.balance -= loot
            robber.balance += loot
            robber.karma -= 15
            victim.karma += 5

            self.store.add_transaction(Transaction(
                user_id=robber_id,
                amount=loot,
                transaction_type=TransactionType.ROBBERY_LOOT,
                balance_after=robber.balance,
                description=f"Ограбление игрока {victim_id}",
                related_user_id=victim_id,
            ))
            self.store.add_transaction(Transaction(
                user_id=victim_id,
                amount=-loot,
                transaction_type=TransactionType.ROBBERY_LOSS,
                balance_after=victim.balance,
                description=f"Ограблен игроком {robber_id}",
                related_user_id=robber_id,
            ))
            return True, f"🕵️ Ограбление удалось! Добыча: {loot} монет", loot
        else:
            robber.karma -= 10
            jail_time = ROBBERY_JAIL_HOURS
            robber.jailed_until = datetime.now() + timedelta(hours=jail_time)
            return False, f"🚔 Поймали! Вы в тюрьме на {jail_time} час", 0

    def tax_audit(self, user_id: int) -> Tuple[bool, str, int]:
        user = self.store.get_user(user_id)
        if random.random() > TAX_AUDIT_CHANCE:
            user.karma += 1
            return True, "Проверка пройдена, нарушений нет", 0

        businesses = self.store.get_user_businesses(user_id)
        total_value = sum(b.current_value for b in businesses)
        total_balance = user.balance + user.bank_balance

        fine = int((total_value + total_balance) * TAX_AUDIT_FINE_PERCENT)
        fine = max(fine, 1000)

        if user.balance >= fine:
            user.balance -= fine
        elif user.balance + user.bank_balance >= fine:
            needed = fine - user.balance
            user.balance = 0
            user.bank_balance -= needed
        else:
            user.balance = 0
            user.bank_balance = 0

        user.karma -= 5

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-fine,
            transaction_type=TransactionType.TAX_AUDIT_FINE,
            balance_after=user.balance,
            description=f"Штраф налоговой проверки",
        ))
        return False, f"📋 Налоговая проверка! Штраф: {fine} монет", fine

    def street_find(self, user_id: int) -> Tuple[bool, str, int]:
        if random.random() > 0.05:
            return False, "Ничего не найдено", 0

        find_amount = random.randint(50, 5000)
        user = self.store.get_user(user_id)
        user.balance += find_amount
        user.karma += 2

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=find_amount,
            transaction_type=TransactionType.BONUS,
            balance_after=user.balance,
            description=f"Находка на улице",
        ))
        return True, f"🍀 Вы нашли {find_amount} монет!", find_amount


# ============================================================
# СЕРВИС МОДЕРАЦИИ
# ============================================================

class ModerationService:
    def __init__(self, store: DataStore):
        self.store = store

    def check_permission(self, moderator_id: int, chat_id: int, action: str) -> Tuple[bool, str]:
        if is_super_admin(moderator_id):
            return True, ""

        level = self.store.get_admin_level(moderator_id, chat_id)
        if level <= 0:
            return False, "У вас нет прав модератора"

        if not has_permission(level, action):
            return False, f"Недостаточно прав. Ваш уровень: {level}"

        return True, ""

    def warn_user(self, moderator_id: int, target_id: int, chat_id: int,
                  reason: str = "") -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "warn")
        if not can_mod:
            return False, error

        if is_super_admin(target_id):
            return False, "Нельзя выдать варн супер-админу"

        target_level = self.store.get_admin_level(target_id, chat_id)
        moderator_level = self.store.get_admin_level(moderator_id, chat_id)
        if target_level >= moderator_level and not is_super_admin(moderator_id):
            return False, "Нельзя выдать варн администратору с таким же или более высоким уровнем"

        active_warns = self.store.get_active_warns(target_id, chat_id)
        if len(active_warns) >= MAX_WARNS_BEFORE_BAN - 1:
            self.ban_user(0, target_id, chat_id, f"Авто-бан: {MAX_WARNS_BEFORE_BAN} варнов")
            return True, f"Варн #{len(active_warns) + 1} выдан. Автоматический бан за {MAX_WARNS_BEFORE_BAN} варнов"

        log = ModLog(
            chat_id=chat_id,
            moderator_id=moderator_id,
            target_id=target_id,
            action=ModActionType.WARN,
            reason=reason,
            expires_at=datetime.now() + timedelta(days=WARN_EXPIRATION_DAYS),
        )
        self.store.add_mod_log(log)

        chat_config = self.store.get_chat(chat_id)
        chat_stats = self.store.get_chat_stats(chat_id)
        chat_stats.warns_today += 1

        return True, f"Варн #{len(active_warns) + 1} выдан пользователю {target_id}"

    def mute_user(self, moderator_id: int, target_id: int, chat_id: int,
                  duration_minutes: int = DEFAULT_MUTE_DURATION_MINUTES,
                  reason: str = "") -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "mute")
        if not can_mod:
            return False, error

        if is_super_admin(target_id):
            return False, "Нельзя замутить супер-админа"

        target_level = self.store.get_admin_level(target_id, chat_id)
        moderator_level = self.store.get_admin_level(moderator_id, chat_id)
        if target_level >= moderator_level and not is_super_admin(moderator_id):
            return False, "Нельзя замутить администратора с таким же или более высоким уровнем"

        valid, error = validate_duration_minutes(duration_minutes)
        if not valid:
            return False, error

        expires_at = datetime.now() + timedelta(minutes=duration_minutes)
        target = self.store.get_user(target_id)
        target.muted_until = expires_at

        log = ModLog(
            chat_id=chat_id,
            moderator_id=moderator_id,
            target_id=target_id,
            action=ModActionType.MUTE,
            reason=reason,
            duration_minutes=duration_minutes,
            expires_at=expires_at,
        )
        self.store.add_mod_log(log)

        chat_stats = self.store.get_chat_stats(chat_id)
        chat_stats.mutes_today += 1

        return True, f"Пользователь {target_id} замучен на {duration_minutes} мин"

    def unmute_user(self, moderator_id: int, target_id: int, chat_id: int) -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "mute")
        if not can_mod:
            return False, error

        target = self.store.get_user(target_id)
        if target.muted_until is None or target.muted_until <= datetime.now():
            return False, "Пользователь не замучен"

        target.muted_until = None

        active_mutes = self.store.get_active_mutes(target_id, chat_id)
        for log in active_mutes:
            log.is_active = False
            log.removed_by = moderator_id
            log.removed_at = datetime.now()

        return True, f"Мут с пользователя {target_id} снят"

    def kick_user(self, moderator_id: int, target_id: int, chat_id: int,
                  reason: str = "") -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "kick")
        if not can_mod:
            return False, error

        if is_super_admin(target_id):
            return False, "Нельзя кикнуть супер-админа"

        log = ModLog(
            chat_id=chat_id,
            moderator_id=moderator_id,
            target_id=target_id,
            action=ModActionType.KICK,
            reason=reason,
        )
        self.store.add_mod_log(log)

        chat_stats = self.store.get_chat_stats(chat_id)
        chat_stats.kicks_today += 1

        return True, f"Пользователь {target_id} кикнут"

    def ban_user(self, moderator_id: int, target_id: int, chat_id: int,
                 reason: str = "", duration_minutes: int = 0) -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "ban")
        if not can_mod:
            return False, error

        if is_super_admin(target_id):
            return False, "Нельзя забанить супер-админа"

        expires_at = datetime.now() + timedelta(minutes=duration_minutes) if duration_minutes > 0 else None

        log = ModLog(
            chat_id=chat_id,
            moderator_id=moderator_id,
            target_id=target_id,
            action=ModActionType.BAN,
            reason=reason,
            duration_minutes=duration_minutes,
            expires_at=expires_at,
        )
        self.store.add_mod_log(log)

        chat_stats = self.store.get_chat_stats(chat_id)
        chat_stats.bans_today += 1

        if duration_minutes > 0:
            return True, f"Пользователь {target_id} забанен на {duration_minutes} мин"
        return True, f"Пользователь {target_id} забанен навсегда"

    def unban_user(self, moderator_id: int, target_id: int, chat_id: int) -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "ban")
        if not can_mod:
            return False, error

        for log in self.store.mod_logs:
            if (log.target_id == target_id and log.chat_id == chat_id
                    and log.action == ModActionType.BAN and log.is_active):
                log.is_active = False
                log.removed_by = moderator_id
                log.removed_at = datetime.now()

        return True, f"Пользователь {target_id} разбанен"

    def global_ban_user(self, moderator_id: int, target_id: int, reason: str = "") -> Tuple[bool, str]:
        if not is_super_admin(moderator_id):
            return False, "Только супер-админ может банить глобально"

        log = ModLog(
            chat_id=0,
            moderator_id=moderator_id,
            target_id=target_id,
            action=ModActionType.GLOBAL_BAN,
            reason=reason,
        )
        self.store.add_mod_log(log)

        return True, f"Пользователь {target_id} забанен глобально"

    def global_unban_user(self, moderator_id: int, target_id: int) -> Tuple[bool, str]:
        if not is_super_admin(moderator_id):
            return False, "Только супер-админ может разбанивать глобально"

        for log in self.store.mod_logs:
            if (log.target_id == target_id
                    and log.action == ModActionType.GLOBAL_BAN and log.is_active):
                log.is_active = False
                log.removed_by = moderator_id
                log.removed_at = datetime.now()

        return True, f"Глобальный бан с пользователя {target_id} снят"

    def clear_messages(self, moderator_id: int, chat_id: int,
                       count: int = 10, target_id: Optional[int] = None) -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "clear_chat")
        if not can_mod:
            return False, error

        if count < 1 or count > 1000:
            return False, "Количество сообщений от 1 до 1000"

        log = ModLog(
            chat_id=chat_id,
            moderator_id=moderator_id,
            target_id=target_id or 0,
            action=ModActionType.CLEAR,
            reason=f"Удалено {count} сообщений",
            duration_minutes=count,
        )
        self.store.add_mod_log(log)

        return True, f"Удалено {count} сообщений"

    def lock_chat(self, moderator_id: int, chat_id: int) -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "chat_settings")
        if not can_mod:
            return False, error

        chat_config = self.store.get_chat(chat_id)
        chat_config.is_locked = True

        log = ModLog(
            chat_id=chat_id,
            moderator_id=moderator_id,
            target_id=0,
            action=ModActionType.LOCK,
            reason="Чат закрыт",
        )
        self.store.add_mod_log(log)

        return True, "Чат закрыт"

    def unlock_chat(self, moderator_id: int, chat_id: int) -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "chat_settings")
        if not can_mod:
            return False, error

        chat_config = self.store.get_chat(chat_id)
        chat_config.is_locked = False

        log = ModLog(
            chat_id=chat_id,
            moderator_id=moderator_id,
            target_id=0,
            action=ModActionType.UNLOCK,
            reason="Чат открыт",
        )
        self.store.add_mod_log(log)

        return True, "Чат открыт"

    def set_slowmode(self, moderator_id: int, chat_id: int, seconds: int) -> Tuple[bool, str]:
        can_mod, error = self.check_permission(moderator_id, chat_id, "chat_settings")
        if not can_mod:
            return False, error

        if seconds < 0 or seconds > 3600:
            return False, "Слоумод от 0 до 3600 секунд"

        chat_config = self.store.get_chat(chat_id)
        chat_config.slowmode_seconds = seconds

        log = ModLog(
            chat_id=chat_id,
            moderator_id=moderator_id,
            target_id=0,
            action=ModActionType.SLOWMODE,
            reason=f"Слоумод {seconds} сек",
            duration_minutes=seconds,
        )
        self.store.add_mod_log(log)

        if seconds == 0:
            return True, "Слоумод выключен"
        return True, f"Слоумод установлен: {seconds} сек"

    def check_auto_moderation(self, message_text: str, user_id: int, chat_id: int) -> Optional[ModLog]:
        chat_config = self.store.get_chat(chat_id)

        if chat_config.ii_moderation_enabled:
            toxicity = self.analyze_toxicity(message_text)
            user = self.store.get_user(user_id)
            user.toxicity_score = user.toxicity_score * 0.9 + toxicity * 0.1

            if toxicity > 0.8:
                return ModLog(
                    chat_id=chat_id,
                    moderator_id=0,
                    target_id=user_id,
                    action=ModActionType.MUTE,
                    reason=f"ИИ-модерация: токсичность {toxicity:.0%}",
                    duration_minutes=60,
                    expires_at=datetime.now() + timedelta(hours=1),
                )

            if toxicity > 0.5 and user.toxicity_score > 0.6:
                return ModLog(
                    chat_id=chat_id,
                    moderator_id=0,
                    target_id=user_id,
                    action=ModActionType.WARN,
                    reason=f"ИИ-модерация: повышенная токсичность {user.toxicity_score:.0%}",
                    expires_at=datetime.now() + timedelta(days=WARN_EXPIRATION_DAYS),
                )

        if chat_config.antimat_enabled:
            for word in chat_config.filter_words:
                if word.lower() in message_text.lower():
                    return ModLog(
                        chat_id=chat_id,
                        moderator_id=0,
                        target_id=user_id,
                        action=ModActionType.WARN,
                        reason=f"Авто-варн: запрещённое слово",
                        expires_at=datetime.now() + timedelta(days=WARN_EXPIRATION_DAYS),
                    )

        if chat_config.antispam_enabled:
            msg_count = self.store.increment_message_counter(user_id, f"spam_{chat_id}")
            if msg_count > 5:
                return ModLog(
                    chat_id=chat_id,
                    moderator_id=0,
                    target_id=user_id,
                    action=ModActionType.MUTE,
                    reason="Авто-мут: спам",
                    duration_minutes=10,
                    expires_at=datetime.now() + timedelta(minutes=10),
                )

        if chat_config.antilink_enabled:
            if "http://" in message_text or "https://" in message_text or "t.me/" in message_text:
                return ModLog(
                    chat_id=chat_id,
                    moderator_id=0,
                    target_id=user_id,
                    action=ModActionType.WARN,
                    reason="Авто-варн: ссылки запрещены",
                    expires_at=datetime.now() + timedelta(days=WARN_EXPIRATION_DAYS),
                )

        return None

    def analyze_toxicity(self, text: str) -> float:
        toxic_words = [
            "тупой", "идиот", "дурак", "дебил", "лох", "чмо",
            "убейся", "сдохни", "ненавижу", "отвратительный",
            "бесишь", "заткнись", "пошёл ты", "fuck", "shit",
        ]
        text_lower = text.lower()
        score = 0.0
        for word in toxic_words:
            if word in text_lower:
                score += 0.15
        return min(score, 1.0)


# ============================================================
# СЕРВИС КЛАНОВ
# ============================================================

class ClanService:
    def __init__(self, store: DataStore, economy_service: EconomyService):
        self.store = store
        self.economy = economy_service

    def create_clan(self, leader_id: int, name: str) -> Tuple[bool, str, Optional[Clan]]:
        user = self.store.get_user(leader_id)
        if user.balance < CLAN_CREATION_COST:
            return False, f"Недостаточно средств. Нужно: {CLAN_CREATION_COST}", None

        existing = self.store.get_clan_by_name(name)
        if existing:
            return False, "Клан с таким названием уже существует", None

        existing_clan = self.store.get_user_clan(leader_id)
        if existing_clan:
            return False, "Вы уже состоите в клане", None

        user.balance -= CLAN_CREATION_COST

        clan = Clan(
            name=name,
            leader_id=leader_id,
            members=[leader_id],
        )
        self.store.clans[clan.clan_id] = clan
        self.store.user_clans[leader_id] = clan.clan_id

        self.store.add_transaction(Transaction(
            user_id=leader_id,
            amount=-CLAN_CREATION_COST,
            transaction_type=TransactionType.CLAN_CREATION,
            balance_after=user.balance,
            description=f"Создание клана {name}",
        ))

        return True, f"Клан '{name}' создан", clan

    def join_clan(self, user_id: int, clan_name: str) -> Tuple[bool, str]:
        clan = self.store.get_clan_by_name(clan_name)
        if clan is None:
            return False, "Клан не найден"

        if len(clan.members) >= MAX_CLAN_MEMBERS:
            return False, "Клан заполнен"

        existing_clan = self.store.get_user_clan(user_id)
        if existing_clan:
            return False, "Вы уже в клане"

        self.store.add_clan_member(clan.clan_id, user_id)
        return True, f"Вы вступили в клан '{clan.name}'"

    def leave_clan(self, user_id: int) -> Tuple[bool, str]:
        clan = self.store.get_user_clan(user_id)
        if clan is None:
            return False, "Вы не в клане"

        if clan.leader_id == user_id:
            if len(clan.members) > 1:
                return False, "Сначала передайте лидерство другому"
            else:
                self.store.remove_clan_member(clan.clan_id, user_id)
                del self.store.clans[clan.clan_id]
                return True, "Клан распущен"

        self.store.remove_clan_member(clan.clan_id, user_id)
        return True, f"Вы покинули клан '{clan.name}'"

    def deposit_treasury(self, user_id: int, amount: int) -> Tuple[bool, str]:
        clan = self.store.get_user_clan(user_id)
        if clan is None:
            return False, "Вы не в клане"

        user = self.store.get_user(user_id)
        if user.balance < amount:
            return False, f"Недостаточно средств. Баланс: {user.balance}"

        user.balance -= amount
        clan.treasury += amount

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-amount,
            transaction_type=TransactionType.CLAN_DEPOSIT,
            balance_after=user.balance,
            description=f"Взнос в казну клана {clan.name}",
        ))

        return True, f"Внесено {amount} в казну клана. Казна: {clan.treasury}"

    def declare_war(self, attacker_leader_id: int, defender_clan_name: str) -> Tuple[bool, str, Optional[ClanWar]]:
        attacker_clan = self.store.get_user_clan(attacker_leader_id)
        if attacker_clan is None:
            return False, "Вы не в клане", None
        if attacker_clan.leader_id != attacker_leader_id:
            return False, "Только лидер может объявлять войну", None
        if attacker_clan.treasury < 100000:
            return False, "Нужно 100000 в казне для войны", None

        defender_clan = self.store.get_clan_by_name(defender_clan_name)
        if defender_clan is None:
            return False, "Клан противника не найден", None
        if defender_clan.clan_id == attacker_clan.clan_id:
            return False, "Нельзя воевать с собой", None

        attacker_clan.treasury -= 100000

        war = ClanWar(
            attacker_clan_id=attacker_clan.clan_id,
            defender_clan_id=defender_clan.clan_id,
            status=ClanWarStatus.PENDING,
        )
        self.store.clan_wars[war.war_id] = war

        return True, f"Война объявлена клану '{defender_clan.name}'. Ожидание ответа", war

    def accept_war(self, defender_leader_id: int, war_id: str) -> Tuple[bool, str]:
        war = self.store.get_clan_war(war_id)
        if war is None:
            return False, "Война не найдена"

        defender_clan = self.store.get_clan(war.defender_clan_id)
        if defender_clan is None or defender_clan.leader_id != defender_leader_id:
            return False, "Только лидер обороняющегося клана может принять войну"

        if war.status != ClanWarStatus.PENDING:
            return False, "Война не в ожидании"

        war.status = ClanWarStatus.ACTIVE
        war.started_at = datetime.now()
        war.ends_at = datetime.now() + timedelta(hours=CLAN_WAR_DURATION_HOURS)

        return True, "Война началась!"

    def decline_war(self, defender_leader_id: int, war_id: str) -> Tuple[bool, str]:
        war = self.store.get_clan_war(war_id)
        if war is None:
            return False, "Война не найдена"

        defender_clan = self.store.get_clan(war.defender_clan_id)
        if defender_clan is None or defender_clan.leader_id != defender_leader_id:
            return False, "Только лидер может отклонить войну"

        war.status = ClanWarStatus.DECLINED

        attacker_clan = self.store.get_clan(war.attacker_clan_id)
        if attacker_clan:
            attacker_clan.treasury += 50000

        return True, "Война отклонена. Атакующий клан получил 50000 назад"

    def add_war_score(self, clan_id: str, points: int) -> None:
        for war in self.store.get_active_clan_wars():
            if war.attacker_clan_id == clan_id:
                war.attacker_score += points
            elif war.defender_clan_id == clan_id:
                war.defender_score += points

    def finalize_war(self, war_id: str) -> Tuple[bool, str]:
        war = self.store.get_clan_war(war_id)
        if war is None or war.status != ClanWarStatus.ACTIVE:
            return False, "Война не активна"

        if war.ends_at > datetime.now():
            return False, "Война ещё не завершена"

        attacker_clan = self.store.get_clan(war.attacker_clan_id)
        defender_clan = self.store.get_clan(war.defender_clan_id)

        if war.attacker_score > war.defender_score:
            winner = attacker_clan
            loser = defender_clan
            war.winner_id = war.attacker_clan_id
        elif war.defender_score > war.attacker_score:
            winner = defender_clan
            loser = attacker_clan
            war.winner_id = war.defender_clan_id
        else:
            war.status = ClanWarStatus.FINISHED
            return True, "Ничья! Казна не тронута"

        if loser:
            loot = int(loser.treasury * CLAN_WAR_LOOT_PERCENT)
            loser.treasury -= loot
            loser.wars_lost += 1
            loser.war_debuff_until = datetime.now() + timedelta(days=3)

        if winner:
            winner.treasury += loot
            winner.wars_won += 1

        war.loot_amount = loot
        war.status = ClanWarStatus.FINISHED

        return True, f"Война завершена! Победитель: {winner.name if winner else 'Нет'}. Захвачено: {loot}"


# ============================================================
# СЕРВИС БРАКОВ
# ============================================================

class MarriageService:
    def __init__(self, store: DataStore, economy_service: EconomyService):
        self.store = store
        self.economy = economy_service

    def propose(self, proposer_id: int, target_id: int) -> Tuple[bool, str]:
        if proposer_id == target_id:
            return False, "Нельзя жениться на себе"

        proposer = self.store.get_user(proposer_id)
        target = self.store.get_user(target_id)

        if proposer.marriage_status == MarriageStatus.MARRIED:
            return False, "Вы уже в браке"
        if target.marriage_status == MarriageStatus.MARRIED:
            return False, "Пользователь уже в браке"
        if proposer.balance < MARRIAGE_COST:
            return False, f"Недостаточно средств. Нужно: {MARRIAGE_COST}"

        return True, f"Предложение отправлено. Ожидайте ответа"

    def accept_marriage(self, proposer_id: int, target_id: int) -> Tuple[bool, str]:
        proposer = self.store.get_user(proposer_id)
        target = self.store.get_user(target_id)

        if proposer.marriage_status == MarriageStatus.MARRIED:
            return False, "Предложивший уже в браке"
        if target.marriage_status == MarriageStatus.MARRIED:
            return False, "Вы уже в браке"

        if proposer.balance < MARRIAGE_COST:
            return False, f"У предложившего недостаточно средств"

        proposer.balance -= MARRIAGE_COST
        proposer.marriage_status = MarriageStatus.MARRIED
        proposer.spouse_id = target_id

        target.marriage_status = MarriageStatus.MARRIED
        target.spouse_id = proposer_id

        self.store.add_transaction(Transaction(
            user_id=proposer_id,
            amount=-MARRIAGE_COST,
            transaction_type=TransactionType.MARRIAGE_COST,
            balance_after=proposer.balance,
            description=f"Брак с {target_id}",
            related_user_id=target_id,
        ))

        return True, "💍 Брак заключён! Поздравляем!"

    def divorce(self, initiator_id: int) -> Tuple[bool, str]:
        initiator = self.store.get_user(initiator_id)
        if initiator.marriage_status != MarriageStatus.MARRIED:
            return False, "Вы не в браке"

        spouse = self.store.get_user(initiator.spouse_id) if initiator.spouse_id else None
        if initiator.balance < DIVORCE_COST:
            return False, f"Недостаточно средств. Нужно: {DIVORCE_COST}"

        initiator.balance -= DIVORCE_COST
        initiator.marriage_status = MarriageStatus.DIVORCED

        if spouse:
            spouse.marriage_status = MarriageStatus.DIVORCED
            spouse.spouse_id = None

            if spouse.joint_balance_enabled:
                spouse.joint_balance_enabled = False

        initiator.spouse_id = None
        if initiator.joint_balance_enabled:
            initiator.joint_balance_enabled = False

        self.store.add_transaction(Transaction(
            user_id=initiator_id,
            amount=-DIVORCE_COST,
            transaction_type=TransactionType.DIVORCE_COST,
            balance_after=initiator.balance,
            description=f"Развод",
        ))

        return True, "💔 Развод оформлен"


# ============================================================
# СЕРВИС ДОСТИЖЕНИЙ
# ============================================================

class AchievementService:
    def __init__(self, store: DataStore):
        self.store = store
        self.initialize_achievements()

    def initialize_achievements(self) -> None:
        for config in ACHIEVEMENTS_CONFIG:
            achievement = Achievement(
                achievement_id=config["achievement_id"],
                name=config["name"],
                description=config["description"],
                category=config["category"],
                reward=config["reward"],
                hidden=config.get("hidden", False),
            )
            self.store.achievements[achievement.achievement_id] = achievement

    def check_and_award(self, user_id: int, achievement_id: int) -> Tuple[bool, str]:
        user = self.store.get_user(user_id)
        if achievement_id in user.achievements:
            return False, "Достижение уже получено"

        achievement = self.store.get_achievement(achievement_id)
        if achievement is None:
            return False, "Достижение не найдено"

        user.achievements.add(achievement_id)
        if achievement.reward > 0:
            user.balance += achievement.reward

            self.store.add_transaction(Transaction(
                user_id=user_id,
                amount=achievement.reward,
                transaction_type=TransactionType.BONUS,
                balance_after=user.balance,
                description=f"Награда за достижение: {achievement.name}",
            ))

        return True, f"🏆 Достижение: {achievement.name}! +{achievement.reward} монет"

    def check_all_conditions(self, user_id: int) -> List[Tuple[int, bool, str]]:
        user = self.store.get_user(user_id)
        results = []

        if 1 not in user.achievements and user.total_messages > 0:
            results.append((1, True, self.check_and_award(user_id, 1)[1]))

        if 2 not in user.achievements and user.balance >= 100_000:
            results.append((2, True, self.check_and_award(user_id, 2)[1]))

        if 3 not in user.achievements and user.balance >= 1_000_000:
            results.append((3, True, self.check_and_award(user_id, 3)[1]))

        if 4 not in user.achievements and user.balance >= 1_000_000_000:
            results.append((4, True, self.check_and_award(user_id, 4)[1]))

        if 5 not in user.achievements and user.balance == 0:
            results.append((5, True, self.check_and_award(user_id, 5)[1]))

        if 11 not in user.achievements:
            businesses = self.store.get_user_businesses(user_id)
            if len(businesses) > 0:
                results.append((11, True, self.check_and_award(user_id, 11)[1]))

        if 12 not in user.achievements:
            businesses = self.store.get_user_businesses(user_id)
            if len(businesses) >= 5:
                results.append((12, True, self.check_and_award(user_id, 12)[1]))

        if 13 not in user.achievements:
            businesses = self.store.get_user_businesses(user_id)
            if len(businesses) >= 10:
                results.append((13, True, self.check_and_award(user_id, 13)[1]))

        if 24 not in user.achievements:
            sessions = self.store.get_user_game_sessions(user_id)
            if len(sessions) >= 10:
                results.append((24, True, self.check_and_award(user_id, 24)[1]))

        if 41 not in user.achievements and user.marriage_status == MarriageStatus.MARRIED:
            results.append((41, True, self.check_and_award(user_id, 41)[1]))

        if 44 not in user.achievements and user.total_messages >= 100:
            results.append((44, True, self.check_and_award(user_id, 44)[1]))

        if 45 not in user.achievements and user.total_messages >= 1000:
            results.append((45, True, self.check_and_award(user_id, 45)[1]))

        return results


# ============================================================
# СЕРВИС СТРАХОВКИ
# ============================================================

class InsuranceService:
    def __init__(self, store: DataStore, economy_service: EconomyService):
        self.store = store
        self.economy = economy_service

    def buy_insurance(self, user_id: int) -> Tuple[bool, str, Optional[Insurance]]:
        user = self.store.get_user(user_id)
        if user.balance < INSURANCE_MIN_BALANCE:
            return False, "Минимальный баланс для страховки: 1000", None

        existing = self.store.get_user_active_insurance(user_id)
        if existing:
            return False, "У вас уже есть активная страховка", None

        coverage = user.balance
        premium = int(coverage * INSURANCE_COST_PERCENT)
        premium = max(premium, 100)

        if user.balance < premium:
            return False, f"Недостаточно средств. Нужно: {premium}", None

        user.balance -= premium
        insurance = Insurance(
            user_id=user_id,
            coverage_amount=coverage,
            premium_paid=premium,
        )
        self.store.insurances[insurance.insurance_id] = insurance

        user.insurance_active = True
        user.insurance_expires = insurance.expires_at

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-premium,
            transaction_type=TransactionType.INSURANCE_PURCHASE,
            balance_after=user.balance,
            description=f"Покупка страховки на {coverage}",
        ))

        return True, f"Страховка куплена. Покрытие: {coverage}, премия: {premium}", insurance

    def process_claim(self, user_id: int, reason: InsuranceClaimReason, loss_amount: int) -> Tuple[bool, str, int]:
        user = self.store.get_user(user_id)
        insurance = self.store.get_user_active_insurance(user_id)

        if insurance is None:
            return False, "Нет активной страховки", 0

        return_percent = INSURANCE_RETURN_PERCENT
        if reason == InsuranceClaimReason.TAX_AUDIT:
            return_percent = 0.10
        elif reason == InsuranceClaimReason.LOAN_DEFAULT:
            return_percent = 0.15

        payout = int(loss_amount * return_percent)
        payout = min(payout, insurance.coverage_amount)

        user.balance += payout
        insurance.active = False
        insurance.claims.append({
            "reason": reason.value,
            "loss_amount": loss_amount,
            "payout": payout,
            "timestamp": datetime.now().isoformat(),
        })

        user.insurance_active = False
        user.insurance_expires = None

        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=payout,
            transaction_type=TransactionType.INSURANCE_PAYOUT,
            balance_after=user.balance,
            description=f"Выплата страховки: {reason.value}",
        ))

        return True, f"Страховая выплата: {payout} монет ({return_percent:.0%} от {loss_amount})", payout


# ============================================================
# СЕРВИС РЕПУТАЦИИ
# ============================================================

class ReputationService:
    def __init__(self, store: DataStore):
        self.store = store

    def vote(self, voter_id: int, target_id: int, vote_type: str) -> Tuple[bool, str, int]:
        if voter_id == target_id:
            return False, "Нельзя голосовать за себя", 0

        voter = self.store.get_user(voter_id)
        target = self.store.get_user(target_id)

        now = datetime.now()
        last_vote = voter.last_vote_times.get(target_id)
        if last_vote:
            hours_passed = (now - last_vote).total_seconds() / 3600
            if hours_passed < REPUTATION_VOTE_COOLDOWN_HOURS:
                remaining = REPUTATION_VOTE_COOLDOWN_HOURS - hours_passed
                return False, f"Голосовать можно раз в сутки. Осталось {int(remaining)} ч", target.reputation_score

        mutual_count = voter.mutual_vote_counts.get(target_id, 0)
        week_ago = now - timedelta(days=7)
        if last_vote and last_vote > week_ago and mutual_count >= REPUTATION_MUTUAL_LIMIT_PER_WEEK:
            return False, "Лимит взаимных голосов исчерпан", target.reputation_score

        change = 1 if vote_type.lower() in ["+", "плюс", "plus", "up", "вверх"] else -1
        target.reputation_score += change

        voter.last_vote_times[target_id] = now
        if target_id in voter.mutual_vote_counts:
            voter.mutual_vote_counts[target_id] += 1
        else:
            voter.mutual_vote_counts[target_id] = 1

        level = get_reputation_level(target.reputation_score)
        level_data = REPUTATION_LEVELS[level]

        if change > 0:
            return True, f"👍 Репутация {target_id}: {target.reputation_score} ({level_data['title']})", target.reputation_score
        return True, f"👎 Репутация {target_id}: {target.reputation_score} ({level_data['title']})", target.reputation_score

    def get_reputation_info(self, user_id: int) -> Dict[str, Any]:
        user = self.store.get_user(user_id)
        level = get_reputation_level(user.reputation_score)
        level_data = REPUTATION_LEVELS[level]
        return {
            "score": user.reputation_score,
            "level": level.value,
            "title": level_data["title"],
            "color": level_data["color"],
            "karma": user.karma,
        }


print("Логика обработки + бизнес-сценарии загружены успешно.")
print(f"CasinoService: 6 методов")
print(f"AuctionService: 3 метода")
print(f"CrimeService: 5 методов")
print(f"ModerationService: 12 методов")
print(f"ClanService: 8 методов")
print(f"MarriageService: 3 метода")
print(f"AchievementService: 3 метода")
print(f"InsuranceService: 2 метода")
print(f"ReputationService: 3 метода")

# ============================================================
# НОВЫЕ ФИЧИ: ИНВЕСТИЦИИ, СТРОИТЕЛЬСТВО, ИГРЫ, ЛОТЕРЕЯ, КВЕСТЫ
# ============================================================

from datetime import datetime, timedelta
from typing import Tuple, Dict, List, Optional
import random
import asyncio
import math

from models import TransactionType, BusinessStatus
from utils import format_currency, format_duration


# ============================================================
# 1. ИНВЕСТИЦИИ
# ============================================================

class InvestmentSystem:
    def __init__(self, store, economy):
        self.store = store
        self.economy = economy
        
        self.investment_types = {
            "stocks": {
                "name": "Акции",
                "min": 10000,
                "profit": 0.15,
                "duration_hours": 24,
                "risk": 0.10,
                "emoji": "📈"
            },
            "crypto": {
                "name": "Криптовалюта",
                "min": 5000,
                "profit": 0.25,
                "duration_hours": 12,
                "risk": 0.20,
                "emoji": "🪙"
            },
            "real_estate": {
                "name": "Недвижимость",
                "min": 50000,
                "profit": 0.10,
                "duration_hours": 48,
                "risk": 0.05,
                "emoji": "🏠"
            },
            "startup": {
                "name": "Стартап",
                "min": 100000,
                "profit": 0.40,
                "duration_hours": 72,
                "risk": 0.30,
                "emoji": "🚀"
            },
            "gold": {
                "name": "Золото",
                "min": 20000,
                "profit": 0.08,
                "duration_hours": 36,
                "risk": 0.03,
                "emoji": "🥇"
            },
        }
        
        self.active_investments: Dict[int, List[Dict]] = {}
        
    async def invest(self, user_id: int, invest_type: str, amount: int) -> Tuple[bool, str]:
        user = self.store.get_user(user_id)
        
        if invest_type not in self.investment_types:
            return False, "❌ Неизвестный тип инвестиций"
        
        invest_data = self.investment_types[invest_type]
        
        if amount < invest_data["min"]:
            return False, f"❌ Минимальная сумма: {format_currency(invest_data['min'])}"
        
        if user.balance < amount:
            return False, f"❌ Недостаточно средств! Баланс: {format_currency(user.balance)}"
        
        user.balance -= amount
        
        investment = {
            "type": invest_type,
            "amount": amount,
            "started_at": datetime.now(),
            "finish_at": datetime.now() + timedelta(hours=invest_data["duration_hours"]),
            "profit": invest_data["profit"],
            "risk": invest_data["risk"],
            "active": True,
        }
        
        if user_id not in self.active_investments:
            self.active_investments[user_id] = []
        
        self.active_investments[user_id].append(investment)
        
        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-amount,
            transaction_type=TransactionType.BUSINESS_PURCHASE,
            balance_after=user.balance,
            description=f"Инвестиция в {invest_data['name']}",
        ))
        
        return True, f"✅ {invest_data['emoji']} Инвестиция в {invest_data['name']} на {format_currency(amount)}\n⏳ Длительность: {invest_data['duration_hours']} часов"

    async def collect_investment(self, user_id: int) -> Tuple[bool, str]:
        user = self.store.get_user(user_id)
        
        if user_id not in self.active_investments or not self.active_investments[user_id]:
            return False, "❌ У вас нет активных инвестиций"
        
        total_profit = 0
        completed = []
        
        for i, inv in enumerate(self.active_investments[user_id]):
            if not inv["active"]:
                continue
            
            if datetime.now() >= inv["finish_at"]:
                if random.random() < inv["risk"]:
                    inv["active"] = False
                    completed.append(i)
                    total_profit -= inv["amount"] * 0.5
                    continue
                
                profit = int(inv["amount"] * inv["profit"])
                user.balance += inv["amount"] + profit
                total_profit += profit
                inv["active"] = False
                completed.append(i)
        
        if total_profit == 0:
            return False, "❌ Нет завершённых инвестиций"
        
        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=total_profit,
            transaction_type=TransactionType.BUSINESS_INCOME,
            balance_after=user.balance,
            description=f"Прибыль с инвестиций",
        ))
        
        return True, f"✅ Прибыль с инвестиций: {format_currency(total_profit)}"


# ============================================================
# 2. СТРОИТЕЛЬСТВО БИЗНЕСА
# ============================================================

class BusinessBuilder:
    def __init__(self, store, economy):
        self.store = store
        self.economy = economy
        
        self.business_types = {
            "coffee_shop": {
                "name": "Кофейня",
                "build_time": 1,
                "upgrade_time": 2,
                "base_income": 500,
                "cost": 50000,
                "emoji": "☕"
            },
            "restaurant": {
                "name": "Ресторан",
                "build_time": 2,
                "upgrade_time": 3,
                "base_income": 1500,
                "cost": 150000,
                "emoji": "🍽️"
            },
            "hotel": {
                "name": "Гостиница",
                "build_time": 4,
                "upgrade_time": 4,
                "base_income": 3500,
                "cost": 500000,
                "emoji": "🏨"
            },
            "factory": {
                "name": "Завод",
                "build_time": 6,
                "upgrade_time": 5,
                "base_income": 6000,
                "cost": 1000000,
                "emoji": "🏭"
            },
            "farm": {
                "name": "Ферма",
                "build_time": 1,
                "upgrade_time": 2,
                "base_income": 800,
                "cost": 80000,
                "emoji": "🌾"
            },
            "mine": {
                "name": "Шахта",
                "build_time": 3,
                "upgrade_time": 3,
                "base_income": 4000,
                "cost": 600000,
                "emoji": "⛏️"
            },
        }
        
        self.projects: Dict[int, Dict] = {}
        
    async def start_construction(self, user_id: int, biz_type: str) -> Tuple[bool, str]:
        user = self.store.get_user(user_id)
        
        if biz_type not in self.business_types:
            return False, "❌ Неизвестный тип бизнеса"
        
        biz_data = self.business_types[biz_type]
        
        if user.balance < biz_data["cost"]:
            return False, f"❌ Нужно денег: {format_currency(biz_data['cost'])}"
        
        if user_id in self.projects:
            return False, "❌ У вас уже есть строящийся бизнес!"
        
        user.balance -= biz_data["cost"]
        
        self.projects[user_id] = {
            "type": "build",
            "biz_type": biz_type,
            "started_at": datetime.now(),
            "finish_at": datetime.now() + timedelta(hours=biz_data["build_time"]),
        }
        
        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-biz_data["cost"],
            transaction_type=TransactionType.BUSINESS_PURCHASE,
            balance_after=user.balance,
            description=f"Строительство {biz_data['name']}",
        ))
        
        return True, f"🚧 {biz_data['emoji']} Начато строительство {biz_data['name']}!\n⏳ Длительность: {biz_data['build_time']} часа"

    async def start_upgrade(self, user_id: int, business_id: str) -> Tuple[bool, str]:
        business = self.store.get_business(business_id)
        if not business:
            return False, "❌ Бизнес не найден"
        
        if business.owner_id != user_id:
            return False, "❌ Это не ваш бизнес"
        
        if business.level >= 10:
            return False, "❌ Бизнес уже максимального уровня"
        
        if user_id in self.projects:
            return False, "❌ У вас уже есть строящийся объект!"
        
        biz_data = self.business_types.get(business.business_type)
        if not biz_data:
            return False, "❌ Тип бизнеса не найден"
        
        self.projects[user_id] = {
            "type": "upgrade",
            "business_id": business_id,
            "started_at": datetime.now(),
            "finish_at": datetime.now() + timedelta(hours=biz_data["upgrade_time"]),
        }
        
        return True, f"🔧 Начато улучшение {business.name}!\n⏳ Длительность: {biz_data['upgrade_time']} часа"

    async def finish_construction(self, user_id: int) -> Tuple[bool, str]:
        if user_id not in self.projects:
            return False, "❌ У вас нет строящихся объектов"
        
        project = self.projects[user_id]
        
        if datetime.now() < project["finish_at"]:
            remaining = (project["finish_at"] - datetime.now()).total_seconds()
            return False, f"⏳ Осталось: {format_duration(int(remaining))}"
        
        if project["type"] == "build":
            biz_data = self.business_types[project["biz_type"]]
            business = Business(
                owner_id=user_id,
                name=biz_data["name"],
                business_type=project["biz_type"],
                hourly_income=biz_data["base_income"],
                purchase_price=biz_data["cost"],
                current_value=biz_data["cost"],
            )
            self.store.add_business(business)
            result_text = f"✅ {biz_data['emoji']} {biz_data['name']} построен! 🎉"
            
        else:
            business = self.store.get_business(project["business_id"])
            if business:
                business.level += 1
                business.hourly_income = int(business.hourly_income * 1.3)
                result_text = f"✅ {business.name} улучшен до {business.level} уровня! 🎉"
            else:
                return False, "❌ Бизнес не найден"
        
        del self.projects[user_id]
        return True, result_text


# ============================================================
# 3. НОВЫЕ ИГРЫ
# ============================================================

class NewGames:
    def __init__(self, store, economy, telegram_client):
        self.store = store
        self.economy = economy
        self.tg = telegram_client
        
        self.games = {
            "darts": {"emoji": "🎯", "win": {6: 10, 5: 5, 4: 3}},
            "bowling": {"emoji": "🎳", "win": {6: 10, 5: 5, 4: 3}},
            "football": {"emoji": "⚽", "win": {5: 10, 4: 5, 3: 3}},
            "basketball": {"emoji": "🏀", "win": {5: 10, 4: 5, 3: 3}},
        }
        
    async def play(self, user_id: int, chat_id: int, game: str, bet: int) -> Tuple[bool, str, Dict]:
        user = self.store.get_user(user_id)
        
        if game not in self.games:
            return False, "❌ Неизвестная игра", {}
        
        if bet < 10 or bet > 10000:
            return False, "❌ Ставка от 10 до 10000", {}
        
        if user.balance < bet:
            return False, f"❌ Недостаточно средств!", {}
        
        result = await self.tg.send_dice(chat_id, emoji=self.games[game]["emoji"])
        
        if not result or "result" not in result:
            return False, "❌ Ошибка", {}
        
        value = result["result"]["value"]
        multiplier = self.games[game]["win"].get(value, 0)
        
        if multiplier > 0:
            win_amount = bet * multiplier
            user.balance += win_amount
            result_text = f"🏆 {game.upper()}! +{format_currency(win_amount)}"
        else:
            win_amount = -bet
            user.balance -= bet
            result_text = f"💀 Проигрыш: {format_currency(bet)}"
        
        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=win_amount if win_amount > 0 else -bet,
            transaction_type=TransactionType.CASINO_WIN if win_amount > 0 else TransactionType.CASINO_BET,
            balance_after=user.balance,
            description=f"{game.upper()}: {value}",
        ))
        
        return True, result_text, {
            "game": game,
            "value": value,
            "win_amount": win_amount,
            "balance": user.balance
        }


# ============================================================
# 4. ЛОТЕРЕЯ
# ============================================================

class LotterySystem:
    def __init__(self, store, economy, telegram_client):
        self.store = store
        self.economy = economy
        self.tg = telegram_client
        
        self.ticket_price = 100
        self.tickets: Dict[int, List[int]] = {}
        self.jackpot = 10000
        
    async def buy_ticket(self, user_id: int, count: int = 1) -> Tuple[bool, str]:
        user = self.store.get_user(user_id)
        cost = self.ticket_price * count
        
        if user.balance < cost:
            return False, f"❌ Нужно: {format_currency(cost)}"
        
        user.balance -= cost
        self.jackpot += int(cost * 0.8)
        
        if user_id not in self.tickets:
            self.tickets[user_id] = []
        
        for _ in range(count):
            self.tickets[user_id].append(random.randint(100000, 999999))
        
        return True, f"🎫 Куплено {count} билетов!\n💰 Джекпот: {format_currency(self.jackpot)}"
    
    async def draw(self) -> Tuple[bool, str]:
        if not self.tickets:
            return False, "❌ Нет билетов"
        
        total_tickets = sum(len(t) for t in self.tickets.values())
        winner_id = None
        
        roll = random.randint(1, total_tickets)
        current = 0
        
        for uid, tickets in self.tickets.items():
            current += len(tickets)
            if roll <= current:
                winner_id = uid
                break
        
        if not winner_id:
            return False, "❌ Ошибка розыгрыша"
        
        winner = self.store.get_user(winner_id)
        win_amount = self.jackpot
        winner.balance += win_amount
        
        self.store.add_transaction(Transaction(
            user_id=winner_id,
            amount=win_amount,
            transaction_type=TransactionType.CASINO_WIN,
            balance_after=winner.balance,
            description=f"Выигрыш в лотерею!",
        ))
        
        self.jackpot = 10000
        self.tickets.clear()
        
        return True, f"🎉 ПОБЕДИТЕЛЬ: {winner_id}!\n💰 Выигрыш: {format_currency(win_amount)}"


# ============================================================
# 5. ЗДОРОВЬЕ
# ============================================================

class HealthSystem:
    def __init__(self, store, economy):
        self.store = store
        self.economy = economy
        
    async def check_health(self, user_id: int) -> Tuple[bool, str, int]:
        user = self.store.get_user(user_id)
        
        if not hasattr(user, "health"):
            user.health = 100
        
        if not user.house_id:
            if random.random() < 0.05:
                user.health -= random.randint(5, 15)
                if user.health < 0:
                    user.health = 0
                return False, "🤒 Вы заболели из-за отсутствия дома!", user.health
        
        return True, f"❤️ Здоровье: {user.health}/100", user.health
    
    async def treat(self, user_id: int) -> Tuple[bool, str]:
        user = self.store.get_user(user_id)
        cost = 100
        
        if user.balance < cost:
            return False, f"❌ Лечение стоит {format_currency(cost)}"
        
        user.balance -= cost
        user.health = 100
        
        return True, "💊 Вы полностью вылечились!"


# ============================================================
# 6. КВЕСТЫ
# ============================================================

class QuestSystem:
    def __init__(self, store, economy):
        self.store = store
        self.economy = economy
        
        self.quests = {
            "work_5": {"name": "Поработать 5 раз", "reward": 500, "target": 5, "type": "work"},
            "message_10": {"name": "Написать 10 сообщений", "reward": 200, "target": 10, "type": "message"},
            "casino_3": {"name": "Сыграть 3 раза в казино", "reward": 300, "target": 3, "type": "casino"},
            "business_collect": {"name": "Собрать доход с бизнеса", "reward": 400, "target": 1, "type": "business"},
            "earn_1000": {"name": "Заработать 1000 монет", "reward": 500, "target": 1000, "type": "earn"},
        }
        
    async def get_quests(self, user_id: int) -> str:
        user = self.store.get_user(user_id)
        
        if not hasattr(user, "quests"):
            user.quests = {}
        
        lines = ["📋 **ЕЖЕДНЕВНЫЕ КВЕСТЫ:**"]
        
        for key, data in self.quests.items():
            progress = user.quests.get(key, 0)
            done = "✅" if progress >= data["target"] else "⬜"
            lines.append(f"{done} {data['name']} ({progress}/{data['target']}) +{data['reward']} монет")
        
        return "\n".join(lines)
    
    async def check_progress(self, user_id: int, quest_type: str, amount: int = 1) -> None:
        user = self.store.get_user(user_id)
        
        if not hasattr(user, "quests"):
            user.quests = {}
        
        for key, data in self.quests.items():
            if data["type"] == quest_type:
                user.quests[key] = user.quests.get(key, 0) + amount
                
                if user.quests[key] >= data["target"]:
                    if not user.quests.get(f"{key}_done", False):
                        user.balance += data["reward"]
                        user.quests[f"{key}_done"] = True
                        self.store.add_transaction(Transaction(
                            user_id=user_id,
                            amount=data["reward"],
                            transaction_type=TransactionType.BONUS,
                            balance_after=user.balance,
                            description=f"Квест: {data['name']}",
                        ))


# ============================================================
# 7. РЕЙТИНГ
# ============================================================

class ChatRanking:
    def __init__(self, store):
        self.store = store
        
    async def get_ranking(self, chat_id: int, limit: int = 10) -> str:
        lines = ["🏆 **РЕЙТИНГ ЧАТА:**"]
        
        users = sorted(self.store.users.values(), key=lambda u: u.balance, reverse=True)[:limit]
        for i, user in enumerate(users, 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
            lines.append(f"{medal} {user.user_id}: {format_currency(user.balance)}")
        
        return "\n".join(lines)


print("✅ НОВЫЕ ФИЧИ ЗАГРУЖЕНЫ!")
# ============================================================
# РЕАЛИСТИЧНАЯ СИСТЕМА
# Экономика, Налоги, Банк, Бизнес, Медицина, Транспорт, Жизнь
# ============================================================

from datetime import datetime, timedelta
from typing import Tuple, Dict, List, Optional
import random
import json
import asyncio

from models import TransactionType, BusinessStatus, User
from utils import format_currency, format_duration, logger


# ============================================================
# 1. РЕАЛЬНАЯ ЭКОНОМИКА
# ============================================================

class RealEconomy:
    def __init__(self, store):
        self.store = store
        
        self.inflation_rate = 0.02
        self.crisis_chance = 0.05
        self.gdp = 0
        self.money_supply = 0
        self.economic_cycle = 50
        
    async def update_economy(self):
        """Обновление экономики"""
        total_money = self.store.get_total_money_in_circulation()
        total_users = self.store.get_total_users()
        
        if total_users > 0:
            avg_money = total_money / total_users
            if avg_money > 1000000:
                self.inflation_rate = 0.05
            elif avg_money > 100000:
                self.inflation_rate = 0.03
            else:
                self.inflation_rate = 0.01
        
        await self.apply_inflation()
        await self.check_crisis()
        self.economic_cycle = max(0, min(100, self.economic_cycle + random.uniform(-5, 5)))
    
    async def apply_inflation(self):
        """Применить инфляцию"""
        for business in self.store.businesses.values():
            if business.status == BusinessStatus.ACTIVE:
                business.current_value = int(business.current_value * (1 + self.inflation_rate))
                business.purchase_price = int(business.purchase_price * (1 + self.inflation_rate))
        
        for house in self.store.houses.values():
            house.price = int(house.price * (1 + self.inflation_rate))
        
        for vehicle in self.store.vehicles.values():
            vehicle.price = int(vehicle.price * (1 + self.inflation_rate))
    
    async def check_crisis(self):
        """Проверка кризиса"""
        if random.random() < self.crisis_chance:
            for user in self.store.users.values():
                loss = int(user.balance * random.uniform(0.10, 0.30))
                user.balance -= loss
                user.stress += 20
            logger.warning("❗ ЭКОНОМИЧЕСКИЙ КРИЗИС!")
            return True
        return False


# ============================================================
# 2. РЕАЛЬНЫЙ БАНК
# ============================================================

class RealBank:
    def __init__(self, store):
        self.store = store
        
        self.deposit_rate = 0.08
        self.loan_rate = 0.15
        self.mortgage_rate = 0.10
        self.credit_card_rate = 0.25
        self.overdraft_limit = 10000
        
    async def take_loan(self, user_id: int, amount: int, loan_type: str = "cash") -> Tuple[bool, str]:
        """Взять кредит"""
        user = self.store.get_user(user_id)
        
        rates = {
            "cash": self.loan_rate,
            "mortgage": self.mortgage_rate,
            "car": 0.12,
            "credit_card": self.credit_card_rate,
            "micro": 0.50,
        }
        
        if loan_type not in rates:
            return False, "❌ Неизвестный тип кредита. Доступны: cash, mortgage, car, credit_card, micro"
        
        if user.loan_amount > 0:
            return False, f"❌ У вас уже есть кредит! Остаток: {format_currency(user.loan_amount)}"
        
        if hasattr(user, "loan_blocked") and user.loan_blocked:
            return False, "❌ Вы не можете брать кредит из-за просрочки!"
        
        if amount < 1000:
            return False, "❌ Минимальная сумма кредита: 1000 монет"
        
        # Проверка платёжеспособности
        monthly_income = await self.calculate_income(user_id)
        max_payment = monthly_income * 0.4
        
        loan_term = 30
        monthly_payment = (amount * (1 + rates[loan_type])) / loan_term
        
        if monthly_payment > max_payment and max_payment > 0:
            return False, f"❌ Платёж {format_currency(monthly_payment)} превышает 40% дохода"
        
        # Выдача кредита
        user.balance += amount
        user.loan_amount = int(amount * (1 + rates[loan_type]))
        user.loan_due_date = datetime.now() + timedelta(days=30)
        user.credit_history = max(0, user.credit_history - 0.05)
        
        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.LOAN_TAKE,
            balance_after=user.balance,
            description=f"Кредит {loan_type}: {amount}",
        ))
        
        return True, f"✅ Кредит выдан!\nСумма: {format_currency(amount)}\nК оплате: {format_currency(user.loan_amount)}\nСрок: 30 дней"
    
    async def calculate_income(self, user_id: int) -> int:
        """Расчёт дохода игрока"""
        user = self.store.get_user(user_id)
        income = 0
        
        if user.is_employed:
            income += user.job_salary
        
        businesses = self.store.get_user_businesses(user_id)
        for b in businesses:
            if b.status == BusinessStatus.ACTIVE:
                income += b.hourly_income * 24 * 30
        
        return income
    
    async def check_overdue_loans(self):
        """Проверка просроченных кредитов"""
        now = datetime.now()
        
        for user in self.store.users.values():
            if user.loan_amount > 0 and user.loan_due_date:
                if now > user.loan_due_date:
                    days_overdue = (now - user.loan_due_date).days
                    
                    if days_overdue <= 3:
                        penalty = int(user.loan_amount * 0.05)
                        user.loan_amount += penalty
                    elif days_overdue <= 7:
                        penalty = int(user.loan_amount * 0.15)
                        user.loan_amount += penalty
                        user.credit_history = max(0, user.credit_history - 0.1)
                    elif days_overdue <= 14:
                        penalty = int(user.loan_amount * 0.30)
                        user.loan_amount += penalty
                        user.credit_history = max(0, user.credit_history - 0.2)
                        user.loan_blocked = True
                    else:
                        await self.bankruptcy(user.user_id)
    
    async def bankruptcy(self, user_id: int):
        """Банкротство"""
        user = self.store.get_user(user_id)
        
        # Списание всех денег
        user.balance = 0
        user.bank_balance = 0
        
        # Списание имущества (50% бизнесов)
        businesses = self.store.get_user_businesses(user_id)
        for b in businesses[:len(businesses)//2]:
            self.store.remove_business(b.business_id)
        
        user.loan_amount = 0
        user.loan_due_date = None
        user.credit_history = 0
        user.loan_blocked = True
        
        logger.warning(f"💀 Игрок {user_id} обанкротился!")


# ============================================================
# 3. РЕАЛЬНЫЙ БИЗНЕС
# ============================================================

class RealBusiness:
    def __init__(self, store):
        self.store = store
        
        self.ip_cost = 5000
        self.ip_tax = 0.20
        self.ip_annual_cost = 2000
        
    async def register_ip(self, user_id: int, name: str) -> Tuple[bool, str]:
        """Регистрация ИП"""
        user = self.store.get_user(user_id)
        
        if user.has_ip:
            return False, "❌ У вас уже есть ИП!"
        
        if user.balance < self.ip_cost:
            return False, f"❌ Регистрация ИП стоит {format_currency(self.ip_cost)}"
        
        user.balance -= self.ip_cost
        user.has_ip = True
        user.ip_name = name
        user.ip_date = datetime.now()
        
        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-self.ip_cost,
            transaction_type=TransactionType.BUSINESS_PURCHASE,
            balance_after=user.balance,
            description=f"Регистрация ИП: {name}",
        ))
        
        return True, f"✅ ИП '{name}' зарегистрировано!"
    
    async def get_ip_info(self, user_id: int) -> str:
        """Информация об ИП"""
        user = self.store.get_user(user_id)
        
        if not user.has_ip:
            return "❌ У вас нет ИП"
        
        info = f"📋 ИНФОРМАЦИЯ ОБ ИП:\n"
        info += f"Название: {user.ip_name}\n"
        info += f"Дата регистрации: {user.ip_date.strftime('%d.%m.%Y') if user.ip_date else 'Неизвестно'}\n"
        info += f"Налог: {self.ip_tax*100:.0f}%\n"
        info += f"Годовой сбор: {format_currency(self.ip_annual_cost)}"
        
        return info


# ============================================================
# 4. РЕАЛЬНЫЙ ТРАНСПОРТ
# ============================================================

class RealTransport:
    def __init__(self, store):
        self.store = store
        
        self.cars = {
            "economy": {"price": 50000, "fuel": 6, "insurance": 3000, "name": "Эконом", "emoji": "🚗"},
            "standard": {"price": 150000, "fuel": 8, "insurance": 5000, "name": "Стандарт", "emoji": "🚙"},
            "premium": {"price": 500000, "fuel": 10, "insurance": 10000, "name": "Премиум", "emoji": "🚘"},
            "luxury": {"price": 1500000, "fuel": 12, "insurance": 20000, "name": "Люкс", "emoji": "🏎️"},
            "sport": {"price": 3000000, "fuel": 15, "insurance": 30000, "name": "Спорт", "emoji": "🏁"},
        }
        
    async def buy_car(self, user_id: int, car_type: str) -> Tuple[bool, str]:
        """Покупка машины"""
        user = self.store.get_user(user_id)
        
        if car_type not in self.cars:
            return False, "❌ Доступны: economy, standard, premium, luxury, sport"
        
        car = self.cars[car_type]
        
        if user.balance < car["price"]:
            return False, f"❌ Машина стоит {format_currency(car['price'])}"
        
        user.balance -= car["price"]
        user.car_id = car_type
        user.car_fuel = 100
        user.car_insurance = False
        
        self.store.add_transaction(Transaction(
            user_id=user_id,
            amount=-car["price"],
            transaction_type=TransactionType.VEHICLE_PURCHASE,
            balance_after=user.balance,
            description=f"Покупка {car['name']}",
        ))
        
        return True, f"{car['emoji']} {car['name']} куплена за {format_currency(car['price'])}"
    
    async def refuel_car(self, user_id: int) -> Tuple[bool, str]:
        """Заправка машины"""
        user = self.store.get_user(user_id)
        
        if not user.car_id:
            return False, "❌ У вас нет машины!"
        
        cost = 500
        if user.balance < cost:
            return False, f"❌ Заправка стоит {format_currency(cost)}"
        
        user.balance -= cost
        user.car_fuel = 100
        
        return True, "⛽ Машина заправлена!"
    
    async def pay_car_tax(self, user_id: int) -> Tuple[bool, str]:
        """Оплата налога на авто"""
        user = self.store.get_user(user_id)
        
        if not user.car_id:
            return False, "❌ У вас нет машины!"
        
        car_taxes = {
            "economy": 5000,
            "standard": 10000,
            "premium": 25000,
            "luxury": 50000,
            "sport": 75000,
        }
        
        tax = car_taxes.get(user.car_id, 5000)
        
        if user.balance < tax:
            user.car_fines += 1
            return False, f"❌ Налог {format_currency(tax)} не оплачен! Штраф +500"
        
        user.balance -= tax
        return True, f"✅ Налог на авто оплачен: {format_currency(tax)}"


# ============================================================
# 5. РЕАЛЬНАЯ МЕДИЦИНА
# ============================================================

class RealMedicine:
    def __init__(self, store):
        self.store = store
        
        self.visit_cost = 1000
        self.medicine_cost = 500
        self.hospital_cost = 10000
        self.insurance_cost = 5000
        
    async def visit_doctor(self, user_id: int) -> Tuple[bool, str]:
        """Посещение врача"""
        user = self.store.get_user(user_id)
        
        if user.balance < self.visit_cost:
            return False, f"❌ Приём у врача стоит {format_currency(self.visit_cost)}"
        
        user.balance -= self.visit_cost
        user.health = min(100, user.health + 20)
        user.last_doctor_visit = datetime.now()
        
        if user.is_sick:
            user.is_sick = False
            user.sick_until = None
            return True, "🏥 Вы вылечились!"
        
        return True, "👨‍⚕️ Вы посетили врача, здоровье +20"
    
    async def buy_insurance(self, user_id: int) -> Tuple[bool, str]:
        """Покупка страховки"""
        user = self.store.get_user(user_id)
        
        if user.has_insurance:
            return False, "❌ У вас уже есть страховка!"
        
        if user.balance < self.insurance_cost:
            return False, f"❌ Страховка стоит {format_currency(self.insurance_cost)}"
        
        user.balance -= self.insurance_cost
        user.has_insurance = True
        
        return True, f"✅ Медицинская страховка куплена за {format_currency(self.insurance_cost)}"


# ============================================================
# 6. РЕАЛЬНАЯ ЖИЗНЬ
# ============================================================

class RealLife:
    def __init__(self, store):
        self.store = store
        
        self.daily_expenses = {
            "food": 500,
            "utilities": 300,
            "transport": 200,
            "internet": 100,
            "phone": 100,
            "entertainment": 500,
        }
        
    async def daily_life(self, user_id: int) -> Tuple[bool, str]:
        """Ежедневные расходы"""
        user = self.store.get_user(user_id)
        total = sum(self.daily_expenses.values())
        
        if user.balance < total:
            user.stress += 20
            user.health -= 10
            return False, f"💀 Не хватает на жизнь! Нужно {format_currency(total)}\nСтресс +20, Здоровье -10"
        
        user.balance -= total
        
        user.hunger = max(0, user.hunger - 20)
        user.sleep = max(0, user.sleep - 10)
        user.stress = max(0, user.stress + 5)
        
        if random.random() < 0.05:
            user.is_sick = True
            user.sick_until = datetime.now() + timedelta(days=3)
            return True, "🤒 Вы заболели! Посетите врача."
        
        return True, f"✅ Ежедневные расходы: {format_currency(total)}\nЖизнь продолжается!"
    
    async def sleep(self, user_id: int) -> Tuple[bool, str]:
        """Сон"""
        user = self.store.get_user(user_id)
        user.sleep = 100
        user.stress = max(0, user.stress - 20)
        user.health = min(100, user.health + 10)
        
        return True, "😴 Вы отлично выспались! Здоровье +10, Стресс -20"


# ============================================================
# 7. РЕАЛЬНЫЕ НАЛОГИ
# ============================================================

class RealTaxes:
    def __init__(self, store):
        self.store = store
        
        self.tax_rates = {
            "income": 0.13,
            "property": 0.01,
            "business": 0.20,
            "car": 0.05,
            "crypto": 0.13,
        }
        
    async def calculate_taxes(self, user_id: int) -> int:
        """Расчёт налогов игрока"""
        user = self.store.get_user(user_id)
        total_tax = 0
        
        if user.monthly_income > 0:
            total_tax += int(user.monthly_income * self.tax_rates["income"])
        
        if user.house_id:
            house = self.store.get_house(user.house_id)
            if house:
                total_tax += int(house.price * self.tax_rates["property"])
        
        businesses = self.store.get_user_businesses(user_id)
        for b in businesses:
            if b.status == BusinessStatus.ACTIVE:
                total_tax += int(b.current_value * self.tax_rates["business"])
        
        if user.car_id:
            cars = {"economy": 50000, "standard": 150000, "premium": 500000, "luxury": 1500000, "sport": 3000000}
            car_price = cars.get(user.car_id, 50000)
            total_tax += int(car_price * self.tax_rates["car"])
        
        return total_tax
    
    async def pay_taxes(self, user_id: int) -> Tuple[bool, str]:
        """Оплата налогов"""
        user = self.store.get_user(user_id)
        tax_amount = await self.calculate_taxes(user_id)
        
        if tax_amount == 0:
            return True, "✅ Нет налогов к оплате"
        
        if user.balance < tax_amount:
            user.tax_debt += tax_amount
            return False, f"❌ Недостаточно средств! Налог: {format_currency(tax_amount)}\nДолг по налогам: {format_currency(user.tax_debt)}"
        
        user.balance -= tax_amount
        user.tax_history.append({
            "date": datetime.now().isoformat(),
            "amount": tax_amount,
            "paid": True,
        })
        
        return True, f"✅ Налоги оплачены: {format_currency(tax_amount)}"


# ============================================================
# РЕГИСТРАЦИЯ В HANDLERS
# ============================================================

def register_real_system(dispatcher):
    """Регистрация реалистичных команд"""
    
    dispatcher.command_map.update({
        # Экономика
        "экономика": lambda uid, cid, args: get_economy_info(uid),
        
        # Банк
        "кредит": lambda uid, cid, args: take_loan(uid, args),
        "кредит инфо": lambda uid, cid, args: get_loan_info(uid),
        
        # Бизнес
        "регистрация ип": lambda uid, cid, args: register_ip(uid, args),
        "ип инфо": lambda uid, cid, args: get_ip_info(uid),
        
        # Транспорт
        "купить машину": lambda uid, cid, args: buy_car(uid, args),
        "заправить": lambda uid, cid, args: refuel_car(uid),
        "налог авто": lambda uid, cid, args: pay_car_tax(uid),
        
        # Медицина
        "врач": lambda uid, cid, args: visit_doctor(uid),
        "страховка": lambda uid, cid, args: buy_insurance(uid),
        
        # Жизнь
        "жизнь": lambda uid, cid, args: daily_life(uid),
        "сон": lambda uid, cid, args: sleep(uid),
        "стресс": lambda uid, cid, args: get_stress(uid),
        
        # Налоги
        "налоги": lambda uid, cid, args: pay_taxes(uid),
        "налог инфо": lambda uid, cid, args: get_tax_info(uid),
    })
    
    return dispatcher


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

async def get_economy_info(user_id: int) -> Tuple[bool, str]:
    return True, "📊 Информация об экономике доступна в /экономика", {}

async def take_loan(user_id: int, args: List[str]) -> Tuple[bool, str]:
    if len(args) < 2:
        return False, "❌ Использование: кредит [сумма] [тип]\nТипы: cash, mortgage, car, credit_card, micro", None
    try:
        amount = int(args[0])
        loan_type = args[1]
        bank = RealBank(store)
        return await bank.take_loan(user_id, amount, loan_type)
    except ValueError:
        return False, "❌ Сумма должна быть числом", None

async def get_loan_info(user_id: int) -> Tuple[bool, str]:
    user = store.get_user(user_id)
    if user.loan_amount <= 0:
        return True, "✅ У вас нет кредитов", None
    info = f"💳 Информация о кредите:\nДолг: {format_currency(user.loan_amount)}\n"
    if user.loan_due_date:
        days = (user.loan_due_date - datetime.now()).days
        info += f"Дней до оплаты: {days}\n"
    info += f"Кредитная история: {user.credit_history*100:.0f}%"
    return True, info, {}

async def register_ip(user_id: int, args: List[str]) -> Tuple[bool, str]:
    if not args:
        return False, "❌ Укажите название ИП", None
    business = RealBusiness(store)
    return await business.register_ip(user_id, " ".join(args))

async def get_ip_info(user_id: int) -> Tuple[bool, str]:
    business = RealBusiness(store)
    return True, await business.get_ip_info(user_id), {}

async def buy_car(user_id: int, args: List[str]) -> Tuple[bool, str]:
    if not args:
        return False, "❌ Укажите тип: economy, standard, premium, luxury, sport", None
    transport = RealTransport(store)
    return await transport.buy_car(user_id, args[0])

async def refuel_car(user_id: int) -> Tuple[bool, str]:
    transport = RealTransport(store)
    return await transport.refuel_car(user_id)

async def pay_car_tax(user_id: int) -> Tuple[bool, str]:
    transport = RealTransport(store)
    return await transport.pay_car_tax(user_id)

async def visit_doctor(user_id: int) -> Tuple[bool, str]:
    medicine = RealMedicine(store)
    return await medicine.visit_doctor(user_id)

async def buy_insurance(user_id: int) -> Tuple[bool, str]:
    medicine = RealMedicine(store)
    return await medicine.buy_insurance(user_id)

async def daily_life(user_id: int) -> Tuple[bool, str]:
    life = RealLife(store)
    return await life.daily_life(user_id)

async def sleep(user_id: int) -> Tuple[bool, str]:
    life = RealLife(store)
    return await life.sleep(user_id)

async def get_stress(user_id: int) -> Tuple[bool, str]:
    user = store.get_user(user_id)
    return True, f"😰 Уровень стресса: {user.stress}/100", {"stress": user.stress}

async def pay_taxes(user_id: int) -> Tuple[bool, str]:
    taxes = RealTaxes(store)
    return await taxes.pay_taxes(user_id)

async def get_tax_info(user_id: int) -> Tuple[bool, str]:
    taxes = RealTaxes(store)
    tax_amount = await taxes.calculate_taxes(user_id)
    return True, f"📊 Ваши налоги: {format_currency(tax_amount)}", {"tax": tax_amount}

# Глобальные переменные для доступа
store = None

def init_real_system(store_instance):
    global store
    store = store_instance

print("✅ РЕАЛИСТИЧНАЯ СИСТЕМА ЗАГРУЖЕНА!")
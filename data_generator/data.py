import random
import copy
import requests
from datetime import datetime
from faker import Faker
from mealgenerator import get_meal


class Product:
    def __init__(self, name):
        self.name = name
        self.market_cost = random.randint(50, 2000)


class Employee:
    def __init__(self, full_name):
        self.name = full_name
        self.age = random.randint(20, 50)


class Restaraunt:
    def __init__(self, adress):
        self.adress = adress
        self.capacity = random.randint(50, 150)
        self.rent = random.randint(50000, 150000)


class Menu:
    def __init__(self):
        self.function = random.choices(["сезонное", "обычное", "стоп-лист"])


class Job:
    def __init__(self, id_restaraunt, id_employee, job):
        self.id_restaraunt = id_restaraunt
        self.id_employee = id_employee
        self.job = job
        self.salary = random.randint(25000, 100000)
        self.experience = random.randint(0, 60)


class RestarauntMenu:
    def __init__(self, id_menu, id_restaraunt):
        self.id_menu = id_menu
        self.id_restaraunt = id_restaraunt


class MenuPosition:
    def __init__(self, id_menu, id_meal):
        self.id_menu = id_menu
        self.id_meal = id_meal


class Check:
    def __init__(self, id_restaraunt):
        self.id_restaraunt = id_restaraunt
        self.date = (
            Faker()
            .date_between(start_date="-1y", end_date="now")
            .strftime("%Y/%d/%m, %H:%M:%S")
        )


class MealCheck:
    def __init__(self, id_meal, id_check):
        self.id_meal = id_meal
        self.id_check = id_check


class Ingridient:
    def __init__(self, id_meal, id_product):
        self.id_meal = id_meal
        self.id_product = id_product
        self.gram = random.randint(50, 500)


class Storage:
    def __init__(self, id_restaraunt):
        self.id_restaraunt = id_restaraunt
        self.capacity = random.randint(1000, 5000)


class StorageProduct:
    def __init__(self, id_storage, id_product):
        self.id_storage = id_storage
        self.id_product = id_product
        self.amount = random.randint(10, 180)


def gen_id(list_items):
    for i, item in enumerate(list_items):
        item.id = i
    return list_items


def gen_employees(k: int):
    names = ["Петр", "Иван", "Степан", "Константин", "Павел", "Даниил"]
    surnames = ["Иванов", "Сидоров", "Петров", "Чижиков", "Гардеев", "Обломов"]
    patronymics = [
        "Петрович",
        "Александрович",
        "Федорович",
        "Иванович",
        "Леонидович",
        "Сергеевич",
    ]
    people_names = set()
    while len(people_names) < k:
        full_name = "{surname} {name} {patronymic}".format(
            surname=random.choice(surnames),
            name=random.choice(names),
            patronymic=random.choice(patronymics),
        )
        people_names.add(full_name)

    employees = []

    for name in people_names:
        employees.append(Employee(name))

    return gen_id(employees)


def gen_products(meals):
    products = []
    for meal in meals:
        for name in meal.ingredients:
            products.append(Product(name))
    return gen_id(products)


def gen_restarants(k):
    adresses = set()
    city = ["Москва", "Санкт-Петербург", "Казань"]
    streets = ["ул.Ленина", "ул.Карбышева", "ул.Кирова"]
    while len(adresses) < k:
        adress = (
            random.choice(city)
            + ", "
            + random.choice(streets)
            + f", д.{random.randint(1,50)}"
        )
        adresses.add(adress)
    adresses = list(adresses)
    restaraunts = []
    for adress in adresses:
        restaraunts.append(Restaraunt(adress))
    return gen_id(restaraunts)


def gen_menus(k):
    menus = [Menu() for _ in range(k)]
    return gen_id(menus)


def gen_jobs(employees, restarants):
    jobs = []
    for i in range(len(restarants)):
        jobs.append(Job(restarants[i].id, employees[i].id, "директор"))
    for i in range(len(restarants), len(employees)):
        jobs.append(
            Job(
                restarants[random.randint(0, len(restarants) - 1)].id,
                employees[i].id,
                random.choice(["повар", "менеджер", "бармен", "официант"]),
            )
        )
    return jobs


def gen_restaraunt_menu(restarants, menus):
    stoplists = [menu for menu in menus if menu.function == "стоп-list"]
    not_stoplists = [menu for menu in menus if menu.function != "стоп-list"]
    restaraunt_menu = []
    for restarant in restarants:
        restaraunt_menu.append(
            RestarauntMenu(random.choice(not_stoplists).id, restarant.id)
        )
    for stoplist in stoplists:
        restaraunt_menu.append(
            RestarauntMenu(stoplist.id, random.choice(restarants).id)
        )
    return restaraunt_menu


def gen_menu_position(menus, meals, k):
    k = min(len(meals), k)
    menu_position = []
    for menu in menus:
        positions = set()
        while len(positions) < k:
            positions.add(random.choice(meals).id)
        for position in list(positions):
            menu_position.append(MenuPosition(menu.id, position))
    return menu_position


def gen_check(restarants, k):
    checks = []
    for restarant in restarants:
        for i in range(k):
            checks.append(Check(restarant.id))

    return gen_id(checks)


def gen_meal_check(checks, meals):
    meal_check = []
    for check in checks:
        k = random.randint(1, 5)
        meals_ids = set()
        while len(meals_ids) < k:
            meals_ids.add(random.choice(meals).id)
        for meal_id in meals_ids:
            meal_check.append(MealCheck(meal_id, check.id))
    return meal_check


def gen_ingridient(meals, products):
    ingridients = []
    for meal in meals:
        sum_costs = 0
        for product in products:
            if product.name in meal.ingredients:
                ingridient = Ingridient(meal.id, product.id)
                sum_costs += ingridient.gram * product.market_cost / 1000
                ingridients.append(ingridient)
        meal.cost = int(sum_costs * (100 + random.randint(10, 100)) / 100)
    return ingridients


def gen_storage(restarants):
    storages = []
    for restarant in restarants:
        storages.append(Storage(restarant.id))
    return gen_id(storages)


def gen_storage_produst(storages, restaraunt_menu, menu_position, ingridients):
    storages_produsts = []
    for storage in storages:
        products_ids = set()
        for r_m in restaraunt_menu:
            if storage.id_restaraunt == r_m.id_restaraunt:
                for menu_pos in menu_position:
                    if r_m.id_menu == menu_pos.id_menu:
                        for ingridient in ingridients:
                            if ingridient.id_meal == menu_pos.id_meal:
                                products_ids.add(ingridient.id_product)
        for id_product in products_ids:
            storages_produsts.append(StorageProduct(storage.id, id_product))
    return storages_produsts

def change_key(in_str):
    first = True
    ans = ''
    for s in in_str:
        if s.islower() or first:
            if not s.islower():
                first = False
            ans += s
        else:
            ans += '_' + s.lower()
            
    return ans

def get_insert(list_obj):
    ans = []
    for obj in list_obj:
        d = copy.deepcopy(obj.__dict__)
        if obj.__class__.__name__ == 'Meal':
            d = {'id': d["id"],
                 'name':d['name'],
                 "time":d["time"],
                 "type":d['type'],
                 'cost':d['cost']
                 }
        k = d.keys()
        v = list(map(str, d.values()))
        k_s = ', '.join(k)
        v_s = ', '.join(v)
        s = f'INSERT INTO {change_key(obj.__class__.__name__)}({k_s}) VALUES ({v_s});'
        ans.append(s)
    return ans


if __name__ == "__main__":
    ans = []
    employees = gen_employees(20)
    meals = gen_id([get_meal() for _ in range(20)])
    products = gen_products(meals)
    restarants = gen_restarants(3)
    menus = gen_menus(3)
    jobs = gen_jobs(employees, restarants)
    restaraunt_menu = gen_restaraunt_menu(restarants, menus)
    menu_position = gen_menu_position(menus, meals, 10)
    checks = gen_check(restarants, 10)
    meal_check = gen_meal_check(checks, meals)
    ingridients = gen_ingridient(meals, products)
    storages = gen_storage(restarants)
    storage_produst = gen_storage_produst(
        storages, restaraunt_menu, menu_position, ingridients
    )
    
    ans += get_insert(employees)
    ans += get_insert(meals)
    ans += get_insert(products)
    ans += get_insert(restarants)
    ans += get_insert(menus)
    ans += get_insert(jobs)
    ans += get_insert(restaraunt_menu)
    ans += get_insert(menu_position)
    ans += get_insert(checks)
    ans += get_insert(meal_check)
    ans += get_insert(ingridients)
    ans += get_insert(storages)
    ans += get_insert(storage_produst)
    
    with open('data.txt', 'w') as f:
        for s in ans:
            f.write(s + '\n')
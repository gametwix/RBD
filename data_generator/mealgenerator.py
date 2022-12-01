import requests
from pydantic import BaseModel, root_validator, Field, validator, Extra
from typing import List
import random


class Meal(BaseModel, extra=Extra.allow):
    name: str = Field(None, alias="strMeal")
    strIngredient1: str
    strIngredient2: str
    strIngredient3: str
    strIngredient4: str
    strIngredient5: str

    @root_validator(pre=False)
    def ingredients_to_list(cls, values):
        ingredients = []
        for i in range(1, 6):
            if values[f"strIngredient{i}"] != "":
                ingredients.append(values[f"strIngredient{i}"].lower())
            values.pop(f"strIngredient{i}")
        values["ingredients"] = ingredients
        return values

    @root_validator(pre=False)
    def gen_params(cls, values):
        values["time"] = random.randint(300, 3600)
        values["type"] = random.choice(["суп", "напиток", "закуска", "салат", "десерт"])
        return values

    @validator("name")
    def normalize_name(cls, v):
        return v.lower()


class Meals(BaseModel):
    meals: List[Meal]


def get_meal():
    resp = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
    meals = Meals.parse_raw(resp.text)
    return meals.meals[0]

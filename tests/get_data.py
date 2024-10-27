from faker import Faker


fake = Faker()


def get_dish_data() -> dict:
    return {"name": fake.name(), "description_of_cooking": fake.pystr()}


def get_product_data() -> dict:
    return {"name": fake.name(), "measure": fake.pystr()}


def get_product_in_dish_data(dish: dict, product: dict) -> dict:
    return {
        "dish": dish["id"],
        "product": product["id"],
        "quantity": round(fake.pyfloat(min_value=1, max_value=1000000), 3)
    }
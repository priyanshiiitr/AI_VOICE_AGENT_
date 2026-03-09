from database.db import create_reservation

menu = {
    "margherita pizza": 250,
    "pasta alfredo": 300,
    "veg burger": 180,
    "cold coffee": 120
}


def get_menu():
    items = []
    for item, price in menu.items():
        items.append(f"{item.title()} - ₹{price}")
    return "\n".join(items)


def get_price(item_name: str):
    item = item_name.lower()
    if item in menu:
        return f"{item.title()} costs ₹{menu[item]}"
    return "Sorry, that item is not on the menu."


def restaurant_hours():
    return "We are open from 10 AM to 11 PM."


def restaurant_location():
    return "We are located on MG Road, Bangalore."


def book_table(name: str, people: int, time: str):

    create_reservation(name, people, time)

    return f"Reservation confirmed for {people} people at {time}."
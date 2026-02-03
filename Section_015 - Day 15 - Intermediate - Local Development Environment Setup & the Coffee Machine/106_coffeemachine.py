# ============================================================
# COFFEE MACHINE — MULTI PRODUCT, SINGLE PAYMENT SYSTEM
# ============================================================

MENU = {
    "espresso": {
        "ingredients": {"water": 50, "milk": 0, "coffee": 18},
        "cost": 120
    },
    "latte": {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 180
    },
    "cappuccino": {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 200
    }
}

resources = {"water": 1000, "milk": 800, "coffee": 500}
money_earned = 0

coins = {"10rs": 10, "20rs": 20, "50rs": 50, "100rs": 100}
machine_on = True


# -------------------------
# UI HELPERS
# -------------------------
def line():
    print("=" * 40)


def show_menu():
    print("☕ AVAILABLE COFFEES")
    for drink, data in MENU.items():
        print(f"- {drink.title():12} ₹{data['cost']}")
    line()


# -------------------------
# RESOURCE CHECK (CART LEVEL)
# -------------------------
def check_resources(cart):
    required = {"water": 0, "milk": 0, "coffee": 0}

    for drink, qty in cart.items():
        for ing, amt in MENU[drink]["ingredients"].items():
            required[ing] += amt * qty

    for ing in required:
        if resources[ing] < required[ing]:
            return False, ing

    return True, None


# -------------------------
# DEDUCT RESOURCES
# -------------------------
def make_order(cart):
    for drink, qty in cart.items():
        for ing, amt in MENU[drink]["ingredients"].items():
            resources[ing] -= amt * qty


# -------------------------
# PAYMENT HANDLING
# -------------------------
def take_payment(total_cost):
    print(f"💰 Total amount to pay: ₹{total_cost}")
    total_paid = 0

    for coin, value in coins.items():
        count = int(input(f"How many {coin} coins?: "))
        total_paid += count * value

    if total_paid < total_cost:
        print("❌ Not enough money. Payment refunded.")
        return False, 0

    change = total_paid - total_cost
    if change > 0:
        print(f"🔁 Change returned: ₹{change}")

    return True, total_cost


# =========================
# MAIN LOOP
# =========================
print("\nWELCOME TO THE COFFEE MACHINE ☕")
line()

while machine_on:
    print("""
1. Order Coffee
2. View Report
3. Turn Off Machine
""")
    choice = input("Select option: ")
    line()

    # -------------------------
    # ORDER FLOW
    # -------------------------
    if choice == "1":
        cart = {}
        total_cost = 0

        show_menu()

        while True:
            drink = input("Choose coffee (or 'done'): ").lower()
            if drink == "done":
                break

            if drink not in MENU:
                print("Invalid coffee name")
                continue

            qty = int(input(f"How many {drink}s?: "))
            cart[drink] = cart.get(drink, 0) + qty
            total_cost += MENU[drink]["cost"] * qty

            print(f"Added {qty} {drink}(s)")

        if not cart:
            print("No items selected")
            line()
            continue

        print("\n🧾 ORDER SUMMARY")
        for drink, qty in cart.items():
            print(f"{drink.title():12} x{qty}")
        print(f"Total: ₹{total_cost}")
        line()

        ok, missing = check_resources(cart)
        if not ok:
            print(f"❌ Not enough {missing}")
            line()
            continue

        success, earned = take_payment(total_cost)
        if not success:
            line()
            continue

        make_order(cart)
        money_earned += earned
        print("✅ Order complete. Enjoy your coffee ☕")
        line()

    # -------------------------
    # REPORT
    # -------------------------
    elif choice == "2":
        print("📊 MACHINE REPORT")
        print(f"Water : {resources['water']} ml")
        print(f"Milk  : {resources['milk']} ml")
        print(f"Coffee: {resources['coffee']} g")
        print(f"Money : ₹{money_earned}")
        line()

    # -------------------------
    # SHUTDOWN
    # -------------------------
    elif choice == "3":
        print("🔌 Turning off machine")
        machine_on = False

    else:
        print("Invalid option")
        line()

def calculate_total(prices):
    total = 0

    for price in prices:
        total += price

    return total


def apply_discount(total, discount):
    return total - (total * discount)


def checkout(prices, discount=0):
    total = calculate_total(prices)
    discounted_total = apply_discount(total, discount)

    return round(discounted_total, 2)


if __name__ == "__main__":
    prices = [100, 200, 50]
    discount = 10

    print("Final total:", checkout(prices, discount))
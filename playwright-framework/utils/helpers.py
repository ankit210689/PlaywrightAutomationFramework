from typing import List, Dict


def parse_price(price_text: str) -> float:
    # price_text expected like "$29.99"
    return float(price_text.replace("$", ""))


def save_order_details(path: str, items: List[Dict], total: str):
    with open(path, "w") as f:
        for it in items:
            f.write(f"{it['name']} - {it['price']}\n")
        f.write(f"Total: {total}\n")


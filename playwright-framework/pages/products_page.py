from playwright.sync_api import Page
from typing import List, Dict


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page

    def list_items(self) -> List[Dict]:
        items = []
        rows = self.page.query_selector_all('.inventory_item')
        for r in rows:
            name = r.query_selector('.inventory_item_name').inner_text().strip()
            price = r.query_selector('.inventory_item_price').inner_text().strip()
            btn = r.query_selector('button')
            items.append({'name': name, 'price': price, 'add_btn': btn})
        return items

    def add_items_above(self, price_threshold: float):
        items = self.list_items()
        for it in items:
            price = float(it['price'].replace('$', ''))
            if price > price_threshold:
                it['add_btn'].click()

    def go_to_cart(self):
        self.page.click('.shopping_cart_link')
        self.page.wait_for_selector('.cart_list')


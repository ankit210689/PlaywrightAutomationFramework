from playwright.sync_api import Page
from typing import List, Dict


class CartPage:
    def __init__(self, page: Page):
        self.page = page

    def get_cart_items(self) -> List[Dict]:
        items = []
        rows = self.page.query_selector_all('.cart_item')
        for r in rows:
            name = r.query_selector('.inventory_item_name').inner_text().strip()
            price = r.query_selector('.inventory_item_price').inner_text().strip()
            items.append({'name': name, 'price': price})
        return items

    def checkout(self):
        self.page.click('#checkout')
        self.page.wait_for_selector('#checkout_info_container')


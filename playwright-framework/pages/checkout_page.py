from playwright.sync_api import Page
from typing import Dict


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_info(self, first: str, last: str, postal: str):
        self.page.fill('#first-name', first)
        self.page.fill('#last-name', last)
        self.page.fill('#postal-code', postal)

    def continue_to_overview(self):
        self.page.click('#continue')
        self.page.wait_for_selector('.summary_info')

    def finish(self):
        self.page.click('#finish')
        self.page.wait_for_selector('.complete-header')

    def get_order_summary(self) -> Dict:
        items = [e.inner_text().strip() for e in self.page.query_selector_all('.inventory_item_name')]
        total = self.page.query_selector('.summary_total_label').inner_text().strip()
        return {'items': items, 'total': total}

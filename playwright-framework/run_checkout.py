import os
import json
import pathlib
from playwright.sync_api import sync_playwright

# Ensure project root on path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[0]
import sys
sys.path.insert(0, str(PROJECT_ROOT))

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import save_order_details


def main():
    data_path = PROJECT_ROOT / 'data' / 'checkout_data.json'
    with open(data_path) as f:
        data = json.load(f)

    with sync_playwright() as p:
        print('Launching browser (headed)...')
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.saucedemo.com')

        login = LoginPage(page)
        login.login('standard_user', 'secret_sauce')

        products = ProductsPage(page)
        products.add_items_above(10.0)
        products.go_to_cart()

        cart = CartPage(page)
        cart_items = cart.get_cart_items()
        print(f'Cart items found: {len(cart_items)}')
        if len(cart_items) == 0:
            print('No items in cart; exiting')
            browser.close()
            return
        cart.checkout()

        checkout = CheckoutPage(page)
        checkout.fill_info(data['first_name'], data['last_name'], data['postal_code'])
        checkout.continue_to_overview()
        summary = checkout.get_order_summary()
        print('Summary collected:', summary)
        checkout.finish()

        out_dir = PROJECT_ROOT / 'reports'
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / 'order_details.txt'
        save_order_details(str(out_path), [{'name': n, 'price': ''} for n in summary['items']], summary['total'])
        print('Wrote report to:', out_path)
        print('Report contents:')
        with open(out_path) as f:
            print(f.read())

        page.wait_for_timeout(2000)
        browser.close()


if __name__ == '__main__':
    main()


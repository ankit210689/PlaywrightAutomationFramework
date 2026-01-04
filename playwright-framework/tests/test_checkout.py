import os
import sys
import json
import pathlib
from playwright.sync_api import sync_playwright

# Ensure project root is on sys.path so 'pages' and 'utils' imports work when running pytest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import save_order_details


def test_checkout_flow(tmp_path):
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'checkout_data.json')
    with open(data_path) as f:
        data = json.load(f)

    with sync_playwright() as p:
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
        assert len(cart_items) > 0, "No items added to cart"
        cart.checkout()

        checkout = CheckoutPage(page)
        checkout.fill_info(data['first_name'], data['last_name'], data['postal_code'])
        checkout.continue_to_overview()

        # collect order summary on the overview page before finishing (total is shown on overview)
        summary = checkout.get_order_summary()

        checkout.finish()

        out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'order_details.txt'))
        print(f"DEBUG: writing order details to: {out_path}")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        save_order_details(out_path, [{'name': n, 'price': ''} for n in summary['items']], summary['total'])
        print(f"DEBUG: file exists after save? {os.path.exists(out_path)}")
        try:
            with open(out_path, 'r') as _f:
                contents = _f.read()
            print("DEBUG: file contents:\n" + contents)
        except Exception as e:
            print(f"DEBUG: could not read file after save: {e}")

        # keep the browser open briefly for observation
        page.wait_for_timeout(2000)
        browser.close()

from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def login(self, username: str, password: str):
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        # wait for products page
        self.page.wait_for_selector(".inventory_list")


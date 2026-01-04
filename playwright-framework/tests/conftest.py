import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session')
def playwright_context():
    with sync_playwright() as p:
        yield p


@pytest.fixture()
def browser(playwright_context):
    browser = playwright_context.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


import pytest
from playwright.sync_api import sync_playwright

from app_pages.add_client_financial_account_page.add_client_financial_account_page import AddClientFinancialAccountPage
from app_pages.advisor_accounts_page.advisor_accounts_page import AccountsPage
from app_pages.advisor_client_page.advisor_client_page import AdvisorClientPage, DeleteReason
from app_pages.advisor_main_page.advisor_main_page import AdvisorMainPage
from app_pages.login_page.login_page import LoginPage
from config.config_manager import ConfigManager

from core.utils.entities_utils import fake_new_client


@pytest.fixture(scope="session")
def config():
    return ConfigManager("test-env.ini")


@pytest.fixture(scope="function")
def page(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--start-maximized'], headless=False)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        request.cls.login_page = LoginPage(page)
        request.cls.advisor_main_page = AdvisorMainPage(page)
        request.cls.advisor_client_page = AdvisorClientPage(page)
        request.cls.accounts_page = AccountsPage(page)
        request.cls.add_client_financial_account_page = AddClientFinancialAccountPage(browser=browser)
        yield page
        page.close()


@pytest.fixture(scope="function", autouse=True)
def goto(page, config):
    url = config.login_url
    page.goto(url, timeout=100000)


@pytest.fixture
def new_client(request, page):
    client = fake_new_client()
    yield client
    AdvisorClientPage(page).delete_client_id(reason=DeleteReason.OTHER, reason_to_provide="Delete auto test user")







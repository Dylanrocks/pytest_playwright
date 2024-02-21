from playwright.sync_api import sync_playwright, Page

from app_pages.base_page import BasePage


class LoginPage(BasePage):
    WAIT_FOR_ELEMENT_TO_BE_PRESENT_LOCATOR = '#loginEmail'
    LOGIN_EMAIL_LOCATOR = '#loginEmail'
    LOGIN_PASSWORD_LOCATOR = '#loginPassword'
    LOGIN_BUTTON_SELECTOR = '#loginForm button'
    ORG_SELECTOR = 'select[name="orgId"]'

    def __init__(self, page: Page, timeout_sec: int = 180):
        super().__init__(page)
        self.page = page
        self.timeout_sec = timeout_sec

    def login(self, email: str, password: str, org: str):
        self.page.fill(selector=self.LOGIN_EMAIL_LOCATOR, value=email)
        self.page.fill(selector=self.LOGIN_PASSWORD_LOCATOR, value=password)
        self.page.click(selector=self.LOGIN_BUTTON_SELECTOR)
        self.page.select_option(selector=self.ORG_SELECTOR, label=org)
        self.page.click(selector=self.LOGIN_BUTTON_SELECTOR)







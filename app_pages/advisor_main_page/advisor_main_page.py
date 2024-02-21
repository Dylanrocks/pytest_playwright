from enum import Enum

from playwright.sync_api import sync_playwright, Page

from app_pages.base_page import BasePage


class Tabs(Enum):
    ACCOUNTS = "Accounts"
    CLIENTS = "Clients"


class AdvisorMainPage(BasePage):
    WAIT_FOR_ELEMENT_TO_BE_PRESENT_LOCATOR = '#loginEmail'
    MAINTENANCE_NOTIFICATION_LOCATOR = '#maintenance-notification'
    MAINTENANCE_NOTIFICATION_BTN_LOCATOR = '#maintenance-notification button'
    TABS_LOCATOR = '//*[@id="main-header-container"]//*[text()="{tab.value}"]'

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    def wait_for_maintenance_notification(self):
        # Wait for the notification element to appear
        notification = self.page.wait_for_selector(self.MAINTENANCE_NOTIFICATION_LOCATOR, timeout=50000)
        # If the notification element appears, click on the button
        if notification:
            notification.click()
            self.page.click(selector=self.MAINTENANCE_NOTIFICATION_BTN_LOCATOR)

    def click_tab(self, tab: Tabs):
        selector = self.TABS_LOCATOR.replace('{tab.value}', tab.value)
        self.page.click(selector=selector)
        self.page.wait_for_load_state()

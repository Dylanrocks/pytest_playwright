from playwright.sync_api import Page


class BasePage:
    BASE_URL = None
    pr_page = None
    WAIT_FOR_ELEMENT_TO_BE_PRESENT_LOCATOR = None

    def __init__(self, page: Page = None):
        self.page = page

    def wait_for_page_to_load(self):
        element = self.page.wait_for_selector(selector=self.WAIT_FOR_ELEMENT_TO_BE_PRESENT_LOCATOR)
        if not element:
            raise Exception('page was not loaded successfully')





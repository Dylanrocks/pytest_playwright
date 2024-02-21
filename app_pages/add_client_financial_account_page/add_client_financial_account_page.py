from playwright.sync_api import Browser, Page


class AddClientFinancialAccountPage:
    WAIT_FOR_ELEMENT_TO_BE_PRESENT_LOCATOR = '//button[text()="Get started"]'
    GET_STARTED_LINK_SELECTOR = '//button[text()="Get started"]'
    FINANCIAL_INSTITUTION_RESULT_SELECTOR = '//span[@class="brokerName" and text()={financial_institution}]'
    SEARCH_FINANCIAL_INSTITUTION_SELECTOR = 'input[type="text"]'
    CONNECT_LOGIN_SELECTOR = 'input[name="LOGIN"]'
    CONNECT_PASSWORD_SELECTOR = 'input[name="PASSWORD"]'
    CONNECT_SECURELY_BTN_SELECTOR = '#account-login-btn'
    LOG_IN_ERROR_SELECTOR = '//span[text()="We couldn\'t log you in"]'
    FINANCIAL_INSTITUTION_SEARCH_RESULTS_SELECTOR = 'span[class*=brokerName]'
    PR_OPTION_SELECTOR = '#OP_OPTION'

    def __init__(self, browser: Browser = None, page: Page = None):
        self.browser = browser
        self.new_context = None
        self.page = page

    def _get_financial_institution_element(self, financial_institution):
        financial_institution = f'"{financial_institution}"'
        selector = self.FINANCIAL_INSTITUTION_RESULT_SELECTOR.replace('{financial_institution}', financial_institution)
        element = self.page.wait_for_selector(selector=selector)
        return element

    def get_financial_institution_search_results(self) -> list[str]:
        search_results = []
        self.page.wait_for_selector(selector=self.FINANCIAL_INSTITUTION_SEARCH_RESULTS_SELECTOR, strict=False)
        search_results_elements = self.page.query_selector_all(selector=self.FINANCIAL_INSTITUTION_SEARCH_RESULTS_SELECTOR)
        if search_results_elements:
            search_results = [element.text_content() for element in search_results_elements]
        return search_results

    def launch_client_financial_account_in_new_browser(self, url):
        self.new_context = self.browser.new_context(no_viewport=True)
        self.page = self.new_context.new_page()
        self.page.goto(url)

    def click_get_started(self):
        self.page.click(selector=self.GET_STARTED_LINK_SELECTOR)

    def search_financial_institution(self, financial_institution):
        self.page.type(self.SEARCH_FINANCIAL_INSTITUTION_SELECTOR, financial_institution)

    def click_financial_institution(self, financial_institution: str):
        self._get_financial_institution_element(financial_institution).click()

    def fill_credentials_and_connect(self, username, password, check_op_option=False, close_browser=True):
        self.page.fill(selector=self.CONNECT_LOGIN_SELECTOR, value=username)
        self.page.fill(selector=self.CONNECT_PASSWORD_SELECTOR, value=password)
        if check_op_option:
            if self.page.locator(selector=self.PR_OPTION_SELECTOR).is_visible():
                self.page.select_option(selector=self.PR_OPTION_SELECTOR, value='otp', timeout=0)
        self.page.click(selector=self.CONNECT_SECURELY_BTN_SELECTOR)
        self._wait_for_error_login_error(close_browser=close_browser)

    def _wait_for_error_login_error(self, close_browser=True):
        self.page.wait_for_selector(selector=self.LOG_IN_ERROR_SELECTOR, state="visible", timeout=180000)
        if close_browser:
            self.new_context.close()

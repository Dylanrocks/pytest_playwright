from playwright.sync_api import Page

from app_pages.add_client_financial_account_page.add_client_financial_account_page import AddClientFinancialAccountPage
from app_pages.advisor_main_page.advisor_main_page import AdvisorMainPage, Tabs
from core.elements.table_element import TableElement
from core.utils.entities_utils import fake_credentials


class AccountsPage(AdvisorMainPage):
    MANAGED_ACCOUNTS_TABLE_CONTAINER_SELECTOR = '//div[@id="managed-accounts"]/table'
    UPDATED_CREDENTIALS_SELECTOR = '//a[text()="Update credentials"]'
    OK_FILTER_BTN_SELECTOR = '//*[@id="statusSelectWrap"]//*[contains(text(), "OK")]'
    STATUS_FILTER_BTN_SELECTOR = '#statusSelectWrap'
    ALL_STATUSES_OPTION_SELECTOR = '//span[text()="All statuses"]'
    PENDING_ACCESS_OPTION_SELECTOR = '//span[text()="Pending access"]'

    def __init__(self, page: Page):
        super().__init__(page)
        self.managed_accounts_table = TableElement(self.page, self.MANAGED_ACCOUNTS_TABLE_CONTAINER_SELECTOR)

    def get_account(self):
        self.page.wait_for_selector(self.MANAGED_ACCOUNTS_TABLE_CONTAINER_SELECTOR, state='attached', timeout=3000)
        account = self.managed_accounts_table.get_column_values(column_name='ACCOUNT')
        return account

    def get_pending_access_accounts(self, with_tooltip=None) -> list[str]:
        self.page.wait_for_timeout(2000)
        pending_access_with_incorrect_credentials = []
        client_list = self.get_account()
        for index, item in enumerate(client_list):
            account_label, tooltip = self.managed_accounts_table.get_call_value_and_tooltip(
                column_name='STATUS', row_number=index + 1)
            if with_tooltip in tooltip:
                pending_access_with_incorrect_credentials.append(item)
        return pending_access_with_incorrect_credentials

    def update_account_credentials(self, account_list):

        for index, item in enumerate(account_list):
            self.managed_accounts_table.click_on_cell_by_column_and_row(column_name='STATUS', row_number=index + 1)
            self.page.click(selector=self.UPDATED_CREDENTIALS_SELECTOR)
            update_account_page = AddClientFinancialAccountPage(page=self.page)
            creds: dict = fake_credentials()
            update_account_page.fill_credentials_and_connect(creds['username'], creds['password'], check_op_option=True, close_browser=False)
            super().click_tab(Tabs.ACCOUNTS)

    def filter_table(self, fiter_column: str, filter_option: str):
        self.page.click(selector=self.STATUS_FILTER_BTN_SELECTOR)
        self.page.click(selector=self.ALL_STATUSES_OPTION_SELECTOR)
        self.page.click(selector=self.PENDING_ACCESS_OPTION_SELECTOR)
        self.page.click(selector=self.OK_FILTER_BTN_SELECTOR)
        #TODO- should implement wait for loader to appear and disappear intead of wait_for_timeout
        self.page.wait_for_timeout(2000)

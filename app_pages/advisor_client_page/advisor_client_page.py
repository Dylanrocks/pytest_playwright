from enum import Enum

from playwright.sync_api import Page

from app_pages.advisor_main_page.advisor_main_page import AdvisorMainPage
from core.elements.table_element import TableElement


class DeleteReason(Enum):
    CLIENT_DOES_NOT_SEE_VALUE = "Client does not see the value"
    ADVISOR_DOES_NOT_SEE_VALUE = "Advisor does not see the value"
    CLIENT_NO_LONGER_WITH_FIRM = "The client is no longer with my firm"
    PONTERA_TECH_ISSUES = "Pontera technology or service issues"
    OTHER = "Other"


class AdvisorClientPage(AdvisorMainPage):
    WAIT_FOR_ELEMENT_TO_BE_PRESENT_LOCATOR = '#addNewClientBtnId'
    ADD_NEW_CLIENT_BTN_LOCATOR = '#addNewClientBtnId'
    FIRST_NAME_LOCATOR = '#first_name'
    LAST_NAME_LOCATOR = '#last_name'
    SSN_LOCATOR = '#ssn'
    EMAIL_LOCATOR = '#email'
    CONTACT_PHONE_LOCATOR = '#contactPhone'
    CITY_LOCATOR = '#city'
    STATE_LOCATOR = 'select[name="state"]'
    ADVISOR_NAME_LOCATOR = 'select[name="repId"]'
    SAVE_CLIENT_BTN = '#save-client-changes-btn'
    ADD_ACCOUNT_BTN = '.btn_add-new-type'
    ASK_CLIENT_TO_ADD_ACCOUNT_CONTAINER = "//div[contains(@class, 'method-wrapper') and .//div[contains(text(), 'Ask client to add their accounts')]]"
    GET_LINK_LOCATOR = '//*[text()="Get link"]'
    ASK_CLIENT_TO_ADD_ACCOUNT_DIALOG = '#copyInviteLinkModal[role="dialog"]'
    INVITE_URL_INPUT_SELECTOR = 'input#invite-url'
    MANAGED_ACCOUNTS_TABLE_CONTAINER_LOCATOR = '//app-accounts-table-alch[@tabletype="managed-accounts"]'
    DELETE_CLIENT_BTN_LOCATOR = '#delete-client-id'
    CLIENT_TABLE_CONTAINER_LOCATOR = '//table[contains(@class, "managed-accounts")]'
    CLOSE_ADD_ACCOUNT_DIALOG = '//button[text()="Close"]'
    BACK_BUTTON = '//span[text()="Back"]'
    SUBMIT_BTN_LOCATOR = 'div#userActionFeedback button.btn'

    def __init__(self, page: Page):
        super().__init__(page)
        self.managed_accounts_table = TableElement(self.page, self.MANAGED_ACCOUNTS_TABLE_CONTAINER_LOCATOR)
        self.client_table = TableElement(self.page, self.CLIENT_TABLE_CONTAINER_LOCATOR)

    def create_new_client(self, client_dict: dict):
        self.page.click(selector=self.ADD_NEW_CLIENT_BTN_LOCATOR)
        self.page.fill(selector=self.FIRST_NAME_LOCATOR, value=client_dict['First name'])
        self.page.fill(selector=self.LAST_NAME_LOCATOR, value=client_dict['Last name'])
        self.page.fill(selector=self.SSN_LOCATOR, value=client_dict['SSN / ITIN'])
        self.page.fill(selector=self.EMAIL_LOCATOR, value=client_dict['Email'])
        self.page.fill(selector=self.CONTACT_PHONE_LOCATOR, value=client_dict['Mobile phone'])
        self.page.fill(selector=self.CITY_LOCATOR, value=client_dict['City'])
        self.page.select_option(selector=self.STATE_LOCATOR, label=client_dict['State'])
        self.page.select_option(selector=self.ADVISOR_NAME_LOCATOR, label=client_dict['Advisor Name'])
        self.page.click(selector=self.SAVE_CLIENT_BTN)

    def click_add_account(self):
        self.page.click(selector=self.ADD_ACCOUNT_BTN)

    def click_ask_client_to_add_account(self):
        self.page.click(selector=self.ASK_CLIENT_TO_ADD_ACCOUNT_CONTAINER)

    def click_get_info(self):
        get_link_full_path = self.ASK_CLIENT_TO_ADD_ACCOUNT_CONTAINER + self.GET_LINK_LOCATOR
        self.page.click(selector=get_link_full_path)

    def get_invite_url(self) -> str:
        self.page.wait_for_selector(selector=self.INVITE_URL_INPUT_SELECTOR)
        # Get the value attribute of the input element, which represents the text
        url = self.page.input_value(selector=self.INVITE_URL_INPUT_SELECTOR)
        return url

    def close_add_account_dialog(self):
        self.page.click(selector=self.CLOSE_ADD_ACCOUNT_DIALOG)

    def click_back(self):
        self.page.click(selector=self.BACK_BUTTON)

    def delete_client_id(self, reason: DeleteReason, reason_to_provide: str):
        self.page.locator(selector=self.DELETE_CLIENT_BTN_LOCATOR).click()
        self.page.get_by_label(reason.value).click()
        self.page.get_by_label(reason.value).click()
        self.page.get_by_role("textbox").fill(reason_to_provide)
        self.page.click(selector=self.SUBMIT_BTN_LOCATOR)

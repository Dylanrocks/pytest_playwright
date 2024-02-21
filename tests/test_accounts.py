import pytest
from assertpy import soft_assertions, assert_that
from app_pages.advisor_main_page.advisor_main_page import Tabs
from core.utils.entities_utils import fake_credentials
from tests.base_test import BaseTest


class TestInaccessibleAccounts(BaseTest):
    CREDENTIALS: dict = fake_credentials()

    @pytest.fixture(autouse=True)
    def setup(self, config):
        self.login_page.login(config.user_name, config.user_password, config.firm)

    def test_new_account_failed_connection_due_wrong_credentials_gets_pending_access_label_with_tooltip(self,
                                                                                                        new_client):
        self.advisor_client_page.create_new_client(new_client)
        self.advisor_client_page.click_add_account()
        self.advisor_client_page.click_ask_client_to_add_account()
        self.advisor_client_page.click_get_info()
        url = self.advisor_client_page.get_invite_url()
        self.add_client_financial_account_page.launch_client_financial_account_in_new_browser(url)
        self.add_client_financial_account_page.click_get_started()
        self.add_client_financial_account_page.search_financial_institution('S. Nottingham Investments')
        financial_institution_search_results = self.add_client_financial_account_page.get_financial_institution_search_results()
        assert_that(financial_institution_search_results).described_as('financial institution').contains('S. Nottingham Investments')
        assert_that(financial_institution_search_results).described_as('financial institution').starts_with('S. Nottingham Investments')
        self.add_client_financial_account_page.click_financial_institution('S. Nottingham Investments')
        self.add_client_financial_account_page.fill_credentials_and_connect(self.CREDENTIALS['username'],
                                                                            self.CREDENTIALS['password'])

        self.advisor_client_page.close_add_account_dialog()
        self.advisor_client_page.click_back()

        self.advisor_client_page.client_table.click_on_cell(new_client['Full name'])
        account_label, tooltip = self.advisor_client_page.managed_accounts_table.get_call_value_and_tooltip(
            column_name='STATUS', row_number=1)

        with soft_assertions():
            assert_that(account_label).described_as('Account status').is_equal_to('Pending access')
            assert_that(tooltip).described_as('Status tooltip').is_equal_to('The client provided incorrect credentials. Please click here for more details.')

    def test_incorrect_credentials_accounts_status_is_the_same_after_credentials_update(self):
        self.advisor_main_page.click_tab(Tabs.ACCOUNTS)
        self.accounts_page.filter_table(fiter_column='Status', filter_option='Pending access')
        accounts_before_update = self.accounts_page.get_pending_access_accounts(with_tooltip='incorrect credentials')
        self.accounts_page.update_account_credentials(accounts_before_update)
        accounts_after_update = self.accounts_page.get_pending_access_accounts(with_tooltip='incorrect credentials')
        assert_that(accounts_after_update).is_equal_to(accounts_before_update)



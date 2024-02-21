from app_pages.add_client_financial_account_page.add_client_financial_account_page import AddClientFinancialAccountPage
from app_pages.advisor_accounts_page.advisor_accounts_page import AccountsPage
from app_pages.advisor_client_page.advisor_client_page import AdvisorClientPage
from app_pages.advisor_main_page.advisor_main_page import AdvisorMainPage
from app_pages.login_page.login_page import LoginPage


class BaseTest:
    login_page: LoginPage
    advisor_main_page: AdvisorMainPage
    advisor_client_page: AdvisorClientPage
    accounts_page: AccountsPage
    add_client_financial_account_page: AddClientFinancialAccountPage

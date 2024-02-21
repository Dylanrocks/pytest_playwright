from playwright.sync_api import ElementHandle, Page


class TableElement:
    def __init__(self, page: Page, table_container: str):
        self.page = page
        self.table_container = table_container

    def get_column_header_names(self) -> list[str]:
        """

        :return: the names of the table columns as list of strings
        """
        table = self.page.wait_for_selector(selector=self.table_container)
        table.wait_for_selector("th")
        headers = table.query_selector_all("th")
        column_list = []
        i: ElementHandle
        for i in headers:
            column_list.append(i.inner_text().strip())
        return column_list

    def _get_column_elements(self, column_name) -> list[ElementHandle]:
        """

        :param column_name: gets the name of the column in the table
        :return: list of column ElementHandle that are column cell values
        """
        column_header_names = self.get_column_header_names()
        column_index = column_header_names.index(column_name)
        column_index = column_index + 1
        call_xpath_index = f'//tbody//td[{column_index}]'
        cell_xpath = self.table_container + call_xpath_index
        cell_elements = self.page.query_selector_all(selector=cell_xpath)
        return cell_elements

    def get_column_values(self, column_name):
        """

        :param column_name: gets the name of the column in the table
        :return: the names of the table column cell values as list of strings
        """
        elements_values = self._get_column_elements(column_name)

        column_value_list = []
        i: ElementHandle
        for i in elements_values:
            column_value_list.append(i.inner_text().strip('- \n'))
        return column_value_list

    def _get_column_element(self, column_name, row_num: int) -> ElementHandle:
        """

        :param column_name: gets the name of the column in the table
        :param row_num: row number in the table
        :return: the cell element by column name and row number
        """
        column_header_names = self.get_column_header_names()
        column_index = column_header_names.index(column_name)
        column_index = column_index + 1
        call_xpath_index = f'//tbody//tr[{row_num}]//td[{column_index}]'
        cell_xpath = self.table_container + call_xpath_index
        cell_element = self.page.wait_for_selector(selector=cell_xpath, timeout=2000)
        #cell_element = self.page.query_selector(selector=cell_xpath)
        return cell_element

    def get_call_value_and_tooltip(self, column_name: str, row_number: int) -> tuple[str, str]:
        """

        :param column_name: gets the name of the column in the table
        :param row_number: row number in the table
        :return: the cell innner value and tooltip by column name and row number
        """
        cell_element = self._get_column_element(column_name, row_number)
        cell_value = cell_element.query_selector(selector="//div[@class = 'status-inner']").text_content()
        cell_tooltip = cell_element.query_selector('div').get_attribute('data-original-title')
        return cell_value, cell_tooltip

    def click_on_cell(self, cell_value: str):
        """

        :param cell_value: clicking on element by the cell inner value in the table. Example: Name value
        """
        self.page.click(selector=f"//tbody//tr//td[contains(., {cell_value})]")

    def click_on_cell_by_column_and_row(self, column_name: str, row_number: int):
        """
        clicking on element by the cell inner value in the table
        :param column_name: gets the name of the column in the table
        :param row_number: row number in the table
        """
        cell_element = self._get_column_element(column_name, row_number)
        cell_element.click()



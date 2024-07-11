from typing import Any, Self

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


class WebScrapper:
    def __init__(self) -> None:
        self._driver = self._setup_driver()

    def _setup_driver(self) -> webdriver.Chrome:
        """Setup selenium webdriver"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        # overcome limited resource problems
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("lang=en")
        # open Browser in maximized mode
        options.add_argument("start-maximized")
        # disable infobars
        options.add_argument("disable-infobars")
        # disable extension
        options.add_argument("--disable-extensions")
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation"],
        )
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=options)
        return driver

    def navigate_to(self, url: str, expect_to: str) -> Self:
        """Navigate to a given url and assert some string in the title."""
        self._driver.get(url)
        assert expect_to in self._driver.title
        return self

    def select_search_type(self, option_value: str) -> Self:
        """Interact with the select element and change it's value"""
        select_element = self._driver.find_element(By.ID, "segment")
        select = Select(select_element)
        select.select_by_value(option_value)

        return self

    def get_table_data(self) -> dict[str, list[str]]:
        """Retrieve the table data from the website."""
        all_table_data: dict[str, list[str]] = {}
        while True:
            # Just wait for the table to load
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//table/tbody"),
                ),
            )
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "pagination-next"),
                ),
            )

            table = self._driver.find_element(By.XPATH, "//table/tbody")
            pagination_next = self._driver.find_element(
                By.CLASS_NAME,
                "pagination-next",
            )
            # Each tr maps the current possibilities. It will be just tr -> td[n], tr -> td[n]
            # The first td[0] can be either the product or just a blank line that
            # contains some other data that must be in a list
            elements = table.find_elements(By.TAG_NAME, "tr")
            parse_data(all_table_data, elements)

            if "disabled" in pagination_next.get_dom_attribute("class"):
                break

            pagination_next.click()

        return all_table_data


def parse_data(
    retrievable_data: dict[str, list[Any]],
    rows: list[Any],
) -> None:
    """Parse data gathered from the website"""
    header = ""
    for row in rows:
        data = [a.text for a in row.find_elements(By.TAG_NAME, "td")]
        header = data.pop(0)

        if header not in retrievable_data:
            retrievable_data[header] = []

        retrievable_data[header].append(data)

from typing import Self

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

    def switch_to_iframe(self, iframe_id: str) -> Self:
        """Switch to the desired iframe by using the iframe_id from the page."""
        iframe = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, iframe_id)),
        )[0]
        self._driver.switch_to.frame(iframe)
        return self

    def get_table_data(self):
        """Retrieve the table data from the website."""
        table = self._driver.find_element(By.XPATH, "//table/tbody")

        # Each tr maps the current possibilities. It will be just tr -> td[n], tr -> td[n]
        # The first td[0] can be either the product or just a blank line that
        # contains some other data that must be in a list
        return table.find_elements(By.TAG_NAME, "tr")


def parse_data(rows: list) -> dict[str, list[str]]:
    """Parse data gathered from the website"""
    header = ""
    ordered_data = {}

    for row in rows:
        data = [a.text for a in row.find_elements(By.TAG_NAME, "td")]
        # It means that we have a header in here
        if len(data) == 6:
            header = data[0]
            # We don't care about the name in the data, only to take it as a header
            data.pop(0)

        if header not in ordered_data:
            ordered_data[header] = []

        ordered_data[header].append(data)

    return ordered_data

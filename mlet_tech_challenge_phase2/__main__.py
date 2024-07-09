from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# URL para mapear o endereço de consulta do pregão da B3
B3_AJUSTES_DO_PREGAO = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/derivativos/ajustes-do-pregao/"


def setup_driver():
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

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)

    return driver


def main() -> int:
    driver = setup_driver()
    driver.get(B3_AJUSTES_DO_PREGAO)
    assert "Ajustes do pregão | B3" in driver.title
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "bvmf_iframe")),
    )[0]
    driver.switch_to.frame(iframe)
    table = driver.find_element(By.XPATH, "//table/tbody")

    # Each tr maps the current possibilities. It will be just tr -> td[n], tr -> td[n]
    # The first td[0] can be either the product or just a blank line that contains some other data that must be in a list
    rows = table.find_elements(By.TAG_NAME, "tr")

    current_header = ""
    previous_header = ""
    b3_data = {}
    for row in rows:
        data = [a.text for a in row.find_elements(By.TAG_NAME, "td")]
        # It means that we have a header in here
        if len(data) == 6:
            current_header = data[0]
            # We don't care about the name in the data, only to take it as a header
            data.pop(0)

        if current_header not in b3_data:
            b3_data[current_header] = []

        b3_data[current_header].append(data)

        if current_header != previous_header:
            previous_header = current_header

    # pprint.pprint(b3_data)
    print(len(b3_data))
    return 0


if __name__ == "__main__":
    main()

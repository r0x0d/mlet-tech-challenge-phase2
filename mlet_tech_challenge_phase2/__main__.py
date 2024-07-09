from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
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

b3_data = {}

def main() -> int:
    driver = setup_driver()
    driver.get(B3_AJUSTES_DO_PREGAO)
    assert "Ajustes do pregão | B3" in driver.title
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "bvmf_iframe")))[0]
    driver.switch_to.frame(iframe)
    table = driver.find_element(By.XPATH, "//table/tbody")
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        current_data = []
        current_header = ""
        for a in row.find_elements(By.TAG_NAME, "td"):
            has_rowspan = a.get_dom_attribute("rowspan") is not None

            if has_rowspan:
                current_header = a.text
            else:
                current_data.append(a.text)

        b3_data.update({current_header: current_data})

    print(b3_data)
    return 0

if __name__ == "__main__":
    main()

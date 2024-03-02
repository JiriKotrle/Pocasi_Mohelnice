from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Nastavíme cestu k WebDriveru, například pro Chrome
# !!! musím si stáhnout verrzi 122.0.6261.95
driver_path = '/path/to/chromedriver'

# Inicializujeme webový prohlížeč
driver = webdriver.Chrome(executable_path=driver_path)

# Otevřeme webovou stránku
url = "http://portal.envitech.eu:81/ovzdusi-lostice/station/1/emission/7?from=2024-03-02&interval=day&displayCharts=true&displayTables=true&updateControls="
driver.get(url)

try:
    # Předpokládejme, že rozklikávací okno má identifikátor 'dropdown-menu'
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'dropdown-menu'))
    )
    
    # Klikneme na rozklikávací okno
    dropdown_menu.click()
    
    # Zvolíme hodnotu, kterou chceme vybrat (předpokládáme, že hodnota má identifikátor 'option-value')
    option_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'option-value'))
    )
    
    # Klikneme na vybranou hodnotu
    option_value.click()
    
    # Pokud je potřeba nějaká další akce, můžeme ji zde provést
    
finally:
    # Ukončíme prohlížeč
    driver.quit()

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import os

os.system('cls')

url_teplota = "http://portal.envitech.eu:81/ovzdusi-lostice/station/1/emission/7?from=2024-03-02&interval=day&displayCharts=true&displayTables=true&updateControls="

def get_temperature(url_teplota):
    response = get(url_teplota)
    soup = BeautifulSoup(response.text, features="html.parser")
    td_temperatures = soup.find_all("td")
    temperatures_str = []

    for td in td_temperatures:
        temp = td.get_text(strip=True)
        temperatures_str.append(temp)
    
    temperatures = []

    for x in temperatures_str:
        try:
            y = float(x)
            temperatures.append(y)
        except ValueError:
            temperatures.append(x)

    temp_4hr_avg = []

    i = 0
    for x in temperatures:
    temp_avg_0_4 =

    print(temperatures)
    
    

get_temperature(url_teplota)
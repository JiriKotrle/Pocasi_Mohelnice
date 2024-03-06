from requests import get
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import os

os.system('cls')

# def get_url_temp():
#     aktualni_datum = datetime.now()
#     vcerejsi_datum = aktualni_datum - timedelta(days=1)
#     datum = vcerejsi_datum.strftime('%Y-%m-%d')

#     url1 = "http://portal.envitech.eu:81/ovzdusi-lostice/station/1/emission/7?from="
#     url2 = "&interval=day&displayCharts=true&displayTables=true&updateControls="

#     url_teplota = url1 + datum + url2
#     print(url_teplota)
#     return url_teplota

# def get_temperature(url_teplota):
#     response = get(url_teplota)
#     soup = BeautifulSoup(response.text, features="html.parser")
#     td_temperatures = soup.find_all("td")
#     temperatures_str = []

#     for td in td_temperatures:
#         temp = td.get_text(strip=True)
#         temperatures_str.append(temp)
    
#     temperatures = []

#     for x in temperatures_str:
#         try:
#             y = float(x)
#             temperatures.append(y)
#         except ValueError:
#             temperatures.append(x)
    
#     return temperatures
    
# def get_averages(temperatures):
#     i = 0
#     time_int = [4,8,12,16,20,24]
#     prumery = []

#     for ii in time_int:
#         dn = 0
#         suma = sum(x for x in temperatures[i:ii] if x != "DN")
#         dn = sum(1 for x in temperatures[i:ii] if x == "DN")
#         prumer = round((suma/(4-dn)), 2)
#         prumery.append(prumer)
#         i = i + 4

#     print(prumery)
    
url_prec = "https://hydro.chmi.cz/hppsoldv/hpps_act_rain.php?day_offset=1&fpob=OS&fdp=&fkraj=&ordrstr=11&startpage=2"

def get_prec(url_prec):
    response = get(url_prec)
    soup =  BeautifulSoup(response.text, features="html.parser")
    rows = soup.find_all('tr')
   
    for row in rows:
        if 'Dubicko' in row.text:  # Kontrola, zda řetězec obsahuje text "Dubicko"
            all_data = [cell.text for cell in row.find_all('td')]
           
    dataset_1 = list(all_data[2:9])
    dataset_2 = list(all_data[10:27])
    precipitation_str = dataset_1+dataset_2
    precipitation = [float(x) for x in precipitation_str]
    return precipitation

def get_averages_prec(precipitation):
    i = 0
    time_int = [4,8,12,16,20,24]
    prumery = []

    for ii in time_int:
        suma = sum(x for x in precipitation[i:ii])
        print(suma)
        prumer = round((suma/4), 2)
        prumery.append(prumer)
        i = i + 4

    print(prumery)

# precipitation = get_prec(url_prec)
# precipitation = [1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8]
# get_averages_prec(precipitation)

def get_datum(url_prec):
    response = get(url_prec)
    soup =  BeautifulSoup(response.text, features="html.parser")
    rows = soup.find_all('th')

    for row in rows:
        if "Datum" in row:
            print(row.strip())  # Print the element containing "Datum"

            
get_datum(url_prec)

# def get_result():
#     url_teplota = get_url_temp()
#     get_temperature(url_teplota)
#     temperatures = get_temperature(url_teplota)
#     get_averages(temperatures)

# get_result()
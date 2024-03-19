from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import os
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider  # Import Slider


os.system('cls')

def get_url_temp():
    aktualni_datum = datetime.now()
    urls_temp = []

    for i in range(1,8):
        zpetne_datum = aktualni_datum - timedelta(days=i)
        datum = zpetne_datum.strftime('%Y-%m-%d')

        url1 = "http://portal.envitech.eu:81/ovzdusi-lostice/station/1/emission/7?from="
        url2 = "&interval=day&displayCharts=true&displayTables=true&updateControls="

        url_teplota = url1 + datum + url2
        urls_temp.append(url_teplota)
    
    return(urls_temp)
    

def get_url_prec():
    url1 = "https://hydro.chmi.cz/hppsoldv/hpps_act_rain.php?day_offset="
    url2 = "&fpob=OS&fdp=&fkraj=&ordrstr=11&startpage=2"
    urls_prec = []

    for i in range(1,8):
        url_prec = url1 + str(i) + url2
        urls_prec.append(url_prec)

    return(urls_prec)


urls_temp = get_url_temp()
urls_prec = get_url_prec()

for x in range(1,8):
    url_temp = urls_temp[x-1]
    url_prec = urls_prec[x-1]
    print(url_prec, url_temp)



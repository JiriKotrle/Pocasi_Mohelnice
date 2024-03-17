from requests import get
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import os
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider  # Import Slider


os.system('cls')

def get_url_temp():
    aktualni_datum = datetime.now()
    vcerejsi_datum = aktualni_datum - timedelta(days=1)
    datum = vcerejsi_datum.strftime('%Y-%m-%d')

    url1 = "http://portal.envitech.eu:81/ovzdusi-lostice/station/1/emission/7?from="
    url2 = "&interval=day&displayCharts=true&displayTables=true&updateControls="

    url_teplota = url1 + datum + url2
    print(url_teplota)
    return url_teplota







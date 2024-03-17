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
    return url_teplota


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
    return temperatures


def get_temp_hr(temperatures):
    
    time_int = [4,8,12,16,20,24]
    temp_hrs = []

    for i in time_int:
        if temperatures[i-1] != "DN":
            temp = temperatures[i-1]
        elif temperatures[i-2] != "DN":
            temp = temperatures[i-2]
        elif temperatures[i-3] != "DN":
            temp = temperatures[i-3]
        else:
            temp = temperatures[i-4]
        temp_hrs.append(temp)
    return(temp_hrs)


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

def get_sums_prec(precipitation):
    i = 0
    time_int = [4,8,12,16,20,24]
    sum_prec = []

    for ii in time_int:
        suma = round(sum(x for x in precipitation[i:ii]),2)
        sum_prec.append(suma)
        i = i + 4
    return(sum_prec)


def get_datum(url_prec):
    response = get(url_prec)
    soup =  BeautifulSoup(response.text, features="html.parser")
    rows = soup.find_all('th')
    day = []
    for row in rows:
        if "Datum" in row.get_text():
            whole_datum = row.get_text()  # Print the element containing "Datum"
            datum = whole_datum.replace("Datum", "").strip()
            day.append(datum)
           
            return(day)
   

def create_pocasi_csv(day, temp_hrs, sum_prec): 
    columns = [
        "datum", "temp_4 hrs", "temp_8 hrs", "temp_12 hrs", "temp_16 hrs", "temp_20 hrs", "temp_24 hrs",
        "prec_4 hrs", "prec_8 hrs", "prec_12 hrs", "prec_16 hrs", "prec_20 hrs", "prec_24 hrs"
        ]
    
    all_data =[day + temp_hrs + sum_prec]
    
    print(all_data)
    df = pd.DataFrame(all_data, columns = columns)
    print(df)
    df.to_csv("pocasi.csv", index=False, encoding='cp1250', sep='\t', decimal=",")


def update_pocasi_csv(day, temp_hrs, sum_prec):
    # Vytvoření nového řádku s novými daty
    all_data = [day + temp_hrs + sum_prec]

    # Načtení existujícího souboru CSV
    df = pd.read_csv("pocasi.csv", sep='\t', encoding='cp1250',decimal=',')

    # poslední datum v .csv
    last_date = df['datum'].iloc[-1]
    if last_date in day:
        return

    else: 
        new_df = pd.DataFrame(all_data, columns=df.columns)
        print(new_df)

        # Spojení původního DataFrame a nového DataFrame
        df = pd.concat([df, new_df], ignore_index=True)

        # Uložení aktualizovaného DataFrame zpět do souboru CSV
        df.to_csv("pocasi.csv", index=False, sep='\t', encoding='cp1250', decimal=',')


def plot_chart():
    df = pd.read_csv("pocasi.csv", sep='\t', encoding='cp1250',decimal=',')

    # získání teplot z celého csv:
    y_values_temp = []
    # projede řádky
    for i in range(len(df)):
        # projede sloupce:
        for ii in range(6):
            temp = df.iloc[i,ii+1]
            y_values_temp.append(temp)
    print(y_values_temp)

    # získání srážek z celého csv:
    y_values_prec = []
    for i in range(len(df)):
        # projede sloupce:
        for ii in range(6,12):
            prec = df.iloc[i,ii+1]
            y_values_prec.append(prec)

    # vytvoření osy X:
    columns_name = ['4 hrs', '8 hrs', '12 hrs', '16 hrs', '20 hrs', '24 hrs']
    list_datums = df['datum'].tolist()
    x_values = []
    index = 1
    for i in list_datums:
        for ii in columns_name:
            x_value = "_".join([i,ii, f'({str(index)})'])
            x_values.append(x_value)
            index += 1

    # Vykreslení grafu
    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    # Graf pro teploty
    ax.plot(x_values, y_values_temp, marker='x', color='r', label='Teploty (°C)')
    ax.set_ylabel('Teploty (°C)', color='r')
    ax.tick_params(axis='y', labelcolor='r')

    # Graf pro srážky jako sloupcový graf
    ax2.bar(x_values, y_values_prec, color='b', alpha=0.5, label='Suma srážek za poslední 4 hod (mm)')
    ax2.set_ylabel('Suma srážek za poslední 4 hod (mm)', color='b')

    ax.set_xticks(x_values)

    # Nastavení úhlu natočení názvů na ose x a velikosti písma
    ax.set_xticklabels(x_values, rotation=90, fontsize=6)

    # Posunutí okrajů grafu nahoru
    plt.subplots_adjust(bottom=0.2)

    # Popisky os
    ax.set_xlabel('Datum_čas_index')

    # Název grafu
    plt.title('Graf teplot a srážek')

    # Vytvoření slideru
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.2, 0.0, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax_slider, 'Index', 10, len(x_values), valinit=1)

    def update(val):
        index = int(slider.val)
        ax.set_xlim(index - 10, index + 10)  # Updatuje rozsah zobrazených hodnot
        ax2.set_xlim(index - 10, index + 10)
        fig.canvas.draw_idle()  # Překreslí graf po změně

    slider.on_changed(update)

    # Zobrazení legendy
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Zobrazení grafu
    plt.show()

def get_result():
    url_teplota = get_url_temp()
    get_temperature(url_teplota)
    temperatures = get_temperature(url_teplota)
    temp_hrs = get_temp_hr(temperatures)
    get_prec(url_prec)
    precipitation = get_prec(url_prec)
    sum_prec = get_sums_prec(precipitation)
    day = get_datum(url_prec)
    
    try:
        update_pocasi_csv(day, temp_hrs, sum_prec)
    except FileNotFoundError:
        create_pocasi_csv(day, temp_hrs, sum_prec)
    plot_chart()


get_result()


# auto spuštění
# natáhnutí dat ode dne posledního spuštění ke dni aktuálního spuštění (např. když se týden nespustí tak si dotáhne chybějící data)
# spojit do jedné funkce get_url, kde se pro každé z url vytvoří seznam s hodnotami 7 dní zpět. poté for fce která seznami projde a předá konkrétní url pro získání srážek a teploty

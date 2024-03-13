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
    
def get_averages(temperatures):
    i = 0
    time_int = [4,8,12,16,20,24]
    avg_temp = []

    for ii in time_int:
        dn = 0
        suma = sum(x for x in temperatures[i:ii] if x != "DN")
        dn = sum(1 for x in temperatures[i:ii] if x == "DN")
        prumer = round((suma/(4-dn)), 2)
        avg_temp.append(prumer)
        i = i + 4

    print(avg_temp)
    return(avg_temp)



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

    print(sum_prec)
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
            print(day)
            return(day)
   

def create_pocasi_csv(day, avg_temp, avg_prec): 
    columns = [
        "datum", "temp (0-4)", "temp (5-8)", "temp (9-12)", "temp(13-16)", "temp(17-20)", "temp(21-24)",
        "prec(0-4)", "prec(5-8)", "prec(9-12)", "prec(13-16)", "prec(17-20)", "prec(21-24)"
        ]
    
    all_data =[day + avg_temp + avg_prec]
    
    print(all_data)
    df = pd.DataFrame(all_data, columns = columns)
    print(df)
    df.to_csv("pocasi.csv", index=False, encoding='cp1250', sep='\t', decimal=",")



def update_pocasi_csv(day, avg_temp, avg_prec):
    # Vytvoření nového řádku s novými daty
    all_data = [day + avg_temp + avg_prec]

    # Načtení existujícího souboru CSV
    df = pd.read_csv("pocasi.csv", sep='\t', encoding='cp1250',decimal=',')
    print(df)

    new_df = pd.DataFrame(all_data, columns=df.columns)
    print(new_df)

    # Spojení původního DataFrame a nového DataFrame
    df = pd.concat([df, new_df], ignore_index=True)

    # Uložení aktualizovaného DataFrame zpět do souboru CSV
    df.to_csv("pocasi.csv", index=False, sep='\t', encoding='cp1250', decimal=',')


def plot_chart():
    df = pd.read_csv("pocasi.csv", sep='\t', encoding='cp1250',decimal=',')

    y_values_temp = []
    # projede řádky
    for i in range(len(df)):
        # projede sloupce:
        for ii in range(6):
            temp = df.iloc[i,ii+1]
            y_values_temp.append(temp)
    print(y_values_temp)

    temp_columns_name = ['temp(0-4)', 'temp(5-8)', 'temp(9-12)', 'temp(13-16)', 'temp(17-20)', 'temp(21-24)']
    prec_columns_name = ['prec(0-4)', 'prec(5-8)', 'prec(9-12)', 'prec(13-16)', 'prec(17-20)', 'prec(21-24)']

    list_datums = df['datum'].tolist()
    print(list_datums)

    x_values = []
    index = 1

    for i in list_datums:
        for ii in temp_columns_name:
            x_value = " ".join([f'({str(index)})',ii,i])
            x_values.append(x_value)
            index += 1
    print(x_values)


    fig, ax = plt.subplots()

    plt.plot(x_values, y_values_temp, marker='x')
    
    # Nastavení úhlu natočení názvů na ose x a velikosti písma
    plt.xticks(rotation=90, fontsize=6)

    # Posunutí okrajů grafu nahoru
    plt.subplots_adjust(bottom=0.3)

    # Popisky os
    plt.xlabel('Osa X')
    plt.ylabel('Osa Y')

    # Název grafu
    plt.title('Graf teplot (°C)')

    # Vytvoření slideru
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.2, 0.0, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax_slider, 'Index', 10, len(x_values), valinit=1)

    def update(val):
        index = int(slider.val)
        ax.set_xlim(index - 10, index + 10)  # Updatuje rozsah zobrazených hodnot
        fig.canvas.draw_idle()  # Překreslí graf po změně

    slider.on_changed(update)
    # Zobrazení grafu
    plt.show()

def get_result():
    url_teplota = get_url_temp()
    get_temperature(url_teplota)
    temperatures = get_temperature(url_teplota)
    avg_temp = get_averages(temperatures)
    get_prec(url_prec)
    precipitation = get_prec(url_prec)
    avg_prec = get_sums_prec(precipitation)
    day = get_datum(url_prec)
    
    try:
        update_pocasi_csv(day, avg_temp, avg_prec)
    except FileNotFoundError:
        create_pocasi_csv(day, avg_temp, avg_prec)
    plot_chart()


get_result()
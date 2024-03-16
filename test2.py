import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Slider  # Import Slider

os.system('cls')

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
    print(y_values_prec)

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
    print(x_values)


    # Vykreslení grafu
    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    # Graf pro teploty
    ax.plot(x_values, y_values_temp, marker='x', color='r', label='Teploty (°C)')
    ax.set_ylabel('Teploty (°C)', color='r')
    ax.tick_params(axis='y', labelcolor='r')

    # Graf pro srážky jako sloupcový graf
    ax2.bar(x_values, y_values_prec, color='b', alpha=0.5, label='Srážky (mm)')
    ax2.set_ylabel('Srážky (mm)', color='b')

    # Nastavení úhlu natočení názvů na ose x a velikosti písma
    ax.set_xticklabels(x_values, rotation=90, fontsize=6)


    # Posunutí okrajů grafu nahoru
    plt.subplots_adjust(bottom=0.2)

    # Popisky os
    ax.set_xlabel('Osa X')

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

plot_chart()

# upravit názvy osy x
# srážky brát jako sumu za 4 hod
# teplotu jako aktuální hodnotu v čase 4,8,12,16,20,24
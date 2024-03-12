import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Slider  # Import Slider

os.system('cls')


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

    temp_columns_name = ['temp (0-4)', 'temp (5-8)', 'temp (9-12)', 'temp(13-16)', 'temp(17-20)', 'temp(21-24)']
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
    plt.title('Opakované hodnoty na ose X')

    # Vytvoření slideru
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax_slider, 'Index', 1, len(x_values), valinit=1)

    def update(val):
        index = int(slider.val)
        ax.set_xlim(index - 10, index + 10)  # Updatuje rozsah zobrazených hodnot
        fig.canvas.draw_idle()  # Překreslí graf po změně

    slider.on_changed(update)
    # Zobrazení grafu
    plt.show()

plot_chart()
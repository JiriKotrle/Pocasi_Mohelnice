import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np

os.system('cls')


def plot_chart():
    df = pd.read_csv("pocasi.csv", sep='\t', encoding='cp1250',decimal=',')

    x_values = 3*[0,4,8,12,16,20]
    print(x_values)

    y_values_temp = []
    # projede řádky
    for i in range(len(df)):
        # projede sloupce:
        for ii in range(6):
            temp = df.iloc[i,ii+1]
            y_values_temp.append(temp)

    plt.plot(range(len(x_values)), y_values_temp)

# Popisky os
    plt.xlabel('Osa X')
    plt.ylabel('Osa Y')

# Název grafu
    plt.title('Opakované hodnoty na ose X')

# Zobrazení grafu
    plt.show()

plot_chart()
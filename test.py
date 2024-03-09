import pandas as pd
import os

os.system('cls')

avg_temp = [21.38, 0.36, 21.94, 62.86, 6.97, 5.73]
avg_prec = [0.00, 0.01, 0.00, 0.05, 0.0, 0.0]
day = ['10.03.2024']



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

# Aktualizace souboru CSV
update_pocasi_csv(day, avg_temp, avg_prec)




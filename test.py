import matplotlib.pyplot as plt

# Teploty a srážky
y_values_temp = [20, 22, 25, 24, 23, 21]  # Příklad teplot
y_values_prec = [0, 2, 5, 3, 1, 0]          # Příklad srážek

# Hodiny
x_values = [4, 8, 12, 16, 20, 24]

# Vykreslení grafu
fig, ax1 = plt.subplots()

# Graf pro teploty
color = 'tab:red'
ax1.set_xlabel('Hodiny')
ax1.set_ylabel('Teploty (°C)', color=color)
ax1.plot(x_values, y_values_temp, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Vytvoření druhé osy x pro srážky
ax2 = ax1.twinx()  

# Graf pro srážky jako sloupcový graf
color = 'tab:blue'
ax2.set_ylabel('Srážky (mm)', color=color)
ax2.bar(x_values, y_values_prec, color=color, alpha=0.5) # sloupcový graf pro srážky
ax2.tick_params(axis='y', labelcolor=color)

# Nastavení osy x
plt.xticks(x_values)

# Zobrazení grafu
plt.title('Teploty a srážky v průběhu dne')
plt.show()




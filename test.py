seznam = [9.31, 9.35, 9.46, 9.44, 9.31, 8.62, 8.03, 7.7, 8.59, 9.48, 9.78, 10.39, 10.9, 11.64, 11.97, 12.11, 11.79, 11.29, 10.75, 10.08, 9.88, 9.92, 9.68, 'DN']


i = 0
time_int = [4,8,12,16,20,24]

prumery = []

for ii in time_int:
    dn = 0
    suma = sum(x for x in seznam[i:ii] if x != "DN")
    dn = sum(1 for x in seznam[i:ii] if x == "DN")
    prumer = suma/ (4-dn)
    prumery.append(prumer)
    i = i + 4

print(prumery)
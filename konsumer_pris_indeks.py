import csv
import matplotlib.pyplot as plt
from os import path

path = 'konsumprisindeks.csv'
data = []
with open(path, "r", encoding="utf-8") as f:
    for line in f.readlines():
        #line.encode('utf-8').strip()
        new_line = line.replace(',', '.')
        data.append(new_line)

for line in data:
    print(line)

with open(path, 'w') as file:
    for line in data:
        file.write(line)

""" try:
    with open("konsumprisindeks.csv", encoding="utf-8") as f:
        csv_leser = csv.reader(f, delimiter=";")
        overskrift = next(csv_leser)

        # Henter kolonnenummerene til de ulike overskriftene
        kol_status = overskrift.index("Status")
        kol_lagnavn = overskrift.index("NameFormatted")
        kol_totaltid = overskrift.index("NetTime")
        kol_plassering = overskrift.index("RankClass")
        kol_klassenavn = overskrift.index("ClassName")
        kol_type_lag = overskrift.index("ClubTeamFormatted")
        kol_nasjon = overskrift.index("Nation")
        
        for rad in csv_leser:

            # Ignorerer deltakere som ikke kom i mål
            if rad[kol_status] != "TIME":
                continue

            lagnavn = rad[kol_lagnavn]
            totaltid = float(rad[kol_totaltid]) / 1000 # Deler på 1000 for å få tiden i s
            plassering = int(rad[kol_plassering])
            klassenavn = rad[kol_klassenavn]
            type_lag = rad[kol_type_lag]
            nasjon = rad[kol_nasjon]

            deltakere.append(Deltaker(lagnavn, totaltid, plassering, klassenavn, type_lag, nasjon))
except FileNotFoundError:
    print("Sørg for at du kjører filen fra inne i holmenkollstafetten-mappen!")
    exit() """
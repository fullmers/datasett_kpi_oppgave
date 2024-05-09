import csv
import matplotlib.pyplot as plt
from os import path

path = 'konsumprisindeks.csv'
data = []
with open(path, "r") as f:
    for line in f.readlines():
        line.encode('utf-8').strip()
        new_line = line.replace(',', '.')
        data.append(new_line)

with open(path, 'w') as file:
    for line in data:
        file.write(line)

class KonsumerPrisIndeks:
    def __init__(self, aar, gjennomsnitt,jan,feb,mar,apr,mai,jun,jul,aug,sep,okt,nov,des):
        self.aar = aar
        self.gjennomsnitt = gjennomsnitt
        self.jan = jan
        self.feb = feb
        self.mar = mar
        self.apr = apr
        self.mai = mai
        self.jun = jun
        self.jul = jul
        self.aug = aug
        self.sep = sep
        self.okt = okt
        self.nov = nov
        self.des = des
        self.months = [jan,feb,mar,apr,mai,jun,jul,aug,sep,okt,nov,des]


kpis = [] 

try:
    with open("konsumprisindeks.csv") as f:
        csv_leser = csv.reader(f, delimiter=";")
        overskrift = next(csv_leser)

        # Henter kolonnenummerene til de ulike overskriftene
        kol_år = overskrift.index('Aar')
        kol_gjennomsnitt = overskrift.index("gjennomsnitt")
        kol_jan = overskrift.index("Jan")
        kol_feb = overskrift.index("Feb")
        kol_mar = overskrift.index("Mar")
        kol_apr = overskrift.index("Apr")
        kol_mai = overskrift.index("Mai")
        kol_jun = overskrift.index("Jun")
        kol_jul = overskrift.index("Jul")
        kol_aug = overskrift.index("Aug")
        kol_sep = overskrift.index("Sep")
        kol_okt = overskrift.index("Okt")
        kol_nov = overskrift.index("Nov")
        kol_des = overskrift.index("Des")
      
        for rad in csv_leser:
            aar = rad[kol_år]
            gjennomsnitt = float(rad[kol_gjennomsnitt])
            jan = float(rad[kol_jan])   
            feb = float(rad[kol_feb])
            mar = float(rad[kol_mar])
            apr = float(rad[kol_apr])
            mai = float(rad[kol_mai])
            jun = float(rad[kol_jun])
            jul = float(rad[kol_jul])
            aug = float(rad[kol_aug])
            sep = float(rad[kol_sep])
            okt = float(rad[kol_okt])
            nov = float(rad[kol_nov])
            des = float(rad[kol_des])
            kpi = KonsumerPrisIndeks(aar=aar,gjennomsnitt=gjennomsnitt,jan=jan,feb=feb,mar=mar,apr=apr,mai=mai,jun=jun,jul=jul,aug=aug,sep=sep,okt=okt,nov=nov,des=des)
            kpis.append(kpi)
       #     deltakere.append(Deltaker(lagnavn, totaltid, plassering, klassenavn, type_lag, nasjon))
except FileNotFoundError:
    print("Sørg for at du kjører filen fra inne i holmenkollstafetten-mappen!")
    exit()       

my_max = 0
for kpi in kpis:
    temp_max = max(kpi.months)
    if temp_max > my_max:
        my_max = temp_max
print(my_max)
for kpi in kpis:
    if my_max in kpi.months:
        print(kpi.aar)
        print(kpi.months)

my_min = my_max + 1
for kpi in kpis:
    temp_min = min(kpi.months)
    if temp_min < my_min and temp_min != -1:
        my_min = temp_min
print(my_min)

for kpi in kpis:
    if my_min in kpi.months:
        print(kpi.aar)
        print(kpi.months)


import csv
import matplotlib.pyplot as plt
from os import path
from enum import Enum

#clean data, replace , with . in numbers. replace . with Nan
""" data = []
with open('konsumprisindeks.csv', "r", encoding='utf-8') as f:
    for line in f.readlines():
        new_line1 = line.replace('.', 'NaN')
        new_line2 = new_line1.replace(',', '.')
        data.append(new_line2)

with open('konsumprisindeks_ny.csv', 'w',encoding='utf-8') as file:
    for line in data:
        file.write(line) """

class KonsumerPrisIndeks:
    def __init__(self, år, gjennomsnitt,months):
        self.år = år
        self.gjennomsnitt = gjennomsnitt
        self.months = months
        self.endring_gjennom_år = self.months[-1] - self.months[0]
        
kpis = [] 

try:
    with open('konsumprisindeks_ny.csv', encoding='utf-8') as f:
        csv_leser = csv.reader(f, delimiter=";")
        overskrift = next(csv_leser)
    
        for rad in csv_leser:
            år = float(rad[overskrift.index("År")])
            gjennomsnitt = float(rad[overskrift.index("gjennomsnitt")])
            jan = float(rad[overskrift.index("Jan")])   
            feb = float(rad[overskrift.index("Feb")])
            mar = float(rad[overskrift.index("Mar")])
            apr = float(rad[overskrift.index("Apr")])
            mai = float(rad[overskrift.index("Mai")])
            jun = float(rad[overskrift.index("Jun")])
            jul = float(rad[overskrift.index("Jul")])
            aug = float(rad[overskrift.index("Aug")])
            sep = float(rad[overskrift.index("Sep")])
            okt = float(rad[overskrift.index("Okt")])
            nov = float(rad[overskrift.index("Nov")])
            des = float(rad[overskrift.index("Des")])
            months = [jan,feb,mar,apr,mai,jun,jul,aug,sep,okt,nov,des]
            kpi = KonsumerPrisIndeks(år=år,
                                     gjennomsnitt=gjennomsnitt,
                                     months=months)
            kpis.append(kpi)
except FileNotFoundError:
    print("file not found")
    exit()       

my_max = 0
my_min = 1000

for kpi in kpis:
    temp_max = max(kpi.months)
    if temp_max > my_max:
        my_max = temp_max
    
    temp_min = min(kpi.months)
    if temp_min < my_min:
        my_min = temp_min

#alternative
#my_max = max(max(kpi.months) for kpi in kpis)
#my_min = min(min(kpi.months) for kpi in kpis) 


max_kpi_years = []
min_kpi_years = []
for kpi in kpis:
    if my_max in kpi.months:
        max_kpi_years.append(kpi)            
    if my_min in kpi.months:
        min_kpi_years.append(kpi)

class Months(Enum):
    jan = 0
    feb = 1
    mar = 2
    apr = 3
    mai = 4
    jun = 5
    jul = 6
    aug = 7
    sep = 8
    okt = 9
    nov = 10
    des = 11

def print_months_and_years(value, value_type, years: KonsumerPrisIndeks):
    for year in years:
        print('in ' + str(year.år) + ' the kpi had a ' + value_type + ' value of ' + str(value) + ' in the following months: ')
        index = 0
        month_list = []
        for index, month in enumerate(year.months):
            if month == value:
                month_list.append(Months(index).name)
        print(str(month_list)  + '\n')

print_months_and_years(my_min, 'min', min_kpi_years)
print_months_and_years(my_max, 'max', max_kpi_years)

max_difference = max(kpis[1:], key=lambda kpi: kpi.endring_gjennom_år)
print(max_difference.år)
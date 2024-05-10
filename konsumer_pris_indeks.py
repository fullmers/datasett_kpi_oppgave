import csv
import matplotlib.pyplot as plt
from os import path
from enum import Enum
import math

clean_data_file = 'konsumprisindeks_ny.csv'
original_data_file = 'konsumprisindeks.csv'

#clean data:
# 1) replace , with . in numbers
# 2) replace . with NaN so that all kpi values can be handled as floats
# 3) write updated lines to a new file 
def clean_data():
    # clean the data, but only once.
    if not path.isfile(clean_data_file):
        print("cleaning data")
        data = []
        try:
            with open(original_data_file, "r", encoding='utf-8') as f:
                for line in f.readlines():
                    new_line1 = line.replace('.', 'NaN')
                    new_line2 = new_line1.replace(',', '.')
                    data.append(new_line2)
                    print(new_line2)
        except IOError as e:
            print("I/O error: {0}, {1}".format(e.strerror, original_data_file))
            exit()

        try:
            with open(clean_data_file, 'w',encoding='utf-8') as file:
                for line in data:
                    file.write(line)
        except IOError as e:
            print("I/O error: {0}, {1}".format(e.strerror, clean_data_file))
            exit()
    else:
        print("data already cleaned") 


clean_data()

class KonsumerPrisIndeks:
    def __init__(self, år, gjennomsnitt,months):
        self.år = år
        self.gjennomsnitt = gjennomsnitt
        self.months = months
        self.endring_gjennom_år = abs(self.months[-1] - self.months[0])
      
kpis = [] 

try:
    with open(clean_data_file, encoding='utf-8') as f:
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
except IOError as e:
   print("I/O error: {0}, {1}".format(e.strerror, clean_data_file))
   exit() 


#3a - finner max og min KPI og tilhørende år og måneder 
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

#samle år som har max eller min kpi inne i
max_kpi_years = []
min_kpi_years = []
for kpi in kpis:
    if my_max in kpi.months:
        max_kpi_years.append(kpi)            
    if my_min in kpi.months:
        min_kpi_years.append(kpi)

#skriver ut måneder som lesebart ord. 
#måned data tilhøre til indeks i months list i KonsumerPrisIndeks objekt
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
        print('in ' + f"{year.år:.0f}" + ' the kpi had a ' + value_type + ' value of ' + str(value) + ' in the following months: ')
        index = 0
        month_list = []
        for index, month in enumerate(year.months):
            if month == value:
                month_list.append(Months(index).name)
        print(str(month_list)  + '\n')

print_months_and_years(my_min, 'min', min_kpi_years)
print_months_and_years(my_max, 'max', max_kpi_years)

#1b - finne år med største forskell mellom jan og des

max_difference = max(kpis[1:], key=lambda kpi: kpi.endring_gjennom_år)
print(max_difference.endring_gjennom_år)
print(str(int(max_difference.år)) + " var året med største forskjell fra jan til des. Forskellen var "+ f'{max_difference.endring_gjennom_år:.2f}')


#2a plotter
år = [kpi.år for kpi in kpis][1:]
gjennomsnitt_kpi_list = [kpi.gjennomsnitt for kpi in kpis][1:]

plt.figure(1)
plt.plot(år,gjennomsnitt_kpi_list)
plt.title("Gjennomsnitt konsumerprisindeks (KPI) over tid")
plt.ylabel("KPI")
plt.xlabel("År")


month_data_2022 = []
month_label_2022 = []


for index, month in enumerate(kpis[0].months):
    if not math.isnan(month):
        month_data_2022.append(month)
        month_label_2022.append(Months(index).name)

plt.figure(2)
plt.title("Konsumerprisindeks (KPI) i 2022")
plt.xlabel("måned")
plt.ylabel("KPI")
plt.ylim(115,130)
plt.bar(month_label_2022, month_data_2022)
plt.show()

#3a kalkulator
def gjennomsnitt_kpi_i_år(kpi_i_år):
    for kpi in kpis:
        if int(kpi.år) == int(kpi_i_år):
            return kpi.gjennomsnitt
            break

def pris_i_annet_år(år_1, år_2,pris_i_år_2):
    gjennomsnitt_kpi_i_år_1 = gjennomsnitt_kpi_i_år(år_1)
    gjennomsnitt_kpi_i_år_2 = gjennomsnitt_kpi_i_år(år_2)
    pris_i_år_1 = pris_i_år_2 * gjennomsnitt_kpi_i_år_1 / gjennomsnitt_kpi_i_år_2
    return pris_i_år_1

check_kpi_i_år_2000 = gjennomsnitt_kpi_i_år(2000)
print(check_kpi_i_år_2000)

check_pris_i_annet_år =pris_i_annet_år(2010,2000,45)
print(check_pris_i_annet_år)
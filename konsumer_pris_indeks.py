import csv
import matplotlib.pyplot as plt
from os import path
import math

ren_data_fil = 'konsumprisindeks_ny.csv'
opprinelig_data_fil = 'konsumprisindeks.csv'

# rener data:
# 1) . => NaN så Python kan håndtere alle data som float 
# 2) , => .  så Python forstår desimaltall i data
# 3) skriv oppdaterte linje til en ny fil 
def ren_data():
    # ren data, men bare en gang.
    #hvis fil fines ikke trenger å kjøre ren prosess igjen
    if not path.isfile(ren_data_fil): 
        print("rener data")
        data = []
        try:
            with open(opprinelig_data_fil, "r", encoding='utf-8') as f:
                for linje in f.readlines():
                    ny_linje1 = linje.replace('.', 'NaN')
                    ny_linje2 = ny_linje1.replace(',', '.')
                    data.append(ny_linje2)
        except IOError as e:
            print("I/O error: {0}, {1}".format(e.strerror, opprinelig_data_fil))
            exit()

        try:
            with open(ren_data_fil, 'w',encoding='utf-8') as file:
                for line in data:
                    file.write(line)
        except IOError as e:
            print("I/O error: {0}, {1}".format(e.strerror, ren_data))
            exit()
    else:
        print("data allerede rent") 


ren_data()

class KonsumerPrisIndeks:
    def __init__(self, år, gjennomsnitt,måneder: dict):
        self.år = år
        self.gjennomsnitt = gjennomsnitt
        self.måneder = måneder
        self.endring_gjennom_år = abs(self.måneder.get("des") - self.måneder.get("jan"))

#lager list av KonsumerPrisIndeks objekter fra data
kpis = [] 
try:
    with open(ren_data_fil, encoding='utf-8') as f:
        csv_leser = csv.reader(f, delimiter=";")
        overskrift = next(csv_leser)
    
        for rad in csv_leser:
            år = float(rad[overskrift.index("År")])
            gjennomsnitt = float(rad[overskrift.index("gjennomsnitt")])
            months = {"jan":float(rad[overskrift.index("Jan")]),
                      "feb":float(rad[overskrift.index("Feb")]),
                      "mar":float(rad[overskrift.index("Mar")]),
                      "apr":float(rad[overskrift.index("Apr")]),
                      "mai":float(rad[overskrift.index("Mai")]),
                      "jun":float(rad[overskrift.index("Jun")]),
                      "jul":float(rad[overskrift.index("Jul")]),
                      "aug":float(rad[overskrift.index("Aug")]),
                      "sep":float(rad[overskrift.index("Sep")]),
                      "okt":float(rad[overskrift.index("Okt")]),
                      "nov":float(rad[overskrift.index("Nov")]),
                      "des":float(rad[overskrift.index("Des")])} 
                      
            kpi = KonsumerPrisIndeks(år=år,
                            gjennomsnitt=gjennomsnitt,
                            måneder=months)
            kpis.append(kpi)
except IOError as e:
   print("I/O error: {0}, {1}".format(e.strerror, ren_data))
   exit() 


#1 - finner max og min KPI og tilhørende år og måneder
 
def fine_max_og_min_kpi():
    min_max = 0
    min_min = 1000
    for kpi in kpis:
        temp_max = max(list(kpi.måneder.values()))
        if temp_max > min_max:
            min_max = temp_max
        
        temp_min = min(list(kpi.måneder.values()))
        if temp_min < min_min:
            min_min = temp_min
    return (min_max, min_min)

#alternative
#my_max = max(max(kpi.months) for kpi in kpis)
#my_min = min(min(kpi.months) for kpi in kpis) 

#samle år som har max eller min kpi inne i
def skriv_år_og_måneder_med_verdi(søk_verdi, verdi_type, kpis):
    for kpi in kpis:
        print('I ' + f"{kpi.år:.0f}" + ' hadde kpi en ' + verdi_type + ' verdi av ' + str(søk_verdi) + ' i den følgende måneder: ')
        month_list = []
        for month, kpi_value in kpi.måneder.items(): 
            if kpi_value == søk_verdi:
                month_list.append(month)
        print(str(month_list)  + '\n')

def samle_og_skrive_max_min_():
    (min_max, min_min) = fine_max_og_min_kpi()
    max_kpi_år_list = []
    min_kpi_år_list = []
    for kpi in kpis:
        if min_max in list(kpi.måneder.values()):
            max_kpi_år_list.append(kpi)            
        if min_min in list(kpi.måneder.values()):
            min_kpi_år_list.append(kpi)
    skriv_år_og_måneder_med_verdi(min_max, 'max', max_kpi_år_list)
    skriv_år_og_måneder_med_verdi(min_min, 'min', min_kpi_år_list)

samle_og_skrive_max_min_()

#1b - finne år med største forskell mellom jan og des

def år_med_største_forskjell():
    max_forskjell = max(kpis[1:], key=lambda kpi: kpi.endring_gjennom_år)
    print(str(int(max_forskjell.år)) + " var året med største kpi forskjell fra jan til des. Forskellen var "+ f'{max_forskjell.endring_gjennom_år:.2f}')
#år_med_største_forskjell()


# 2 plotter
def lag_plotter():
    år = [kpi.år for kpi in kpis][1:]
    gjennomsnitt_kpi_list = [kpi.gjennomsnitt for kpi in kpis][1:]

    plt.figure(1)
    plt.plot(år,gjennomsnitt_kpi_list)
    plt.title("Gjennomsnitt konsumerprisindeks (KPI) over tid")
    plt.ylabel("KPI")
    plt.xlabel("År")

    month_data_2022 = []
    month_label_2022 = []

    for month, kpi_value in kpis[0].måneder.items(): 
        if not math.isnan(kpi_value):
            month_data_2022.append(kpi_value)
            month_label_2022.append(month)

    plt.figure(2)
    plt.title("Konsumerprisindeks (KPI) i 2022")
    plt.xlabel("måned")
    plt.ylabel("KPI")
    plt.ylim(115,130)
    plt.bar(month_label_2022, month_data_2022)
    plt.show()

# lag_plotter()

#3a kalkulator
def gjennomsnitt_kpi_i_år(kpi_i_år):
    for kpi in kpis:
        if int(kpi.år) == int(kpi_i_år):
            return kpi.gjennomsnitt
    return None

def pris_i_annet_år(år_1, år_2,pris_i_år_2):
    try:
        gjennomsnitt_kpi_i_år_1 = gjennomsnitt_kpi_i_år(år_1)
        gjennomsnitt_kpi_i_år_2 = gjennomsnitt_kpi_i_år(år_2)
        pris_i_år_1 = pris_i_år_2 * gjennomsnitt_kpi_i_år_1 / gjennomsnitt_kpi_i_år_2
    except Exception:
        print('ikke funnet år i data')
        exit()

    return pris_i_år_1

check_kpi_i_år_2000 = gjennomsnitt_kpi_i_år(2000)
print(check_kpi_i_år_2000)

check_pris_i_annet_år =pris_i_annet_år(2010,2000,45)
print(check_pris_i_annet_år)
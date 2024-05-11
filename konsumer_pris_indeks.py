import csv
import matplotlib.pyplot as plt
from os import path
import math

vasket_data_fil = 'konsumprisindeks_ny.csv'
opprinelig_data_fil = 'konsumprisindeks.csv'
def vask_data():
    ''' vask_data() formater opprinelige input data ("data cleaning" på engelsk).
    Det skulle kjøres bare en gang. Hvis fil med vasket data fines så ikke trenges å kjøre prosessen igjen'''
    if path.isfile(vasket_data_fil):
        print("data allerede vasket")
        return
    print("vasker data")
    data = []
    try:
        with open(opprinelig_data_fil, "r", encoding='utf-8') as f:
            for linje in f.readlines():
                # . => NaN så Python kan håndtere alle data som float 
                ny_linje1 = linje.replace('.', 'NaN')
                # , => .  så Python forstår desimaltall i data
                ny_linje2 = ny_linje1.replace(',', '.')
                data.append(ny_linje2)
    except IOError as e:
        print("I/O error: {0}, {1}".format(e.strerror, opprinelig_data_fil))
        exit()

    try:
        with open(vasket_data_fil, 'w',encoding='utf-8') as file:
            for line in data:
                file.write(line)
    except IOError as e:
        print("I/O error: {0}, {1}".format(e.strerror, vasket_data_fil))
        exit()

class KonsumerPrisIndeks:
    '''KonsumerPrisIndeks (KPI) inneholder alle data fra input csv, som er 
    år, gjenommsnitt KPI og KPI for hvert måned i året. 
    I tillegg så er det "endring_gjennom_år" som er endring i KPI fra jan til des i året. Dette felt er ikke i opprinelige data men er nyttig for noe spørsmål om det. 

    Det har ingen funksjoner bortsett fra init. Så det funker i praksis som en "data class" uten @dataclass decorator.
    '''
    def __init__(self, år: int, gjennomsnitt: float, måneder: dict):
        self.år = år
        self.gjennomsnitt = gjennomsnitt
        self.måneder = måneder
        self.endring_gjennom_år = abs(self.måneder.get("des") - self.måneder.get("jan"))

#lager list av KonsumerPrisIndeks objekter fra data
def lager_KPI_objekt_list_fra_data() -> list[KonsumerPrisIndeks]:
    kpis = []
    try:
        with open(vasket_data_fil, encoding='utf-8') as f:
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
            return kpis
    except IOError as e:
        print("I/O error: {0}, {1}".format(e.strerror, vask_data))
        exit() 


# 1a
def finne_max_og_min_kpi(kpis: list[KonsumerPrisIndeks]):
    ''' Finner max og min KPI verdi fra hele datasett'''
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
#my_max = max(max(kpi.måneder.values()) for kpi in kpis)
#my_min = min(min(kpi.måneder.values()) for kpi in kpis) 

def samle_og_skrive_max_min(kpis: list[KonsumerPrisIndeks]):
    '''Dette finner min og max KPI verdiene i gitt data og skriver ut hvilke år og måneder verdiene finnes i.'''
    (min_max, min_min) = finne_max_og_min_kpi(kpis)
    max_kpi_år_list = []
    min_kpi_år_list = []
    for kpi in kpis:
        if min_max in list(kpi.måneder.values()):
            max_kpi_år_list.append(kpi)            
        if min_min in list(kpi.måneder.values()):
            min_kpi_år_list.append(kpi)

    for kpi in max_kpi_år_list:
        print('I ' + f'{kpi.år:.0f}' + ' hadde KPI en max verdi av ' + str(min_max) + ' i de følgende månedene: ')
        max_month_list = []
        for month, kpi_value in kpi.måneder.items(): 
            if kpi_value == min_max:
                max_month_list.append(month)
        print(max_month_list)

    for kpi in min_kpi_år_list:
        print('I ' + f"{kpi.år:.0f}" + ' hadde KPI en min verdi av ' + str(min_min) + ' i de følgende månedene: ')
        min_month_list = []
        for month, kpi_value in kpi.måneder.items(): 
            if kpi_value == min_min:
                min_month_list.append(month)
        print(min_month_list)

#1b
def år_med_største_forskjell(kpis: list[KonsumerPrisIndeks]):
    '''Dette finner år med største forskjell mellom januar og desember og skriver det ut.'''
    kpis_uten_2022 = kpis[1:]
    max_forskjell = max(kpis_uten_2022, key=lambda kpi: kpi.endring_gjennom_år)
    print(str(int(max_forskjell.år)) + " var året med største KPI forskjell fra jan til des. Forskellen var "+ f'{max_forskjell.endring_gjennom_år:.2f}')

# 2 plotter
def lag_plotter(kpis: list[KonsumerPrisIndeks]):
    år = [kpi.år for kpi in kpis][1:] #list av år untatt 2022
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

#3a kalkulator
def gjennomsnitt_kpi_i_år(kpi_i_år, kpis: list[KonsumerPrisIndeks]):
    ''' Dette finner gjennomsnittlig KPI i et gitt år'''
    for kpi in kpis:
        # hvis kpis hadde vært et map fra år til KPI, kunne vi her bare slått
        # opp, i stedet for å iterere gjennom lista
        if int(kpi.år) == int(kpi_i_år):
            return kpi.gjennomsnitt
    return None

def pris_i_annet_år(år_1, år_2,pris_i_år_2, kpis: list[KonsumerPrisIndeks]):
    '''Gitt pris i et år og et annet år, finner dette pris i annet året'''
    gjennomsnitt_kpi_i_år_1 = gjennomsnitt_kpi_i_år(år_1, kpis)
    gjennomsnitt_kpi_i_år_2 = gjennomsnitt_kpi_i_år(år_2, kpis)
    pris_i_år_1 = pris_i_år_2 * gjennomsnitt_kpi_i_år_1 / gjennomsnitt_kpi_i_år_2
    print('I ' + str(år_1) + ' kostet noe ' + f'{pris_i_år_1:.2f}'  + ' som kostet ' + f'{pris_i_år_2:.2f}' + ' i ' + str(år_2) )
    return pris_i_år_1

def main():
    vask_data()
    kpis = lager_KPI_objekt_list_fra_data()

    finne_max_og_min_kpi(kpis)
    samle_og_skrive_max_min(kpis)

    år_med_største_forskjell(kpis)
    #lag_plotter(kpis)

    pris_i_annet_år(år_1=2010, år_2=2000, pris_i_år_2=45, kpis=kpis)

main()

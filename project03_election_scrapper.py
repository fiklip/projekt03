"""

ELECTION SCRAPPER - okres Pelhřimov

project03_election_scrapper_v2.py: třetí projekt do Engeto Online Python Akademie, verze 2

author: Filip Vrbík

email: filip.vrbik@vzp.cz

discord: filip.vrbik

"""

# potřebné knihovny ke spuštění skriptu

import sys

import requests

from bs4 import BeautifulSoup as bs

import csv

import logging


# Nastavení logování

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#== FUNKCE kontrola_url(url_okresu) ==#
#== kontrola správně zadané url ==#

def kontrola_url(url_okresu):
    if not url_okresu.startswith("http://") and not url_okresu.startswith("https://"):
        logging.error("Zadaná URL není platná. Má začínat 'http://' nebo 'https://'.")
        sys.exit(1)

#== FUNKCE kontrola_csv(csv_soubor) ==#
#== kontrola správně zadané přípony a platných znaků u CSV souboru ==#

def kontrola_csv(csv_soubor):
    if not csv_soubor.endswith('.csv'):
        logging.error("Název CSV souboru musí končit na '.csv'.")
        sys.exit(1)

    spravne_znaky = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    for znak in csv_soubor[:-4]:  # Bez '.csv'
        if znak not in spravne_znaky:
            logging.error("Název CSV souboru může obsahovat pouze platné znaky (písmena, číslice, podtržítka, pomlčky).")
            sys.exit(1)


#== FUNKCE ziskani_url_obci()==#
#==Vytvoření slovníku kód obce: url s výsledky voleb v dané obci==#

def ziskani_url_obci(url_okresu) -> dict:
    
    zacatek_url = "https://www.volby.cz/pls/ps2017nss/"
    kody_obci_url = {}
    
    # odeslání požadavku GET
    odpoved_okres = requests.get(url_okresu).text

    # parsování vráceného HTML souboru
    rozdelene_html = bs(odpoved_okres, features="html.parser")

    #získávám tagy td, class="cislo", ve kterém je hledané url
    tagy_td_cislo = rozdelene_html.find_all("td", {"class": "cislo"})

    # z vybraných tagů vybírám url na výsledky za jednotlivé obce a jejich unik. kódy
    # vytváří se úplný zápis url ze zkráceného
    for n in range(len(tagy_td_cislo)):
        url_obce = tagy_td_cislo[n].findChild().get("href")
        kod_obce = tagy_td_cislo[n].findChild().get_text()
        kody_obci_url[kod_obce] = zacatek_url + url_obce
    return kody_obci_url


#== FUNKCE vytvoreni_hlavicky_csv ==#
#== Vytvoření hlavičky ==#

def vytvoreni_hlavicky_pro_csv(kody_obci_url: dict) -> list:
 
    logging.info("Vytvářím hlavičku CSV.")

    # vytvoření eng hlavičky csv souboru
    csv_hlavicka_eng = ["code", "location", "registered", "envelopes", "valid"]
    
    #náhodně vybraná obec pro zjištění názvů polit. stran
    odpoved_obec_hlavicka = requests.get(list(kody_obci_url.values())[0]).text
    rozdelene_html_obec_hlavicka = bs(odpoved_obec_hlavicka, features="html.parser")
    
    #nalezení názvů politických stran v náhodné obci
    hlasy_pro_stranu = rozdelene_html_obec_hlavicka.find_all("td", {"class": "overflow_name"})
    
    # prázdný list pro ukládání názvů polit. stran
    politicke_strany = list()
    
    # for cyklus pro postupné přidávání polit. stran do listu
    for n in range(len(hlasy_pro_stranu)):
        politicke_strany.append(hlasy_pro_stranu[n].get_text())
    
    #finální verze hlavičky
    csv_hlavicka = csv_hlavicka_eng + politicke_strany

    return csv_hlavicka

#== FUNKCE vytvor_csv_s_hlavickou(csv_hlavicka) ==#
#== Vytvoření prádzdného csv souboru s hlavičkou pro konkrétní okres ==#

def vytvor_csv_s_hlavickou(csv_hlavicka: list):
    with open(csv_soubor, mode="w", newline="", encoding="utf-8") as zapis_csv:
        zapisovac = csv.writer(zapis_csv)
        zapisovac.writerow(csv_hlavicka)

#== FUNKCE pro nalezení a zápis konkrétních hodnot pro každou obec ==#
#== Všechny tyto funkce vstupují do funkce "nacitani_dat_do_csv()" ==#

# nalezení názvu obce
def najdi_nazev_obce(rozdelene_html_obec):          
    nazev_obce = rozdelene_html_obec.find("h3", string=lambda text: "Obec:" in text).text
    list_pro_zapis.append(nazev_obce[7:].strip())   # strip užito pro odstranění prázdných znaků v názvech obcí

# nalezení počtu reg. voličů
def najdi_reg_volice(rozdelene_html_obec):          
    reg_volici = rozdelene_html_obec.find("td", {"headers": "sa2"}).get_text()
    list_pro_zapis.append(reg_volici)

# nalezení počtu vydaných obálek
def najdi_vyd_obalky(rozdelene_html_obec):          
    vyd_obalky = rozdelene_html_obec.find("td", {"headers": "sa3"}).get_text()
    list_pro_zapis.append(vyd_obalky)

# nalezení počtu platných hlasů
def najdi_plat_hlasy(rozdelene_html_obec):          
    platne_hlasy = rozdelene_html_obec.find("td", {"headers": "sa6"}).get_text()
    list_pro_zapis.append(platne_hlasy)

# nalezení hlasů pro politické strany v tabulce 1
def najdi_hlasy_pro_stranu_1(rozdelene_html_obec):  
        hlasy_pro_stranu = rozdelene_html_obec.find_all("td", {"headers": "t1sa2 t1sb3", "class": "cislo"})
        for n in range(len(hlasy_pro_stranu)):      # for cyklus pro postupné přidávání polit. stran do listu
            list_pro_zapis.append(hlasy_pro_stranu[n].get_text())

# nalezení hlasů pro politické strany v tabulce 2
def najdi_hlasy_pro_stranu_2(rozdelene_html_obec):  
        hlasy_pro_stranu = rozdelene_html_obec.find_all("td", {"headers": "t2sa2 t2sb3", "class": "cislo"})
        for n in range(len(hlasy_pro_stranu)):      # for cyklus pro postupné přidávání polit. stran do listu
            list_pro_zapis.append(hlasy_pro_stranu[n].get_text())



#== FUNKCE nacitani_dat_do_csv() ==#
#== Export všech dat do výsledného csv souboru ==#

def nacitani_dat_do_csv(kody_obci_url: dict):

    logging.info("Načítám data do CSV.")

    # prázdný zápisový list pro hodnoty každé obce
    global list_pro_zapis
    list_pro_zapis = list()

    # pro každou obec se načítá url a parsuje html
    for obec_url, obec_kod in zip(kody_obci_url.values(), kody_obci_url.keys()):
        list_pro_zapis.append(obec_kod)
        odpoved_obec = requests.get(obec_url).text
        rozdelene_html_obec = bs(odpoved_obec, features="html.parser")

        najdi_nazev_obce(rozdelene_html_obec)
        najdi_reg_volice(rozdelene_html_obec)
        najdi_vyd_obalky(rozdelene_html_obec)
        najdi_plat_hlasy(rozdelene_html_obec)
        najdi_hlasy_pro_stranu_1(rozdelene_html_obec)
        najdi_hlasy_pro_stranu_2(rozdelene_html_obec)

    # zápis hodnot
        with open(csv_soubor, mode="a", newline="", encoding="utf-8") as zapis_csv:
            zapisovac = csv.writer(zapis_csv)
            zapisovac.writerow(list_pro_zapis)
    
    #obnovení listu pro zápis, aby byl připraven na další řádek/obec    
        list_pro_zapis = list()



#== SPUŠTĚNÍ FUNKCÍ ==#

if __name__ == "__main__":
    
    # systémové argumenty
    url_okresu = sys.argv[1] # "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6103" #
    csv_soubor = sys.argv[2] # "export.csv" #  

    # kontrola správnosti vstupů
    kontrola_url(url_okresu)
    kontrola_csv(csv_soubor)

    # získání url s výsledky voleb v obcích daného okresu
    kody_obci_url = ziskani_url_obci(url_okresu)

    # vytvářím hlavičku výsledného csv souboru
    csv_hlavicka = vytvoreni_hlavicky_pro_csv(kody_obci_url)

    # vytvoření prázdného csv s hlavičkou
    vytvor_csv_s_hlavickou(csv_hlavicka)

    # načítání dat za každou obec do csv
    nacitani_dat_do_csv(kody_obci_url)

    logging.info("CSV soubor vytvořen, program ukončen. Du prát.")

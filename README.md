## **Engeto python akademie - třetí projekt**
Autor: Filip Vrbík, filip.vrbik@vzp.cz

Praha, 2024

V rámci třetího projektu je napsán program, pomocí kterého se stahují výsledky voleb do Poslanecké sněmovny PČR z roku 2017. Výsledný textový soubor obsahuje výsledky agregované na úroveň obcí ve vybraném okrese ČR.

### Instalace knihoven

Knihovny, které je potřeba nainstalovat pro správné fungování tohoto projektu, jsou uvedeny v souboru **requirements.txt**. 
Před samotnou instalací knihoven je vhodné vyvtořit nové virtuální prostředí a do něj nainstalovat knihovny. Ve Windows viz:

`python -m venv nove_vp # vytvoření nového virtuálního prostředí nove_vp`

`.\nove_vp\Scripts\activate # aktivace nového virtuálního prostředí`

`pip install -r requirements.txt # instalace potřebných knihoven`


### Spuštění programu

Program se spouští s dvěma argumenty, které musejí být správně vyplněny.
Prvním argumentem je URL okresu, ze kterého se budou data stahovat, druhým argumentem je název souboru s příponou csv, do kterého se budou data exportovat.
K URL jednotlivých okresů pro stahování dat se uživatel dostane po kliknutí na **X** ve sloupci **Výběr obce** u požadovaného okresu na tomto **[webu](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)**. 

Spuštění programu ve Windows na příkladu okresu Pelhřimov viz:

`python project03_election_scrapper_v2.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6103" "pelhrimov_export.csv"`

### Logy u úspěšně spuštěného programu

`2024-10-31 15:09:49,199 - INFO - Vytvářím hlavičku CSV.`

`2024-10-31 15:09:50,019 - INFO - Načítám data do CSV.`

`2024-10-31 15:10:27,892 - INFO - CSV soubor vytvořen, program ukončen.`

### Ukázka z výsledného csv souboru

`code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,...`

`509388,Arneštovice,68,54,54,3,0,0,14,...`

`561118,Bácovice,63,37,37,0,0,0,5,0,3,...`

`561126,Bělá,45,29,27,2,0,0,5,0,1,0,0,...`



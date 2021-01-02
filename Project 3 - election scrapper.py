import csv
import requests
from bs4 import BeautifulSoup as BS


def naplnit_Data(urlParams,kod_obce):
    web = requests.get("https://volby.cz/pls/ps2017nss/"+urlParams)
    soup2 = BS(web.text,"html.parser")
    data = [kod_obce]
    #print(soup2)
    for i in soup2.find_all("h3"):
        if "Obec:" in i.text:
            data.append(i.text.split(":")[-1].strip())
    data.append(soup2.find("td",attrs={"headers":"sa2"}).text.replace("\xa0"," "))
    data.append(soup2.find("td", attrs={"headers": "sa3"}).text.replace("\xa0"," "))
    data.append(soup2.find("td", attrs={"headers": "sa6"}).text.replace("\xa0"," "))
    for x in soup2.find_all("td",attrs={"headers":"t1sa2 t1sb3"}):
        data.append(x.text.replace("\xa0"," "))
    for x in soup2.find_all("td",attrs={"headers":"t2sa2 t2sb3","class":"cislo"}):
        data.append(x.text.replace("\xa0"," "))
    return data

def zapsatCSV(hlavicka,data,nazev_souboru):
    f = open(nazev_souboru+".csv","w",newline="\n")
    writter = csv.writer(f)
    writter.writerow(hlavicka)
    writter.writerows(data)
    f.flush()
    f.close()

def hlavicka(urlParams):
    web = requests.get("https://volby.cz/pls/ps2017nss/" + urlParams)
    soup3 = BS(web.text, "html.parser")
    head = ["Kod_obce","nazev_obce","registrovani_volici","vydane_listky","platne_listky"]
    for x in soup3.find_all("td", attrs={"headers": "t1sa1 t1sb2"}):
        head.append(x.text)
    for x in soup3.find_all("td", attrs={"headers": "t2sa1 t2sb2", "class":""}):
        head.append(x.text)
    return head

def zdroj(url):
    zdroj = requests.get(url)
    soup = BS(zdroj.text,"html.parser")
    return soup

def data(zdroj):
    data = [naplnit_Data(x.find("a")["href"],x.text) for x in zdroj.find_all("td",attrs={"class":"cislo"})]
    head =  hlavicka(zdroj.find("td",attrs={"class":"cislo"}).find("a")["href"])
    return(head,data)

def checkUrl(url):
    if "https://volby.cz/pls/ps2017nss/ps32" not in url:
        print("Adresa neodkazuje na stránku s výběrem obcí, zadej znovu")
        return False
    else:
        return True

rightUrl = False
print("Z této adresy {} si pomocí X v možnosti 'Výběr obce' zvol, jaké obce se mají zpracovat.".format("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"))
while rightUrl == False:
    adresa = input("Odkaz na danou stránku zkopíruj sem: ")
    rightUrl = checkUrl(adresa)
soubor = input("Zadej název souboru, kam se exportují výsledky voleb: ")
print("Zpracovávám...")
zapsatCSV(*data((zdroj(adresa))),soubor)
print("Hotovo. Výsledek najdeš v souboru {}.csv .".format(soubor) )
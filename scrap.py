import errno
from gettext import find
from pickle import FALSE
from re import T
from sre_constants import FAILURE
#from tkinter import FIRST
from requests_html import HTMLSession
import csv
import time

hus = 1

def main():
    print("--INFO--\n vælge et hus nummer 1 - 14, for alle huse tast 0")
    hus = int(input("hus: "))
    if hus == 0:
        alle_huse()
    else:
        enkelt_hus(hus)
    main()


def alle_huse():
    hus = 1 # ændre denne til 4 hvis hus 3, 4 ikke er oprettet
    i = 1 # ændre denne til 4 hvis hus 3, 4 ikke er oprettet
    while (i < 20):
        hus = hus + 1  # looper alle huse igennem
        s = HTMLSession()
        url = 'https://lundagersgartneri.dk/location/hus-{}/'.format(hus)  # url bliver indsat det ønskede hus nummer
       
        print(hus, "ud af 14")  # viser hvor langt den er nået

        def get_links(url):
            r = s.get(url)
            items = r.html.find('div.astra-shop-thumbnail-wrap')  # finder dette tag ved hver billede og gemmer link
            links = []
            for item in items:
                links.append(
                item.find('a', first=True).attrs['href'])  # tager alle link fra selve vare siden på det følgene hus
            return links

        print("Antal vare i hus:", len(get_links(url)))

        def get_productdata(link):
            r = s.get(link)
            title = r.html.find('div.elementor-element.elementor-element-5a161fd.elementor-widget.elementor-widget-woocommerce-product-title.elementor-page-title.elementor-widget-heading')[0].text  # finder titel
            try:
                lager = r.html.find(
                    'div.elementor-element.elementor-element-6876ca6.elementor-widget.elementor-widget-woocommerce-product-stock')[
                    0].full_text
            except:
                lager = "På lager"  # hvis ikke fundet indsættes "lager" som i følge siden er lavet sådan
            try:
                bord2 = r.html.find(
                    'div.elementor-element.elementor-element-f7abaf4.elementor-widget.elementor-widget-heading')[
                    0].full_text  # linje 2 fra hjemmeside placering
            except:
                bord2 = "-"  # hvis ikke fundet indsættes "-"
            try:
                bord = r.html.find(
                    'div.elementor-element.elementor-element-c0806ec.elementor-widget.elementor-widget-heading')[
                    0].full_text  # linje 1 fra hjemmeside placering
            except:
                bord = "-"  # hvis ikke fundet indsættes "-"
            #try:
            #    hus = r.html.find('div.elementor-element.elementor-element-2030407.elementor-widget.elementor-widget-shortcode')[0].full_text
            #except:
            #    hus = "-" # hvis ikke fundet indsættes "-"
            product = {
                'Vare': title.strip(),
                'Lager Status': lager.strip(),
                'Placering 1': bord.strip(),
                'Placering 2': bord2.strip(),
            #    'Hus': hus
            }
            # gemmer alle tags
            print(product)
            return product

        results = []
        links = get_links(url)
        for link in links:
            results.append(get_productdata(link))
            time.sleep(1)
            # gemmer hvert hus nummer i hver csv fil
        with open('hus{}.csv'.format(hus), 'w', encoding='utf16', newline='') as f:
            fc = csv.DictWriter(f, fieldnames=results[0].keys(), )
            fc.writeheader()
            fc.writerows(results)
            print(hus, "Færdig")

        i = +1
    exit(0)


def enkelt_hus(hus):
    hus = hus
    s = HTMLSession()
    url = 'https://lundagersgartneri.dk/location/hus-{}/'.format(hus)  # hjemmeside link
    print("Hus nr:", hus, "begyndt")

    def get_links(url):
        r = s.get(url)
        items = r.html.find('div.astra-shop-thumbnail-wrap')  # finder alle produkter på siden
        links = []
        for item in items:
            links.append(item.find('a', first=True).attrs['href'])
        return links

    print("Antal vare i hus:", len(get_links(url)))

    def get_productdata(link):
        
        r = s.get(link)
        title = r.html.find('div.elementor-element.elementor-element-5a161fd.elementor-widget.elementor-widget-woocommerce-product-title.elementor-page-title.elementor-widget-heading')[0].text  # finder første titel med h1 stor text
        try:
            lager = r.html.find(
                'div.elementor-element.elementor-element-6876ca6.elementor-widget.elementor-widget-woocommerce-product-stock')[
                0].full_text
        except:
            lager = "På lager"  # hvis ikke fundet indsættes "lager" som i følge siden er lavet sådan
        try:
            bord2 = \
            r.html.find('div.elementor-element.elementor-element-f7abaf4.elementor-widget.elementor-widget-heading')[
                0].full_text  # linje 2 fra hjemmeside placering
        except:
            bord2 = "-"  # hvis ikke fundet indsættes "-"
        try:
            bord = \
            r.html.find('div.elementor-element.elementor-element-c0806ec.elementor-widget.elementor-widget-heading')[
                0].full_text  # linje 1 fra hjemmeside placering
        except:
            bord = "-"  # hvis ikke fundet indsættes "-"
        #try:
            #hus = r.html.find('li.slw-product-location')[0].full_text
            #hus = r.html.find('div.elementor-element.elementor-element-2030407.elementor-widget.elementor-widget-shortcode')[0].full_text
       # except:
       #     hus = "-"
       # try:
       #     placering2 = r.html.find('ui.slw-product-locations-list')[0].full_text
       # except:
       #     placering2 = "-"
        product = {
            'Vare': title.strip(),
            'Lager Status': lager.strip(),
            'Placering 1': bord.strip(),
            'Placering 2': bord2.strip(),
           # 'Hus': hus,
           # 'Hus anden': placering2
        }
        # gemmer alle tags
        print(product)
        return product

    results = []
    links = get_links(url)

    for link in links:
        results.append(get_productdata(link))
        time.sleep(1)
        

    with open('hus{}.csv'.format(hus), 'w', encoding='utf16', newline='') as f:
        fc = csv.DictWriter(f, fieldnames=results[0].keys(), )
        fc.writeheader()
        fc.writerows(results)
    print(hus, "Færdig")
main()


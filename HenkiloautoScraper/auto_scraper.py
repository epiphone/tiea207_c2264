# -*- coding:utf-8 -*-
'''

Version 0.3
Created on 6.4.2013

Scraper, jolla screipataan matkatiedot henkilöautolla matkustaessa. Haetaan siis
tietty reitti ja ilmoitetaan sen kilometrimäärä sekä aika.
Tässä kannattaa käyttää dictionaryja

@author: Peter R

Paluuarvot: lähtöaika, paluuaika, matkan pituus, linkki google mapsiin
'''

from lxml import html
import urllib


def main():
    ''' Pääfunktio alkaa tästä '''

    #Muuttujia
    lahtopaikka = "Rautalampi"
    saapumispaikka = "Jyväskylä"
    matkan_pituus = 0


    # Dictionary, johon laitetaan lahtopaikka ja saapumispaikka
    params = {"saddr": lahtopaikka, "daddr": saapumispaikka}


    #Haetaan tästä osoitteesta tietoa, eli Rautalampi-Jyväskylä -väli. Käytetään params-dictionarya
    url_matka = "http://maps.google.fi/maps?" + urllib.urlencode(params)


    # Haetaan html-tiedosto, luodaan lxml-olio:
    try:
        root_matka = html.parse(url_matka)
    except IOError:
        print "Reitin tietojen skreippaaminen ep�onnistui"
        return


    #"//ol[class='dir-altroute-mult dir-mrgn']//li[1]//div//div[1]"

    reitti = root_matka.xpath("//ol[@id='dir_altroutes_body']//li[1]//div//div[1]//span")


    matkan_pituus = float(reitti[0].text_content().split()[0].replace(",","."))

    matkan_kesto = reitti[1].text_content()


    print "Reitti %s - %s: %s km, %s" % (lahtopaikka, saapumispaikka, matkan_pituus, matkan_kesto)



if __name__ == "__main__":
    main()

# -*- coding:utf-8 -*-
'''

Version 0.3
Created on 6.4.2013

Scraper, jolla screipataan matkatiedot henkilöautolla matkustaessa. Haetaan siis
tietty reitti ja ilmoitetaan sen kilometrimäärä sekä aika.
Tässä kannattaa käyttää dictionaryja

@author: Peter R
'''

from lxml import html
import urllib


def main():
    ''' Pääfunktio alkaa tästä '''
   
    #Muuttujia
    lahtopaikka = "Rautalampi"
    saapumispaikka = "Jyväskylä"
    
    
    # Dictionary, johon laitetaan lahtopaikka ja saapumispaikka
    params = {"saddr": lahtopaikka, "daddr": saapumispaikka}
    
   
    #Haetaan tästä osoitteesta tietoa, eli Rautalampi-Jyväskylä -väli. Käytetään params-dictionarya
    url = "http://maps.google.fi/maps?" + urllib.urlencode(params)
   
   
    # Haetaan html-tiedosto, luodaan lxml-olio:
    try:
        root = html.parse(url)
    except IOError:
        print "Skreippaaminen ep�onnistui"
        return
   
   
   
    #"//ol[class='dir-altroute-mult dir-mrgn']//li[1]//div//div[1]"
   
    rows = root.xpath("//ol[@id='dir_altroutes_body']//li[1]//div//div[1]")
    
    
    #Käydään kaikki rivit läpi ja tulostetaan reitin pituus ja matkaan kuluva aika
    # huom. tässä tapauksessa otetaan vain yksi rivi eli ensimmäinen reitti
    for row in rows:
        print "Reitti %s - %s: %s" % (lahtopaikka, saapumispaikka, row.text_content())
    
    
    # Polttoainekulujen hakeminen (tämä ei näytä toimivan!)
    fuel = root.xpath("//div[@id='fuelc_link']//a[@href='javascript:void(0)']")
    
    for row in fuel:
        print(row.text_content() + "€")
    


if __name__ == "__main__":
    main()
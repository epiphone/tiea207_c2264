# -*- coding:utf-8 -*-
# VR:än sivujen skreipperi.
# Lasse Wallden & Aleksi Pekkala
# 11.4.2013

import urllib2
from lxml import html
import webbrowser

# muodostetaan URL hakuehtojen perusteella, testaamisen vuoksi hakuehdot syötetään käsin
#def muodosta_url(mista, minne, lahto_tunnit, lahto_minuutit, lahto_pvm, luokka, ajan_tyyppi):
def muodosta_url():        
        
        mista = raw_input("Mista lahdet?")
        minne = raw_input("Minne menet?")
        print "1=Lähtöaika, 2=Saapumisaika"
        ajan_tyyppi = raw_input ("Tahdotko lähtö vai saapumisajan?:")
        lahto_tunnit = raw_input("Ajan tunnit(01-23):")
        lahto_minuutit = raw_input("Ajan minuutit:(00-59)")
        lahto_pvm = raw_input("Lahdon paivamaara (muodossa XX.YY.ZZZZ):")
        
        if ajan_tyyppi == "1":
            ajan_tyyppi_url = "true"
        if ajan_tyyppi == "2":
            ajan_tyyppi_url = "false"
        
        # url on muodossa "https://shop.vr.fi/onlineshop/JourneySearch.do?request_locale=fi&basic.fromStationVR=Kerava&basic.toStationVR=Tampere&basic.oneWay=true&basic.departureDate.hours=10&basic.oneWay=true&basic.departureDate.mins=42&basic.departureDate.date=31.05.2013&basic.outwardTimeSelection=true&basic.passengerNumbers%5B0%5D.passengerType=84&basic.passengerNumbers%5B0%5D.passengerAmount=1&basic.fiRuGroup=false&basic.campaignCode="
        urli = "https://shop.vr.fi/onlineshop/JourneySearch.do?request_locale=fi&basic.fromStationVR=" + mista + "&basic.toStationVR=" + minne + "&basic.oneWay=true&basic.departureDate.hours=" + lahto_tunnit + "&basic.oneWay=true&basic.departureDate.mins=" + lahto_minuutit + "&basic.departureDate.date=" + lahto_pvm + "&basic.outwardTimeSelection=" + ajan_tyyppi_url +"&basic.passengerNumbers%5B0%5D.passengerType=84&basic.passengerNumbers%5B0%5D.passengerAmount=1&basic.fiRuGroup=false&basic.campaignCode="       
        print "Annettu URL on: " + urli
        print "*********"
        print "Yritetaan avata URL..."
        # Avataan selaimessa URLin toimivuuden testaamiseksi
        webbrowser.open_new(urli)
        return urli

def selvita_hinnat(hinnat):
    lista_hinnoista = list()
    
    for hinta in hinnat:
        elementit = hinta.getchildren()
        hinnan_label = elementit[0].text_content()[:-2]
        lista_hinnoista.append(hinnan_label)

    return lista_hinnoista

def hae_vaihtojen_tiedot(testit):

    for testi in testit:
        indeksi = testi[0].text_content()
        laika = testi[1][0].text_content()
        lpaikka = testi[1][1].text_content()
        saika = testi[2][0].text_content()
        spaikka = testi[2][1].text_content()
        juna_ruma = " ".join(testi[3].text_content())
        juna = juna_ruma.replace(" ", "").split()

        tuloste = "Yhteys NRO: %s | Lahtoaika: %s | Lahtopaikka: %s | Saapumisaika: %s | Saapumispaikka: %s | Juna: %s %s |"
        print tuloste % (indeksi, laika, lpaikka, saika, spaikka, juna[1], juna[2])
    
    return "Kesken"


def main():
    avaaja = urllib2.build_opener(urllib2.HTTPCookieProcessor())

    #Pienten muutosten testaamisen nopeuttamiseksi, urlin muodostaminen on poissa käytöstä, ja käytössä on vakio url
    #urli = muodosta_url(mista, minne, lahto_tunnit, lahto_minuutit, lahto_pvm, luokka, lahto_vai_saapuminen)
    #urli = muodosta_url()
    urli = "https://shop.vr.fi/onlineshop/JourneySearch.do?request_locale=fi&basic.fromStationVR=Kerava&basic.toStationVR=Tampere&basic.oneWay=true&basic.departureDate.hours=10&basic.departureDate.mins=10&basic.departureDate.date=31.07.2013&basic.outwardTimeSelection=false&basic.returnDate.hours=10&basic.returnDate.mins=10&basic.returnDate.date=31.07.2013&basic.returnTimeSelection=true&basic.passengerNumbers%5B0%5D.passengerType=84&basic.passengerNumbers%5B0%5D.passengerAmount=1&basic.fiRuGroup=false&basic.campaignCode="
    root = html.parse(avaaja.open(urli))
    #webbrowser.open_new(urli)

    rows = root.xpath("//table[@id='buyTrip_1']/tbody")

    for row in rows:
        print "******************************************************************************"
        print " "
        yleiset = row.getchildren()[0].getchildren()  # Yhteyden yleiset tiedot

        laika = yleiset[0].text.strip()
        saika = yleiset[1].text.strip()
        vaihtoja = yleiset[2].text.strip()
        kesto = yleiset[3].text.strip()
        #***** Ekan hinnan selvitys ja tulostaminen ****
        #hinnan_paikka = yleiset[4].getchildren()
        #hinta = hinnan_paikka[0].text.encode('utf-8')[:-5]
        # **************************************************
        hinta = selvita_hinnat(row.xpath("tr[1]/td[contains(@class, 'ticketOption')]"))
        #hinta = row.find_class("ticketOption*")
        tuloste = "Lahtoaika: %s | Saapumisaika: %s | Vaihtoja: %s | Kesto: %s | Hinta: %s"
        
        print tuloste % (laika, saika, vaihtoja, kesto, hinta)

        if vaihtoja != "-":
            hae_vaihtojen_tiedot(row.xpath("tr[2]")[0][1])
            #print " ".join(row.xpath("tr[2]")[0].text_content().split())
            #print "Jippii!"
            #print testia

        print " "
            


if __name__ == "__main__":
    main()
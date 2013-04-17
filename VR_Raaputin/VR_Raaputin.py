# -*- coding:utf-8 -*-
# VR:än sivujen skreipperi.
# Lasse Wallden & Aleksi Pekkala
# 11.4.2013
# Aikaa: 14:48, 15:20 - 15:30, 16.4 12:30 - 13:15
#TODO:
#- Poikkeuksien hallintaa
#   * Lähijuniin ei näy ekassa paikassa hintaa... -> Erroria skreipatessa
#   * Hakuehdoilla ei löydy vuoroja
#   * Syöte ei ole validi
#- Ääkköset
#- VR ei yhdistä alennuksia! Ennakko + Opiskelija = Vain ennakko!
#- Mukautus rajapintaan
#- Nyt lopputuloksena tulee vain yhden vaihdon tiedot... Tällänen rakenne ei siis toimi. Suurempi
#  kokonaisuus tai VAIN tietojen haku aliohjelmilla, mutta niiden lisääminen "Pääohjelmassa"?
#- Vaihdossa junan tyyppi esille.
#- 

import urllib2
from lxml import html
import webbrowser

class VrScraper:
    def __init__(self):
        """Konstruktori"""
        pass

# muodostetaan URL hakuehtojen perusteella, testaamisen vuoksi hakuehdot syötetään käsin
#def muodosta_url(mista, minne, lahto_tunnit, lahto_minuutit, lahto_pvm, luokka, ajan_tyyppi):
def muodosta_url(mista, mihin, lahtoaika=None, saapumisaika=None):        
        # Päivämäärä ja aika tulee muodossa "YYYY-MM-DD HH:MM"
        #                                    0123456789012345

        if lahtoaika:
            print "annettu aika: " + lahtoaika
            lahto_pvm = lahtoaika[8:10] + "." + lahtoaika[5:7] + "." + lahtoaika[0:4]
            lahto_tunnit = lahtoaika[11:12]
            lahto_minuutit = lahtoaika[14:15]
            ajan_tyyppi_url = "true"
            urli = ("https://shop.vr.fi/onlineshop/JourneySearch.do?request_locale=fi&basic." +
            "fromStationVR=" + mista + 
            "&basic.toStationVR=" + mihin + 
            "&basic.oneWay=true&basic.departureDate.hours=" + lahto_tunnit + 
            "&basic.oneWay=true&basic.departureDate.mins=" + lahto_minuutit + 
            "&basic.departureDate.date=" + lahto_pvm + 
            "&basic.outwardTimeSelection=" + ajan_tyyppi_url + 
            "&basic.passengerNumbers%5B0%5D.passengerType=84&basic.passengerNumbers%5B0%5D.passengerAmount=1&basic.fiRuGroup=false&basic.campaignCode=")
        
        if saapumisaika:
            print "annettu saapumisaika: " + saapumisaika
            lahto_pvm = saapumisaika[8:9] + "." + saapumisaika[5:6] + "." + saapumisaika[0:4]
            print lahto_pvm
            lahto_tunnit = saapumisaika[11:12]
            print lahto_tunnit
            lahto_minuutit = saapumisaika[14:15]
            print lahto_minuutit
            ajan_tyyppi_url = "false"
            urli = ("https://shop.vr.fi/onlineshop/JourneySearch.do?request_locale=fi&basic." +
            "fromStationVR=" + mista + 
            "&basic.toStationVR=" + mihin + 
            "&basic.oneWay=true&basic.departureDate.hours=" + lahto_tunnit + 
            "&basic.oneWay=true&basic.departureDate.mins=" + lahto_minuutit + 
            "&basic.departureDate.date=" + lahto_pvm + 
            "&basic.outwardTimeSelection=" + ajan_tyyppi_url + 
            "&basic.passengerNumbers%5B0%5D.passengerType=84&basic.passengerNumbers%5B0%5D.passengerAmount=1&basic.fiRuGroup=false&basic.campaignCode=")

        print "Koitetaan avata URL..."
        #webbrowser.open_new(urli)

        return urli

#Selvitetään hinta sen sisätltävästä html-elementistä
def selvita_hinnat(hinnat):
    lista_hinnoista = list()
    
    for hinta in hinnat:
        elementit = hinta.getchildren()
        hinnan_label = elementit[0].text_content()[:-2]
        lista_hinnoista.append(hinnan_label)

    return lista_hinnoista

#Skreipataan vaihtojen tiedot niiden pitämistä HTM-elementeistä
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

        print " "
    
    return "Kesken"

def hae_vaihdot(vaihdot, palaute):
    print " "
    print "TILANNE hae_vaihdot alussa: "
    print palaute
    print " "

    vaihtojen_lista = []
    for vaihto in vaihdot:
        tiedot = dict()
        tiedot['lahtoaika'] = vaihto[1][0].text_content()
        tiedot['saapumisaika'] = vaihto[2][0].text_content()
        tiedot['mista'] = vaihto[1][1].text_content()
        tiedot['minne'] = vaihto[2][1].text_content()
        tiedot['tunnus'] = " ".join(vaihto[3].text_content()).replace(" ", "").split()
        vaihtojen_lista.append(tiedot)

    palaute['vaihdot'] = vaihtojen_lista
    return palaute

def hae_tiedot(palaute, url, root):
    rows = root.xpath("//table[@id='buyTrip_1']/tbody")

    print " "
    print "*****TILANNE hae_tiedot alussa: *****"
    print palaute
    print " "

    for row in rows:
        yleiset = row.getchildren()[0].getchildren()  # Yhteyden yleiset tiedot

        laika = yleiset[0].text.strip()
        palaute['lahtoaika'] = laika
        saika = yleiset[1].text.strip()
        palaute['saapumisaika'] = saika
        vaihtoja = yleiset[2].text.strip()
        kesto = yleiset[3].text.strip()
        palaute['kesto'] = kesto
        #***** Ekan hinnan selvitys ja tulostaminen ****
        #hinnan_paikka = yleiset[4].getchildren()
        #hinta = hinnan_paikka[0].text.encode('utf-8')[:-5]
        # *************************************************
        hinta = selvita_hinnat(row.xpath("tr[1]/td[contains(@class, 'ticketOption')]"))
        #hinta = row.find_class("ticketOption*")
        palaute['hinta'] = hinta
        print " "
        print "****** TILANNE HINTOJEN LISÄÄMISEN JÄLKEEN: *****"
        print palaute
        print " "

        if vaihtoja != "-":
            palaute['vaihtoja'] = vaihtoja
            palaute = hae_vaihdot(row.xpath("tr[2]")[0][1], palaute)
        else:
            palaute['vaihtoja'] = "0"



    return palaute

def hae_matka(mista, mihin, lahtoaika=None, saapumisaika=None, max_tulokset=3, alennusluokka=0):

    palaute = {'mista': mista, 'mihin': mihin}
    print " "
    print "*****TILANNE hae_matkassa: *****"
    print palaute
    print " "
    avaaja = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    url = muodosta_url(mista, mihin, lahtoaika, saapumisaika)
    root = html.parse(avaaja.open(url))
    palaute = hae_tiedot(palaute, url, root)

    return palaute


def main():
    diktionaari = hae_matka("Oulu", "Tampere", "2013-06-05 13:45")
    print " " 
    print "****Kaiken jälkeen: *****"
    print diktionaari
    print " "

    #*********************************************************************************
    #avaaja = urllib2.build_opener(urllib2.HTTPCookieProcessor())

    #Pienten muutosten testaamisen nopeuttamiseksi, urlin muodostaminen on poissa käytöstä, ja käytössä on vakio url
    #urli = muodosta_url(mista, minne, lahto_tunnit, lahto_minuutit, lahto_pvm, luokka, lahto_vai_saapuminen)
    #urli = muodosta_url()
    #urli = "https://shop.vr.fi/onlineshop/JourneySearch.do?request_locale=fi&basic.fromStationVR=Kerava&basic.toStationVR=Tampere&basic.oneWay=true&basic.departureDate.hours=10&basic.departureDate.mins=10&basic.departureDate.date=31.07.2013&basic.outwardTimeSelection=false&basic.returnDate.hours=10&basic.returnDate.mins=10&basic.returnDate.date=31.07.2013&basic.returnTimeSelection=true&basic.passengerNumbers%5B0%5D.passengerType=84&basic.passengerNumbers%5B0%5D.passengerAmount=1&basic.fiRuGroup=false&basic.campaignCode="
    #root = html.parse(avaaja.open(urli))
    #webbrowser.open_new(urli)

    #rows = root.xpath("//table[@id='buyTrip_1']/tbody")

    #for row in rows:
        #print "******************************************************************************"
        #print " "
        #yleiset = row.getchildren()[0].getchildren()  # Yhteyden yleiset tiedot

        #laika = yleiset[0].text.strip()
        #saika = yleiset[1].text.strip()
        #vaihtoja = yleiset[2].text.strip()
        #kesto = yleiset[3].text.strip()
        #***** Ekan hinnan selvitys ja tulostaminen ****
        #hinnan_paikka = yleiset[4].getchildren()
        #hinta = hinnan_paikka[0].text.encode('utf-8')[:-5]
        # **************************************************
        #hinta = selvita_hinnat(row.xpath("tr[1]/td[contains(@class, 'ticketOption')]"))
        #hinta = row.find_class("ticketOption*")
        #tuloste = "Lahtoaika: %s | Saapumisaika: %s | Vaihtoja: %s | Kesto: %s | Hinta: %s"
        
        #print tuloste % (laika, saika, vaihtoja, kesto, hinta)
        #print " "

        #if vaihtoja != "-":
            #hae_vaihtojen_tiedot(row.xpath("tr[2]")[0][1])
            #print " ".join(row.xpath("tr[2]")[0].text_content().split())
            #print "Jippii!"
            #print testia
            


if __name__ == "__main__":
    main()
# -*- coding:utf-8 -*-
# VR:än sivujen skreipperi.
# Lasse Wallden & Aleksi Pekkala
# 17.4.2013
#TODO:
#- Poikkeuksien hallintaa
#   * Lähijuniin ei näy ekassa paikassa hintaa... -> Erroria skreipatessa
#   * Hakuehdoilla ei löydy vuoroja
#   * Syöte ei ole validi
#- Alennusluokkien käsittely
#- Mukautus rajapintaan
#- Nyt lopputuloksena tulee vain yhden vaihdon tiedot... Tällänen rakenne ei siis toimi. Suurempi
#  kokonaisuus tai VAIN tietojen haku aliohjelmilla, mutta niiden lisääminen "Pääohjelmassa"?
#- Vaihdossa junan tyyppi esille.
#- Tulosteissa ääkköset bugaa vielä 

import urllib2
from lxml import html

class VrScraper:
    def __init__(self):
        """Konstruktori"""
        pass

# Korjataan syötteessä olevat ääkköset VR:n haku-urlän kanssa yhteensopivaan muotoon
def korjaa_aakkoset(teksti):
    tulos = teksti.replace("ä", "%C3%A4")
    tulos = tulos.replace("Ä", "%C3%84")
    tulos = tulos.replace("ö", "%C3%B6")
    tulos = tulos.replace("Ö", "&C3%96")

    return tulos

# muodostetaan URL syötteen perusteella
def muodosta_url(mista, mihin, lahtoaika=None, saapumisaika=None):        
    mista = korjaa_aakkoset(mista)
    mihin = korjaa_aakkoset(mihin)

    if lahtoaika:
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
        lahto_pvm = saapumisaika[8:10] + "." + saapumisaika[5:7] + "." + saapumisaika[0:4]
        lahto_tunnit = saapumisaika[11:12]
        lahto_minuutit = saapumisaika[14:15]
        ajan_tyyppi_url = "false"
        urli = ("https://shop.vr.fi/onlineshop/JourneySearch.do?request_locale=fi&basic." +
        "fromStationVR=" + mista + 
        "&basic.toStationVR=" + mihin + 
        "&basic.oneWay=true&basic.departureDate.hours=" + lahto_tunnit + 
        "&basic.oneWay=true&basic.departureDate.mins=" + lahto_minuutit + 
        "&basic.departureDate.date=" + lahto_pvm + 
        "&basic.outwardTimeSelection=" + ajan_tyyppi_url + 
        "&basic.passengerNumbers%5B0%5D.passengerType=84&basic.passengerNumbers%5B0%5D.passengerAmount=1&basic.fiRuGroup=false&basic.campaignCode=")

    return urli

# Haetaan hinnat HTML-elementeistä, palautetaan listana
# TODO! Poikkeuksia on!
def selvita_hinnat(hinnat):
    lista_hinnoista = list()
    
    for hinta in hinnat:
        elementit = hinta.getchildren()
        hinnan_label = elementit[0].text_content()[:-2]
        lista_hinnoista.append(hinnan_label)

    return lista_hinnoista


# Hakee yhteyden vaihtojen tiedot ja palauttaa ne listana dictionaryja
def hae_vaihtojen_tiedot(vaihdot):

    lista_vaihdoista = []
    for vaihto in vaihdot:
        vaihdon_tiedot = {}
        laika = vaihto[1][0].text_content()
        vaihdon_tiedot['lahtoaika'] = laika
        lpaikka = vaihto[1][1].text_content()
        vaihdon_tiedot['lahtopaikka'] = lpaikka
        saika = vaihto[2][0].text_content()
        vaihdon_tiedot['saapumisaika'] = saika
        spaikka = vaihto[2][1].text_content()
        vaihdon_tiedot['saapumispaikka'] = spaikka
        juna_ruma = " ".join(vaihto[3].text_content())
        juna = juna_ruma.replace(" ", "").split()
        vaihdon_tiedot['tunnus'] = juna
        lista_vaihdoista.append(vaihdon_tiedot)

    return lista_vaihdoista


# Hakee matkan tiedot paikasta X paikkaan Y. Palautetaan Dictionaryna, joka sisältää kaiken tarpeellisen tiedon
# TODO - Poikkeusten hallintaa. (Validointi ja matkojen löytymättöyys)
def hae_matka(mista, mihin, lahtoaika=None, saapumisaika=None, max_tulokset=3, alennusluokka=0):
    avaaja = urllib2.build_opener(urllib2.HTTPCookieProcessor())

    urli = muodosta_url(mista, mihin, lahtoaika, saapumisaika)
    
    root = html.parse(avaaja.open(urli))

    rows = root.xpath("//table[@id='buyTrip_1']/tbody")

    lista_yhteyksista = []

    for row in rows:
        yhteyden_tiedot = {}
        yhteyden_tiedot['mista'] = mista
        yhteyden_tiedot['mihin'] = mihin
        yleiset = row.getchildren()[0].getchildren()  # Yhteyden yleiset tiedot
        laika = yleiset[0].text.strip()
        yhteyden_tiedot['lahtoaika'] = laika
        saika = yleiset[1].text.strip()
        yhteyden_tiedot['saapumisaika'] = saika
        vaihtoja = yleiset[2].text.strip()
        yhteyden_tiedot['vaihtoja'] = vaihtoja
        kesto = yleiset[3].text.strip()
        yhteyden_tiedot['kesto'] = kesto
        hinta = selvita_hinnat(row.xpath("tr[1]/td[contains(@class, 'ticketOption')]"))
        yhteyden_tiedot['hinnat'] = hinta
        lista_yhteyksista.append(yhteyden_tiedot)

        if vaihtoja != "-":
            yhteyden_tiedot['vaihdot'] = hae_vaihtojen_tiedot(row.xpath("tr[2]")[0][1])
        
        yhteyden_tiedot['url'] = urli
    
    return lista_yhteyksista

# Tässä vaiheessa main funktiota käytetään vain käynnistämiseen ja syötteiden testaukseen
def main():
    
    #(mista, mihin, lahtoaika=None, saapumisaika=None, max_tulokset=3, alennusluokka=0)
    testataanko = raw_input('Käytetaanko valmista URL-osoitetta? (Y/N)')
    if testataanko == "N":
        mista = raw_input('Mista lahdet?')
        mihin = raw_input('Minne menet?')
        aika = raw_input('saapumis- vai lahtoaika? (S/L)')
        if aika == "S":
            saapumisaika = raw_input('Anna aika muodossa YYYY-MM-DD HH:MM')
            print hae_matka(mista, mihin, saapumisaika, 3, 0)
        if aika == "L":
            lahtoaika = raw_input('Anna aika muodossa YYYY-MM-DD HH:MM')
            print hae_matka(mista, mihin, lahtoaika, saapumisaika=None, maxtulokset=3, alennusluokka=0)
    if testataanko == "Y":
        print hae_matka("Jyväskylä", "Ähtäri", None, "2013-06-05 15:50", 3, 0)
            


if __name__ == "__main__":
    main()
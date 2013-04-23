# -*- coding:utf-8 -*-
# VR:än sivujen skreipperi.
# Lasse Wallden & Aleksi Pekkala
# 22.4.2013
#TODO:
# Critical:
#- Mukautus rajapintaan (Done?)
#- Tulosteissa ääkköset bugaa vielä...?
#- Poikkeuksia, poikkeuksia, poikeuksia....
#Optional
#- urli ostosivulle asti, ei hakutuloksiin

import urllib2
from lxml import html
import pprint


class VRScraper:
    def __init__(self):
        """Konstruktori"""
    pass

    def voidaanko_jatkaa(self, sivu, lahtoaika=None, saapumisaika=None):
        lista_virheista = []
        if sivu.xpath("//ul[@id='fieldsDepartureDateError']") or sivu.xpath("//ul[@id='fieldsDepartureTimeTypeError']"):
            if lahtoaika:
                lista_virheista.append("lahtoaika")
            else:
                lista_virheista.append("saapumisaika")

        if sivu.xpath("//ul[@id='fieldsFromError']"):
            lista_virheista.append("mista")

        if sivu.xpath("//ul[@id='fieldsToError']"):
            lista_virheista.append("mihin")

        if sivu.xpath("//span[@class='errorMessage']"):
            lista_virheista.append(0)

        if len(lista_virheista) < 1:
            lista_virheista.append("True")
            return lista_virheista
        else:
            return lista_virheista

    def laske_alennus(self, hinnat, alennusluokka):
        if alennusluokka in [0, 6]:
            return hinnat
        else:
            if hinnat[1]:
                hinta_lukuna = float(hinnat[1])
                hinnat[1] = hinta_lukuna / 2
                hinnat[1] = round(hinnat[1], 2)
                if hinnat[1] < 2.60:
                    hinnat[1] = 2.60
            if hinnat[2]:
                hinnat[2] = hinnat[2] / 2
                hinnat[2] = round(hinnat[2], 2)

        return hinnat

    # Korjataan syötteessä olevat ääkköset VR:n haku-urlän kanssa yhteensopivaan muotoon
    def korjaa_aakkoset(self, teksti):
        tulos = teksti.replace("ä", "%C3%A4")
        tulos = tulos.replace("Ä", "%C3%84")
        tulos = tulos.replace("ö", "%C3%B6")
        tulos = tulos.replace("Ö", "%C3%96")
        tulos = tulos.replace("å", "%C3%A5")
        tulos = tulos.replace("Å", "%C3%85")

        return tulos

    # muodostetaan URL syötteen perusteella
    def muodosta_url(self, mista, mihin, lahtoaika=None, saapumisaika=None):
        mista = self.korjaa_aakkoset(mista)
        mihin = self.korjaa_aakkoset(mihin)

        if lahtoaika:
            lahto_pvm = lahtoaika[8:10] + "." + lahtoaika[5:7] + "." + lahtoaika[0:4]
            lahto_tunnit = lahtoaika[11:13]
            lahto_minuutit = lahtoaika[14:16]
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
            lahto_tunnit = saapumisaika[11:13]
            lahto_minuutit = saapumisaika[14:16]
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
    def selvita_hinnat(self, hinnat):
        lista_hinnoista = list()
        for hinta in hinnat:
            elementit = hinta.getchildren()
            if hinta.text_content().find("Matka") != -1 or hinta.text_content().find("Ei") != -1 or len(hinta.text_content()) < 1:
                lista_hinnoista.append(None)
                continue
            if len(elementit) >= 1:
                hinnan_label = elementit[0].text_content()[:-2].replace(",", ".")
                if len(hinnan_label) > 0:
                    lista_hinnoista.append(hinnan_label)
                    continue
                else:
                    testi = hinta.text_content().replace(u"€", "")
                    testi = ' '.join(testi.split())
                    testi = testi.replace(",", ".")
                    lista_hinnoista.append(testi)
                    continue
            else:
                lista_hinnoista.append(None)

        if len(lista_hinnoista) < 3:
            lista_hinnoista.append(None)

        return lista_hinnoista

    # Hakee yhteyden vaihtojen tiedot ja palauttaa ne listana dictionaryja
    def hae_vaihtojen_tiedot(self, vaihdot, annettu_aika):
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
            vaihdon_tiedot['tunnus'] = juna[1] + " " + juna[2]
            vaihdon_tiedot['tyyppi'] = juna[1]
            lista_palveluista_html = vaihto[5].getchildren()
            palvelut = []
            if len(lista_palveluista_html) > 2:
                lista_palveluista_html.pop(0)
                lista_palveluista_html.pop(0)
                for palvelu in lista_palveluista_html:
                    palvelut.append(palvelu.get('alt'))
            else:
                palvelut.append("Ei palveluita")
            vaihdon_tiedot['palvelut'] = palvelut
            lista_vaihdoista.append(vaihdon_tiedot)

        return lista_vaihdoista

    # Hakee matkan tiedot paikasta X paikkaan Y. Palautetaan Dictionaryna, joka sisältää kaiken tarpeellisen tiedon
    def hae_matka(self, mista, mihin, lahtoaika=None, saapumisaika=None):
        avaaja = urllib2.build_opener(urllib2.HTTPCookieProcessor())

        urli = self.muodosta_url(mista, mihin, lahtoaika, saapumisaika)
        root = html.parse(avaaja.open(urli))
        virheet = self.voidaanko_jatkaa(root, lahtoaika, saapumisaika)

        if virheet[0] == "True":
            rows = root.xpath("//table[@id='buyTrip_1']/tbody")
            lista_yhteyksista = []
            paikat = root.xpath("//h2[@class='tripheading']")[0].text_content()
            paikat = paikat.replace(" ", "").split()
            lahtee = paikat[0]
            saapuu = paikat[1]
            for row in rows:
                yhteyden_tiedot = {}
                yhteyden_tiedot['mista'] = lahtee
                yhteyden_tiedot['mihin'] = saapuu
                yleiset = row.getchildren()[0].getchildren()
                laika = yleiset[0].text.strip()
                yhteyden_tiedot['lahtoaika'] = laika
                saika = yleiset[1].text.strip()
                yhteyden_tiedot['saapumisaika'] = saika
                kesto = yleiset[3].text.strip()
                yhteyden_tiedot['kesto'] = kesto
                hinta = self.selvita_hinnat(row.xpath("tr[1]/td[contains(@class, 'ticketOption')]"))
                yhteyden_tiedot['hinnat'] = hinta
                lista_yhteyksista.append(yhteyden_tiedot)
                if saapumisaika:
                    yhteyden_tiedot['vaihdot'] = self.hae_vaihtojen_tiedot(row.xpath("tr[2]")[0][1], saapumisaika)
                if lahtoaika:
                    yhteyden_tiedot['vaihdot'] = self.hae_vaihtojen_tiedot(row.xpath("tr[2]")[0][1], lahtoaika)
                yhteyden_tiedot['url'] = urli

            return lista_yhteyksista
        else:
            if virheet[0] == 0:
                return None
            else:
                return {"virhe": virheet}


    # Tässä vaiheessa main funktiota käytetään vain käynnistämiseen ja syötteiden testaukseen
def main():
    screipperi = VRScraper()
    testataanko = raw_input('Tahdotko itse syottaa hakuehdot? (Y/N)')
    if testataanko == "Y":
        mista = raw_input('Mista lahdet?')
        mihin = raw_input('Minne menet?')
        aika = raw_input('saapumis- vai lahtoaika? (S/L)')
        if aika == "S":
            saapumisaika = raw_input('Anna aika muodossa YYYY-MM-DD HH:MM')
            tiedot = screipperi.hae_matka(mista, mihin, None, saapumisaika)
            pprint.pprint(tiedot)
        if aika == "L":
            lahtoaika = raw_input('Anna aika muodossa YYYY-MM-DD HH:MM')
            tiedot = screipperi.hae_matka(mista, mihin, lahtoaika, None)
            pprint.pprint(tiedot)
    if testataanko == "N":
        tiedot = screipperi.hae_matka("Jyväskylä", "Ähtäri", None, "2013-06-05 15:50",)
        pprint.pprint(tiedot)


if __name__ == "__main__":
    main()

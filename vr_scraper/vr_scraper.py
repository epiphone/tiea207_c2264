# -*- coding:utf-8 -*-
# VR:än sivujen skreipperi.
# Lasse Wallden & Aleksi Pekkala
# 25.4.2013
#TODO:
#- Poikkeuksia, poikkeuksia, poikeuksia....

import urllib2
from lxml import html


class VRScraper:
    def __init__(self):
        """Konstruktori"""
    pass

    def ostosivun_url_muodostaja(self, alkuperainen_url, alennusluokka):
        """Palauttaa URL osoitteen, josta voi siirtyä ostamaan pyydetyn alennusluokan lippuja

        Alennusluokkien koodit: 84=Aikuinen, Opiskelija= 85, Eläkeläinen = 86, Juniori = 87
        Varusmies=88, Siviilipalvelusmies=89. Alennusluokkien tunnukset ovat: 0 = Aikuinen,
        1 = Lapsi, 2 = Opiskelija, 3 = Nuoriso, 4 = Eläkeläinen 5 = Varusmies, 6 = Lehdistö,
        7 = Siviilipalvelusmies
        """

        if alennusluokka not in ["0", "1", "2", "3", "4", "5", "6", "7"]:
            return "Kelpaamaton alennusluokka"

        if alennusluokka == "2":
            palaute = alkuperainen_url.replace("passengerType=84", "passengerType=85")

        if alennusluokka in ["1", "3"]:
            palaute = alkuperainen_url.replace("passengerType=84", "passengerType=87")

        if alennusluokka == "4":
            palaute = alkuperainen_url.replace("passengerType=84", "passengerType=86")

        if alennusluokka == "5":
            palaute = alkuperainen_url.replace("passengerType=84", "passengerType=88")

        if alennusluokka == "7":
            palaute = alkuperainen_url.replace("passengerType=84", "passengerType=89")

        if alennusluokka in ["0", "6"]:
            palaute = alkuperainen_url

        return palaute

    def voidaanko_jatkaa(self, sivu, lahtoaika=None, saapumisaika=None):
        """Palauttaa joko listan, jossa mainitaan kaikki virheen aiheuttaneet
           hakuehdot, merkkijonon 'True' jos virheitä ei ole (eli voidaan jatkaa)
           tai nolla, joka tarkoittaa ettei yhteyksiä löytnyt

        Tarkistetaan, onko screpatussa sivussa virheilmoituksia ja lisätään virehiden
        merkintä jokaisesta löytyneestä virhetyypistä.
        """

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

        if sivu.xpath("//div[@class='systemerrorDiv']"):
            lista_virheista.append("CERR")

        if len(lista_virheista) < 1:
            lista_virheista.append("True")
            return lista_virheista
        else:
            return lista_virheista

    def laske_alennus(self, hinnat, alennusluokka):
        """Palauttaa mahdollisen alennuksen mukaiset hinnat

        Tarkistetaan, mihin alennusluokkaan hakija kuuluu, jonka jälkeen lasketaan
        alennus hinnat listan indekseissä 1 ja 2 oleville hinnoille, mikäli hakija
        on oikeutettu alennuksiin. Hinnat listan indeksissä 0 on ennakkolippujen
        hinnat, joihin ei saa erikseen lisäalennusta. Alennusluokkien tunnukset
        ovat: 0 = Aikuinen, 1 = Lapsi, 2 = Opiskelija, 3 = Nuoriso, 4 = Eläkeläinen
        5 = Varusmies/Siviilipalvelusmies, 6 = Lehdistö
        """

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

    def korjaa_aakkoset(self, teksti):
        """Palauttaa annetun merkkijonon, jossa olevat ääkköset on muutettu
            VR:än haku-url:ää tukevaan muotoon

        Muutetaan annetussa merkkijonossa olevat ääkköset seuraavasti:
        ä => %C3%A4, Ä => %C3%84, ö => %C3%B6, Ö => %C3%96 å => %C3%A5
        Å => %C3%85
        """

        tulos = teksti.replace("ä", "%C3%A4")
        tulos = tulos.replace("Ä", "%C3%84")
        tulos = tulos.replace("ö", "%C3%B6")
        tulos = tulos.replace("Ö", "%C3%96")
        tulos = tulos.replace("å", "%C3%A5")
        tulos = tulos.replace("Å", "%C3%85")

        return tulos

    def muodosta_url(self, mista, mihin, lahtoaika=None, saapumisaika=None):
        """Palauttaa url-osoitteen, jonka avulla voidaan suorittaa hakuehtojen
           mukainen haku VR:än verkkokaupasta

           lahto- ja saapumisajasta erotellaan päivämäärä ja minuutit, jonka jälkeen
           kaikki parametrit asetetaan paikoilleen url:än muodostavaan merkkijonoon
           ja palautetaan se.
        """

        bad_chars = 'äÄöÖåÅ'
        if any((bad_char in mista) for bad_char in bad_chars):
            mista = self.korjaa_aakkoset(mista)
        if any((bad_char in mihin) for bad_char in bad_chars):
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

    def selvita_hinnat(self, hinnat):
        """Palauttaa listan hinnoista

        VR tarjoaa kolmenlaisia lippuja: Tavallisia (Eko), Ennakko ja Joustava lippuja.
        Näiden lippujen hinnat sijoitetaan palautettavaan listaan seuraavasti:
        [Ennakkolippu, Ekolippu, Joustavalippu]. Mikäli jotakin lippuluokkaa ei ole
        haettuun yhteyteen saatavilla, on lippuluokan hinnan indeksissä arvo None
        """
        try:
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
                        teksti = hinta.text_content().replace(u"€", "")
                        teksti = ' '.join(teksti.split())
                        teksti = teksti.replace(",", ".")
                        lista_hinnoista.append(teksti)
                        continue
                else:
                    lista_hinnoista.append(None)

            if len(lista_hinnoista) < 3:
                lista_hinnoista.append(None)

            return lista_hinnoista
        except:
            return ["Hintojen haussa tapahtui virhe!"]

    def hae_vaihtojen_tiedot(self, vaihdot, annettu_aika):
        """Palauttaa listan matkan yhteyksistä, joista jokaisen tiedot on omassa
           dictionaryssaan.

        Luodaan lista yhteyksien tietojen säilömistä varten, jonka jälkeen muodostetaan
        jokaisesta yhteydestä oma dictionary rakenne, joka sisältää tiedot: lähtöpaikka,
        saapumispaikka, lahtoaika, saapumisaika, junan tunnus, junan tyyppi ja junassa
        olevat palvelut.
        """

        try:
            lista_vaihdoista = []
            for vaihto in vaihdot:
                vaihdon_tiedot = {}
                laika = vaihto[1][0].text_content()
                vaihdon_tiedot['lahtoaika'] = laika
                lpaikka = vaihto[1][1].text_content()
                vaihdon_tiedot['mista'] = lpaikka
                saika = vaihto[2][0].text_content()
                vaihdon_tiedot['saapumisaika'] = saika
                spaikka = vaihto[2][1].text_content()
                vaihdon_tiedot['mihin'] = spaikka
                juna_ruma = " ".join(vaihto[3].text_content())
                juna = juna_ruma.replace(" ", "").split()
                vaihdon_tiedot['tunnus'] = juna[1]
                if len(juna) > 2:
                    vaihdon_tiedot['tunnus'] = vaihdon_tiedot['tunnus'] + " " + juna[2]
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
        except:
            return "Vaihtojen haussa tapahtui virhe"

        return lista_vaihdoista

    def hae_matka(self, mista, mihin, lahtoaika=None, saapumisaika=None):
        """Palauttaa listan dictionaryista, jotka sisältävät matkoihin liittyvän tiedon tai
           listan siitä, mitkä hakuehdot aiheuttivat virheen tai None arvon, mikäli hakueh-
           doilla ei löytnyt matkoja.

        Avataan hakuehtojen mukaisen url-osoitteen takaa löytyvä HTML-sivu
        käsiteltäväksi, josta sitten raaputetaan kaikki tarpeellinen tieto
        dictionary rakenteeseen, joka palautetaan.
        """

        avaaja = urllib2.build_opener(urllib2.HTTPCookieProcessor())

        urli = self.muodosta_url(mista, mihin, lahtoaika, saapumisaika)
        try:
            root = html.parse(avaaja.open(urli))
            virheet = self.voidaanko_jatkaa(root, lahtoaika, saapumisaika)
        except:
            return{"virhe": "Palvelu ei saatavilla"}

        if virheet[0] == "True":
            rows = root.xpath("//table[@id='buyTrip_1']/tbody")
            lista_yhteyksista = []
            paikat = root.xpath("//h2[@class='tripheading']")[0].text_content()
            paikat = paikat.replace(" ", "").split()
            lahtee = paikat[0][:-1]
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


def main():
    """
    Mainia käytetään vain toimivuuden testaamiseen. Haku voidaan suorittaa joko valmiilla ehdoilla
    tai hakuehdot voidaan syöttää itse käsin.
    """

    import webbrowser
    import pprint

    screipperi = VRScraper()
    print "Tahdotko itse syottaa hakuehdot? (Y/N) Alennusluokkaa testataksesi, valitse A"
    testataanko = raw_input(': ')
    if testataanko == "Y":

        mista = raw_input('Mista lahdet? >>>')
        mihin = raw_input('Minne menet? >>>')
        aika = raw_input('saapumis- vai lahtoaika? (S/L): ')
        if aika == "S":
            saapumisaika = raw_input('Anna aika muodossa YYYY-MM-DD HH:MM >>>')
            tiedot = screipperi.hae_matka(mista, mihin, None, saapumisaika)
            #webbrowser.open_new(screipperi.muodosta_url(mista, mihin, None, saapumisaika))
            pprint.pprint(tiedot)
        if aika == "L":
            lahtoaika = raw_input('Anna aika muodossa YYYY-MM-DD HH:MM >>>')
            tiedot = screipperi.hae_matka(mista, mihin, lahtoaika, None)
            #webbrowser.open_new(screipperi.muodosta_url(mista, mihin, lahtoaika, None))
            pprint.pprint(tiedot)
    if testataanko == "N":
        tiedot = screipperi.hae_matka("Jyväskylä", "Ähtäri", None, "2013-06-05 15:50",)
        pprint.pprint(tiedot)
    if testataanko == "A":
        print ("0 = Aikuinen, 1 = Lapsi, 2 = Opiskelija, 3 = Nuoriso, 4 = Eläkeläinen 5 = Varusmies, 6 = Lehdistö, 7 = Siviilipalvelusmies")
        alennus = raw_input('Mihin alennusluokkaan kuulut? >>>')
        url_testi = screipperi.ostosivun_url_muodostaja(screipperi.muodosta_url("Jyväskylä", "Ähtäri", None, "2013-06-05 15:50"), alennus)
        webbrowser.open_new(url_testi)

if __name__ == "__main__":
    main()

# -*- coding:utf-8 -*-
'''

Created on 6.4.2013

Scraper, jolla screipataan matkatiedot henkilöautolla matkustaessa. Haetaan siis
tietty reitti ja ilmoitetaan sen kilometrimäärä sekä aika.
Tässä kannattaa käyttää dictionaryja

@author: Peter R

Paluuarvot: lähtöaika, paluuaika, matkan pituus, linkki google mapsiin

HUOM. huomasin, että jos reitin lähtöpaikka ja määränpää eivät ole
täysin oikein kirjoitettu, niin tämä saattaa lisätä pari kilometriä lisää
reitin pituuteen
'''

from lxml import html
import urllib
import datetime
# import json  käytä tätä, jos meinaat tehdä googlen API:lla


class AutoScraper():
    '''
        Scraper-luokka, jolla haetaan tietyn reitin tiedot henkilöautolla mentäessä
    '''

    def __init__(self):
        ''' Konstruktori '''
        pass

    def hae_matka(self, mista, mihin, lahtoaika=None, saapumisaika=None):
        '''
            Haetaan matkan tiedot henkilöautolle google mapsin avulla.
            lahto- ja saapumisaika tulee merkkijonona muodossa "YYYY-MM-DD HH:MM"
            Matkan kesto palautetaan muodossa "HH:MM"
        '''


        # Luodaan url
        url = self.luo_url(mista, mihin)

        site = urllib.urlopen(url)

        # Haetaan html-tiedosto, luodaan lxml-olio. Funktio itse palauttaa
        # poikkeuksen, jos kaikki ei mene putkeen
        root_matka = html.parse(site)

        # Tarkistetaan onnistuiko googlemaps löytämään reitin annetuilla
        # tiedoilla. Jos ei löytynyt, mutta ehdotuksia annettiin, niin
        # käytetään ehdotuksia hyväksi. Jos ehdotuksia on vain yksi kappale
        # niin haetaan reitin tiedot uudestaan kyseisellä ehdotuksella.
        # Jos ehdotuksia on useampi, niin palautetaan nämä virhe-ilmoituksen
        # kanssa.

        error = root_matka.xpath("//div[@class='dir_warnbox_content']/img/@src")

        # Jos ehdotuksia löytyi
        if (len(error) > 0):

            uudet_tiedot = root_matka.xpath("//td[@class='ddw-dla']//div[2]")

            # Jos ehdotus koskee lähtöpaikkaa
            if (error[0].find("greenA") > -1):

                # Yritetään muuttaa hakuehtona käytettävä lähtöpaikka
                # ensimmäiseksi annetuksi hakuehdoksi. Jos tämä ei
                # onnistu, niin palautetaan virhe.
                try:
                    mista = uudet_tiedot[0].text_content().split()[0]
                except Exception:
                    return {
                                "virhe": "mista"
                                }
                # Jos ehdotuksia on useampi, niin palautetaan nämä virhe-
                # ilmoituksen kera
                if (len(uudet_tiedot) > 1):

                    ehdotukset = []

                    for i in uudet_tiedot:
                        ehdotus = ""

                        lista = i.text_content().split()

                        # Jos ehdotus ei ole tarpeeksi pitkä
                        if (len(lista) > 2):
                            for j in range(2, len(lista)):
                                ehdotus = ehdotus + lista[j]
                        else:
                            ehdotus = lista[0] + lista[1]

                        ehdotukset.append(ehdotus)

                        return {
                                "virhe": "mista",
                                "ehdotukset": ehdotukset
                                }

            # Jos ehdotus koskee määränpäätä
            if (error[0].find("greenB") > -1):

                # Yritetään muuttaa hakuehtona käytettävä määränpää
                # ensimmäiseksi annetuksi hakuehdoksi. Jos tämä ei
                # onnistu, niin palautetaan virhe.
                try:
                    mihin = uudet_tiedot[0].text_content().split()[0]
                except Exception:
                    return {
                                "virhe": "mihin"
                                }

                # Jos ehdotuksia on useampi, niin palautetaan nämä virhe-
                # ilmoituksen kera
                if (len(uudet_tiedot) > 1):

                    ehdotukset = []

                    # käydään kaikki ehdotukset läpi ja syötetään ne taulukkoon
                    # siten, että poimitaan ehdotuksen osoiteriviltä paikkakunta
                    for i in uudet_tiedot:

                        ehdotus = ""

                        lista = i.text_content().split()

                        # Jos ehdotus ei ole tarpeeksi pitkä
                        if (len(lista) > 2):
                            for j in range(2, len(lista)):
                                ehdotus = ehdotus + lista[j]
                        else:
                            ehdotus = lista[0] + lista[1]

                        ehdotukset.append(ehdotus)

                    return {
                            "virhe": "mihin",
                            "ehdotukset": ehdotukset
                            }

        # Luodaan url uudestaan päivitetyillä tiedoilla
        url = self.luo_url(mista, mihin)
        site = urllib.urlopen(url)

        # Haetaan html-tiedosto, luodaan lxml-olio. Funktio itse palauttaa
        # poikkeuksen, jos kaikki ei mene putkeen
        root_matka = html.parse(site)

        # Screipataan tiedot
        reitti = root_matka.xpath("//ol[@id='dir_altroutes_body']//li[1]//div" +
                                  "//div[1]//span")


        # Erotellaan kilometrimäärä haetusta merkkijonosta ja muutetaan pilkku
        # pisteeksi. Tässä tarkistetaan myös, että onnistuiko haku
        # oikeanlaisella tavalla
        try:
            # Jos haettu kilometrimäärä on vähintään tuhat, niin otetaan
            # huomioon tuhansien ja satojen väliin jäävä välilyönti
            if (len(reitti[0].text_content()) > 7):
                matkan_pituus = float(reitti[0].text_content().split()[0] +
                    reitti[0].text_content().split()[1].replace(",", "."))
            else:
                matkan_pituus = float(reitti[0].text_content().split()[0].
                                  replace(",", "."))
        except Exception:
            # Ei löytynyt yhteyksiä
            return { "virhe": "eitietoa"}

        # Tutkitaan, onko matkan kesto vain minuutteja (alle tunti)
        if (len(reitti[1].text_content().split()) < 3):
            matkan_kesto = "00:" + reitti[1].text_content().split()[0]
        else:
            matkan_kesto = (reitti[1].text_content().split()[0] + ":" +
                reitti[1].text_content().split()[2])

        # Muokataan merkkijono sovittuun formaattiin eli muotoon HH:MM
        if (len(matkan_kesto.split(':')[0]) < 2):
            matkan_kesto = "0" + matkan_kesto

        if (len(matkan_kesto.split(':')[1]) < 2):
            matkan_kesto = matkan_kesto[0:2] + ":0" + matkan_kesto[3]

        # Screipataan myös lähtö- ja määräpaikka tietojen palautusta varten
        paikat_mista = root_matka.xpath("//div[@oi='wi0']/table/tbody/tr/" +
                                        "td[@class='ddw-addr']/div/div")

        paikat_mihin = root_matka.xpath("//div[@oi='wi1']/table/tbody/tr/" +
                                        "td[@class='ddw-addr']/div/div")

        # Jos haetun reitin lähtö- ja määräpaikka ovat jonkin yrityksen tms.
        # osoitteet, niin haetaan osoitetiedoista oikea paikkakunta

        # Lähtöpaikalle:
        if (len(paikat_mista) > 1):

            mista = ""

            # Luodaan lista, joka sisältää kaikki merkkijonot screipatun listan
            # viimeiseltä riviltä
            lista = paikat_mista[1].text_content().split()

            for i in range(2, len(lista)):
                mista = mista + lista[i]

        else:
            mista = paikat_mista[0].text_content()

        # Määränpäälle:
        if (len(paikat_mihin) > 1):

            mihin = ""
            # Luodaan lista, joka sisältää kaikki merkkijonot screipatun listan
            # viimeiseltä riviltä
            lista = paikat_mihin[1].text_content().split()

            for i in range(2, len(lista)):
                mihin = mihin + lista[i]

        else:
            mihin = paikat_mihin[0].text_content()


        # Palautettavat tiedot reitistä
        matkan_tiedot = {"mista": mista, "mihin": mihin,
                         "kesto": matkan_kesto, "matkanpituus": matkan_pituus,
                         "url": url}

        # Palautetaan tiedot
        return matkan_tiedot

    def luo_url(self, mista, mihin):
        ''' Luodaan url, josta haetaan tiedot. Tämän tarkoituksena on muokata
            ääkköset oikeaan muotoon
        
        '''

        # Dictionary, johon laitetaan lahtopaikka ja saapumispaikka
        params = {"saddr": mista, "daddr": mihin}

        # Luodaan url
        url_matka = "http://maps.google.fi/maps?" + urllib.urlencode(params)

        # Palautetaan
        return url_matka


# Testataan toimiiko luokka
def main():
    ''' Pääfunktio alkaa tästä. Tämä on AutoScraper-luokan testausta '''

    # Muuttujia
    lahtopaikka = "Ivalooo"
    saapumispaikka = "Jyväsky"
    lahtoaika = datetime.datetime(2013, 4, 16, 12, 20)  # klo 12:20

    auto_scraper = AutoScraper()

    tiedot = auto_scraper.hae_matka(lahtopaikka, saapumispaikka, lahtoaika,
        0)

    # Tulostetaan tulokset
    try:
        for rivi in tiedot.iteritems():
            print rivi
    except Exception:
        print "Ei tietoja palautettavaksi"


if __name__ == "__main__":
    main()

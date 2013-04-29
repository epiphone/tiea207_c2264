# -*- coding:utf-8 -*-
'''

Created on 6.4.2013

Scraper, jolla screipataan matkatiedot henkilöautolla matkustaessa. Haetaan siis
tietty reitti ja ilmoitetaan sen kilometrimäärä sekä aika.
Tässä kannattaa käyttää dictionaryja

@author: Peter R

Paluuarvot: lähtöaika, paluuaika, matkan pituus, matkan kesto, linkki google
mapsiin

Tämä käyttää nyt Google Distance Matrix APIa
'''

import urllib
import datetime
import json


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


        # Haetaan tiedot dictionaryyn
        matkan_tiedot = json.load(site)

        # Tarkistetaan tapahtuiko virhe: jos tapahtui, niin palautetaan --------
        # virhetta kuvaileva koodi.

        # Jos syötteessä on virhe (esim. tyhjä syöte jommassa kummassa, jne)
        if (matkan_tiedot["status"] == "INVALID_REQUEST"):
            return { "virhe": "INVALIDI_PYYNTO"}


        # Jos lähtöpaikan tai määränpään tietoja ei löydy, niin palautetaan
        # virhe "mista_ja_mihin"
        if (matkan_tiedot["origin_addresses"][0] == "" and
            matkan_tiedot["destination_addresses"][0] == ""):
            return { "virhe": "mista_ja_mihin"}

        # Jos lahtopaikan tietoja ei löydy, niin palautetaan virhe: "mista"
        if (matkan_tiedot["origin_addresses"][0] == ""):
            return { "virhe": "mista"}

        # Jos määränpään tietoja ei löydy, niin palautetaan virhe: "mihin"
        if (matkan_tiedot["destination_addresses"][0] == ""):
            return { "virhe": "mihin"}

        # En tiedä tarvitaanko tätä
        # if (matkan_tiedot["rows"][0]["elements"][0]["status"] == "NOT_FOUND"):
            # return { "virhe": "EI_LOYTYNYT"}

        if (matkan_tiedot["rows"][0]["elements"][0]["status"] ==
            "ZERO_RESULTS"):
            return { "virhe": "EI_REITTIA"}

        if (matkan_tiedot["rows"][0]["elements"][0]["status"] ==
            "OVER_QUERY_LIMIT"):
            return { "virhe": "LIIKAA_KYSELYITA"}

        if (matkan_tiedot["rows"][0]["elements"][0]["status"] ==
            "REQUEST_DENIED"):
            return { "virhe": "EI_KAYTTO-OIKEUTTA"}

        if (matkan_tiedot["rows"][0]["elements"][0]["status"] ==
            "UNKNOWN_ERROR"):
            return { "virhe": "SERVER_ERROR"}

        # ----------------------------------------------------------------------

        # Jos status=OK, niin palautetaan haetut tiedot
        if (matkan_tiedot["rows"][0]["elements"][0]["status"] == "OK"):

            pituus = matkan_tiedot["rows"][0]["elements"][0]["distance"]["text"]
            kesto = matkan_tiedot["rows"][0]["elements"][0]["duration"]["text"]

            # Erotellaan kilometrimäärä haetusta merkkijonosta ja muutetaan
            # pilkku pisteeksi. Jos haettu kilometrimäärä on vähintään tuhat,
            # niin otetaan huomioon tuhansien ja satojen väliin jäävä välilyönti
            if (len(pituus) > 7):
                matkan_pituus = float(pituus.split()[0] +
                    pituus.split()[1].replace(",", "."))
            else:
                matkan_pituus = float(pituus.split()[0].
                                  replace(",", "."))

            # Tutkitaan, onko matkan kesto vain minuutteja (alle tunti)
            if (len(kesto.split()) < 3):
                matkan_kesto = "00:" + kesto.split()[0]
            else:
                matkan_kesto = (kesto.split()[0] + ":" +
                    kesto.split()[2])

            # Muokataan merkkijono sovittuun formaattiin eli muotoon HH:MM
            if (len(matkan_kesto.split(':')[0]) < 2):
                matkan_kesto = "0" + matkan_kesto

            if (len(matkan_kesto.split(':')[1]) < 2):
                matkan_kesto = matkan_kesto[0:2] + ":0" + matkan_kesto[3]

            # Poimitaan varsinainen, haun kautta saatu lähtö- sekä
            # saapumispaikka.
            mista = matkan_tiedot["origin_addresses"][0].split(',')[0]
            mihin = matkan_tiedot["destination_addresses"][0].split(',')[0]

            # Palautettava url on googlemapsiin
            params = {"saddr": mista, "daddr": mihin, "hl": "fi"}

            # Luodaan url
            url_palautettava = ("http://maps.google.fi/maps?"
                     + urllib.urlencode(params))

            # Palautetaan tiedot reitistä
            return {"mista": mista, "mihin": mihin,
                         "kesto": matkan_kesto, "matkanpituus": matkan_pituus,
                         "url": url_palautettava}

        # Palautetaan virhe, jos ei palauteta mitään muuta. Eli tässä
        # tapauksessa ei saatu mitään irti kyseisestä urlista.
        return {"virhe": "EI_YHTEYTTA_SIVULLE"}

    def luo_url(self, mista, mihin):
        ''' Luodaan url, josta haetaan tiedot. Tämän tarkoituksena on muokata
            ääkköset oikeaan muotoon. Palauttaa urlin Google Directions APIa
            varten.
        '''

        # Dictionary, johon laitetaan lahtopaikka, saapumispaikka, kieli ja
        # sensor
        params = {"origins": mista, "destinations": mihin, "sensor": "false",
                  "language": "fi-FI"}

        # Luodaan url
        url_matka = ("http://maps.googleapis.com/maps/api/distancematrix/json?"
                     + urllib.urlencode(params))

        # Palautetaan valmis url
        return url_matka

# Testataan toimiiko luokka
def main():
    ''' Pääfunktio alkaa tästä. Tämä on AutoScraper-luokan testausta '''

    # Muuttujia
    lahtopaikka = ""
    saapumispaikka = "suonenjoki (suonenjoki)"
    lahtoaika = datetime.datetime(2013, 4, 16, 12, 20)  # klo 12:20

    auto_scraper = AutoScraper()

    tiedot = auto_scraper.hae_matka(lahtopaikka, saapumispaikka, lahtoaika,
        0)

    # Tulostetaan tulokset
    for rivi in tiedot.iteritems():
        print rivi

if __name__ == "__main__":
    main()

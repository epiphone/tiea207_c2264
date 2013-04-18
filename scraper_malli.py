# -*-coding:utf-8-*-
# Pohja skreipperin toteuttamiselle.


class Scraper:
    def laske_alennus(hinnat, alennusluokka):
        """HUOM! Tämä vain VR:lle.

        - hinnat on lista kolmesta eri hinnasta (mahdollisesti None)
        - alennusluokka on kokonaisluku
        - palautetaan listana alennusluokan mukaiset hinnat.

        Jos alennuksia saa vain peruslipuista, voi hinnat-parametrin korvata
        liukulukutyyppisellä hinta-parametrilla, samoin myös paluuarvossa.
        """

        # TODO toteutus tähän

        return None

    def hae_matka(self, mista, mihin, lahtoaika=None, saapumisaika=None):
        """Palauttaa valitulle matkalle löytyneet yhteydet.

        - Lähtö- ja saapumisajat ovat merkkijonoja muodossa "YYYY-mm-dd HH:MM".
        - lahtoaika- ja saapumisaika-parametreista vain toinen on käytössä.
        - alennusluokan ei tulisi vaikuttaa siihen mitä sivua skreipataan;
          haetaan lippujen hinnat aina tarjoajan sivulta oletusalennusluokalla,
          ja muokataan hintoja palvelimella annetun alennusluokan mukaan
          --> vältytään turhalta skreippaamiselta. Alennusehdot pitää selvittää
          tarjoajan sivuilta.
        - ...tosin matkahuollolta voidaan joutua skreippaamaan kaikki hinnat
          mystisten hintasääntöjen takia.
        """

        # Tähän skreippaukset.

        # Esimerkki paluuarvosta, kun skreippaaminen onnistuu ja yhteyksiä löytyy.
        # AINAKIN nämä tiedot tulisi löytyä:
        return [
            # 1. yhteys
            {"lahtoaika": "16:59",
            "saapumisaika": "22:22",
            "mista": "jyväskylä",
            "mihin": "helsinki",
            "kesto": "05:30",
            "hinta": [28.84, 33.93, None],  # VR:llä on eri hintaluokkia: Ennakko, Perus, Kampanja. Matkahuollolla ei tarvitse palauttaa ku yks arvo.
            "vaihdot": [
                # 1. vaihtoyhteys
                {"palvelut": ["Tupakointitila", "Poreamme"],
                "lahtoaika": "16:59",
                "saapumisaika": "20:00",
                "mista": "jyväskylä",
                "mihin": "tampere",
                "tyyppi": "Pikajuna",      # Pikajuna/Pendolino/InterCity/Lähijuna/muu? Matkahuollolla pika/perus/muu?
                "tunnus": "Pikajuna 123"}, # VR:llä junan nimi, matkahuollolla esim. "pika Rovaniemi - Helsinki"

                # 2. vaihtoyhteys
                {"lahtoaika": "20:10",
                "saapumisaika": "22:22",
                "mista": "tampere",
                "mihin": "helsinki",
                "tyyppi": "Pendolino",
                "tunnus": "Pendolino 666"}
            ],
            "url": "http://linkki-ostosivulle.fi"
            },
            # 2. yhteys jne...
            {"lahtoaika": "..."}
        ]

        """
        Esimerkin 1. yhteys on siis sellainen yhteys, joka lähtee 16:59,
        saapuu 22:22, ja jossa vaihdetaan junaa ja odotellaan 10min Tampereella
        """

        # Jos skreippaaminen epäonnistuu siinä vaiheessa kun html:ää haetaan,
        # (html.load(url)) laukeaa poikkeus joten sitä ei tarvitse erikseen käsitellä.

        # Jos sivu latautuu, mutta annettua lähtö- tai saapumispaikkaa ei löydy,
        # tai paikka tulee tarkentaa, voitaisiin palauttaa esim. tällainen arvo:

        return {
            "virhe": "mista",  # mista/mihin/mitä muita virheitä voi tulla?
            "ehdotukset": ["jyväskylä", "syväskylä"]  # antaako VR edes ehdotuksia?
        }

        # Jos skreippaaminen onnistuu mutta yhteyksiä ei löydy,
        # palautetaan tyhjiöarvo

        return None

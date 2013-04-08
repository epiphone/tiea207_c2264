# -*-coding:utf-8-*-
# Pohja skreipperin toteuttamiselle.

class Scraper:
    def __init__(self):
        """Konstruktori"""
        pass

    def hae_matka(self, mista, mihin, lahtoaika=None, saapumisaika=None,
        max_tulokset=3, alennusluokka=0):
        """Palauttaa valitulle matkalle löytyneet yhteydet.

        - Lähtö- ja saapumisajat ovat datetime-olioita.
        - lahtoaika- ja saapumisaika-parametreista vain toinen on käytössä.
        - max_tulokset määrittää montako tulosta palautetaan; palautetaan
          aina x kappaletta yhteyksiä, jotka ovat lähinnä annettua aikaehtoa.
        - alennusluokan ei tulisi vaikuttaa siihen mitä sivua skreipataan;
          haetaan lippujen hinnat aina tarjoajan sivulta oletusalennusluokalla,
          ja muokataan hintoja palvelimella annetun alennusluokan mukaan
          --> vältytään turhalta skreippaamiselta. Alennusehdot pitää selvittää
          tarjoajan sivuilta.
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
                {"lahtoaika": "16:59",
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
            "ehdotukset": ["jyväskylä", "syväskylä"]
        }

        # Jos skreippaaminen onnistuu mutta yhteyksiä ei löydy,
        # palautetaan tyhjiöarvo

        return None
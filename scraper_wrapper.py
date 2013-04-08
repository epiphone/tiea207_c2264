# -*-coding:utf-8-*-
# Moduuli käärii eri skreipperit yhteisen rajapinnan alle.

# TODO: Nämä käyttöön kun ovat valmiita:
# import mh_scraper
# import vr_scraper
# import auto_scraper


class VRScraper:
    """Tilapäinen dummy-luokka."""
    def hae_matka(*args, **kwargs):
        return [
            {"lahtoaika": "2013-04-05 16:59",
            "saapumisaika": "2013-04-05 22:22",
            "mista": "jyväskylä",
            "mihin": "helsinki",
            "hinta": [28.84, 33.93, None],
            "vaihdot": [
                {"lahtoaika": "2013-04-05 16:59",
                "saapumisaika": "2013-04-05 20:00",
                "mista": "jyväskylä",
                "mihin": "tampere",
                "tyyppi": "Pikajuna",
                "tunnus": "Pikajuna 123"},
               {"lahtoaika": "2013-04-05 20:10",
                "saapumisaika": "2013-04-05 22:22",
                "mista": "tampere",
                "mihin": "helsinki",
                "tyyppi": "Pendolino",
                "tunnus": "Pendolino 666"}
            ],
            "url": "http://linkki-ostosivulle.fi"
            }
        ]


class MHScraper:
    """Tilapäinen dummy-luokka."""
    def hae_matka(*args, **kwargs):
        return [
            {"lahtoaika": "2013-04-05 16:59",
            "saapumisaika": "2013-04-05 22:22",
            "mista": "jyväskylä",
            "mihin": "helsinki",
            "hinta": [28.84, 33.93, None],
            "vaihdot": [
                {"lahtoaika": "2013-04-05 16:59",
                "saapumisaika": "2013-04-05 20:00",
                "mista": "jyväskylä",
                "mihin": "tampere",
                "tunnus": "Pikavuoro"}],
                "tyyppi": "Pikavuoro Jyväskylä - Helsinki",
               "url": "http://linkki-ostosivulle.fi"
            }
        ]


class AutoScraper:
    """Tilapäinen dummy-luokka."""
    def hae_matka(*args, **kwargs):
        return [
            {"lahtoaika": "2013-04-05 16:59",
            "saapumisaika": "2013-04-05 22:22",
            "km":356,

        ]


def hae_matka(mista=None, mihin=None, lahtoaika=None, saapumisaika=None,
    bussi=True, juna=True, auto=True):
    """Palauttaa valitulle matkalle eri yhteydet."""
    pass  # TODO

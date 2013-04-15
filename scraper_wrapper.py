# -*-coding:utf-8-*-
# Moduuli käärii eri skreipperit yhteisen rajapinnan alle.

# TODO: Nämä käyttöön kun ovat valmiita:
# import mh_scraper
# import vr_scraper
# import auto_scraper
import logging
from thread_helper import do_threaded_work
try:
    from google.appengine.api import memcache
except ImportError:
    logging.info("App Enginen apia ei löydetty")

    class Memcache:
        """dummy-luokka sovelluksen testaamiseksi ilman GAE:a"""
        def __init__(self):
            self.store = {}

        def get(self, key):
            '''Returns requested key'''
            if key in self.store:
                return self.store[key]["value"]
            else:
                return None

        def set(self, key, value, expires=None):
            '''Set value to memcache'''
            self.store[key] = {"value": value, "expires": expires}

        def add(self, key, value, expires=None):
            '''Set value to memcache'''
            self.store[key] = {"value": value, "expires": expires}


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
        return {
            "lahtoaika": "2013-04-05 16:59",
            "saapumisaika": "2013-04-05 22:22",
            "km": 356,
            "url": "http://linkki-kartalle.fi"
        }


class BensaScraper:
    """Tilapäinen dummy-luokka."""
    def hae_hinta(*args, **kwargs):
        return [1.672, 1.721, 1.555]


class ScraperWrapper:
    """Käärii scraperit yhden rajapinnan alle."""

    def __init__(self):
        self.vr_scraper = VRScraper()
        self.mh_scraper = MHScraper()
        self.auto_scraper = AutoScraper()
        self.bensa_scraper = BensaScraper()
        self.scraperit = [self.vr_scraper, self.mh_scraper,
            self.auto_scraper]

    def hae_matka(self, mista=None, mihin=None, lahtoaika=None, saapumisaika=None,
        bussi=True, juna=True, auto=True, alennusluokka=0):
        """Palauttaa valitulle matkalle eri yhteydet."""
        # assert saapumisaika

        def f(scraper):

            if scraper is self.mh_scraper:
                tulos = memcache.get("mh_" + )
            return scraper.hae_matka(mista, mihin, lahtoaika, saapumisaika)
            # TODO: aseta cache

        scraperit = zip(self.scraperit, [juna, bussi, auto])
        scraperit = [s for s, b in scraperit if b]

        results = do_threaded_work(scraperit, f)
        return results


wrapper = ScraperWrapper()

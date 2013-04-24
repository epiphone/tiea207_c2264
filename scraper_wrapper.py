# -*-coding:utf-8-*-
# Moduuli käärii eri skreipperit yhteisen rajapinnan alle.

# TODO: Nämä käyttöön kun ovat valmiita:
import logging
from mh_raaputin.raaputin_alpha import MHScraper
from henkiloauto_scraper.auto_scraper import AutoScraper
from hinta_scraper import hinta_scraper
from vr_scraper.vr_scraper import VRScraper
from thread_helper import do_threaded_work
try:
    from google.appengine.api import memcache
except ImportError:
    logging.info("App Enginen apia ei löydetty")

    class Memcache:
        """Dummy-luokka sovelluksen testaamiseksi ilman GAE:a"""
        def __init__(self):
            self.store = {}

        def get(self, key):
            """Returns requested key"""
            if key in self.store:
                return self.store[key]["value"]
            else:
                return None

        def set(self, key, value, expires=None):
            """Set value to memcache"""
            self.store[key] = {"value": value, "expires": expires}

        def add(self, key, value, expires=None):
            """Set value to memcache"""
            self.store[key] = {"value": value, "expires": expires}
    memcache = Memcache()

# Käytetään näitä hintoja, jos hintojen hakeminen epäonnistuu
HINNAT_BACKUP = [1.638, 1.688, 1.52]


# class MHScraper:
#     """Tilapäinen dummy-luokka."""
#     def hae_matka(*args, **kwargs):
#         return [
#             {"lahtoaika": "2013-04-05 16:59",
#             "saapumisaika": "2013-04-05 22:22",
#             "mista": "jyväskylä",
#             "mihin": "helsinki",
#             "kesto": "04:23",
#             "hinnat": [28.84, 33.93, None],
#             "vaihdot": [
#                 {"lahtoaika": "2013-04-05 16:59",
#                 "saapumisaika": "2013-04-05 20:00",
#                 "mista": "jyväskylä",
#                 "mihin": "tampere",
#                 "tunnus": "Pikavuoro"}],
#                 "tyyppi": "Pikavuoro Jyväskylä - Helsinki",
#                "url": "http://linkki-ostosivulle.fi"
#             }
#         ]


class ScraperWrapper:
    """Käärii scraperit yhden rajapinnan alle."""

    def __init__(self):
        self.vr_scraper = VRScraper()
        self.mh_scraper = MHScraper()
        self.auto_scraper = AutoScraper()
        self.scraperit = [self.vr_scraper, self.mh_scraper,
            self.auto_scraper]

    def hae_matka(self, mista=None, mihin=None, lahtoaika=None, saapumisaika=None,
        bussi=True, juna=True, auto=True, alennusluokka=0):
        """Palauttaa valitulle matkalle eri yhteydet."""
        assert mista and mihin
        assert lahtoaika is not None or saapumisaika is not None

        try:
            mista = mista.encode("utf-8")
            mihin = mihin.encode("utf-8")
        except UnicodeDecodeError:
            pass

        dt = lahtoaika or saapumisaika
        pvm = dt.split()[0]

        def f(scraper):
            """Apufunktio, joka tarkistaa välimuistin ja hakee tarvittaessa
            uuden tuloksen skreipperiltä."""
            # Määritetään skreipperistä riippuva välimuistin avain:
            if scraper is self.mh_scraper:
                tyyppi = "bussi"
                cache_avain = "mh_" + mista + mihin + pvm
            elif scraper is self.vr_scraper:
                # TODO Tälle ei tule paljoa osumia, parempi vaihtoehto?
                tyyppi = "juna"
                cache_avain = "vr_" + mista + mihin + dt
            else:
                tyyppi = "auto"
                cache_avain = "auto_" + mista + mihin

            tulos = memcache.get(cache_avain)
            if tulos is not None:
                logging.info("CACHE HIT, key:" + cache_avain)
                # return tulos, tyyppi
            else:
                try:
                    tulos = scraper.hae_matka(mista, mihin, lahtoaika, saapumisaika)
                    if tulos:
                        if "virhe" in tulos:
                            # TODO Virheiden käsittely
                            return tulos, tyyppi
                        else:
                            # TODO Atm cache-arvo vanhenee
                            memcache.set(cache_avain, tulos, 60 * 60 * 60)
                    else:
                        tulos = {"virhe": "Ei yhteyksiä [%s]"
                            % tyyppi}
                except IOError:
                    tulos = {
                        "virhe": "Sivun avaaminen epäonnistui [%s]" % tyyppi}

            # Jos haetaan automatkaa, lasketaan polttoaineen hinta:
            if tyyppi == "auto" and tulos and "matkanpituus" in tulos:
                hinnat = self.hae_bensan_hinnat()
                pit = tulos["matkanpituus"]
                tulos["hinnat"] = [round(pit * (6.0 / 100.0) * h, 2) for h in hinnat]

            assert tulos is not None  # TODO debug
            return tulos, tyyppi

        # Palautetaan vain halutut matkustusvaihtoehdot:
        matkat = do_threaded_work(self.scraperit, f)
        lokaalit = locals()
        matkat = {tyyppi: matka for matka, tyyppi in matkat if lokaalit[tyyppi]}
        return matkat

    def hae_bensan_hinnat(self):
        """Hakee bensan hinnat hinta_scraper-moduulia käyttäen."""
        hinnat = memcache.get("hinnat")
        if hinnat not in [None, []]:
            # Hinnat löytyivät välimuistista
            logging.info("CACHE HIT, key: hinnat")
            return hinnat

        try:
            hinnat = hinta_scraper.hae_hinta()
            if not hinnat:
                logging.info("Polttoainehintojen skreippaaminen epäonnistui.")
                return HINNAT_BACKUP
        except IOError:
            logging.info("Polttoaine-urlin avaaminen epäonnistui")
            return HINNAT_BACKUP

        memcache.set("hinnat", hinnat, 60 * 60 * 24 * 7)
        return hinnat

# Testaamisen nopeuttamiseksi:
wrapper = ScraperWrapper()

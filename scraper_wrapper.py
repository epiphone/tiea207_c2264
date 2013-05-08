# -*-coding:utf-8-*-
# Moduuli käärii eri skreipperit yhteisen rajapinnan alle.

import logging
from mh_raaputin.raaputin_alpha import MHScraper
from henkiloauto_scraper.auto_scraper import AutoScraper
from hinta_scraper import hinta_scraper
from vr_scraper.vr_scraper import VRScraper
from thread_helper import do_threaded_work
from google.appengine.api import memcache
import json

# Käytetään näitä hintoja, jos hintojen hakeminen epäonnistuu
HINNAT_BACKUP = [1.638, 1.688, 1.52]


class ScraperWrapper:
    """Käärii scraperit yhden rajapinnan alle."""

    def __init__(self):
        self.vr_scraper = VRScraper()
        self.mh_scraper = MHScraper()
        self.auto_scraper = AutoScraper()
        self.scraperit = [self.vr_scraper, self.mh_scraper,
            self.auto_scraper]
        self.paikat = json.load(open("paikat.json", "r"))

    def hae_matka(self, mista=None, mihin=None, lahtoaika=None, saapumisaika=None,
        bussi=True, juna=True, auto=True, alennusluokka=0):
        """Palauttaa valitulle matkalle eri yhteydet."""
        assert mista and mihin
        assert lahtoaika is not None or saapumisaika is not None

        # Selvitetään haettuja paikkoja vastaavat MH:n ja VR:n paikat:
        for k, v in self.paikat.iteritems():
            if k == mista:
                mista_auto = mista
                mista = v
                if isinstance(mihin, list):
                    break
            if k == mihin:
                mihin_auto = mihin
                mihin = v
                if isinstance(mista, list):
                    break

        if not isinstance(mista, list):
            return dict(virhe="mista")
        if not isinstance(mihin, list):
            return dict(virhe="mihin")

        mista_mh, mista_vr = [x.encode("utf-8") for x in mista]
        mihin_mh, mihin_vr = [x.encode("utf-8") for x in mihin]

        dt = lahtoaika or saapumisaika
        pvm = dt.split()[0]

        def f(scraper):
            """Apufunktio, joka tarkistaa välimuistin ja hakee tarvittaessa
            uuden tuloksen skreipperiltä."""
            # Määritetään skreipperistä riippuva välimuistin avain:
            if scraper is self.mh_scraper:
                mista, mihin = mista_mh, mihin_mh
                tyyppi = "bussi"
                cache_avain = "mh_%s_%s_%s" % (mista, mihin, pvm)
            elif scraper is self.vr_scraper:
                # TODO Tälle ei tule paljoa osumia, parempi vaihtoehto?
                mista, mihin = mista_vr, mihin_vr
                tyyppi = "juna"
                cache_avain = "vr_%s_%s_%s" % (mista, mihin, dt)
            else:
                mista, mihin = mista_auto, mihin_auto
                tyyppi = "auto"
                cache_avain = "auto_%s_%s" % (mista, mihin)

            if not mista or not mihin:
                return dict(virhe="ei yhteyksia [%s]" % tyyppi)

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
                            memcache.set(cache_avain, tulos, 60 * 60 * 48)
                    else:
                        tulos = {"virhe": "ei yhteyksiä [%s]"
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
        lok = locals()
        matkat = {tyyppi: matka for matka, tyyppi in matkat if lok[tyyppi]}
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

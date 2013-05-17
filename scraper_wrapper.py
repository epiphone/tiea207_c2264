# -*-coding:utf-8-*-
"""
Moduuli käärii eri skreipperit yhteisen rajapinnan alle.

Aleksi Pekkala
"""

# Scraperit:
from mh_raaputin import MHScraper
from henkiloauto_scraper import AutoScraper
from vr_scraper import VRScraper
from hinta_scraper import hinta_scraper

from math import ceil
from thread_helper import do_threaded_work
import logging
import json
try:
    from google.appengine.api import memcache
except ImportError:
    class DummyMemcache():
        """
        Mahdollistaa moduulin testaamisen ilman App Engineä.
        """
        def set(*args, **kwargs):
            return None

        def get(*args, **kwargs):
            return None

    memcache = DummyMemcache()


# Käytetään näitä, jos hintojen hakeminen epäonnistuu:
HINNAT_BACKUP = [1.638, 1.688, 1.52]


class ScraperWrapper:
    """Käärii scraperit yhden rajapinnan alle."""

    def __init__(self):
        self.vr_scraper = VRScraper()
        self.mh_scraper = MHScraper()
        self.auto_scraper = AutoScraper()
        self.scraperit = [
            self.vr_scraper,
            self.mh_scraper,
            self.auto_scraper]
        paikat = json.load(open("paikat.json", "r"))
        for k, v in paikat.iteritems():
            paikat[k] = [p.encode("utf-8") if p else None for p in v]
        self.paikat = paikat

    def hae_matka(self, mista=None, mihin=None, lahtoaika=None, saapumisaika=None,
            bussi=True, juna=True, auto=True, alennusluokka=0, max_lkm=6,
            polttoaine=0, kulutus=6.5):
        """
        Palauttaa valitulle matkalle löytyneet yhteydet.
        """
        assert type(mista) == type(mihin) == unicode
        assert lahtoaika is not None or saapumisaika is not None  # TODO debug
        logging.info("hae_matka(mista=%s, mihin=%s" % (mista, mihin))

        # Selvitetään haettuja paikkoja vastaavat MH:n, VR:n ja Googlen paikat:
        for k, v in self.paikat.iteritems():
            if k == mista:
                mista = v
                if isinstance(mihin, list):
                    break
            if k == mihin:
                mihin = v
                if isinstance(mista, list):
                    break

        # Jos paikkoja ei löytynyt:
        if not isinstance(mista, list):
            return dict(virhe="mista")
        if not isinstance(mihin, list):
            return dict(virhe="mihin")

        mista_mh, mista_vr, mista_auto = mista
        mihin_mh, mihin_vr, mihin_auto = mihin

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
                return {"virhe": "paikkakunnalla ei ole asemaa"}, tyyppi

            tulos = memcache.get(cache_avain)
            if tulos is not None:
                logging.info("CACHE HIT, key:" + cache_avain)
            else:
                try:
                    tulos = scraper.hae_matka(
                        mista, mihin, lahtoaika, saapumisaika)
                    if tulos:
                        if "virhe" in tulos:
                            # TODO Virheiden käsittely
                            return tulos, tyyppi
                        else:
                            memcache.set(cache_avain, tulos, 60 * 60 * 48)
                    else:
                        tulos = {"virhe": "ei yhteyksiä"}
                except IOError:
                    tulos = {"virhe": "sivun avaaminen epäonnistui"}

            if tyyppi != "auto" and not "virhe" in tulos:
                tulos = self.rajaa_tulokset(tulos, max_lkm, lahtoaika,
                    saapumisaika)

            # Jos haetaan automatkaa, lasketaan polttoaineen hinta:
            if tyyppi == "auto" and tulos and "matkanpituus" in tulos:
                hinta = self.hae_bensan_hinnat()[polttoaine]
                pit = tulos["matkanpituus"]
                tulos["polttoaineen_hinta"] = hinta
                tulos["hinta"] = round(pit * (kulutus / 100.0) * hinta, 2)

            assert tulos is not None  # TODO debug
            return tulos, tyyppi

        # Palautetaan vain halutut matkustusvaihtoehdot:
        matkat = do_threaded_work(self.scraperit, f)
        lok = locals()
        matkat = {tyyppi: matka for matka, tyyppi in matkat if lok[tyyppi]}
        return matkat

    def hae_bensan_hinnat(self):
        """
        Hakee bensan hinnat hinta_scraper-moduulia käyttäen.
        """
        hinnat = memcache.get("hinnat")
        if hinnat not in [None, []]:
            # Hinnat löytyivät välimuistista
            logging.info("CACHE HIT, key: hinnat")
            return hinnat

        try:
            hinnat = hinta_scraper.hae_hinta()
            if not hinnat:
                logging.error("Polttoainehintojen skreippaaminen epäonnistui.")
                return HINNAT_BACKUP
        except IOError:
            logging.error("Polttoaine-urlin avaaminen epäonnistui")
            return HINNAT_BACKUP

        memcache.set("hinnat", hinnat, 60 * 60 * 24 * 7)
        return hinnat

    def rajaa_tulokset(self, tulos, max_lkm, lahtoaika, saapumisaika):
        """
        Rajaa hakutuloksista halutun määrän tuloksia.
        """
        if len(tulos) <= max_lkm:
            return tulos

        if lahtoaika:
            aika = lahtoaika.split()[1]
            attr = "lahtoaika"
        else:
            aika = saapumisaika.split()[1]
            attr = "saapumisaika"

        ret = None

        for i, matka in enumerate(tulos):
            if matka[attr] > aika:
                askeleet_vas = min(int(ceil((max_lkm - 1) / 2.0)), i)
                askeleet_oik = max_lkm - 1 - askeleet_vas
                askeleet_vas += (i + askeleet_oik + 1) - len(tulos)
                ret = tulos[i - askeleet_vas:i + askeleet_oik + 1]

        if not ret:
            ret = tulos[-max_lkm:]

        assert len(ret) == min(max_lkm, len(tulos))  # TODO debug
        return ret


# Testaamisen nopeuttamiseksi:
wrapper = ScraperWrapper()
tdt = "2013-05-22 22:22"
oulu = u"oulu"
tampere = u"tampere"


def test(aika="15:00"):
    matkat = wrapper.hae_matka(oulu, tampere, tdt)
    return matkat, wrapper.rajaa_tulokset(matkat["bussi"], 6, "asd " + aika, None)

# -*-coding:utf-8-*-
"""
Joukkoliikenteen hintavertailusovellus.


"""

import web
from scraper_wrapper import ScraperWrapper
from datetime import datetime, timedelta
import time
import logging


### GLOBAALIT & ASETUKSET ###


LOMAKE_PVM_FORMAATTI = "%d.%m.%Y %H:%M"
SOVELLUS_PVM_FORMAATTI = "%Y-%m-%d %H:%M"
JS_PVM_FORMAATTI = "%Y-%m-%dT%H:%M"

# (x, y) missä x on polttoaine (95, 98, diesel) ja y on keskikulutus (l/100km)
KULUTUSLUOKAT = [(0, 4.5), (0, 6.5), (0, 8.5), (1, 4.5), (1, 6.5), (1, 8.5),
    (2, 3.7), (2, 5.7), (2, 7.7)]
ALENNUSLUOKAT = ["Aikuinen", "Lapsi (4-11v)", "Nuori (12-16v)", "Opiskelija",
    "Varusmies", "Siviilipalvelusmies", "Eläkeläinen", "Lehdistö"]
# Reititykset:
urls = (
    "/", "Index",
    "/haku", "Haku"
)

scraper = ScraperWrapper()
render = web.template.render("templates/", base="base")


### SIVUT ###


class Index:
    def GET(self):
        """Pääsivu, joka sisältää hakuikkunan."""
        return render.index()


class Haku:
    def GET(self):
        """Sivu, joka esittää haun tulokset."""
        # Mitataan matkaselvityksen kesto:  # TODO debug
        t = time.time()

        # Poimitaan parametrit URLista:
        inp = web.input(h=None, min=None, pvm=None, juna=False, bussi=False,
            auto=False, tyyppi="saapumisaika", vis=False, ale=0, kulutus=0)
        mista, mihin = inp.mista, inp.mihin
        h, mins, pvm = inp.h, inp.min, inp.pvm
        juna, bussi, auto = inp.juna, inp.bussi, inp.auto
        ale, kulutusluokka = int(inp.ale), int(inp.kulutus)
        aikatyyppi = inp.tyyppi
        visualisaatio = True if inp.vis else False

        # Validoitaan parametrit:
        if not mista or not mihin:
            return "Lähtö- ja saapumispaikka tulee määrittää."  # TODO
        if not ale in range(7):
            return "Virheellinen alennusluokka."  # TODO
        if not kulutusluokka in range(9):
            return "Virheellinen kulutusluokka."  # TODO
        if any(x is None or x == "" for x in [h, mins, pvm]):
            return "Aika ja pvm tulee määrittää."  # TODO

        polttoaine, kulutus = KULUTUSLUOKAT[int(kulutusluokka)]

        # Haettiinko saapumis- vai lähtöajan perusteella:
        aika = formatoi_aika(h, mins, pvm)
        if aikatyyppi == "saapumisaika":
            saika, laika = aika, None
        else:
            saika, laika = None, aika

        params = dict(
            mista=mista.lower(),
            mihin=mihin.lower(),
            lahtoaika=laika,
            saapumisaika=saika,
            bussi=bussi,
            juna=juna,
            auto=auto,
            alennusluokka=ale,
            polttoaine=polttoaine,
            kulutus=kulutus)

        logging.info(str(params))  # TODO debug
        matkat = scraper.hae_matka(**params)
        taydenna_matkatiedot(matkat, pvm, laika, saika)

        # TODO turhat parametrit pois
        t = str(round(time.time() - t, 2))
        if visualisaatio:
            dt = laika or saika
            dt = dt.split()[0] + "T" + dt.split()[1]
            return render.results_vis(matkat=matkat, params=params, t=t, dt=dt,
                pvm=pvm, h=h, mins=mins, aikatyyppi=aikatyyppi,
                aleluokka=ale, aleluokat=ALENNUSLUOKAT)
        return render.results(matkat=matkat, params=params, t=t)


### APUFUNKTIOT & TEMPLATEFUNKTIOT ###


def kesto_tunneiksi(kesto):
    """
    Palauttaa kestomerkkijonon liukulukuna.

    >>> kesto_tunneiksi("05:30")
    5.5
    """
    tunnit, minuutit = kesto.split(":")
    return round(float(tunnit) + float(minuutit) / 60, 2)


def taydenna_matkatiedot(matkat, pvm, lahtoaika, saapumisaika):
    """
    Lisää skreipattuihin matkatietoihin lisätietoja.

    mm. lasketaan kestomerkkijonosta tunnit, ja lisätään javascriptin
    Date-luokan ymmärtämiä aikamerkkijonoja.
    """
    aika_js = lambda x: "T".join(x.split())

    if "auto" in matkat and not "virhe" in matkat["auto"]:
        auto = matkat["auto"]
        auto["luokka"] = "auto"

        auto["tunnit"] = kesto_tunneiksi(auto["kesto"])
        if lahtoaika:
            auto["js_aika"] = aika_js(lahtoaika)
        else:
            dt = datetime.strptime(saapumisaika, SOVELLUS_PVM_FORMAATTI)
            dt -= timedelta(hours=auto["tunnit"])
            auto["js_aika"] = dt.strftime(JS_PVM_FORMAATTI)

    for luokka in ["juna", "bussi"]:
        if not luokka in matkat or "virhe" in matkat[luokka]:
            continue

        for matka in matkat[luokka]:
            matka["luokka"] = luokka

            # TODO tulevaisuudessa vain yksi hinta
            for hinta in matka["hinnat"] + [999.9]:
                if hinta:
                    matka["hinta"] = hinta
                    break

            pvm_str = " ".join([pvm, matka["lahtoaika"]])
            dt = datetime.strptime(pvm_str, LOMAKE_PVM_FORMAATTI)
            matka["js_aika"] = dt.strftime(JS_PVM_FORMAATTI)
            matka["vaihdot_lkm"] = len(matka["vaihdot"]) - 1
            matka["tunnit"] = kesto_tunneiksi(matka["kesto"])
            matka["tyyppi"] = " - ".join(v["tunnus"] for v in matka["vaihdot"])


def formatoi_aika(h, mins, pvm):
    """
    Formatoi parametrien tunnit, minuutit ja päivämäärän
    muotoon YYYY-mm-dd HH:MM

    >>> formatoi_aika(4, 56, "1.12.2012")
    '2012-12-01 04:56'
    """
    pvm_str = "%s %s:%s" % (pvm, h, mins)
    dt = datetime.strptime(pvm_str, LOMAKE_PVM_FORMAATTI)
    return datetime.strftime(dt, SOVELLUS_PVM_FORMAATTI)


### INIT ###


app = web.application(urls, globals(), autoreload=False)
web.config.debug = True  # TODO
gae_app = app.gaerun()  # Tämä takaa App Engine-yhteensopivuuden

if __name__ == "__main__":
    app.run()

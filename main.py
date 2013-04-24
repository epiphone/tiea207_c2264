# -*-coding:utf-8-*-
# Joukkoliikenteen hintavertailusovellus


import web
from scraper_wrapper import ScraperWrapper
from datetime import datetime, timedelta
import re
import logging
import time



### TEMPLATE-APUFUNKTIOT ###

# TODO

### GLOBAALIT & ASETUKSET ###


LOMAKE_PVM_FORMAATTI = "%d.%m.%Y %H:%M"
SOVELLUS_PVM_FORMAATTI = "%Y-%m-%d %H:%M"

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
        inp = web.input(h=None, min=None, pvm=None, ale="0", juna=False,
            bussi=False, auto=False, aikatyyppi="saapumisaika")
        mista, mihin = inp.mista, inp.mihin
        h, mins, pvm, ale = inp.h, inp.min, inp.pvm, inp.ale
        juna, bussi, auto = inp.juna, inp.bussi, inp.auto
        aikatyyppi = inp.aikatyyppi

        # Validoitaan parametrit:
        if not mista or not mihin:
            return "Lähtö- ja saapumispaikka tulee määrittää."  # TODO
        if not int(ale) in range(7):
            return "Virheellinen alennusluokka."  # TODO
        if any(x is None or x == "" for x in [h, mins, pvm]):
            return "Aika ja pvm tulee määrittää."  # TODO

        # Haettiinko saapumis- vai lähtöajan perusteella:
        pvm = formatoi_aika(h, mins, pvm)
        if aikatyyppi == "saapumisaika":
            saika = pvm
            laika = None
        else:
            saika = None
            laika = pvm

        params = dict(mista=mista, mihin=mihin, lahtoaika=laika,
            saapumisaika=saika, bussi=bussi, juna=juna, auto=auto,
            alennusluokka=ale)  # TODO debug
        matkat = scraper.hae_matka(**params)

        t = str(round(time.time() - t, 2))
        return render.results(matkat=matkat, params=params, t=t)


### APUFUNKTIOT ###


def formatoi_aika(h, mins, pvm):
    """Formatoi parametrien tunnit, minuutit ja päivämäärän
    muotoon YYYY-mm-dd HH:MM

    >>> formatoi_aika(4, 56, "1.12.2012")
    '2012-12-01 04:56'
    """
    pvm_str = "%s %s:%s" % (pvm, h, mins)
    dt = datetime.strptime(pvm_str, LOMAKE_PVM_FORMAATTI)
    return datetime.strftime(dt, SOVELLUS_PVM_FORMAATTI)


### SOVELLUKSEN KÄYNNISTÄMINEN ###


app = web.application(urls, globals(), autoreload=False)
web.config.debug = True  # TODO
gae_app = app.gaerun()  # Tämä takaa App Engine-yhteensopivuuden

if __name__ == "__main__":
    app.run()

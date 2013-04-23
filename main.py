# -*-coding:utf-8-*-
# Joukkoliikenteen hintavertailusovellus


import web
from scraper_wrapper import ScraperWrapper
from datetime import datetime, timedelta
import re


### APUFUNKTIOT ###


def formatoi_aika(h, mins, pvm):
    """Formatoi parametrien tunnit, minuutit ja päivämäärän
    muotoon YYYY-mm-dd HH:MM

    >>> formatoi_aika()
    '2013-03-01 12:40'
    """



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
        # Poimitaan parametrit URLista:
        inp = web.input(h=None, min=None, pvm=None, ale=0, juna=False,
            bussi=False, auto=False, aikatyyppi="saapumisaika")
        mista, mihin = inp.mista, inp.mihin
        h, mins, pvm, ale = inp.h, inp.min, inp.pvm, inp.ale
        juna, bussi, auto = inp.juna, inp.bussi, inp.auto
        tyyppi = inp.aikatyyppi
        return str()

        # Validoitaan parametrit:
        if not mista or not mihin:
            return "Lähtö- ja saapumispaikka tulee määrittää."  # TODO
        if not ale in range(7):
            return "Virheellinen alennusluokka."  # TODO
        if any(x is None or x == "" for x in [h, mins, pvm]):
            return "Aika ja pvm tulee määrittää."  # TODO
        pvm = formatoi_aika(h, mins, pvm)

        matkat = scraper.hae_matka(mista, mihin, laika, saika, bussi, juna,
            auto, ale)
        return render.results(matkat=matkat)


app = web.application(urls, globals(), autoreload=False)
web.config.debug = True
gae_app = app.gaerun()  # Tämä takaa App Engine-yhteensopivuuden

if __name__ == "__main__":
    app.run()

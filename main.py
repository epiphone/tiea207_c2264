# -*-coding:utf-8-*-
# Joukkoliikenteen hintavertailusovellus


import web
from scraper_wrapper import ScraperWrapper
from datetime import datetime, timedelta
import re


### APUFUNKTIOT ###


def formatoi_aika(pvm, aika):
    """Formatoi päivämäärän (muotoa dd.mm.YYYY) ja ajan
    muotoon YYYY-mm-dd HH:MM

    >>> formatoi_aika("1.3.2013", "12.40")
    '2013-03-01 12:40'
    """
    ajat = map(int, re.findall("\d+", aika))
    assert len(ajat) == 2
    td = timedelta(hours=ajat[0], minutes=ajat[1])
    dt = datetime.strptime(pvm, LOMAKE_PVM_FORMAATTI) + td
    return datetime.strftime(dt, SOVELLUS_PVM_FORMAATTI)


### TEMPLATE-APUFUNKTIOT ###

# TODO

### GLOBAALIT & ASETUKSET ###


LOMAKE_PVM_FORMAATTI = "%d.%m.%Y"
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
        inp = web.input(lahtoaika=None, saapumisaika=None, lahtopvm=None,
            saapumispvm=None, ale=0, juna=False, bussi=False, auto=False)
        mista, mihin = inp.mista, inp.mihin
        laika, saika = inp.lahtoaika, inp.saapumisaika
        lpvm, spvm = inp.lahtopvm, inp.saapumispvm
        ale = int(inp.ale)
        juna, bussi, auto = inp.juna, inp.bussi, inp.auto

        # Validoitaan parametrit:
        if not mista or not mihin:
            return "Lähtö- ja saapumispaikka tulee määrittää."  # TODO
        if not ale in range(7):
            return "Virheellinen alennusluokka."  # TODO
        if laika and lpvm:
            laika = formatoi_aika(lpvm, laika)
            saika = None
        elif saika and spvm:
            saika = formatoi_aika(lpvm, laika)
            laika = None
        else:
            return "Joko lähtöaika tai saapumisaika tulee määrittää."  # TODO

        matkat = scraper.hae_matka(mista, mihin, laika, saika, bussi, juna,
            auto, ale)
        return render.results(matkat=matkat)


app = web.application(urls, globals(), autoreload=False)
web.config.debug = True
gae_app = app.gaerun()  # Tämä takaa App Engine-yhteensopivuuden

if __name__ == "__main__":
    app.run()

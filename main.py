# -*-coding:utf-8-*-
# Joukkoliikenteen hintavertailusovellus


import web
from scraper_wrapper import ScraperWrapper


urls = (
    "/", "Index",
    "/haku", "Haku"
)

scraper = ScraperWrapper()
render = web.template.render("templates/", base="base")


class Index:
    def GET(self):
        """Pääsivu, joka sisältää hakuikkunan."""
        return render.index()


class Haku:
    def GET(self):
        """Sivu, joka esittää haun tulokset."""
        # Poimitaan parametrit URLista:
        inp = web.input(lahtoaika=None, saapumisaika=None, ale=0,
            juna=False, bussi=False, auto=False)
        mista, mihin = inp.mista, inp.mihin
        laika, saika = inp.lahtoaika, inp.saapumisaika
        ale = int(inp.ale)
        juna, bussi, auto = inp.juna, inp.bussi, inp.auto

        # Validoitaan parametrit:
        if not mista or not mihin:
            return "Lähtö- ja saapumispaikka tulee määrittää."  # TODO
        if not ale in range(7):
            return "Virheellinen alennusluokka."  # TODO
        if not laika and not saika:
            return "Joko lähtöaika tai saapumisaika tulee määrittää."  # TODO

        matkat = scraper.hae_matka(mista, mihin, laika, saika, bussi, juna,
            auto, ale)
        return render.results(matkat=matkat)

app = web.application(urls, globals(), autoreload=False)
web.config.debug = True
gae_app = app.gaerun()  # Tämä takaa App Engine-yhteensopivuuden

if __name__ == "__main__":
    app.run()

# -*-coding:utf-8-*-
"""
Joukkoliikenteen hintavertailusovellus.

Reititykset, templatet yms.

Aleksi Pekkala
"""

import web
from scraper_wrapper import ScraperWrapper
from datetime import datetime, timedelta
import time


### GLOBAALIT & ASETUKSET ###


LOMAKE_PVM_FORMAATTI = "%d.%m.%Y %H:%M"
SOVELLUS_PVM_FORMAATTI = "%Y-%m-%d %H:%M"
JS_PVM_FORMAATTI = "%Y-%m-%dT%H:%M"

# (x, y) missä x on polttoaine (95, 98, diesel) ja y on keskikulutus (l/100km)
KULUTUSLUOKAT = [(0, 4.5), (0, 6.5), (0, 8.5), (1, 4.5), (1, 6.5), (1, 8.5),
    (2, 3.7), (2, 5.7), (2, 7.7)]
ALENNUSLUOKAT = [(0, "Aikuinen"), (1, "Lapsi (4-11v)"), (3, "Nuori (12-16v)"),
    (2, "Opiskelija"), (5, "Varusmies"), (7, "Siviilipalvelusmies"),
    (4, "Eläkeläinen"), (6, "Lehdistö")]

# Reititykset:
urls = (
    "/", "Index",
    "/haku", "Haku",
    "/info", "Info",
    "/palaute", "Palaute"
)

scraper = ScraperWrapper()


### TEMPLATET ###


def hae_ikonin_url(palvelu):
    """
    Palauttaa VR:n palvelua vastaavaan ikonin URLin.
    """
    def f(char):
        if char == u"ä":
            return u"a"
        if char == u"ö":
            return u"o"
        if char == " ":
            return "_"
        if char in [" ", ",", "."]:
            return ""
        return char

    url = palvelu.lower()
    url = "".join([f(c) for c in url])
    return "/static/img/vr_ikonit/" + url + ".gif"

template_globs = {"hae_ikonin_url": hae_ikonin_url}
render = web.template.render("templates/", base="base", globals=template_globs)


### SIVUT ###


class Index:
    def GET(self):
        """Pääsivu, joka sisältää hakuikkunan."""
        return render.index(aleluokat=ALENNUSLUOKAT)


class Haku:
    def GET(self):
        """Sivu, joka esittää haun tulokset."""
        # Mitataan matkaselvityksen kesto:  # TODO debug
        t = time.time()

        # Poimitaan parametrit URLista:
        inp = web.input(h=None, min=None, pvm=None, juna=False, bussi=False,
            auto=False, tyyppi="saapumisaika", debug=False, ale=0, kulutus=0)

        mista, mihin = inp.mista, inp.mihin
        h, mins, pvm = inp.h, inp.min, inp.pvm
        juna, bussi, auto = inp.juna, inp.bussi, inp.auto
        ale, kulutusluokka = int(inp.ale), int(inp.kulutus)
        aikatyyppi = inp.tyyppi
        debug_view = True if inp.debug else False

        # Validoitaan parametrit:
        if not mista or not mihin:
            return "Lähtö- ja saapumispaikka tulee määrittää."  # TODO
        if not ale in range(8):
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
            aleluokka=ale,
            polttoaine=polttoaine,
            kulutus=kulutus,
            max_lkm=5)

        matkat = scraper.hae_matka(**params)
        if "virhe" in matkat:
            return "virhe: " + matkat["virhe"]  # TODO virheenkäsittely
        taydenna_matkatiedot(matkat, pvm, laika, saika)

        mh_ja_vr = []
        for x in ["juna", "bussi"]:
            if x in matkat and matkat[x] and not "virhe" in matkat[x]:
                mh_ja_vr += matkat[x]
        mh_ja_vr = sorted(mh_ja_vr, key=lambda x: x["lahtoaika"])

        # TODO turhat parametrit pois
        t = str(round(time.time() - t, 2))
        if debug_view:
            return render.results_debug(matkat=matkat, params=params, t=t)

        dt = laika or saika
        dt = dt.split()[0] + "T" + dt.split()[1]
        return render.results(matkat=matkat, params=params, t=t, dt=dt,
            pvm=pvm, h=h, mins=mins, aikatyyppi=aikatyyppi,
            aleluokka=ale, aleluokat=ALENNUSLUOKAT, mh_ja_vr=mh_ja_vr)


class Info:
    def GET(self):
        """
        Palauttaa staattisen infosivun.
        """
        return render.info()


class Palaute:
    def GET(self):
        """
        Palauttaa palautesivun.
        """
        return render.palaute()


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
    if "auto" in matkat and matkat["auto"] and not "virhe" in matkat["auto"]:
        auto = matkat["auto"]
        auto["id"] = "row-auto"
        auto["luokka"] = "auto"
        auto["js_hinnat"] = str(auto["hinta"]) + "€"

        auto["tunnit"] = kesto_tunneiksi(auto["kesto"])
        if lahtoaika:
            dt = datetime.strptime(lahtoaika, SOVELLUS_PVM_FORMAATTI)
            auto["js_aika"] = dt.strftime(JS_PVM_FORMAATTI)
            auto["lahtoaika"] = dt.strftime("%H:%M")
            dt += timedelta(hours=auto["tunnit"])
            auto["saapumisaika"] = dt.strftime("%H:%M")
        else:
            dt = datetime.strptime(saapumisaika, SOVELLUS_PVM_FORMAATTI)
            auto["saapumisaika"] = dt.strftime("%H:%M")
            dt -= timedelta(hours=auto["tunnit"])
            auto["js_aika"] = dt.strftime(JS_PVM_FORMAATTI)
            auto["lahtoaika"] = dt.strftime("%H:%M")

    for luokka in ["juna", "bussi"]:
        if not luokka in matkat or not matkat[luokka]:
            continue
        if "virhe" in matkat[luokka]:
            continue

        for i, matka in enumerate(matkat[luokka]):
            matka["luokka"] = luokka

            # TODO tulevaisuudessa vain yksi hinta
            if matka["hinnat"]:
                for hinta in matka["hinnat"] + [999.9]:
                    if hinta:
                        matka["hinta"] = hinta
                        break
            else:
                matka["hinta"] = 999.9

            matka["id"] = "row-%s%d" % (luokka, i)
            pvm_str = " ".join([pvm, matka["lahtoaika"]])
            dt = datetime.strptime(pvm_str, LOMAKE_PVM_FORMAATTI)
            matka["js_aika"] = dt.strftime(JS_PVM_FORMAATTI)
            hinnat = "/".join([str(h) + "€" if h else "-" for h in matka["hinnat"]])
            matka["js_hinnat"] = hinnat or "-"
            matka["vaihdot_lkm"] = len(matka["vaihdot"]) - 1
            matka["tunnit"] = kesto_tunneiksi(matka["kesto"])
            matka["tyyppi"] = "-".join(v["tyyppi"] for v in matka["vaihdot"])


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

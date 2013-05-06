# -*-coding:utf-8-*-
# Paikannimien yhtenäistäminen - testailua
# Aleksi Pekkala

import urllib
import urllib2
from lxml import html
from multiprocessing import Pool
import json


URL_MH = "http://matkahuolto.info/lippu/fi/autocomplete"
URL_LV = "http://alk.tiehallinto.fi/www2/valimatkat/"


def hae_paikat():
    """Palauttaa tiehallinnon välimatkapalvelussa listatut paikannimet."""
    sivu = urllib2.urlopen(URL_LV)
    root = html.parse(sivu)
    select = root.xpath("//select[count(option)>20]")[0]
    return [rivi.text.strip().lower() for rivi in select.iterchildren()]


def hae_mh(query):
    """Palauttaa listan niistä matkahuollon paikannimistä, joiden alussa
    on annettu hakuehto."""
    if isinstance(query, unicode):
        query = query.encode("utf-8")
    data = urllib.urlencode({"term": query})
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
    req = urllib2.Request(URL_MH, data, headers)
    res = urllib2.urlopen(req)
    parser = html.HTMLParser(encoding="utf-8")
    root = html.parse(res, parser)
    try:
        rivit = root.xpath("//li")
        if not rivit:
            return []
        return [rivi.text.strip().lower() for rivi in rivit]
    except AssertionError:
        return []


def selvita_yhteydet(paikat):
    lkm = len(paikat)
    yhteydet = lkm * [[]]
    for i, paikka in enumerate(paikat):
        print "%d/%d: %s" % (i + 1, lkm, paikka)
        if paikka in hae_mh(paikka):
            yhteydet[i] = paikka
            print "löytyi"
        else:
            print "ei löytynyt"
    return yhteydet


def f(paikka):
    print paikka
    return hae_mh(paikka)


def selvita_yhteydet_async(paikat, poolsize=20):
    pool = Pool(poolsize)
    return pool.map(f, paikat)


def suorita():
    try:
        json_file = open("paikat.json")
        data = json.load(json_file)
    except IOError:
        data = None

    if not data:
        # Haetaan tiehallinnon paikkapalvelun 470 paikkakuntaa:
        paikat = hae_paikat()
        uudet_paikat = []
        for i, paikka in enumerate(paikat):
            # Muokataan "jämsä, kaipola" --> "kaipola (jämsä)"
            paikka = paikka.replace(u"(yhdistetty)", u"").strip()
            if paikka.endswith(u" kko"):
                paikka = paikka.replace(u" kko", u"")
            paikka = paikka.replace(u"jyväskylän mlk", u"jyväskylä")
            osat = paikka.split(",")
            if len(osat) == 3:
                if osat[2].strip() == "raja":
                    osat = osat[:2]
            if len(osat) == 2:
                if osat[1].strip() in ["kko.", "kesk."]:
                    uusi_paikka = osat[0].strip()
                else:
                    uusi_paikka = "%s (%s)" % (osat[1].strip(), osat[0].strip())
                print "Muokattiin %s -> %s" % (paikka, uusi_paikka)
                uudet_paikat.append(uusi_paikka)
            else:
                uudet_paikat.append(paikka)
        paikat = uudet_paikat

        # Haetaan Matkahuollon hakutulokset jokaiselle haetulle paikalle:
        mh_paikat = selvita_yhteydet_async(paikat)
        data = {p: mh_paikat[i] for i, p in enumerate(paikat)}
        json_file = open("paikat.json", "w")
        json_file.write(json.dumps(data))
        json_file.close()

    d = {}
    for paikka, ehdotukset in data.iteritems():
        d[paikka] = ehdotukset
        for ehdotus in ehdotukset:
            if ehdotus == paikka:
                d[paikka] = ehdotus
                continue
            osat = ehdotus.split()
            if len(osat) == 2 and osat[0].strip() == paikka:
                d[paikka] = osat[0].strip()
                continue

    paikat = d.keys()
    loytyneet = [p for p in paikat if isinstance(d[p], basestring)]
    eiloytyneet = [p for p in paikat if p not in loytyneet]
    return d, loytyneet, eiloytyneet

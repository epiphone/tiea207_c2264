# -*-coding:utf-8-*-
# Paikannimien yhtenäistäminen - testailua
# Aleksi Pekkala

import urllib
import urllib2
from lxml import html
from multiprocessing import Pool


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
    if paikka in hae_mh(paikka):
        return paikka
    return None


def selvita_yhteydet_async(paikat, poolsize=20):
    pool = Pool(poolsize)
    return pool.map(f, paikat)


def suorita():
    paikat = hae_paikat()
    print "Paikat haettu, selvitetään yhteydet..."

    yhteydet = selvita_yhteydet_async(paikat)
    loytyneet = [p for i, p in enumerate(paikat) if yhteydet[i]]
    eiloytyneet = [p for i, p in enumerate(paikat) if not yhteydet[i]]
    print "Suora vastaavuus löytyi %d/%d paikalle"\
        % (len(loytyneet), len(paikat))

    print ""
    for paikka in eiloytyneet:
        mh_ehdotukset = hae_mh(paikka)


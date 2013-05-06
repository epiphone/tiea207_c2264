# -*-coding:utf-8-*-
# Paikannimien yhtenäistäminen - testailua
# Aleksi Pekkala

import urllib
import urllib2
from lxml import html
import json
from henkiloauto_scraper.auto_scraperAPI import AutoScraper


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


def avaa_json():
    json_file = open("paikat.json")
    return json.load(json_file)


def testaa_mh():
    paikat = avaa_json()
    eiloyt = []
    for k, v in paikat.iteritems():
        bpaikka, jpaikka = v
        if bpaikka:
            if not bpaikka in hae_mh(bpaikka):
                eiloyt.append({k: bpaikka})
                print "FAIL", k, "==>", bpaikka
            else:
                print " OK ", k, "==>", bpaikka


def testaa_auto():
    s = AutoScraper()
    paikat = avaa_json().keys()
    for paikka in paikat:
        splitted = paikka.split()
        if splitted[-1].startswith("("):
            paikka = splitted[0] + ", " + splitted[-1][1:-1]
        p = str(unicode(paikka).encode("utf-8"))
        print "Yritetään", repr(p)
        matka = s.hae_matka("tampere", p)
        if "virhe" in matka:
            tulos = matka["virhe"]
        else:
            tulos = matka["mihin"]
        print paikka, "==>", tulos

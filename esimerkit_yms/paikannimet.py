# -*-coding:utf-8-*-
# Paikannimien yhtenäistäminen - testailua
# Aleksi Pekkala

import urllib
import urllib2
from lxml import html
import json
from henkiloauto_scraper.auto_scraper import AutoScraper
from vr_scraper.vr_scraper import VRScraper
from mh_raaputin.raaputin_alpha import MHScraper


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


def testaa():
    """
    Testataan paikannimet dramaattisen hitaasti.
    """
    auto_s, mh_s, vr_s = AutoScraper(), MHScraper(), VRScraper()
    paikat = avaa_json()
    dt = "2013-05-20 12:12"

    for k, v in paikat.iteritems():
        print k
        mh_paikka, vr_paikka, auto_paikka = v
        mh_matka = mh_s.hae_matka("oulu", mh_paikka.encode("utf-8"), dt) if mh_paikka else None
        vr_matka = vr_s.hae_matka("oulu", vr_paikka.encode("utf-8"), dt) if vr_paikka else None
        auto_matka = auto_s.hae_matka("oulu", auto_paikka.encode("utf-8"), dt) if auto_paikka else None
        print "- MH:", "VIRHE" if mh_matka and "virhe" in mh_matka else "OK"
        print "- VR:", "VIRHE" if vr_matka and "virhe" in vr_matka else "OK"
        print "- AU:", "VIRHE" if auto_matka and "virhe" in auto_matka else "OK"

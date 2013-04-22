# -*- coding:utf-8 -*-
'''
Luotu 16.4.2013

@author: Juuso Tenhunen
'''
from lxml import html
import urllib

matkat_lista = []

class MHScraper:
    """luokka raaputtimelle"""
    def __init__(self):
        """konstruktori"""
        pass

    def hae_matka(self, mista, mihin, lahtoaika=None, saapumusaika=None):
        """luetaan skreipatut rivit, ja sijoitetaan ne 'Matka' -olioina taulukkoon attribuuttien kera"""
        lahtopaiva = lahtoaika.split(" ")[0]

        dd = lahtopaiva.split("-")[2]
        kk = lahtopaiva.split("-")[1]
        vvvv = lahtopaiva.split("-")[0]

        url = ("http://www.matkahuolto.info/lippu/fi/"
               "connectionsearch?lang=fi&departureStopAreaName=%s"
               "&arrivalStopAreaName=%s"
               "&allSchedules=0&departureDay=%s"
               "&departureMonth=%s"
               "&departureYear=%s"
               "&stat=1&extl=1&search.x=-331&search.y=-383&ticketTravelType=0") % (aakkos_vaihto(mista), aakkos_vaihto(mihin), dd, kk, vvvv)

        sivu = urllib.urlopen(url)

        # Haetaan html-tiedosto, luodaan lxml-olio:
        try:
            root = html.parse(sivu)
        except IOError:
            print "Skreippaaminen epäonnistui"
            return

        err_rows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//div[1]")
        err_row = err_rows[0]

        #Jos haku tuottaa error-boxin, haetaan sen errorin nimi, eikä tehdä enää muuta
        if err_row.attrib["class"] in ["error_wrapper"]:
            return error_msg(err_rows)


        #jos hakuvirhettä ei tule, jatketaan normaalisti
        else:

            rows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//table[2]//tr")

            for i, row in enumerate(rows[1:]):

                children = row.getchildren()

                if len(children) == 7:
                    vaihto = " ".join(children[6].text_content().split())
                    matkat_lista[-1]['vaihdot'][-1]['saapumisaika'] = vaihto.split()[-1][1:-1].split('-')[0]
                    matkat_lista[-1]['vaihdot'][-1]['mihin'] = vaihto.split()[0]
                    matkat_lista[-1]['vaihdot'].append({'lahtoaika': vaihto.split()[-1][1:-1].split('-')[-1],
                                                       'saapumisaika': matkat_lista[-1]['saapumisaika'],
                                                       'mista': vaihto.split()[0],
                                                       'mihin': "",
                                                       'tyyppi': "",
                                                       'tunnus': "",
                                                       'vaihto_nro': matkat_lista[-1]['vaihdot'][-1]['vaihto_nro'] + 1})

                    matkat_lista[-1]['vaihto_lkm'] = matkat_lista[-1]['vaihto_lkm'] + 1
                    continue

                if children[1].text_content().strip() ==  "":
                    matkat_lista[-1]['vaihdot'][-1]['mihin'] = mihin
                    matkat_lista[-1]['vaihdot'][-1]['tyyppi'] = children[6].text_content().split()[0]
                    matkat_lista[-1]['vaihdot'][-1]['tunnus'] = children[6].text_content()
                    continue

                matka = {'indeksi': i,
                         'lahtoaika': children[1].text_content(),
                         'saapumisaika': children[3].text_content(),
                         'laituri': children[4].text_content(),
                         'kesto': keston_vaihto(children[5].text_content()),
                         'hinta': children[10].text_content(),
                         'vaihto_lkm': 0,
                         'vaihdot': [
                                # 1. vaihtoyhteys
                                {'lahtoaika': children[1].text_content(),
                                 'saapumisaika': children[3].text_content(),
                                 'mista': mista,
                                 'mihin': mihin,
                                 'tyyppi': children[6].text_content().split()[0],
                                 'tunnus': children[6].text_content(),
                                 'vaihto_nro': 1}
                                 ]
                                }

                matkat_lista.append(matka)

            return matkat_lista

def aakkos_vaihto(nimi):
    """Vaihtaa Ääkköset urlin vaatimiin muotoihin"""
    uusi_nimi = nimi.replace('ä', "%E4")
    uusi_nimi = uusi_nimi.replace('Ä', "%C4")
    uusi_nimi = uusi_nimi.replace('ö', "%D6")
    uusi_nimi = uusi_nimi.replace('Ö', "%F6")
    uusi_nimi = uusi_nimi.replace('å', "%E5")
    uusi_nimi = uusi_nimi.replace('Å', "%C5")
    return uusi_nimi

def keston_vaihto(aika):
    """Vaihtaa matkan keston HHh MMmin = HH:MM (esim 5h 15min = 05:15)"""
    kesto = aika.split()
    tunti = kesto[0].replace("h", "")

    if len(tunti) == 1:
        tunti = "0"+tunti

    minuutti = kesto[-1].replace("min","")

    if len(minuutti) == 1:
        minuutti = "0" + minuutti

    return tunti + ":" + minuutti

def error_msg(err_rows):
    """Hakee 'error_wrapper':sta errorin nimen ja tulostaa sen"""
    print err_rows[1].text_content().strip()

def hae_hinnat(url):
    """haetaan kaikki matkan hinnat ja sijoitetaan ne dictionaryyn"""

    try:
        root = html.parse(url)
    except IOError:
        print "Skreippaaminen epäonnistui"
        return

    rows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//table[last()]//tr")

    hinta = {}

    for row in rows[2:3]: #ei huomioda kahta ekaa eikä kolmea viimeistä?

        children = row.getchildren()

        hinta[children[0].text_content()] = children[2].text_content()

# -*- coding:utf-8 -*-
'''
Luotu 2.4.2013

@author: Juuso Tenhunen
'''
from lxml import html

matkatLista = []

lahto = "Ähtäri"
#HUOM Ä=%C4, ä=%E4, Ö
#jyväskylä = jyv%E4skyl%E4
saapu = "Hämeenkyrö"
paiva = "24"
kk = "4"
vuosi = "2013"

def TeeMatka(rows):
    """luetaan skreipatut rivit, ja sijoitetaan ne 'Matka' -olioina taulukkoon attribuuttien kera"""
    for i, row in enumerate(rows[1:]):       

        children = row.getchildren()

        if len(children) == 7:
            vaihto = " ".join(children[6].text_content().split())
            matkatLista[-1]['vaihdot'][-1]['saapumisaika'] = vaihto.split()[-1][1:-1].split('-')[0]
            matkatLista[-1]['vaihdot'][-1]['mihin'] = vaihto.split()[0]
            matkatLista[-1]['vaihdot'].append({'lahtoaika': vaihto.split()[-1][1:-1].split('-')[-1],
                                             'saapumisaika': matkatLista[-1]['saapumisaika'],
                                             'mista': vaihto.split()[0],
                                             'mihin': "",
                                             'tyyppi': "",
                                             'tunnus': "",
                                             'vaihto_nro': matkatLista[-1]['vaihdot'][-1]['vaihto_nro'] + 1})
            
            matkatLista[-1]['vaihto_lkm'] = matkatLista[-1]['vaihto_lkm'] + 1
            continue

        if children[1].text_content().strip() ==  "":
            matkatLista[-1]['vaihdot'][-1]['mihin'] = saapu
            matkatLista[-1]['vaihdot'][-1]['tyyppi'] = children[6].text_content().split()[0]
            matkatLista[-1]['vaihdot'][-1]['tunnus'] = children[6].text_content()
            continue
        
        matka = {'indeksi': i,
                 'lahtoaika': children[1].text_content(),
                 'saapumisaika': children[3].text_content(),
                 'laituri': children[4].text_content(),
                 'kesto': children[5].text_content(),
                 'hinta': children[10].text_content(),
                 'vaihto_lkm': 0,
                 'vaihdot': [
                             # 1. vaihtoyhteys
                             {'lahtoaika': children[1].text_content(),
                              'saapumisaika': children[3].text_content(),
                              'mista': lahto,
                              'mihin': saapu,
                              'tyyppi': children[6].text_content().split()[0],
                              'tunnus': children[6].text_content(),
                              'vaihto_nro': 1}
                             ]
                 }

        matkatLista.append(matka)
        
def Tulosta_Lista():
    """Tulostetaan Matkalista"""
    for matka in matkatLista:
        print "----------------------------------------------------------------"
        print "%s | %s | %s | %s | %s | " % (matka['lahtoaika'], matka['saapumisaika'], matka['laituri'], matka['kesto'], matka['hinta']) + "Vaihtoja: " + str(matka['vaihto_lkm'])
        
        for yhteys in matka['vaihdot']:
            print str(yhteys['vaihto_nro']) + ". VaihtoYhteys"
            print "--> %s | %s | %s | %s | %s | %s" % (yhteys['lahtoaika'], yhteys['saapumisaika'], yhteys['mista'], yhteys['mihin'], yhteys['tyyppi'], yhteys['tunnus'])
        
        print "----------------------------------------------------------------"
        print "\n"
        
def AakkosVaihto(nimi):
    uusi_nimi = nimi.replace('ä', "%E4")
    uusi_nimi = uusi_nimi.replace('Ä', "%C4")
    uusi_nimi = uusi_nimi.replace('ö', "%D6")
    uusi_nimi = uusi_nimi.replace('Ö', "%F6")
    uusi_nimi = uusi_nimi.replace('å', "%E5")
    uusi_nimi = uusi_nimi.replace('Å', "%C5")
    return uusi_nimi


def HintaJarjestys(lista):
    """Järjestetään lista hinnan mukaan nousevaan järjestykseen"""

    for vertmatka in lista:
        for matka in lista:
            if vertmatka.depart == matka.depart:
                continue
            if vertmatka.price < matka.price:

                vertmatka.swap(matka)

def ErrorMsg(errRows):
    """Hakee 'error_wrapper':sta errorin nimen ja tulostaa sen"""
    print errRows[1].text_content().strip()

def main():
    """skreipataan Matkahuollon sivuilta aikataulut"""

    url = "http://www.matkahuolto.info/lippu/fi/connectionsearch?lang=fi&departureStopAreaName="+AakkosVaihto(lahto)+"&arrivalStopAreaName="+AakkosVaihto(saapu)+"&allSchedules=0&departureDay="+paiva+"&departureMonth="+kk+"&departureYear="+vuosi+"&stat=1&extl=1&search.x=-331&search.y=-383&ticketTravelType=0"

    # Haetaan html-tiedosto, luodaan lxml-olio:
    try:
        root = html.parse(url)
    except IOError:
        print "Skreippaaminen epäonnistui"
        return

    errRows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//div[1]")
    errRow = errRows[0]

    #Jos haku tuottaa error-boxin, haetaan sen errorin nimi, eikä tehdä enää muuta
    if errRow.attrib["class"] in ["error_wrapper"]:
        print "Can't see shit captain!"
        ErrorMsg(errRows)

    #jos hakuvirhettä ei tule, jatketaan normaalisti
    else:

        rows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//table[2]//tr")

        TeeMatka(rows)

        Tulosta_Lista()

if __name__ == "__main__":
    main()


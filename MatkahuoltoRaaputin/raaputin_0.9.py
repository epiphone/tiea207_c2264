# -*- coding:utf-8 -*-
'''
Luotu 2.4.2013

@author: Juuso Tenhunen
'''
from lxml import html

matkatLista = []

lahto = "Kuopio"
saapu = "Siilinjärvi"
paiva = "24"
kk = "4"
vuosi = "2013"
# 0 = peruslippu
# 1 = Opiskelijat, Varusmiehet, Sivarit, Lapset -50%
# 2 = Eläkeläiset, Lehdistö, SLAHS:n jäsenet, Nuoriso -30%
lippu_tyyppi = 1

def tee_matka(rows):
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
                 'kesto': keston_vaihto(children[5].text_content()),
                 'hinta': laske_hinta(children[10].text_content(), children[6].text_content().split()[0]),
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
        
def tulosta_lista():
    """Tulostetaan Matkalista"""
    for matka in matkatLista:
        print "----------------------------------------------------------------"
        print "%s | %s | %s | %s | %s | " % (matka['lahtoaika'], matka['saapumisaika'], matka['laituri'], matka['kesto'], matka['hinta']) + "Vaihtoja: " + str(matka['vaihto_lkm'])
        
        for yhteys in matka['vaihdot']:
            print str(yhteys['vaihto_nro']) + ". VaihtoYhteys"
            print "--> %s | %s | %s | %s | %s | %s" % (yhteys['lahtoaika'], yhteys['saapumisaika'], yhteys['mista'], yhteys['mihin'], yhteys['tyyppi'], yhteys['tunnus'])
        
        print "----------------------------------------------------------------"
        print "\n"
        
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

def laske_hinta(alkup_hinta, linja):
    """Vaihtaa matkan hinnan sen mukaan, mikä hintaluokka on kyseessä (normaali, -50%, -30% etc..) VIELÄ KESKEN"""
    try:
        hinta = float(alkup_hinta.replace(",", "."))
    except ValueError:
        return 0
    else:
        if lippu_tyyppi == 0:
            return hinta
    
        if lippu_tyyppi == 1:
            if linja == "vakio" and hinta < 15.50:
                return str(hinta) + " (TODO: taulukko)"
            if linja == "pika" and hinta < 18.80:
                return str(hinta) + " (TODO: taulukko)"
        
            uusihinta = hinta/2
        
            return uusihinta
        
        if lippu_tyyppi == 2:
            if linja == "vakio" and hinta < 15.50:
                return str(hinta) + " (TODO: taulukko)"
            if linja == "pika" and hinta < 18.80:
                return str(hinta) + " (TODO: taulukko)"
        
            uusihinta = hinta - (hinta*0.3)
        
            return uusihinta

def error_msg(errRows):
    """Hakee 'error_wrapper':sta errorin nimen ja tulostaa sen"""
    print errRows[1].text_content().strip()

def main():
    """skreipataan Matkahuollon sivuilta aikataulut"""

    url = "http://www.matkahuolto.info/lippu/fi/connectionsearch?lang=fi&departureStopAreaName="+aakkos_vaihto(lahto)+"&arrivalStopAreaName="+aakkos_vaihto(saapu)+"&allSchedules=0&departureDay="+paiva+"&departureMonth="+kk+"&departureYear="+vuosi+"&stat=1&extl=1&search.x=-331&search.y=-383&ticketTravelType=0"

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
        error_msg(errRows)

    #jos hakuvirhettä ei tule, jatketaan normaalisti
    else:

        rows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//table[2]//tr")

        tee_matka(rows)

        tulosta_lista()

if __name__ == "__main__":
    main()


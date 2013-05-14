# -*- coding:utf-8 -*-
'''
Luotu 16.4.2013

@author: Juuso Tenhunen
'''
from lxml import html
import urllib
import json

class MHScraper:
    """luokka raaputtimelle"""
    def __init__(self):
        """konstruktori"""
        pass
    
    def laske_alennus(self, perus_hinta, alennusluokka, linja):
        """lasketaan alennushinta"""
        if alennusluokka == 0:
            return perus_hinta
        
        if alennusluokka == 1 or alennusluokka == 2 or alennusluokka == 5 or alennusluokka == 7:
            if linja == "vakio" and perus_hinta < 15.50:
                return str(perus_hinta) + " (TODO: taulukko)"
            if linja == "pika" and perus_hinta < 18.80:
                return str(perus_hinta) + " (TODO: taulukko)"
            
            uusihinta = perus_hinta/2
            
            return round(uusihinta, 1)
            
        if alennusluokka == 3 or alennusluokka == 4 or alennusluokka == 6:
            if linja == "vakio" and perus_hinta < 15.50:
                return str(perus_hinta) + " (TODO: taulukko)"
            if linja == "pika" and perus_hinta < 18.80:
                return str(perus_hinta) + " (TODO: taulukko)"
            
            uusihinta = perus_hinta - (perus_hinta*0.3)
            
            return round(uusihinta, 1)
            
        else:
            return {'virhe': "virhe alennuksen laskussa"}
    
    def hae_matka(self, mista, mihin, lahtoaika=None, saapumisaika=None):
        """luetaan skreipatut rivit, ja sijoitetaan ne 'Matka' -olioina
        taulukkoon attribuuttien kera"""
        
        matkat_lista = []
        
        url = self.tee_url(mista, mihin, lahtoaika, saapumisaika)
        
        try:
            sivu = urllib.urlopen(url)
        except IOError:
            return None

        root = html.parse(sivu)

        err_rows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//div[1]")
        err_row = err_rows[0]

        #Jos haku tuottaa error-boxin, haetaan sen errorin nimi,
        #eikä tehdä enää muuta
        if err_row.attrib["class"] in ["error_wrapper"]:
            return self.error_msg(err_rows, lahtoaika,
                                  saapumisaika, root,
                                  mista, mihin)
        

        #jos hakuvirhettä ei tule, jatketaan normaalisti
        else:

            rows = root.xpath("//table//tr[last()]/td[last()]"
                              "//tr[1]//table[2]//tr")
            
            mista_mihin = root.xpath("//table//tr[last()]/td[last()]"
                                     "//tr[1]//table[1]//tr[2]/td[2]")
            
            try:
                asema_mista = mista_mihin[1].text_content().split("\r\n")[4].strip()
            except IndexError:
                return None
                
            asema_mihin = mista_mihin[1].text_content().split("\r\n")[8].strip()
    
            for row in rows[1:]:       

                children = row.getchildren()

                if len(children) == 7:
                    vaihto = " ".join(children[6].text_content().split()).replace(",","")
                    vaihtooa = matkat_lista[-1]['vaihdot']
                    vaihtooa[-1]['saapumisaika'] = (vaihto.split()[-1]
                                                    [1:-1].split('-')[0])
                    vaihtooa[-1]['mihin'] = vaihto.split("(")[0]
                    vaihtooa.append({'lahtoaika': (vaihto.split()[-1]
                                                   [1:-1].split('-')[-1]),
                                     'saapumisaika': (matkat_lista[-1]
                                                      ['saapumisaika']),
                                     'mista': vaihto.split("(")[0],
                                     'mihin': "",
                                     'tyyppi': "",
                                     'tunnus': ""})
                    continue

                if children[1].text_content().strip() ==  "":
                    vaihtoa = matkat_lista[-1]['vaihdot'][-1]
                    vaihtoa['mihin'] = asema_mihin
                    vaihtoa['tyyppi'] = children[6].text_content().split()[0]
                    vaihtoa['tunnus'] = children[6].text_content()
                    continue
                
                if len(children) == 2:
                    continue
        
                matka = {'lahtoaika': children[1].text_content(),
                         'saapumisaika': children[3].text_content(),
                         'mista': asema_mista,
                         'mihin': asema_mihin,
                         'laituri': children[4].text_content(),
                         'kesto': self.keston_vaihto(children[5].text_content()),
                         'hinnat': self.hae_hinnat(children[10].text_content(), children[11].text_content()),
                         'vaihdot': [
                                # 1. vaihtoyhteys
                                {'lahtoaika': children[1].text_content(),
                                 'saapumisaika': children[3].text_content(),
                                 'mista': asema_mista,
                                 'mihin': asema_mihin,
                                 'tyyppi': children[6].text_content().split()[0],
                                 'tunnus': children[6].text_content(),}
                                 ]
                                }

                matkat_lista.append(matka)
            
            return matkat_lista
        
    def hae_uusi_matka(self, mista, mihin, lahtoaika,
                       saapumisaika, mista_id, mihin_id):
        """luetaan skreipatut rivit, ja sijoitetaan ne 'Matka' -olioina
        taulukkoon attribuuttien kera"""
        
        matkat_lista = []
        
        url = self.tee_uusi_url(mista, mihin, lahtoaika,
                                saapumisaika, mista_id, mihin_id)
        
        try:
            sivu = urllib.urlopen(url)
        except IOError:
            return None

        root = html.parse(sivu)

        err_rows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//div[1]")
        err_row = err_rows[0]

        #Jos haku tuottaa error-boxin, haetaan sen errorin nimi,
        #eikä tehdä enää muuta
        if err_row.attrib["class"] in ["error_wrapper"]:
            return self.error_msg(err_rows, lahtoaika,
                                  saapumisaika, root,
                                  mista, mihin)
        

        #jos hakuvirhettä ei tule, jatketaan normaalisti
        else:

            rows = root.xpath("//table//tr[last()]/td[last()]"
                              "//tr[1]//table[2]//tr")
            
            mista_mihin = root.xpath("//table//tr[last()]/td[last()]"
                                     "//tr[1]//table[1]//tr[2]/td[2]")
            
            try:
                asema_mista = mista_mihin[1].text_content().split("\r\n")[4].strip()
            except IndexError:
                return None
                
            asema_mihin = mista_mihin[1].text_content().split("\r\n")[8].strip()
    
            for row in rows[1:]:       

                children = row.getchildren()

                if len(children) == 7:
                    vaihto = " ".join(children[6].text_content().split()).replace(",","")
                    vaihtooa = matkat_lista[-1]['vaihdot']
                    vaihtooa[-1]['saapumisaika'] = (vaihto.split()[-1]
                                                    [1:-1].split('-')[0])
                    vaihtooa[-1]['mihin'] = vaihto.split("(")[0]
                    vaihtooa.append({'lahtoaika': (vaihto.split()[-1]
                                                   [1:-1].split('-')[-1]),
                                     'saapumisaika': (matkat_lista[-1]
                                                      ['saapumisaika']),
                                     'mista': vaihto.split("(")[0],
                                     'mihin': "",
                                     'tyyppi': "",
                                     'tunnus': ""})
                    continue

                if children[1].text_content().strip() ==  "":
                    vaihtoa = matkat_lista[-1]['vaihdot'][-1]
                    vaihtoa['mihin'] = asema_mihin
                    vaihtoa['tyyppi'] = children[6].text_content().split()[0]
                    vaihtoa['tunnus'] = children[6].text_content()
                    continue
                
                if len(children) == 2:
                    continue
        
                matka = {
                    'lahtoaika': children[1].text_content(),
                    'saapumisaika': children[3].text_content(),
                    'mista': asema_mista,
                    'mihin': asema_mihin,
                    'laituri': children[4].text_content(),
                    'kesto': self.keston_vaihto(
                        children[5].text_content()),
                    'hinnat': self.hae_hinnat(children[10].text_content(),
                                              children[11].text_content()),
                    'vaihdot': [
                        # 1. vaihtoyhteys
                        {'lahtoaika': children[1].text_content(),
                         'saapumisaika': children[3].text_content(),
                         'mista': asema_mista,
                         'mihin': asema_mihin,
                         'tyyppi': children[6].text_content().split()[0],
                         'tunnus': children[6].text_content(),}
                            ]
                        }

                matkat_lista.append(matka)
            
            return matkat_lista
        
    def tee_uusi_url(self, mista, mihin, lahtoaika, saapumisaika, mista_id, mihin_id):
        """muodostetaan urli screipattavalle sivulle"""
        
        if saapumisaika is None:
            aika = lahtoaika
        else:
            aika = saapumisaika
 
        paiva = aika.split("-")[2].split(" ")[0]
        kuuk = aika.split("-")[1]
        vvvv = aika.split("-")[0]
        
        url = ("http://www.matkahuolto.info/lippu/fi/"
                "connectionsearch?stat=1&sn0=%s"
                "&sn1=%s&sn2=&snOld0=&snOld1=&"
                "snOld2=&page=criteria&action=&connectionSearchType=&"
                "commuterLineNumber=&selectedDay=%s&selectedMonth=%s&"
                "selectedYear=%s&selectedDayOld=&selectedMonthOld=&"
                "selectedYearOld=&travelDate=&travelDateOld=&"
                "departureStopAreaId=%s&departureStopAreaIdOld=&"
                "departureStopAreaName=%s&departureStopAreaNameOld=&"
                "arrivalStopAreaId=%s&arrivalStopAreaName=%s&arrival"
                "StopAreaNameOld=&"
                "allSchedules=0&select=20134&ticket"
                "TravelType=0&search=search") % (mista, mihin, paiva,
                                                 kuuk, vvvv, mista_id,
                                                 mista, mihin_id, mihin)
               
        return url
        
    def tee_url(self, mista, mihin, lahtoaika, saapumisaika):
        """muodostetaan urli screipattavalle sivulle"""
        
        if saapumisaika is None:
            aika = lahtoaika
        else:
            aika = saapumisaika
 
        paiva = aika.split("-")[2].split(" ")[0]
        kuuk = aika.split("-")[1]
        vvvv = aika.split("-")[0]
    
        url = ("http://www.matkahuolto.info/lippu/fi/"
               "connectionsearch?lang=fi&departureStopAreaName=%s"
               "&arrivalStopAreaName=%s"
               "&allSchedules=0&departureDay=%s"
               "&departureMonth=%s"
               "&departureYear=%s"
               "&stat=1&extl=1&search.x=-331"
               "&search.y=-383") % (self.aakkos_vaihto(mista),
                                    self.aakkos_vaihto(mihin),
                                    paiva, kuuk, vvvv)
               
        return url
        

    def aakkos_vaihto(self, nimi):
        """Vaihtaa Ääkköset urlin vaatimiin muotoihin"""
        if nimi is None:
            return nimi
        uusi_nimi = nimi.replace('ä', "%E4")
        uusi_nimi = uusi_nimi.replace('Ä', "%C4")
        uusi_nimi = uusi_nimi.replace('ö', "%D6")
        uusi_nimi = uusi_nimi.replace('Ö', "%F6")
        uusi_nimi = uusi_nimi.replace('å', "%E5")
        uusi_nimi = uusi_nimi.replace('Å', "%C5")
        return uusi_nimi

    def keston_vaihto(self, aika):
        """Vaihtaa matkan keston HHh MMmin => HH:MM (esim 5h 15min = 05:15)"""
        kesto = aika.split()
        tunti = kesto[0].replace("h", "")
    
        if len(tunti) == 1:
            tunti = "0"+tunti
    
        minuutti = kesto[-1].replace("min","")
    
        if len(minuutti) == 1:
            minuutti = "0" + minuutti
        
        return tunti + ":" + minuutti

    def error_msg(self, err_rows, lahtoaika, saapumisaika, root, mista, mihin):
        """Hakee 'error_wrapper':sta errorin nimen ja tulostaa sen"""
        teksti = err_rows[1].text_content().strip().lower()
        
        if teksti.startswith("annetuilla"):
            return None
        
        if teksti.startswith(u"lähtöpaikkaa"):
            return {'virhe': 'mista'}
        
        if teksti.startswith(u"määräpaikkaa"):
            return {'virhe': 'mihin'}
        
        if teksti.startswith("virheellinen"):
            if saapumisaika is None:
                return {'virhe': 'lahtoaika'}
            else:
                return {'virhe': 'saapumisaika'}
            
        if teksti.startswith("jatka antamillasi"):
            return self.tarkennus_vaaditaan(root, lahtoaika,
                                            saapumisaika, mista, mihin)
            #return {'virhe': "tarkennus"}
            
        else:
            return {'virhe': "muu"}
        
    def tarkennus_vaaditaan(self, root, lahtoaika,saapumisaika, mista, mihin):
        """jos jokin hakuvaihtoehto vaatii tarkennuksen (Ivalo => Ivalo (Inari)
        käsitellään se tässä"""
        
        
        mista_id = ""
        mihin_id = ""
        
        eka_syote = root.xpath("//table//tr[last()]/td[last()]"
                               "//tr[1]//table//tr[1]/td[2]/select")
        toka_syote = root.xpath("//table//tr[last()]/td[last()]"
                                "//tr[1]//table//tr[2]/td[2]/select")

        
        if len(eka_syote) > 0 and len (toka_syote) == 0:
            mista_id = eka_syote[0].value_options[0]
            syote = root.xpath("//table//tr[last()]/td[last()]"
                               "//tr[1]//table//tr[2]/td[2]/input")
            mihin_id = syote[0].attrib['value']
        
        if len(toka_syote) > 0 and len(eka_syote) == 0:
            mihin_id = toka_syote[0].value_options[0]
            syote = root.xpath("//table//tr[last()]/td[last()]"
                               "//tr[1]//table//tr[1]/td[2]/input")
            mista_id = syote[0].attrib['value']
            
        if len(eka_syote) > 0 and len (toka_syote) > 0:
            mista_id = eka_syote[0].value_options[0]
            mihin_id = toka_syote[0].value_options[0]

        return self.hae_uusi_matka(mista, mihin, lahtoaika,
                                   saapumisaika, mista_id, mihin_id)
        
    def hae_hinnat(self, hinta,
                   tarjous):
        """tutkitaan onko hintaa/tarjousta
        olemassa ja palautetaan ne listassa"""
        
        try:
            num_hinta = float(hinta.replace(",", "."))
        except ValueError:
            num_hinta = None
        
        try:
            num_tarjous = float(tarjous.replace(",", "."))
        except ValueError:
            num_tarjous = None
            
        return[num_hinta, num_tarjous]
        

def avaa_json():
    """avataan lista paikoista"""
    json_file = open("paikat.json")
    return json.load(json_file)
           
def testaa():
    """ajetaan testeri paikkalistalle"""
    scraper = MHScraper()
        
    paikat = avaa_json()
    
    mista = ["helsinki", "oulu", "kuopio", "tampere", "savonlinna"]
    
    for k, v in paikat.iteritems():
        
        mh_paikka = v
        index = 0
        if mh_paikka[0] is not None:
            mh_matka = scraper.hae_matka(mista[index],
                                         mh_paikka[0].encode("utf-8"),
                                         None, "2013-05-15 12:01")
        
        if mh_paikka[0] is None:
            print k
            print "none"
            continue
        
        while (mh_matka is None and mh_paikka[0] is not None):
            index = index +1
            if index == len(mista):
                break
            mh_matka = scraper.hae_matka(mista[index],
                       mh_paikka[0].encode("utf-8"), None, "2013-05-15 12:01")
        
        if mh_matka is None:
            print mista[index-1] + " -> " + k
            print "- MH:", "VIRHE: ei matkoja"
        else:
            print mista[index] + " -> " + k
            print "- MH:", "VIRHE: " + mh_matka['virhe'] if mh_matka and "virhe" in mh_matka else "OK"
               
    
def main():
    """testi main"""
    
    testaa()
    
    scraper = MHScraper()
    
    matka = scraper.hae_matka("helsinki", "kuopio",
                              None, "2013-05-14 12:01")
    

    if matka is None:
        print "Ei löytyny mittään"
    
    else:
        if 'virhe' in matka:
            print matka
        
        else:
            for x, matka in enumerate(matka):
                print ("------------------------------"
                       "----------------------------------")
                print str(x+1) + ". Vuoro"
                print "Mistä: " + matka['mista']
                print "Mihin: " + matka['mihin']
                print ("%s | %s | %s | "
                       "%s | %s | ") % (matka['lahtoaika'],
                                        matka['saapumisaika'],
                                        matka['laituri'],
                                        matka['kesto'],
                                        matka['hinnat'])
        
                for i, yhteys in enumerate(matka['vaihdot']):
                    print str(i+1) + ". VaihtoYhteys"
                    print ("--> %s | %s | %s | "
                           "%s | %s | %s") % (yhteys['lahtoaika'],
                                              yhteys['saapumisaika'],
                                              yhteys['mista'],
                                              yhteys['mihin'],
                                              yhteys['tyyppi'],
                                              yhteys['tunnus'])
        
                print ("-----------------------------"
                       "-----------------------------------")
                print "\n"
    
    
                     
if __name__ == "__main__":
    main()
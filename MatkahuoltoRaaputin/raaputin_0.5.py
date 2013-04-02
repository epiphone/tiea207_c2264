# -*- coding:utf-8 -*-
'''
Created on Mar 25, 2013
Updated 2.4.2013

@author: Juuso Tenhunen
'''

from lxml import html
import random
 
matkatLista = []
 
class Matka:
    """Yhden matka-olion luokka. Sisältää kaikki matkan tiedot, kuten myös vaihdot"""
    depart = ""
    arriv = ""
    dock = ""
    dura = ""
    linja = ""
    price = ""
    vaihtolkm = 0
    vaihdot = []
   
    def tulosta(self):
        print "%s | %s | %s | %s | %s | %s" % (self.depart, self.arriv, self.dock, self.dura, self.linja, self.price)
        print "Vaihdot: %s" % (self.vaihtolkm)
        for vaihto in self.vaihdot:
            print "%s" % (vaihto)
        print "\n",
       
    def swap(self,other):
        de = self.depart
        ar = self.arriv
        do = self.dock
        du = self.dura
        li = self.linja
        pr = self.price
        vlkm = self.vaihtolkm
        v = self.vaihdot
       
        self.depart = other.depart
        self.arriv = other.arriv
        self.dock = other.dock
        self.dura = other.dura
        self.linja = other.linja
        self.price = other.price
        self.vaihtolkm = other.vaihtolkm
        self.vaihdot = other.vaihdot
       
        other.depart = de
        other.arriv = ar
        other.dock = do
        other.dura = du
        other.linja = li
        other.price = pr
        other.vaihtolkm = vlkm
        other.vaihdot = v
         
       
def TeeMatka(rows):
    """luetaan skreipatut rivit, ja sijoitetaan ne 'Matka' -olioina taulukkoon attribuuttien kera"""
    for row in rows[1:]:
       
        matka = Matka()
       
        matka.vaihdot = []
 
        children = row.getchildren()
       
        if len(children) == 7:
            vaihto = children[6].text_content()
            matkatLista[-1].vaihdot.append("--->missä: " + " ".join(vaihto.split()))
            matkatLista[-1].vaihtolkm = matkatLista[-1].vaihtolkm + 1
            continue
       
        if children[1].text_content().strip() ==  "":
            matkatLista[-1].vaihdot.append("---->linja: " + children[6].text_content())
            continue
           
        matka.depart = children[1].text_content()
        matka.arriv = children[3].text_content()
        matka.dock = children[4].text_content()
        matka.dura = children[5].text_content()
        matka.linja = children[6].text_content()
        matka.price = children[10].text_content()
       
        matkatLista.append(matka)
       
 
def HintaJarjestys(lista):
    """Järjestetään lista hinnan mukaan nousevaan järjestykseen"""
   
    for vertmatka in lista:
        for matka in lista:
            if vertmatka.depart == matka.depart:
                continue
            if vertmatka.price < matka.price:
 
                vertmatka.swap(matka)
       
def main():
    """skreipataan Matkahuollon sivuilta aikataulut"""
   
    lahto = "kuopio"
    #jyväskylä = jyv%E4skyl%E4
    saapu = "lahti"
    paiva = "4"
    kk = "4"
    vuosi = "2013"
   
    url = "http://www.matkahuolto.info/lippu/fi/connectionsearch?lang=fi&departureStopAreaName="+lahto+"&arrivalStopAreaName="+saapu+"&allSchedules=0&departureDay="+paiva+"&departureMonth="+kk+"&departureYear="+vuosi+"&stat=1&extl=1&search.x=-331&search.y=-383&ticketTravelType=0"
 
    # Haetaan html-tiedosto, luodaan lxml-olio:
    try:
        root = html.parse(url)
    except IOError:
        print "Skreippaaminen ep?onnistui"
        return
 
    rows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//table[2]//tr")
   
    TeeMatka(rows)
   
    #Tätä voi käyttää testatakseen, että varmasti menee suuruusjärkkään
#    for matka in matkatLista:
#        matka.price = random.randint(1,100)
 
    #Näillä voi testata että listassa pysyy myös samanhintaisten matkojen kohdalla
    #lähtöaika järjestys
#    matkatLista[0].price = 5
#    matkatLista[3].price = 5
#    matkatLista[5].price = 5
#    matkatLista[6].price = 5
   
    for matka in matkatLista:
        matka.tulosta()
   
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print "X NYT SITTE KAIKKI SUURUUSJÄRKÄÄN!!!! X"
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \n"
   
    HintaJarjestys(matkatLista)
 
 
    for matka in matkatLista:
        matka.tulosta()
 
if __name__ == "__main__":
    main()

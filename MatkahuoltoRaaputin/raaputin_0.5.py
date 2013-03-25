# -*- coding:utf-8 -*-
'''
Created on Mar 25, 2013

@author: Juuso Tenhunen
'''
from lxml import html
     
def main():
    
    lahto = "kuopio"
    #HUOM!
    #jyväskylä = jyv%E4skyl%E4
    saapu = "jyv%E4skyl%E4"
    paiva = "26"
    kk = "3"
    vuosi = "2013"
       
    url = "http://www.matkahuolto.info/lippu/fi/connectionsearch?lang=fi&departureStopAreaName="+lahto+"&arrivalStopAreaName="+saapu+"&allSchedules=0&departureDay="+paiva+"&departureMonth="+kk+"&departureYear="+vuosi+"&stat=1&extl=1&search.x=-331&search.y=-383&ticketTravelType=0"
     
    # Haetaan html-tiedosto, luodaan lxml-olio:
    try:
        
        root = html.parse(url)
        
    except IOError:
        print "Skreippaaminen epäonnistui"
        return


    rows = root.xpath("//table//tr[last()]/td[last()]//tr[1]//table[2]//tr")
        
    #käydään rivit läpi, ensimmäistä lukuunottamatta
    for row in rows[1:]:
            
        children = row.getchildren()
        #Jos lasten lukumäärä on 7, kyseessä on Bussin "Vaihto" -rivi, tälle
        #pitää tehdä hiemän erilaiset operaatiot
        if len(children) == 7:
            linja = children[6].text_content() #Vaihto-linjan nimi
            dura = children[5].text_content() #tämä tulostaa vain "vaihto"
            print "%s | %s" % (dura.strip(), " ".join(linja.split()))
            continue
               
        depart = children[1].text_content() #lähtöaika
        arriv = children[3].text_content() #saapumisaika
        dock = children[4].text_content() #laituri
        dura = children[5].text_content() #matkan kesto
        linja = children[6].text_content() #linjan nimi
        price = children[10].text_content() #matkan hinta
        #Tulostetaan poimitut tiedot
        print "%s | %s | %s | %s | %s | %s" % (depart, arriv, dock, dura, linja, price)
            
if __name__ == "__main__":
    main()
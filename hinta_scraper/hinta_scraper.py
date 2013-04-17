# -*- coding:utf-8 -*-
'''
Created on 8.4.2013

Scraper, jolla haetaan eri polttoaineiden litrahinnat (95E10, 98E ja diesel) Polttoaine.net-sivulta.
Haetut hinnat ovat keskihintoja.


@author: Peter R
'''


from lxml import html


def main():
    ''' Pääfunktio alkaa tästä '''
    
    
    # Haetaan täältä polttoaineen keskihinta
    url_bensa = "http://www.polttoaine.net/"
    
    # Haetaan html-tiedosto, luodaan lxml-olio:
    try:
        root_bensa = html.parse(url_bensa)
    except IOError:
        print "Polttoaineen tietojen skreippaaminen ep�onnistui"
        return
    
    
    # Polttoainehintojen hakeminen (haetaan Polttoaine.net-sivulta)
    # Hinnat ovat järjestyksessä 95E10, 98E, Diesel   
    hinnat = root_bensa.xpath("//table[@id='Halvin_Kallein']//tr[2]//td[position()>2]")
    

    # Kokeillaan hintojen tulostamista (testausta)    
    print(" 95E10: " + hinnat[0].text_content() + " €/litra")
    print(" 98E: " + hinnat[1].text_content() + " €/litra")
    print(" Diesel: " + hinnat[2].text_content() + " €/litra")
    
if __name__ == "__main__":
    main()
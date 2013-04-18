# -*- coding:utf-8 -*-
'''
Created on 8.4.2013

Scraper, jolla haetaan eri polttoaineiden litrahinnat (95E10, 98E ja
diesel) Polttoaine.net-sivulta. Haetut hinnat ovat keskihintoja.
Hinnat ovat edellisen päivän keskihintoja. Hinnat päivitetään
viiden päivän välein nettisivulle.

@author: Peter R
'''

from lxml import html

import urllib

def hae_hinta():
    '''
        Funktio hakee polttoaineiden keskihinnat (€/litra) polttoaine.net-sivulta.
        Palautetaan lista, jossa
            hinnat[0] = 95E10:n hinta
            hinnat[1] = 98E:n hinta
            hinnat[2] = dieselin hinta
        
    '''

    # Haetaan täältä polttoaineen keskihinta
    url_bensa = "http://www.polttoaine.net/"

    site = urllib.urlopen(url_bensa)

    # Haetaan html-tiedosto, luodaan lxml-olio. Funktio palauttaa
    # poikkeuksen, jos kaikki ei mene putkeen
    root_bensa = html.parse(site)

    # Polttoainehintojen hakeminen (haetaan Polttoaine.net-sivulta)
    # Hinnat ovat järjestyksessä 95E10, 98E, Diesel
    hinnat = root_bensa.xpath("//table[@id='Halvin_Kallein']//tr[2]//td[position()>2]")

    # Tarkistetaan saatiinko screipattua mitään
    if (len(hinnat) < 1):
        print ("Polttoainehintoja ei saatu screipattua")

    # Palautetaan haetut hinnat
    return hinnat

def main():
    ''' Pääfunktio alkaa tästä, testataan löytyivätkö hinnat'''

    hinnat = hae_hinta()

    # Kokeillaan hintojen tulostamista (testausta)
    print(" 95E10: " + hinnat[0].text_content() + " €/litra")
    print(" 98E: " + hinnat[1].text_content() + " €/litra")
    print(" Diesel: " + hinnat[2].text_content() + " €/litra")

if __name__ == "__main__":
    main()

# -*- coding:utf-8 -*-
'''
Created on 8.4.2013

Scraper, jolla haetaan eri polttoaineiden litrahinnat (95E10, 98E ja
diesel) Polttoaine.net-sivulta. Haetut hinnat ovat keskihintoja.
Hinnat ovat edellisen päivän keskihintoja. Hinnat päivitetään
viiden päivän välein nettisivulle.

@author: Peter R
'''
"""
 This file is part of Millä Matkaan.

    Millä Matkaan is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Millä Matkaan is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Millä matkaan.  If not, see <http://www.gnu.org/licenses/>.

"""

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
    hinnat_scrape = root_bensa.xpath("//table[@id='Halvin_Kallein']//tr[2]" +
                              "//td[position()>2]")

    # Tarkistetaan saatiinko screipattua mitään
    if (len(hinnat_scrape) < 1):
        return None

    # Luodaan taulukko, joka sisältää hinnat
    hinnat = [float(hinnat_scrape[0].text_content()),
              float(hinnat_scrape[1].text_content()),
              float(hinnat_scrape[2].text_content())]

    # Palautetaan haetut hinnat
    return hinnat

def main():
    ''' Pääfunktio alkaa tästä, testataan löytyivätkö hinnat'''

    hinnat = hae_hinta()

    # Kokeillaan hintojen tulostamista (testausta)
    print(" 95E10: " + str(hinnat[0]) + " €/litra")
    print(" 98E: " + str(hinnat[1]) + " €/litra")
    print(" Diesel: " + str(hinnat[2]) + " €/litra")

if __name__ == "__main__":
    main()

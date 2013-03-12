# -*- coding:utf-8 -*-
# Esimerkki lxml-moduulin käytöstä skreippaamisessa.
# Aleksi Pekkala 12.3.2013

from lxml import html


def main():
    """Skreipataan siskonmakkarakeiton ravintoarvot.

    HUOM! Tällaiset kommentit eli docstringit saa tulkissa näkyville
    komennolla "help(main)". Esim. lxml:n dokumentteja voisi tutkia komennolla
    "help(lxml)", ja kaikki lxml-moduulin funktiot näkyvät komennolla
    "dir(lxml)".
    """
    url = "http://www.fineli.fi/food.php?foodid=7617&lang=fi"

    # Haetaan html-tiedosto, luodaan lxml-olio:
    try:
        root = html.parse(url)
    except IOError:
        print "Skreippaaminen epäonnistui"
        return

    print "Siskonmakkarakeiton ravintoarvot:"

    # Valitaan sivulta tietyt tr-elementit, nämä selviävät sivun lähdekoodia
    # tutkimalla. Esim. Chromen kehitystyökalut tai Firefoxin Firebug-lisäosa
    # + pythonilla interaktiivisessa tulkissa testaileminen auttavat tässä.
    # Elementtejä voi valita eri tavoin, tässä käytetään xpath-merkkauskieltä,
    # josta löytyy dokumentaatiota mm. täältä: http://www.w3schools.com/xpath/
    rows = root.xpath("//table[2]//td[2]//tr[last()]//tr")

    for row in rows:
        # Jos elementin luokka ei ole "odd" tai "even", skipataan:
        if not row.attrib["class"] in ["odd", "even"]:
            continue

        # Poimitaan ravintoaineen nimi, pitoisuus ja yksikkö rivielementin
        # lapsielementeistä:
        children = row.getchildren()
        # text_content() poimii elementin ja kaikkien lapsielementtien tekstit
        name = children[0].text_content()
        # text poimii vain elementin oman tekstin; tässä korvataan myös "\xa0"
        # eli html-välilyönti normaalilla välilyönnillä
        quantity = children[1].text.replace(u"\xa0", " ")
        unit = children[2].text.replace(u"\xa0", " ")

        # Tulostetaan poimitut tiedot:
        print "%s: %s %s" % (name, quantity, unit)


if __name__ == "__main__":
    main()

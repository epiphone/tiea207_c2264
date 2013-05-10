# -*-coding:utf-8-*-
# Esimerkki VR:n sivujen skreippaamisesta.
#
# Tulostaa tietoja yhteyksistä, joita löytyy kun välinä on
# Rovaniemi - Oulu ja lähtöaikana 10.5.2013 20:00.
#
# Tästä puuttuu poikkeusten käsittely yms.


from lxml import html
import urllib2


def main():
    # Alustetaan http-avaaja cookie-käsittelijän kanssa;
    # nyt opener toimii selaimen tavoin:
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

    url = tee_url("rovaniemi", "oulu", 20, 00, "10.05.2013")

    root = html.parse(opener.open(url))

    # Lista kaikista yhteyksistä
    rows = root.xpath("//table[@id='buyTrip_1']/tbody")

    for row in rows:
        yleiset = row.getchildren()[0].getchildren()  # Yhteyden yleiset tiedot

        laika = yleiset[0].text.strip()
        saika = yleiset[1].text.strip()
        vaihtoja = yleiset[2].text.strip()
        kesto = yleiset[3].text.strip()

        tuloste = "Lahtoaika: %s | Saapumisaika: %s | Vaihtoja: %s | Kesto: %s"
        print tuloste % (laika, saika, vaihtoja, kesto)


def tee_url(mista, mihin, lahtoh, lahtomin, lahtopvm):
    """Palauttaa hakuehtoja vastaavan URLin VR:n sivuille."""
    # TODO: käsittele myös saapumisaika, validoi parametrit

    url = ("https://shop.vr.fi/onlineshop/JourneySearch.do?"
          "basic.fromStationVR=%s&basic.toStationVR=%s&"
          "basic.departureDate.hours=%d&basic.departureDate.mins=%d&"
          "basic.departureDate.date=%s%s")
    loppu = ("&basic.passengerNumbers%5B0%5D.passengerType=84&"
            "basic.passengerNumbers%5B0%5D.passengerAmount=1")
    return url % (mista, mihin, lahtoh, lahtomin, lahtopvm, loppu)


if __name__ == "__main__":
    main()

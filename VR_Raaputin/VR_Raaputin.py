# -*- coding:utf-8 -*-
# VR:än sivujen skreipperi.
# Lasse Wallden
# 10.4.2013

import urllib
from lxml import html
import webbrowser

# muodostetaan URL hakuehtojen perusteella
def muodosta_url(mista, minne, lahto_tunnit, lahto_minuutit, lahto_pvm):
        # url on muodossa "https://shop.vr.fi/onlineshop/JourneySearch.do?request_locale=fi&basic.fromStationVR=Kerava&basic.toStationVR=Tampere&basic.oneWay=true&basic.departureDate.hours=10&basic.oneWay=true&basic.departureDate.mins=42&basic.departureDate.date=31.05.2013&basic.outwardTimeSelection=true&basic.passengerNumbers%5B0%5D.passengerType=84&basic.passengerNumbers%5B0%5D.passengerAmount=1&basic.fiRuGroup=false&basic.campaignCode="
        urli = "https://shop.vr.fi/onlineshop/JourneySearch.do?request_locale=fi&basic.fromStationVR=" + mista + "&basic.toStationVR=" + minne + "&basic.oneWay=true&basic.departureDate.hours=" + lahto_tunnit + "&basic.oneWay=true&basic.departureDate.mins=" + lahto_minuutit + "&basic.departureDate.date=" + lahto_pvm + "&basic.outwardTimeSelection=true&basic.passengerNumbers%5B0%5D.passengerType=84&basic.passengerNumbers%5B0%5D.passengerAmount=1&basic.fiRuGroup=false&basic.campaignCode="       
        print "Annettu URL on: " + urli
        print "*********"
        print "Yritetaan avata URL..."
        # Avataan selaimessa URLin toimivuuden testaamiseksi
        webbrowser.open_new(urli)
        return urli

def main():

    # testaamisen vuoksi, syötetään hakuehdot käsin
    mista = raw_input("Mista lahdet?")
    minne = raw_input("Minne menet?")
    lahto_tunnit = raw_input("Lahtoajan tunnit(01-23):")
    lahto_minuutit = raw_input("Lahtoajan minuutit:(00-59)")
    lahto_pvm = raw_input("Lahdon paivamaara (muodossa XX.YY.ZZZZ):")

    urli = muodosta_url(mista, minne, lahto_tunnit, lahto_minuutit, lahto_pvm)
    site = urllib.urlopen(urli).read()
    root = html.document_fromstring(site)
    # Katsotaan, mitä ollaan saatu irti
    print root.text_content()
    #iidee = "buyTrip_1"
    #taulukko = root.get_element_by_id(iidee, iidee)
    #print taulukko.text_content()

if __name__ == "__main__":
    main()
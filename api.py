import os
import requests
from bs4 import BeautifulSoup
import time

if not os.path.exists("COOKIE"):
    os.mkdir("COOKIE")


def getstr(src, start, end):
    start_index = src.find(start)
    if start_index != -1:
        end_index = src.find(end, start_index)
        if end_index != -1:
            return src[start_index + len(start) : end_index]

    return ""


def getstr_all(src, start, end):
    result = []
    offset = 0

    while True:
        start_pos = src.find(start, offset)
        end_pos = src.find(end, start_pos + len(start))

        if start_pos == -1 or end_pos == -1:
            break

        result.append(src[start_pos + len(start) : end_pos])
        offset = end_pos + len(end)

    return result


ii = {"cookie": str(hash(os.urandom(10))) + ".txt"}

d1 = os.getcwd()
d = d1.replace("\\", "/")

session = requests.session()
g1 = session.get("https://www.city-data.com/indexes/cities/")

CitiesList = getstr(
    g1.text,
    'class="dropdown-menu states-grid-dropdown"><table',
    "</tbody></table></ul></li>",
)

Cities = getstr_all(g1.text, 'href="/city/', '.html">')
totalCities = len(Cities)
print(f"Total Cities: {totalCities}")

for i in range(1):
    currentState = Cities[i]
    print(f"Current State: {currentState}\n\n")

    g = session.get(f"https://www.city-data.com/city/{currentState}.html")

    BigCitiesList = getstr(
        g.text, "<table class='tabBlue tblsort tblsticky' id='cityTAB'>", "</table>"
    )

    soup = BeautifulSoup(BigCitiesList, "html.parser")

    aElements = soup.find_all(
        "a", href=lambda href: href and not href.startswith("javascript:l")
    )

    countBigCities = 0
    for aElement in aElements:
        City_0 = aElement["href"]
        City = City_0.replace(".html", "")
        countBigCities += 1

        print(f"Current City: {City}")

        g = session.get(f"https://www.city-data.com/city/{City}.html")
        rawResult_2 = g.text

        ZipCodes = getstr(
            rawResult_2,
            '<section id="zip-codes" class="zip-codes" data-toc-header="Zip codes">',
            "</section>",
        )
        Zipcode = getstr_all(ZipCodes, '<a href="/zips/', '.html">')
        Zipcode = str(Zipcode).rstrip()

        if not Zipcode:
            Zipcode = getstr(ZipCodes, "<p><b>Zip codes:</b> ", ".</p>")

        MedianIncomes = getstr(
            rawResult_2,
            '<section id="median-income" class="median-income" data-toc-header="Income">',
            "</section>",
        )
        MedianIncome = getstr(
            MedianIncomes,
            "<b>Estimated median household income",
            "<div class='hgraph'><table>",
        )

        soupp = BeautifulSoup(MedianIncome, "html.parser")
        MedianIncome = soupp.get_text().rstrip()

        PopDens = getstr(
            rawResult_2,
            '<section id="population-density" class="population-density">',
            "</section>",
        )
        PopDen = getstr(PopDens, "<p><b>Land area:</b> ", " <b>square miles.")

        BigCoords = getstr(
            rawResult_2, '<section id="coordinates" class="coordinates">', "</section>"
        )
        BigCoord = getstr(BigCoords, "<p>", "</p>")
        BigCoord = BigCoord.split(",")
        lat = BigCoord[0].replace("<b>Latitude:</b> ", "").replace("<b>", "")
        long = BigCoord[1].replace(" Longitude:</b>", "")

        print(f"Zipcodes: {Zipcode}")
        print(f"Estimated median household income: {MedianIncome}")
        print(f"Land area: {PopDen} square miles")
        print(
            f"Latitude: {lat}, Longitude: {long}\n\n============================================================\n\n"
        )
        countBigCities += 1
        time.sleep(5)

    print(f"Total Number: {countBigCities}\n\n")
    time.sleep(5)

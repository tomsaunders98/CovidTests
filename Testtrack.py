from bs4 import BeautifulSoup
import urllib.request
import re
import tabula
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import json
from PyPDF2 import PdfFileReader
import dateparser
from googletrans import Translator
import pandas as pd
import datetime
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pages = {
    'UK' : 'https://www.gov.uk/guidance/coronavirus-covid-19-information-for-the-public#number-of-cases',
    'USA' : 'https://covidtracking.com/data/',
    'SK': 'https://www.cdc.go.kr/board/board.es?mid=&bid=0030',
    'CAN' : 'https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html',
    'IT' : 'https://github.com/pcm-dpc/COVID-19/tree/master/schede-riepilogative/regioni',
    'NOR' : 'https://www.fhi.no/en/id/infectious-diseases/coronavirus/',
    'DEN': 'https://www.ssi.dk/aktuelt/sygdomsudbrud/coronavirus',
    'AUST' : 'https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html',
    'ICE' : 'https://e.infogram.com/e3205e42-19b3-4e3a-a452-84192884450d?parent_url=https%3A%2F%2Fwww.covid.is%2Fdata&src=embed#',
    'JPN' : 'https://www.mhlw.go.jp/stf/houdou/index.html',
    'SPN' : 'https://covid19.isciii.es/',
    'AUS' : {
        'ACT' : 'https://www.covid19.act.gov.au/',
        'NSW' : 'https://www.health.nsw.gov.au/news/Pages/20200329_01.aspx',
        'QLD' : 'https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/current-status-and-contact-tracing-alerts',
        'WA' : 'https://ww2.health.wa.gov.au/Articles/A_E/Coronavirus/COVID19-statistics',
        'VIC' : 'https://www.dhhs.vic.gov.au/media-hub-coronavirus-disease-covid-19',
        'SA' : 'https://www.sahealth.sa.gov.au/wps/wcm/connect/Public+Content/SA+Health+Internet/About+us/News+and+media/all+media+releases/'
    },
    'AUS1' : 'https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert/coronavirus-covid-19-current-situation-and-case-numbers',
    'CZH' : 'https://onemocneni-aktualne.mzcr.cz/covid-19',
    'EST' : 'https://www.terviseamet.ee/en/covid19',
    'HUN' : 'https://koronavirus.gov.hu/',
    'LAT' : 'https://arkartassituacija.gov.lv/',
    'LIT' : 'https://sam.lrv.lt/lt/naujienos/koronavirusas',
    'NED' : 'https://www.rivm.nl/coronavirus/covid-19/informatie-voor-professionals/virologische-dagstaten',
    'RO' : 'https://www.mai.gov.ro/category/comunicate-de-presa/',
    'RUS' : 'https://rospotrebnadzor.ru/about/info/news/',
    'SRB' : 'https://www.zdravlje.gov.rs/sekcija/345852/covid-19.php',
    'SVK' : 'https://mojeezdravie.nczisk.sk/api/v1/ezdravie-stats-proxy-api.php', #api for https://www.korona.gov.sk/
    'SLI' : 'https://www.nijz.si/sl/dnevno-spremljanje-okuzb-s-sars-cov-2-covid-19/',
    'SWE' : 'https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/',
    'SWI' : 'https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html',
    'FRA' : 'https://www.santepubliquefrance.fr/maladies-et-traumatismes/maladies-et-infections-respiratoires/infection-a-coronavirus/articles/infection-au-nouveau-coronavirus-sars-cov-2-covid-19-france-et-monde'

}
monthindanish = {
    'marts' : 'march',
    'april' : 'april',
    'maj' : 'may',
    'juni' : 'june',
    'juli' : 'july'
}
def clearstring(number,date):
    regex = re.compile('[^a-zA-Z0-9 -:.]')
    regex2 = re.compile('[^0-9]')
    number = str(number)
    date = str(date)
    print(number)
    number = regex2.sub('', number)
    date = regex.sub('', date)
    print(date)
    print(number)
    date = dateparser.parse(date)
    return int(number), date


def TrackChanges(Country):
    if Country == "UK":
        page = urllib.request.urlopen(pages["UK"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find(id="number-of-cases-and-deaths").next_element.next_element.next_element.string
        testnumber = re.findall('[0-9,]+', text)[3]
        testdate = ' '.join(text.split(" ")[4:6])
    if Country == "USA":
        page = urllib.request.urlopen(pages["USA"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = int(re.sub(r"[^a-zA-Z0-9 /]", "", soup.find(class_="total-info").previous_element.string))
        text = soup.find(class_="updated").string.split(" ")
        testdate = text[5]
    if Country == "SK":
        page = urllib.request.urlopen(pages["SK"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("span", string=re.compile("updates")).parent['href']
        page = urllib.request.urlopen("https://www.cdc.go.kr" + text)
        soup = BeautifulSoup(page, 'html.parser')
        testdate = soup.find("li").find("b").string
        testnumber = soup.find("tbody").findAll("tr")[3].findAll("td")[1].find("p").string
    if Country == "CAN" :
        page = urllib.request.urlopen(pages["CAN"])
        soup = BeautifulSoup(page, 'html.parser')
        testdate = soup.find("table").find("caption").string
        testdate = testdate.replace("\r", "")
        testdate = testdate.replace("\n", "")
        print(testdate.split())
        testdate = ' '.join(testdate.split()[11:14])


        testnumber = soup.find("td").string
    if Country == "IT":
        page = urllib.request.urlopen(pages["IT"])
        soup = BeautifulSoup(page, 'html.parser')
        text1 = soup.findAll("tr")[-1].findAll("td")
        testdate = text1[2].find("a").string
        text = "https://github.com" + text1[1].find("a")['href']
        downloadtext = text.replace("blob", "raw")
        tables = tabula.read_pdf(downloadtext)
        testnumber = tables[0].iloc[23, 8]
        if len(str(testnumber)) > 8:
            testnumber = ''.join(list(str(testnumber))[:7])
    if Country == "NOR":
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(pages["NOR"], headers=hdr)
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, 'lxml')
        testnumber = soup.find("div", class_="fhi-key-figure-number").get_text()
        testdate = " ".join(soup.find("div", class_="fhi-key-figure-desc").get_text().split(" ")[7:9])
    if Country == "DEN":
        page = urllib.request.urlopen(pages["DEN"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = soup.findAll("td")[1].get_text()
        text = ' '.join(soup.findAll("p")[3].get_text().split(" ")[12:14])
        testdate = ' '.join([monthindanish.get(word, word) for word in text.split()])
    if Country == "AUST":
        page = urllib.request.urlopen(pages["AUST"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = ''.join(soup.findAll("p")[3].get_text().split()[-1])
        testdate = soup.find("span", class_="supertitle").get_text()
    if Country == "JPN":

        page = urllib.request.urlopen(pages["JPN"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("ul", class_="m-listLinkMonth").findAll("li")[-1].find("a")['href']
        print(text)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        page = urllib.request.urlopen(text)
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.findAll("ul", class_="m-listNews")#[1].find("span", string=re.compile("日版")).parent.parent['href']
        done = False
        for link in text:
            if not done:
                try:
                    text = link.find("span", string=re.compile("日版")).parent.parent['href']
                except:
                    continue
                done = True
        if not text:
            return "No data"
        print(text)
        page = urllib.request.urlopen("https://www.mhlw.go.jp/" + text)
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("div", class_="m-grid__col1").find("img")['src']
        #print(url)
        #urllib.request.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        urllib.request.urlretrieve(text, 'image.jpg')
        testnumber = pytesseract.image_to_string(Image.open("image.jpg")).split()
        for test in testnumber:
            if re.match("^[0-9,.]*$", test) != None:
                testnumber = test
        testdate = soup.find("p", class_="m-boxInfo__date").find("time")['datetime']
        #translator = Translator()
        #text = translator.translate(text)
        #testdate = " ".join(text.text.split(" ")[3:5])
    if Country == "CZH":
        page = urllib.request.urlopen(pages["CZH"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = soup.find(id="count-test").string
        text = soup.find(id="last-modified-tests").string.split(" ")
        print(text)
        testdate = ''.join(text[0:3])
        testdate = re.sub('[^0-9 .]','',testdate).strip()
        print(testdate)
    if Country == "EST":
        page = urllib.request.urlopen(pages["EST"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = ''.join(soup.find("div", class_="static static-infobox02").find("ul").findAll("li")[1].find("strong").string.split()[2:4])

        testdate = soup.find("div", class_="field-item even").findAll("p")[-1].get_text()
        testdate = testdate.replace("Last updated", "")
    if Country == "HUN":
        page = urllib.request.urlopen(pages["HUN"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = soup.findAll("span", class_="number")[3].string
        testdate = soup.findAll("div", class_="well-lg text-center")[1].find("p").string
        testdate = ''.join(re.sub('[^0-9 -.]','',testdate ).strip().split()[0])
    if Country == "LAT":
        page = urllib.request.urlopen(pages["LAT"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("div", class_="_1mf _1mj").find("p").get_text()
        testnumber = re.findall('[0-9]+', text)[3]
        testdate = soup.find("div", class_="article text").get_text().split(" ")[2]
    if Country == "LIT":
        page = urllib.request.urlopen(pages["LIT"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("div", class_="text").findAll("li")[5].string
        testnumber = re.findall('[0-9]+', text)
        testdate = soup.find("div", class_="date").string.split(" ")[3]
    if Country == "NED":
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(pages["NED"], headers=hdr)
        try:
            page = urllib.request.urlopen(req)
        except:
            return "No data"
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("table").findAll("td")[7:-1]
        testnum = 0
        for i in range(0, len(text)):
            if i % 5 == 0:
                testnum = int(text[i].get_text()) + testnum
        testnumber = testnum
        testdate = soup.find("table").findAll("tr")[-1].find("td").get_text()
    if Country == "RO":
        page = urllib.request.urlopen(pages["RO"])
        soup = BeautifulSoup(page, 'html.parser')
        url = soup.find("a", string=re.compile("Informare COVID"))['href']
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        testdate = soup.find("span", class_="posted-on").find("time")['datetime']
        text = soup.find("div", class_="entry-content").find("p", string=re.compile("^Până la această dată")).string
        testnumber = ''.join(re.findall('[0-9]+', text)[0:2])
    if Country == "RUS":
        page = urllib.request.urlopen(pages["RUS"])
        soup = BeautifulSoup(page, 'html.parser')
        url = soup.find("a", string=re.compile("Информационный"))['href']
        page = urllib.request.urlopen("https://rospotrebnadzor.ru" + url)
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("p", string=re.compile("лабораторных")).string
        text = re.findall('[0-9]+', text)
        testdate = ''.join(text[0:3])
        testnumber = ''.join(text[3:5])
    if Country == "SRB":
        page = urllib.request.urlopen(pages["SRB"])
        soup = BeautifulSoup(page, 'html.parser')
        url = soup.find("h1", class_="press-title").find("a")['href']
        page = urllib.request.urlopen("https://www.zdravlje.gov.rs/" + url)
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("div", class_="article-date").string
        translator = Translator()
        testdate = translator.translate(text).text
        text = soup.findAll("div", class_="printable")[-1].findAll("p")[-1].string
        testnumber = re.findall('[0-9]+', text)[-1]
    if Country == "SVK":
        page = urllib.request.urlopen(pages["SVK"])
        soup = BeautifulSoup(page, 'html.parser')
        text = json.loads(str(soup))
        testnumber = int(text["tiles"]["k26"]["data"]["d"][-1]["v"]) + int(text["tiles"]["k25"]["data"]["d"][-1]["v"])
        testdate = list(text["tiles"]["k26"]["data"]["d"][-1]["d"])[-3:]
        testdate.insert(1, '/')
        testdate = ''.join(testdate)


    if Country == "SLI":
        page = urllib.request.urlopen(pages["SLI"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.findAll("div", class_="field-item even")[2].find("p").string
        regex = re.compile('[^a-zA-Z0-9 -:.]')
        print(text)
        test = re.findall('[0-9. ]+', text)
        print(test)
        testdate = ''.join(test[0])
        testnumber = ''.join(test[5]).strip()
        print(testnumber)
    # if Country == "SWE": Weekly updates, easier just to get them by hand
    #     page = urllib.request.urlopen(pages["SWE"])
    #     soup = BeautifulSoup(page, 'html.parser')
    #     orig = soup.find("div", id="content-primary").findAll("h2")[1]
    #     text = orig.string
    #     text = re.findall("\((.*?)\)", text)[0]
    #     translator = Translator()
    #     text = translator.translate(text)
    #     testdate = ' '.join(text.text.split(" ")[0:3])
    #     text = soup.find("div", id="content-primary").find("ul")[1]
    #     data = text.findAll("li")
    #     text = [re.findall("Totalt har drygt", line) for line in data]
    #     for i in range(0, len(data)):
    #         if text[i]:
    #             testnumber = ''.join(re.findall('[0-9]+', data[i]))
    if Country == "SWI":
        page = urllib.request.urlopen(pages["SWI"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("a", class_="icon icon--before icon--pdf")['href']
        downloadtext = "https://www.bag.admin.ch" + text
        urllib.request.urlretrieve(downloadtext, 'doc.pdf')
        pdf = PdfFileReader('doc.pdf')
        page = pdf.getPage(0)
        words = page.extractText().split()
        done = False
        for i in range(0, len(words)):
            if words[i] == "ca.":
                testnumber = ''.join(words[i + 1:i + 3])
            if words[i] == "Stand" and not done:
                testdate = ''.join(words[i + 1:i + 4])
                done = True
    if Country == "FRA":
        page = urllib.request.urlopen(pages["FRA"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("div", class_="content__insert-content").findAll("a")[1]['href']
        url = "https://www.santepubliquefrance.fr" + text
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("a", class_="button button--pdf")['href']
        heading = soup.find("h1").string
        heading = heading.replace(" ", "")
        heading = heading.replace(":", "")
        url = "https://www.santepubliquefrance.fr" + text
        urllib.request.urlretrieve(url, 'france/' + heading + '.pdf')
    testnumber, testdate = clearstring(testnumber, testdate)
    return testnumber,testdate


def adddata(country, date, number):
    if date == "No data" or number == "No data":
        return "No data"
    basedata = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0,4):
        d = datetime.timedelta(days=i)
        dt = datetime.datetime.today()
        dt = dt - d
        datestring = f'{dt.day}/{dt.month}/{dt.year}'
        testdatestring = f'{date.day}/{date.month}/{date.year}'
        testdata = pd.read_csv("Testnumbers.csv")
        if datestring not in testdata.columns:
            testdata.insert(len(testdata.columns), datestring, basedata)
        value = testdata.loc[testdata["Country"] == country, [datestring]].values[0]
        print(value)
        if datestring == testdatestring:
            if value == 0:
                testdata.loc[testdata["Country"] == country, [datestring]] = number
        testdata.to_csv("Testnumbers.csv", index=False)
    return testdata



#
countries = ['UK','USA','SK','CAN','IT','NOR','DEN','AUST','JPN','CZH','EST','HUN','LAT','LIT', 'RO','RUS','SRB','SVK','SLI','SWI']



for country in countries:
    print(country)
    changes = TrackChanges(country)
    if changes != "No data":
        print(changes)
        td = adddata(country, changes[1], changes[0])
        print(td)














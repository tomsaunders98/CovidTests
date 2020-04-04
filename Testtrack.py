import urllib.request, re, tabula, pytesseract, json, dateparser, datetime, pandas as pd, numpy as np, sys, logging, math
from bs4 import BeautifulSoup
try:
    from PIL import Image
except ImportError:
    import Image
from PyPDF2 import PdfFileReader
from googletrans import Translator
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#Formating logging
logging.basicConfig(filename='Trackoutput.log')




monthindanish = {
    'marts' : 'march',
    'april' : 'april',
    'maj' : 'may',
    'juni' : 'june',
    'juli' : 'july'
}
testdata = pd.read_csv("Testnumbers.csv")
pages = pd.Series(testdata.Link.values, testdata.Country.values).to_dict()

def clearstring(number,date):
    regex = re.compile('[^a-zA-Z0-9 -:.]')
    regex2 = re.compile('[^0-9]')
    number = str(number)
    date = str(date)
    number = regex2.sub('', number)
    date = regex.sub('', date)
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
        testnumber = soup.find("table").findAll("td")[-1].string
        testdate = soup.find(class_="info-content").string
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
        testdate = soup.find("table", class_="table table-bordered table-condensed").find("caption").string
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
        page = urllib.request.urlopen("https://www.mhlw.go.jp/" + text)
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("div", class_="m-grid__col1").find("img")['src']
        urllib.request.urlretrieve(text, 'image.jpg')
        testnumber = pytesseract.image_to_string(Image.open("image.jpg")).split()
        for test in testnumber:
            if re.match("^[0-9,.]*$", test) != None:
                testnumber = test
        testdate = soup.find("p", class_="m-boxInfo__date").find("time")['datetime']
    if Country == "CZH":
        page = urllib.request.urlopen(pages["CZH"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = soup.find(id="count-test").string
        text = soup.find(id="last-modified-tests").string.split(" ")
        testdate = ''.join(text[0:3])
        testdate = re.sub('[^0-9 .]','',testdate).strip()
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
        page = urllib.request.urlopen(req)
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
        test = re.findall('[0-9. ]+', text)
        testdate = ''.join(test[0])
        testnumber = ''.join(test[5]).strip()
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
    try:
        testnumber
        testdate
    except NameError:
        return 0
    testnumber, testdate = clearstring(testnumber, testdate)
    return testnumber,testdate


def adddata(country, date, number):
    for i in range(0,4):
        d = datetime.timedelta(days=i)
        dt = datetime.datetime.today()
        dt = dt - d
        datestring = f'{dt.day}/{dt.month}/{dt.year}'
        testdatestring = f'{date.day}/{date.month}/{date.year}'
        if datestring not in testdata.columns:
            testdata.insert(6, datestring, np.nan)
        empty = math.isnan(testdata.loc[testdata["Country"] == country, [datestring]].values[0])
        lastvalue = testdata.loc[testdata["Country"] == country]
        lastvalue = lastvalue.iloc[:, 6:-1].max(axis=1, numeric_only=True).values[0]
        if number < lastvalue:
            raise Exception(f"Tests cannot decrease for {country}, largest value is {lastvalue} and attempting to add {number}")
        if datestring == testdatestring and empty:
            testdata.loc[testdata["Country"] == country, [datestring]] = number
            msg = f'Updated {country} at {testdatestring} with {number}'
            print(msg)
            logging.info(msg)
        testdata.to_csv("Testnumbers.csv", index=False)



def mainquery():
    print("Enter country code:")
    x = input()
    print("-------------------------------")
    badcountry = []
    if x != "":
        countries = [x]
    else:
        countries = testdata['Country'].values
    for country in countries:
        try:
            changes = TrackChanges(country)
        except AttributeError as e:
            msg = f"Code for {country} changed:"
            badcountry.append([country, msg, e])
            logging.error('Error at %s', 'division', exc_info=e)
            continue
        except urllib.error.URLError as e:
            msg = f"Potentially blocked from {country}'s website:"
            badcountry.append([country, msg, e.reason])
            logging.error('Error at %s', 'division', exc_info=e)
            continue
        except ValueError as e:
            msg = f"Code for {country} changed: (testnumber not number)"
            badcountry.append([country, msg, e])
            logging.error('Error at %s', 'division', exc_info=e)
            continue
        except Exception as e:
            msg = f"Couldn't find numbers for {country}, unclear why"
            badcountry.append([country, msg, e])
            logging.error('Error at %s', 'division', exc_info=e)
            continue
        if changes == 0:
            msg  = f"No instructions for {country}"
            e = "None"
            badcountry.append([country, msg, e])
            logging.info(msg)
            continue
        else:
            try:
                adddata(country, changes[1], changes[0])
            except Exception as e:
                msg = f'Error adding to database for {country} with value {changes[0]} at {changes[1]}:'
                badcountry.append([country, msg, e])
                logging.error('Error at %s', 'division', exc_info=e)
                continue
    print("-------------------------------")
    if badcountry:
        print("Errors")
        print("-------------------------------")
        for country in badcountry:
            print(country[0])
            print(country[1])
            print(f"Error message:  {country[2]}")
            print("-------------------------------")
    else:
        print("No Errors")
        print("-------------------------------")

if __name__ == '__main__':
    mainquery()
    print("Completed.")











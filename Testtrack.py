import urllib.request, re, tabula, pytesseract, json, dateparser, datetime, pandas as pd, numpy as np, sys, logging, \
    math
from dateparser.search import search_dates
from bs4 import BeautifulSoup

try:
    from PIL import Image
except ImportError:
    import Image
from PyPDF2 import PdfFileReader
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Formating logging
logging.basicConfig(format='%(asctime)-15s %(name)s - %(levelname)s - %(message)s', filename='Trackoutput.log')

# translate months for danish site
monthindanish = {
    'marts': 'march',
    'april': 'april',
    'maj': 'may',
    'juni': 'june',
    'juli': 'july'
}
# load data, create dictionary
testdata = pd.read_csv("Testnumbers.csv")
pages = pd.Series(testdata.Link.values, testdata.Country.values).to_dict()


# parse dates into datetime and numbers into int
def clearstring(number, date):
    regex = re.compile('[^a-zA-Z0-9 -:.]')
    regex2 = re.compile('[^0-9]')
    number = str(number)
    if not isinstance(date, datetime.datetime):
        date = str(date)
        date = regex.sub('', date)
        date = dateparser.parse(date)
    number = regex2.sub('', number)

    return int(number), date


# instructions for scraping websites
def TrackChanges(Country):
    if Country == "UK":
        page = urllib.request.urlopen(pages["UK"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find(id="number-of-cases-and-deaths").next_element.next_element.next_element.string
        testnumber = re.findall('(\d+([\d,]?\d)*(\.\d+)?)', text)[2][0]
        testdate = re.findall('((\d+) April)', text)[0][0]  # a hack but will work for now
    if Country == "USA":
        page = urllib.request.urlopen(pages["USA"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = soup.find("table").find("tbody").findAll("td")[-1].string
        testdate = soup.find("div", class_="infobox-module--content--1toLT").string
    if Country == "SK":
        page = urllib.request.urlopen(pages["SK"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("span", string=re.compile("updates")).parent['href']
        page = urllib.request.urlopen("https://www.cdc.go.kr" + text)
        pages["SK"] = "https://www.cdc.go.kr" + text
        soup = BeautifulSoup(page, 'html.parser')
        testdate = soup.find("li").find("b").string
        testnumber = soup.find("tbody").findAll("tr")[3].findAll("td")[1].find("p").string
    if Country == "CAN":
        page = urllib.request.urlopen(pages["CAN"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("table", class_="table table-bordered table-condensed")
        testdate = search_dates(text.find("caption").string)[0][1]
        testnumber = text.find("td").string
    if Country == "IT":
        page = urllib.request.urlopen(pages["IT"])
        soup = BeautifulSoup(page, 'html.parser')
        text1 = soup.findAll("tr")[-1].findAll("td")
        testdate = text1[2].find("a").string
        text = "https://github.com" + text1[1].find("a")['href']
        downloadtext = text.replace("blob", "raw")
        pages["IT"] = downloadtext
        tables = tabula.read_pdf(downloadtext)
        df = tables[0]
        testnumber = df.iloc[-1,-1]
        print(testnumber)
        if len(str(testnumber)) > 10:
            raise Exception(f"{Country} value of {testnumber} probably too large.")
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
        text = soup.find("div", class_="table-responsive").find("table").find("tbody").findAll("tr")[-1].findAll("td")[-1].string
        print(text)
        testnumber = text
        testdate = soup.find("time").string
    if Country == "JPN":
        page = urllib.request.urlopen(pages["JPN"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("ul", class_="m-listLinkMonth").findAll("li")[-1].find("a")['href']
        page = urllib.request.urlopen(text)
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.findAll("ul",
                            class_="m-listNews")  # [1].find("span", string=re.compile("日版")).parent.parent['href']
        done = False
        for link in text:
            if not done:
                try:
                    text = link.find("span", string=re.compile("日版")).parent.parent['href']
                except:
                    continue
                done = True

        pages["JPN"] = "https://www.mhlw.go.jp/" + text
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
        testdate = re.sub('[^0-9 .]', '', testdate).strip()
    if Country == "EST":
        page = urllib.request.urlopen(pages["EST"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = soup.find("div", class_="static static-simple-2columns clearfix").find("div",
                                                                                            class_="col last").get_text()
        testdate = soup.find("div", class_="field-item even").findAll("p")[-1].get_text()
        testdate = testdate.replace("Last updated", "")
    if Country == "HUN":
        page = urllib.request.urlopen(pages["HUN"])
        soup = BeautifulSoup(page, 'html.parser')
        testnumber = soup.findAll("span", class_="number")[3].string
        testdate = soup.findAll("div", class_="well-lg text-center")[1].find("p").string
        testdate = ''.join(re.sub('[^0-9 -.]', '', testdate).strip().split()[0])
    if Country == "LAT":
        page = urllib.request.urlopen(pages["LAT"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("div", class_="formatedtext text").findAll("p")[3].get_text()
        print(text)
        testnumber = re.findall('[0-9]+', text)[3]
        text = soup.find("div", class_="formatedtext text").find("p").get_text()
        testdate = re.findall('\d+\.\d+\.\d+', text)[0]
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
        text = soup.find("table", id="Corona_tabel").find("tbody").find("tr")
        testdate = text.findAll("td")[2].string
        text1 = text.findAll("td")[1].string
        testnumber = re.findall('\d+\.\d+', text1)[0]
    if Country == "RO":
        page = urllib.request.urlopen(pages["RO"])
        soup = BeautifulSoup(page, 'html.parser')
        url = soup.find("a", string=re.compile("Informare COVID"))['href']
        pages["RO"] = url
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
        pages["RUS"] = "https://rospotrebnadzor.ru" + url
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("p", string=re.compile("лабораторных")).string
        text = re.findall('[0-9]+', text)
        testdate = ''.join(text[0:3])
        testnumber = ''.join(text[3:5])
    if Country == "SRB":
        driver = webdriver.Chrome()
        driver.get(pages["SRB"])
        driver.implicitly_wait(100)
        html = str(driver.find_elements_by_tag_name("html")[0].get_attribute('innerHTML'))
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.find("div", attrs={"data-id":"5eb267c9"}).get_text()
        testdate = re.findall('\d+\.\d+\.\d+', text)[0]
        print(testdate)
        testdate = datetime.datetime.strptime(testdate, '%d.%m.%Y')
        text = soup.find("div", attrs={"data-id":"6bfc932d"}).get_text()
        print(text)
        testnumber = re.findall('\d+\.\d+', text)[-1]
    if Country == "SVK":
        page = urllib.request.urlopen(pages["SVK"])
        soup = BeautifulSoup(page, 'html.parser')
        text = json.loads(str(soup))
        testnumber = int(text["tiles"]["k5"]["data"]["d"][-1]["v"]) + int(text["tiles"]["k6"]["data"]["d"][-1]["v"])
        testdate = list(text["tiles"]["k5"]["data"]["d"][-1]["d"])[-3:]
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
        pages["SWI"] = downloadtext
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
    if Country == "AUS":
        page = urllib.request.urlopen(pages["AUS"])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find("div", class_="bean-block-content").findAll("p")
        testdate = search_dates(text[0].get_text())[0][1]
        testnumber = ''.join(re.findall('[0-9]+', text[1].string)[-2:])
    if Country == "BEL":
        page = urllib.request.urlopen(pages["BEL"])
        soup = BeautifulSoup(page, 'html.parser')
        text = json.loads(str(soup))
        testdate = text[-1]["DATE"]
        text = pd.DataFrame.from_dict(text)
        testnumber = text["TESTS"].sum()
    if Country == "CRO":
        page = urllib.request.urlopen(pages["CRO"])
        soup = BeautifulSoup(page, 'html.parser')
        testdate = search_dates(soup.find("li", class_="time_info").string)[0][1]
        text = soup.find("div", class_="page_content").get_text()
        testnumber = re.findall('(\d+\.\d+ )(?=testiranja)', text)[0]
        print(testnumber)
    if Country == "FIN":  # needtoget selenium for this (javascript blocker)
        driver = webdriver.Chrome()
        driver.get(pages["FIN"])
        driver.implicitly_wait(100)
        html = str(driver.find_elements_by_class_name("journal-content-article")[0].get_attribute('innerHTML'))
        testnumber = re.findall('(\d+([\d,]?\d)*(\.\d+)?)', html)[3][0]
        testdate = re.findall(('<strong>(.*?)</strong>'), html)[0]
        text = testdate.replace('&nbsp;', ' ')
        testdate = search_dates(text)[0][1]
    if Country == "IND":  # certificate verify failed: unable to get local issuer certificate (_ssl.c:1108)
        driver = webdriver.Chrome()
        driver.get(pages["IND"])
        driver.implicitly_wait(100)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        testdate = search_dates(soup.find("a", string=re.compile("Testing: Status Update")).get_text())[0][1]
        url = soup.find("a", string=re.compile("Testing: Status Update"))['href']
        pages["IND"] = url
        urllib.request.urlretrieve(url, 'doc.pdf')
        pdf = PdfFileReader('doc.pdf')
        page = pdf.getPage(0)
        words = page.extractText()
        words = re.findall('(?<=of)(((\d+)|(,)|(\s+))+)(?=samples)', words)[0][0]
        testnumber = re.sub('\s+', "", words)
    if Country == "NZ":
        page = urllib.request.urlopen(pages["NZ"])
        soup = BeautifulSoup(page, 'html.parser')
        testtable = pd.read_html(str(soup.find("th", string="Lab Testing").parent.parent.parent))[0]
        testnumber = testtable.loc[testtable["Lab Testing"] == "Total tested to date", ["Tests"]].values[0]
        testdate = testtable.loc[testtable["Lab Testing"] == "Total tested yesterday", ["Date"]].values[0]
    if Country == "VET":  # might also need selenium
        driver = webdriver.Chrome()
        driver.get(pages["VET"])
        driver.implicitly_wait(100)
        html = str(driver.find_elements_by_tag_name("html")[0].get_attribute('innerHTML'))
        soup = BeautifulSoup(html, 'html.parser')
        testdate = soup.find("small", class_="text-muted1").find("strong").get_text()
        testdate = datetime.datetime.strptime(testdate, '%H:%M %d/%m/%Y')
        testnumber = soup.findAll("span", string=re.compile("Tổng số mẫu đã xét nghiệm cộng dồn:"))[
            0].next_element.next_element.next_element.get_text()

    testnumber, testdate = clearstring(testnumber, testdate)
    return testnumber, testdate


## Data Evaluation and Insertion
def adddata(country, date, number):
    done = False
    for i in range(0, 4):
        d = datetime.timedelta(days=i)
        dt = datetime.datetime.today()
        dt = dt - d

        datestring = f'{dt:%d}/{dt:%m}/{dt.year}'
        testdatestring = f'{date:%d}/{date:%m}/{date.year}'
        if datestring not in testdata.columns:

            testdata.insert(6, datestring, np.nan)
        empty = math.isnan(testdata.loc[testdata["Country"] == country, [datestring]].values[0])
        lastvalue = testdata.loc[testdata["Country"] == country]
        lastvalue = lastvalue.iloc[:, 6:-1].max(axis=1, numeric_only=True).values[0]
        if number < lastvalue:
            raise Exception(
                f"Tests cannot decrease for {country}, largest value is {lastvalue} and attempting to add {number}")
        if datestring == testdatestring and empty:
            testdata.loc[testdata["Country"] == country, [datestring]] = number
            msg = f'Updated {country} at {testdatestring} with {number}'
            print(msg)
            logging.info(msg)
            done = True
        if datestring == testdatestring and not empty:
            raise Exception(f'Attempted to add {number} at {testdatestring} for {country} but cell not empty')
        if i == 3 and not done:
            raise Exception(f'Did not include {country} with value {number} on {testdatestring}. Reason Unknown')
        testdata.to_csv("Testnumbers.csv", index=False)


# Error Handling
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
        except AttributeError as e: #code changed
            badcountry.append([country, e])
            logging.error('Error at %s', 'division', exc_info=e)
            continue
        except urllib.error.URLError as e: #blocked
            badcountry.append([country,  e])
            logging.error('Error at %s', 'division', exc_info=e)
            continue
        except ValueError as e: #code changed
            badcountry.append([country, e])
            logging.error('Error at %s', 'division', exc_info=e)
            continue
        except NameError as e:
            msg = f"No instructions for {country}"
            badcountry.append([country, msg])
            logging.error('Error at %s', 'division', exc_info=e)
            continue
        except Exception as e:
            badcountry.append([country, e])
            logging.error('Error at %s', 'division', exc_info=e)
            continue

        else:
            try:
                adddata(country, changes[1], changes[0])
            except Exception as e:
                badcountry.append([country,  e])
                logging.error('Error at %s', 'division', exc_info=e)
                continue
    print("-------------------------------")
    if badcountry:
        print("Errors")
        print("-------------------------------")
        for country in badcountry:
            print(country[0])
            print(pages[country[0]])
            print(f"Error message:  {country[1]}")
            print("-------------------------------")
    else:
        print("No Errors")
        print("-------------------------------")


if __name__ == '__main__':
    mainquery()
    print("Completed.")

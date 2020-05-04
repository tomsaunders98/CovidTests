# CovidTests
![Tests Per Million](https://github.com/tomsaunders98/CovidTests/raw/master/img/PerMillionBar.png "Tests Per Million")
![Tests Per Million](https://github.com/tomsaunders98/CovidTests/raw/master/img/PerMillionLine.png "Tests Per Million")
(See *Explaning the Data* for information on different data types.)
(*Graphs updated weekly)

This is a **work in progress** to monitor the number of Covid-19 Tests performed by various countries.


## Explaining the Data
The number of Coronavirus tests performed is an important metric of each country's effort to combat the spread of Coronavirus. However, the data on the number of tests completed is often unclear, inconsistent or entirely non-existent. 
For example, Spain has so far released no official data on the number of tests it has performed, despite the fact that regions within Spain are [obliged to provide the government with daily reports on the number of tests completed](https://maldita.es/malditodato/2020/03/23/350000-tests-pruebas-diagnostico-coronavirus-gobierno-hecho-realmente-cambios-criterio/).

On the other hand, Germany and France release their data at extremely irregular intervals. France last officially released data for 24th of March, Germany hasn't released their data since the 20th of March.

Countries are often not clear on exactly what they are measuring when they release the number of tests and  whether this data includes all private tests performed in the country as well.
I have tried to make the data as transparent as possible by including what type of measurement has been used where it is known. There are 3 common types of measurements:

1. **Samples**: The total number of samples analyzed in laboratories. If one person is tested five times it will still count as five tests.
2. **People**: The number of people tested. Even if someone is tested multiple tests it will still only be counted once.
3. **Cases**: The number of cases tested. If one person gets Coronavirus and receives multiple tests it will only be counted once. However, if he gets the virus again it will be counted seperately. 

Whilst this does make it difficult to compare different country's testing efforts it is still informative as long as the caveats in the data are understood. 


## Sources
| Country        | Source Name                                                                                | Source                                                                                                                                                                                                 | ReleaseType        |
|----------------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|
| Australia      | Australian Department of Health                                                            | https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert/coronavirus-covid-19-current-situation-and-case-numbers                                                          | Daily              |
| Austria        | Austrian Ministry for Social Affairs, Health, Care and Consumer Protection                 | https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html                                                                                                 | Daily              |
| Belgium        | Sciensano (Belgian Institute for Health)                                                   | https://epistat.wiv-isp.be/covid/                                                                                                                                                                      | Daily              |
| Canada         | Canadian Government Public Health                                                          | https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html                                                                                                         | Daily              |
| Croatia        | Government Website                                                                         | https://www.koronavirus.hr/najnovije/35                                                                                                                                                                | Daily              |
| Czech Republic | Czech Republic Ministry of Health                                                          | https://onemocneni-aktualne.mzcr.cz/covid-19                                                                                                                                                           | Daily              |
| Denmark        | Statens Serum Institute                                                                    | https://www.ssi.dk/aktuelt/sygdomsudbrud/coronavirus                                                                                                                                                   | Daily              |
| Estonia        | Republic of Estonia Health Board                                                           | https://www.terviseamet.ee/en/covid19                                                                                                                                                                  | Daily              |
| Finland        | Finish Institute for Health and Welfare                                                    | https://thl.fi/en/web/infectious-diseases/what-s-new/coronavirus-covid-19-latest-updates/situation-update-on-coronavirus                                                                               | Daily              |
| France         | Public Health France                                                                       | https://www.santepubliquefrance.fr/maladies-et-traumatismes/maladies-et-infections-respiratoires/infection-a-coronavirus/articles/infection-au-nouveau-coronavirus-sars-cov-2-covid-19-france-et-monde | Tempremental       |
| Germany        | Robert Koch Institute                                                                      | https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Gesamt.html                                                                                                            | Tempremental       |
| Hungary        | Hungarian Government                                                                       | https://koronavirus.gov.hu/                                                                                                                                                                            | Daily              |
| Iceland        | Icelandic Governmet                                                                        | https://e.infogram.com/e3205e42-19b3-4e3a-a452-84192884450d?parent_url=https%3A%2F%2Fwww.covid.is%2Fdata&src=embed#                                                                                    | Daily              |
| India          | Indian Council of Medical Research                                                         | https://www.icmr.gov.in/                                                                                                                                                               | Daily              |
| Italy          | Italian Department of Civil Protection                                                     | https://github.com/pcm-dpc/COVID-19/tree/master/schede-riepilogative/regioni                                                                                                                           | Daily              |
| Japan          | Japanese Minsitry of Health, Labour and Welfare                                            | https://www.mhlw.go.jp/stf/houdou/index.html                                                                                                                                                           | Daily              |
| Latvia         | Latvian Centre for Disease Prevention and Control                                          | https://arkartassituacija.gov.lv/                                                                                                                                                                      | Daily              |
| Lithuania      | Ministry of Health of The Republic of Lithuania                                            | https://sam.lrv.lt/lt/naujienos/koronavirusas                                                                                                                                                          | Daily              |
| Netherlands    | AlleCijfers.nl - Recommended by RVIM (https://www.databronnencovid19.nl/)                  | https://allecijfers.nl/nieuws/statistieken-over-het-corona-virus-en-covid19/                                                                                                          | Daily              |
| New Zealand    | New Zealand Ministry of Health                                                             | https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases                                                               | Daily              |
| Norway         | Norwegian Institue for Public Health                                                       | https://www.fhi.no/en/id/infectious-diseases/coronavirus/                                                                                                                                              | Daily              |
| Romania        | Romanian Ministry of the Interior                                                          | https://www.mai.gov.ro/category/comunicate-de-presa/                                                                                                                                                   | Daily              |
| Russia         | Russian Federal Service for Surveillance on Consumer Rights Protection and Human Wellbeing | https://rospotrebnadzor.ru/about/info/news/                                                                                                                                                            | Daily              |
| Serbia         | Serbian Ministry of Health                                                                 | https://covid19.rs/                                                                                                                                                | Daily              |
| Slovakia       | Slovakian Government                                                                       | https://www.korona.gov.sk/                                                                                                                                    | Daily              |
| Slovenia       | Slovenian National Institute of Public Health                                              | https://www.nijz.si/sl/dnevno-spremljanje-okuzb-s-sars-cov-2-covid-19/                                                                                                                                 | Daily              |
| South Korea    | Korean Centre for Disease Control                                                          | https://www.cdc.go.kr/board/board.es?mid=&bid=0030                                                                                                                                                     | Daily              |
| Sweden         | Public Health Agency of Sweden                                                             | https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/                                                                              | Weekly             |
| Switzerland    | Swiss Federal Office of Public Health                                                      | https://www.bag.admin.ch/bag/de/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html                                       | Weekly             |
| United Kingdom | UK Government                                                                              | https://www.gov.uk/guidance/coronavirus-covid-19-information-for-the-public#number-of-cases                                                                                                            | Daily              |
| United States  | Unofficial Tracker                                                                         | https://covidtracking.com/data/                                                                                                                                                                        | Daily (Unofficial) |
| Vietnam        | Vietnam Ministry of Health                                                                 | https://ncov.moh.gov.vn/                                                                                                                                                                               | Daily              |

## Notes
* Australia releases regular updates on their government [website](https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert/coronavirus-covid-19-current-situation-and-case-numbers). The following Australian states also release totals for tests completed:
	* [New South Wales](https://www.health.nsw.gov.au/news/Pages/20200329_01.aspx)
	* [Queensland](https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/current-status-and-contact-tracing-alerts)
	* [Western Australia](https://ww2.health.wa.gov.au/Articles/A_E/Coronavirus/COVID19-statistics)
	* [Victoria](https://www.dhhs.vic.gov.au/media-hub-coronavirus-disease-covid-19)
	* [Southern Australia](https://www.sahealth.sa.gov.au/wps/wcm/connect/Public+Content/SA+Health+Internet/About+us/News+and+media/all+media+releases/)
	* [Australian Capital Territory](https://www.covid19.act.gov.au/)
* Spain has a [Covid Tracker](https://covid19.isciii.es/) but currently releases no information on tests. The region of Catalonia releases its own information on tests [here](http://www.euskadi.eus/boletin-de-datos-sobre-la-evolucion-del-coronavirus/web01-a2korona/es/).

## Requirements for running the code
* Beautiful Soup 4
* Dateparser
* Googletrans (helpful but probably not essential)
* Pandas / Numpy
* pytesseract (for reading Japan's totals)
* tableau-py (for Italy's PDFs)
* Selenium (for scraping javascript dashboards)

## Files
* Testtrack.py (Scraping code)
* Testnumbers.csv (collated data)
* Testsviz.r (visualisation in R)

## Share Your Thoughts
I'm on twitter at [@tomandthenews](https://twitter.com/tomandthenews). If you have any questions/suggestions please let me know! 


<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />
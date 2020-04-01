# CovidTests
Program to monitor Covid-19 Tests

This is a ** work in progress ** to monitor the number of Covid-19 Tests done by various countries.
The python code scrapes government official sources for daily updates on the number of covid tests completed.

## A few quick notes
* Germany and Spain have no official total of the number of tests completed (that I know of).
* France and Switzerland release totals weekly.
* Australia has a national total of tests that is substantially out of date. Most of its individual territories release daily updates on test numbers apart from the Northern Territories and Tasmania.

There are various countries that have not yet been incorporated into this dataset yet. I am aware of this and am looking to include as many as possible as time goes on.

## Requirements for running the code
* Beautiful Soup 4
* Dateparser
* Googletrans (Helpful probably not essential)
* Pandas / Numpy
* pytesseract (For reading Japan's totals)
* tableau-py (For Italy's PDFs)

## Files
* Testtrack.py (Scraping code)
* Testnumbers.csv (collated data)

## Help me out
I'm on twitter at [@tomandthenews](https://twitter.com/tomandthenews). If you have any questions/suggestions etc. don't hesitate to tweet me or send me a DM. 
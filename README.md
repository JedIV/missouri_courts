missouri_courts
===============

Court Scraper for the Missouri Court System

This webscraper was specifically designed for the 
Missouri courts system, but it can be modified for many other
scraping purposes. 

Many .net (and other) database form frontends update without
url changes. This makes the url hacks that can often be used to
cycle through many pages worth of scrapable data useless. Instead
we can modify qa testing software (in this case Selenium) to cycle
through the pages in an firefox browser window, and then use python's
Beautiful Soup package to actually scrape the data. 

While there's a lot of files in here, the four main guys that make the
thing work are:
* address_grabber.py
* date_court_id_grabber.py
* individual_case_lookup.py
* initial_test_loop.py

You can see the output at the bottom in the three files labeled:
* region_16_final.csv
* region_6_final.csv
* region_7_final.csv

These three files contain extensive information on all of the evictions
(over 54,000) that went to court in the Kansas City area during 2008-2013.
Feel free to use the information as you see fit.

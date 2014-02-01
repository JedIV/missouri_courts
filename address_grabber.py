from bs4 import BeautifulSoup
from pandas import *
import pprint

def extract_address(html):
    soup = BeautifulSoup(html)

    def_address = []
    def_yob = []
    plain_address = []
    def_name = []
    plain_name = []
    rows = soup.findAll("td", { "class" : "detailData" })

    headers = soup.findAll("td", { "class" : "detailSeperator" })

    try:
      defendant_address = ' '.join(rows[3].text.split())
    except:
      defendant_address = ' '

    try:
      defendant_name = ' '.join(headers[3].text.split())
    except:
      defendant_name = ' '

    try:
      plaintiff_address = ' '.join(rows[0].text.split())
    except:
      plaintiff_address = ' '

    try:
      plaintiff_name = ' '.join(headers[0].text.split())
    except:
      plaintiff_name = ' '

    chunks = defendant_address.partition('Year of Birth: ')

    defendant_name = defendant_name.partition(', Defendant')
    plaintiff_name = plaintiff_name.partition(', Plaintiff')

    defendant_address = chunks[0]
    defendant_yob = chunks[2]
    defendant_name = defendant_name[0]
    plaintiff_name = plaintiff_name[0]


    def_address.append(defendant_address)
    def_yob.append(defendant_yob)
    plain_address.append(plaintiff_address)
    def_name.append(defendant_name)
    plain_name.append(plaintiff_name)

    def_address_info = DataFrame({'def_address':def_address,'def_year_of_birth':def_yob,\
    'plaintiff_address':plain_address,'defendant_name':def_name,'plaintiff_name':plain_name})

    return def_address_info

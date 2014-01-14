from bs4 import BeautifulSoup
from pandas import *
import pprint

def extract_address(html):

  soup = BeautifulSoup(html)

  def_address = []
  def_yob = []

  rows = soup.findAll("td", { "class" : "detailData" })

  try:
    defendant_address = ' '.join(rows[3].text.split())
  except:
    defendant_address = ' '

  chunks = defendant_address.partition('Year of Birth: ')

  defendant_address = chunks[0]
  defendant_yob = chunks[2]

  def_address.append(defendant_address)
  def_yob.append(defendant_yob)

  def_address = DataFrame({'def_address':def_address,'def_year_of_birth':def_yob})

  return def_address

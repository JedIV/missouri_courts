from bs4 import BeautifulSoup
from pandas import *

def extract_evictions_table(html):

  soup = BeautifulSoup(html)
  
  try:
    rows = soup.findAll('table')[17].findAll('td')
  except:
    rows = ''

  date_filed = []
  case_number = []
  style_of_case = []
  case_type = []
  location = []


  i=0
  for row in rows:
    i=i+1

    if i > 8:
      if (i - 8) % 6 == 1:
        line = row.contents[0].encode('utf-8').strip("\t\r\n")
        date_filed.append(line)
      if (i - 8) % 6 == 2:
        link=row.find('a')
        line = link.contents[0].encode('utf-8').strip("\t\r\n")
        case_number.append(line)
      if (i - 8) % 6 == 3:
        line = row.contents[0].encode('utf-8').strip("\t\r\n")
        style_of_case.append(line)
      if (i - 8) % 6 == 4:
        line = row.contents[0].encode('utf-8').strip("\t\r\n")
        case_type.append(line)
      if (i - 8) % 6 == 5:
        line = row.contents[0].encode('utf-8').strip("\t\r\n")
        location.append(line)

  case_info=DataFrame({'date':date_filed,'case_number':case_number,'style_of_case':style_of_case,'case_type':case_type,'location':location})
  
  evictions = case_info[case_info.case_type.str.contains("AC Rent and Possession") ]
  return evictions

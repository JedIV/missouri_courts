from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from pandas import *

import unittest, time, re, csv

execfile("date_court_id_grabber.py")

filename = "region_seven_list.csv"

class InitialTestLoop(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.courts.mo.gov/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_initial_test_loop(self):
        with open('weekly_dates.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                week = row
                driver = self.driver
                driver.get(self.base_url + "/casenet/base/welcome.do")
                driver.find_element_by_id("dateSearchImg").click()
                Select(driver.find_element_by_id("courtId")).select_by_visible_text("7th Judicial Circuit (Clay County)")
                driver.find_element_by_id("inputVO.startDate").clear()
                driver.find_element_by_id("inputVO.startDate").send_keys(week)
                driver.find_element_by_id("findButton").click()
                
                #automates loop through of pages within a week
                totalRecords = driver.find_element_by_id("totalRecords").get_attribute("value")
                currentRecord = driver.find_element_by_id("startingRecord").get_attribute("value")
                page = 2
                while(int(currentRecord) < int(totalRecords)):
                    html = driver.page_source
                    evics = extract_evictions_table(html)
                    print evics
                    evics.to_csv(filename, header = False, mode = 'a')
                    page_change_script = "goToThisPage( '" + str(page) + "' )"
                    driver.execute_script(page_change_script)
                    currentRecord = driver.find_element_by_id("startingRecord").get_attribute("value")
                    page = page + 1

    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

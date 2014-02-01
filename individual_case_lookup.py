from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from pandas import *

import unittest, time, re

execfile("address_grabber.py")

filename = "region_6_list_with_addresses.csv"

evictions = read_csv("region_six_list.csv",header = None)
evictions.columns = ['rank','caseID','case_type','date','location','case_style']

class IndividualCaseLookup(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(30)
        self.base_url = "https://www.courts.mo.gov/"
        self.verificationErrors = []
        self.accept_next_alert = True
        driver = self.driver
        driver.get(self.base_url + "/casenet/base/welcome.do")
        driver.find_element_by_id("caseSearchImg").click()
    def test_individual_case_lookup(self):
        driver = self.driver
        for index, row in evictions.iterrows():
            caseID = row['caseID']
            caseID = caseID.strip()
            Select(driver.find_element_by_id("courtId")).select_by_visible_text("6th Judicial Circuit (Platte County)")
            driver.find_element_by_id("inputVO.caseNo").clear()
            driver.find_element_by_id("inputVO.caseNo").send_keys(caseID)
            driver.find_element_by_id("findButton").click()
            driver.find_element_by_link_text(caseID).click()
            go_to_parties = "submitForCaseDetails('parties.do')"
            driver.execute_script(go_to_parties)
            #driver.find_element_by_name("parties").click()
            html = driver.page_source
            evic_addresses = extract_address(html)
            
            evic_addresses['caseID'] = row['caseID'].strip()
            evic_addresses['date'] = row['date'].strip()
            evic_addresses['case_style'] = row['case_style'].strip()
            evic_addresses['case_type'] = row['case_type'].strip()
            evic_addresses['location'] = row['location'].strip()
            evic_addresses.to_csv(filename, header = False, mode = 'a',encoding = 'utf-8')
            Select(driver.find_element_by_id("searchType")).select_by_visible_text("Case Number")
    
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

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
import pandas as pd


class Ipl:
    def __init__(self):
        self.chrome_web = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.chrome_web)
        self.data_skeleton = {}

    def get_data(self, url):
        self.data_skeleton = {'TEAMS': [],
                              'M': [],
                              'W': [],
                              'L': [],
                              'PT': [],
                              'NRR': []}

        self.driver.maximize_window()
        self.driver.get(url)
        bar = self.driver.find_element(By.XPATH, '/html')
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', bar)
        data = self.driver.find_element(By.XPATH, '/html/body/div[1]/section/section/div[5]/div[1]/div['
                                                  '3]/div/div/table/tbody')

        for x in range(1, 25, 2):
            time.sleep(5)

            try:
                team_name = data.find_element(By.XPATH, f'/html/body/div[1]/section/section/div[5]/div[1]/div['
                                                        f'3]/div/div/table/tbody/tr[{x}]/td[1]/a/div/span')
                self.data_skeleton['TEAMS'].append(team_name.text)

                m = data.find_element(By.XPATH, f'/html/body/div[1]/section/section/div[5]/div[1]/div['
                                                f'3]/div/div/table/tbody/tr[{x}]/td[2]')
                self.data_skeleton['M'].append(m.text)

                w = data.find_element(By.XPATH, f'/html/body/div[1]/section/section/div[5]/div[1]/div['
                                                f'3]/div/div/table/tbody/tr[{x}]/td[3]')
                self.data_skeleton['W'].append(w.text)

                l = data.find_element(By.XPATH, f'/html/body/div[1]/section/section/div[5]/div[1]/div['
                                                f'3]/div/div/table/tbody/tr[{x}]/td[4]')
                self.data_skeleton['L'].append(l.text)

                pt = data.find_element(By.XPATH, f'/html/body/div[1]/section/section/div[5]/div[1]/div['
                                                 f'3]/div/div/table/tbody/tr[{x}]/td[7]')
                self.data_skeleton['PT'].append(pt.text)

                nrr = data.find_element(By.XPATH, f'/html/body/div[1]/section/section/div[5]/div[1]/div['
                                                  f'3]/div/div/table/tbody/tr[{x}]/td[8]')
                self.data_skeleton['NRR'].append(nrr.text)

            except NoSuchElementException:
                break

    def save_data(self, tag):
        df = pd.DataFrame(self.data_skeleton)
        df.to_csv(f'data{tag}.csv', index=False)


link_flags = ['2007-08-313494', '2009-374163', '2009-10-418064', '2011-466304', '2012-520932', '2013-586733',
              '2014-695871', '2015-791129', '2016-968923', '2017-1078425', '2018-1131611', '2019-1165643',
              '2020-21-1210595', '2021-1249214', '2022-1298423']

ipl_match = Ipl()

for i, v in enumerate(link_flags, 2008):
    ipl_match.get_data(url=f'https://www.espncricinfo.com/series/indian-premier-league-{v}/points-table-standings')
    ipl_match.save_data(i)

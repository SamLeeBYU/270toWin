from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import random
import pandas as pd

from analyze import Analysis

fips = pd.read_csv("fips.csv")
fips["FIPS"] = fips["FIPS"].astype(int)

class Scraper:

    def __init__(self, url):

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.votes = pd.DataFrame()
        self.url = url

    def go(self):

        self.driver.get(self.url)

    def terminate(self):

        self.driver.close()

    @staticmethod
    def rsleep(n=1):
        for i in range(n):
            time.sleep(random.uniform(1, 3))

    def get_votes(self):
        WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#map"))
            )

        with open('ec.js', 'r') as file:
            ec_script = file.read()
        self.driver.execute_script(ec_script)

        #Selected EC votes
        choices = self.driver.execute_script("return window.getPathData();")
        choices_data = pd.DataFrame.from_dict(choices, orient='index').reset_index()
        choices_data.columns = ["FIPS", "Democrat", "Republican"]
        choices_data["FIPS"] = choices_data["FIPS"].astype(int)

        choices_fips = pd.merge(choices_data, fips, on='FIPS', how='left')

        #Given EC votes
        ec_votes = self.driver.execute_script("return window.getElectoralCollegeData();")
        ec_data = pd.DataFrame(ec_votes)
        ec_data.columns = ["electoralVotes", "Abbr"]

        ec_fips = pd.merge(ec_data, fips, on="Abbr", how="left").sort_values(by="FIPS").reset_index(drop=True)
        votes = pd.merge(choices_data, ec_fips[['FIPS', 'electoralVotes']], on='FIPS', how='left')

        votes['Democrat'] = votes.apply(lambda row: row['electoralVotes']*row['Democrat'], axis=1)
        votes['Republican'] = votes.apply(lambda row: row['electoralVotes']*row['Republican'], axis=1)
        votes = votes.drop(columns=['electoralVotes'])
        votes = votes.dropna() #Drops Maine and Nebraska, which we will add in a bit

        #Special Cases
        special = self.driver.execute_script("return window.getSpecial();")
        special_cases = pd.DataFrame.from_dict(special, orient='index').reset_index()
        special_cases.columns = ['Abbr', 'Democrat', 'Republican']

        votes = pd.merge(votes, fips, on='FIPS', how='left')
        special_cases_fips = pd.merge(special_cases, fips, on='Abbr', how='left')

        votes = pd.concat([votes, special_cases_fips], axis=0)
        self.votes = votes

if __name__ == "__main__":

    maps = {
        "2020": "https://www.270towin.com/maps/2020-actual-electoral-map",
        "SamLee": "https://www.270towin.com/maps/vnRAN"
    }

    for name, url in maps.items():
        print(f"Scraping {name}'s map: {url}")

        scraper = Scraper(url)
        scraper.go()
        scraper.get_votes()
        analyzer = Analysis(scraper.votes, name)
        analyzer.metrics()
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class Animix: 

    def __init__(self):
        self.BASE_URL = "https://animixplay.to"
        self.GECKODRIVER_PATH = "/geckodriver/geckodriver" # TODO: fix this.
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        self.firefoxOptions = Options()
        self.firefoxOptions.add_argument('--headless')
        self.firefoxOptions.add_argument('--ignore-ssl-errors=yes')
        self.firefoxOptions.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Firefox(service=Service(self.GECKODRIVER_PATH), options=self.firefoxOptions)
        self.TRIAL_SLEEP = 1

    def search(self, query):
        results = []
        self.driver.get(self.BASE_URL + "/?q=" + query + "&sengine=all")
        delay = 3
        try:
            episodesTag = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'items')))
            time.sleep(self.TRIAL_SLEEP)
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            items = soup.find("ul", class_="items")
            for entry in items.findAll("li"):
                p = entry.find("p",class_="name").find("a")
                title = p["title"]
                link = p["href"]
                results.append({"name": title, "url": self.BASE_URL + link}) 
        except Exception as e:
            print(e)
            pass
        return results 
        
    def getTotalEpisodes(self, link):
        total = 0
        self.driver.get(link)
        delay = 2
        try:
            episodesSpan = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, 'epsavailable')))
            time.sleep(self.TRIAL_SLEEP)
            total = int(episodesSpan.text)
        except Exception as e:
            print(e)
            pass
        return total 

    def getEpisodes(link, totalEpisodes):
        return [link + "/ep" + str(index) for index in range(1, totalEpisodes + 1)]

    def getEpisodeStream(self, link, episodeNumber):
        self.driver.get(link + "/ep" + str(episodeNumber))
        delay = 2
        source = None
        try:
            iframe = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, 'iframeplayer')))
            time.sleep(self.TRIAL_SLEEP)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            source = soup.find("iframe", id="iframeplayer")["src"]
            source = self.BASE_URL + source
        except Exception as e:
            print(e)
            pass
        return source

    def quitDriver(self):
        self.driver.quit()

    def closeDriver(self):
        self.driver.close()

if __name__ == "__main__":
    animix = Animix()
    results = animix.search("Chainsaw Man")
    topResultTotalEpisodes = animix.getTotalEpisodes(results[0]["url"])
    src = animix.getEpisodeStream(results[0]["url"], 2)
    print(src)
    animix.quitDriver()

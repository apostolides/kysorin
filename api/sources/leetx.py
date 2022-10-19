import requests as r
from bs4 import BeautifulSoup

class Leetx():
    def __init__(self):
        self.BASE_URL = "https://www.1337xx.to"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    # Get a list of torrents based on a query. 
    def search(self, query):
        QUERY_URL = self.BASE_URL + "/search/" + query + "/1"
        results = []
        # Send request to 1337x.
        resp = r.get(QUERY_URL, headers=self.headers)
        if resp.status_code == 200:
            try:
                # Parse response.
                soup = BeautifulSoup(resp.content, "html.parser")
                # Get torrent related fields from each entry in result table.
                mainTable = soup.select(".table-list")[0].find("tbody")
                for tableEntry in mainTable.findAll("tr"):
                    seeders = tableEntry.find("td", class_="seeds").text
                    leechers = tableEntry.find("td", class_="leeches").text
                    uploadTime = tableEntry.find("td", class_="coll-date").text
                    size = tableEntry.find("td", class_="size").text
                    nameIconBundle = tableEntry.find("td", class_="name").find("a", class_= lambda className: className!="icon") 
                    name = nameIconBundle.text
                    href = nameIconBundle["href"]
                    magnet = self.getMagnetFromUrl(self.BASE_URL + href)
                    # Create and append torrent object.
                    torrent = {
                        "name":name,
                        "seeders":seeders,
                        "leechers":leechers,
                        "upload_time":uploadTime,
                        "size":size,
                        "magnet_url":magnet
                    }
                    results.append(torrent)
            except:
                pass
        return results        

    # Scrape magnet url from specified 1337x url.
    def getMagnetFromUrl(self, url):
        resp = r.get(url, headers=self.headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            magnet = soup.select(".torrentdown1")[0]["href"]
            return magnet
        else:
            return None

if __name__ == "__main__":
    leetx = Leetx()
    results = leetx.search("Mr. Robot")
    for res in results:
        print(f"{res['name']} | {res['magnet_url'][:25]}[...]")
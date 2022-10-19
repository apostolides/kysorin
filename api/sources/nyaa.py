import requests as r
from bs4 import BeautifulSoup

class Nyaa():
    def __init__(self):
        self.BASE_URL = "https://nyaa.si"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    # Get a list of torrents based on a query. 
    def search(self, query, trusted = False):
        QUERY_URL = None
        if trusted:
            QUERY_URL = self.BASE_URL + "/?f=2&c=0_0&q=" + query.replace(' ','+')
        else:
            QUERY_URL = self.BASE_URL + "/?f=0&c=0_0&q=" + query.replace(' ','+')
        results = []
        # Send request to nyaa.si.
        resp = r.get(QUERY_URL, headers=self.headers)
        if resp.status_code == 200:
            # Parse response.
            soup = BeautifulSoup(resp.content, "html.parser")
            # Get torrent related fields from each entry in result table.
            mainTable = soup.select(".table")[0].find("tbody")
            for tableEntry in mainTable.findAll("tr"):
                info = tableEntry.findAll("td")
                name = info[1].findAll("a", class_=lambda className: className!="comments")[0].text
                magnet = info[2].findAll("a")[1]["href"]
                size = info[3].text
                uploadTime = info[4].text
                seeders = info[5].text
                leechers = info[6].text
                downloads = info[7].text

                # Create and append torrent object.
                torrent = {
                    "name":name,
                    "seeders":seeders,
                    "leechers":leechers,
                    "upload_time":uploadTime,
                    "size":size,
                    "magnet_url":magnet,
                    "downloads":downloads
                }
                results.append(torrent)
        return results        

if __name__ == "__main__":
    nyaa = Nyaa()
    results = nyaa.search("Naruto Shippuden")
    for res in results:
        print(f"{res['name']} | {res['magnet_url'][:25]}[...]")
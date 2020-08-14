import requests
from match import Match
from bs4 import BeautifulSoup

class Series(object):
    def __init__(self, url):
        url = url + "?view=results"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        values = soup.findAll("a", text="Scorecard")

        for value in values:
            url_given = value["href"]
            if url_given.startswith("https://www.espncricinfo.com"):
                url_given = url_given[len("https://www.espncricinfo.com"):]
            print(url_given)
            match = Match(url_given)
            if match.bowling_team is not None and match.batting_team is not None:
                print(match)
            else:
                print("problem")

start_year = 1972
end_year = 2020
base_url = "https://www.espncricinfo.com/ci/engine/series/index.html?season={};view=season"
def SeriesFinder(year):
    url = base_url.format(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    odis = soup.findAll("section", {"class":"series-summary-wrap"})[1]
    series_tags = odis.findAll("div", {"class":"teams"})
    for tag in series_tags:
        link = tag.find("a")
        Series(link["href"])

def FindAllSeries():
    for i in reversed(range(start_year, end_year + 1)):
        SeriesFinder(i)
        SeriesFinder(str(i) + "%2F" + str(i + 1)[-2:])

def main():
    FindAllSeries()

if __name__ == "__main__":
    main()
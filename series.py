import requests
import csv
from match import Match
from bs4 import BeautifulSoup

class Series(object):
    def __init__(self, url):
        url = url + "?view=results"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        values = soup.findAll("a", text="Scorecard")
        self.matches = list()

        for value in values:
            url_given = value["href"]
            if url_given.startswith("https://www.espncricinfo.com"):
                url_given = url_given[len("https://www.espncricinfo.com"):]
            
            match_id = url_given.split('/')[4]
            self.series_id = url_given.split('/')[2]
            match = Match(self.series_id, match_id)
            if match.valid:
                self.matches.append(match)

    def csv_style(self):
        match_csv = list()
        for match in self.matches:
            if not match.valid:
                continue

            row = dict()
            row['series_id'] = match.series_id
            row['match_id'] = match.match_id
            row['date'] = match.date
            row['year'] = match.date.year
            
            for i, batter in enumerate(match.batting_team):
                row["Batter" + str(i) + "Name"] = batter.name
                row["Batter" + str(i) + "Innings"] = batter.innings
                row["Batter" + str(i) + "Runs"] = batter.runs
                row["Batter" + str(i) + "Average"] = batter.average
                row["Batter" + str(i) + "SR"] = batter.strike_rate

            for i, bowler in enumerate(match.bowling_team):
                row['Bowler' + str(i) + " Name"] = bowler.name
                row['Bowler' + str(i) + " Innings"] = bowler.innings
                row['Bowler' + str(i) + " Runs"] = bowler.runs
                row['Bowler' + str(i) + " Average"] = bowler.average
                row['Bowler' + str(i) + " SR"] = bowler.strike_rate
                row['Bowler' + str(i) + " Economy"] = bowler.Economy
                row['Bowler' + str(i) + " Wickets"] = bowler.wickets
                row['Bowler' + str(i) + " Deliveries"] = bowler.deliveries
            
            match_csv.append(row)

        return match_csv

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
        series = Series(link["href"])
        xs = series.csv_style()
        print(xs)
        for x in xs:
            print(x)

def FindAllSeries():
    for i in reversed(range(start_year, end_year + 1)):
        SeriesFinder(i)
        SeriesFinder(str(i) + "%2F" + str(i + 1)[-2:])

def main():
    FindAllSeries()

if __name__ == "__main__":
    s = Series("https://www.espncricinfo.com/scores/series/19073/afghanistan-in-scot-odis-2019")
    x = s.csv_style()
    for y in x:
        print(y)
    #main()


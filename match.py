import requests
from bs4 import BeautifulSoup
import dateutil.parser as dparser
from ground import Ground
from player import Batsman
from player import Bowler

class Match(object):
    def __init__(self, url):
        self.url = "https://www.espncricinfo.com/" + url
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.date = self.get_date(soup)
        self.ground = self.get_ground_average(soup)
        self.ground_average = self.get_ground_average(soup)
        self.bowling_team = self.get_bowling_team(soup)
        self.batting_team = self.get_batting_team(soup)

    def __repr__(self):
        form = "{},{},{}"
        
        bat_repr = ""
        for batter in self.batting_team:
            bat_repr = bat_repr + str(batter)

        bowl_repr = ""
        for bowler in self.bowling_team[0 : 4]:
            bowl_repr = bowl_repr + str(bowler)
        
        return form.format(self.date, bat_repr, bowl_repr)

    def get_ground_average(self, soup):
        element = soup.find("td", {"class":"font-weight-bold match-venue"})
        ground_info = element.find("a")
        first = ground_info["href"].rfind('/')
        last = ground_info["href"].rfind('.')
        return Ground(ground_info["href"][first + 1 : last], self.date)

    def get_date(self, soup):
        element = soup.find("div", {'class':'desc text-truncate'})
        values = element.text.split(',')

        for date in values[1:]:
            try:
                return dparser.parse(date, fuzzy=True)
            except:
                pass
            
    def get_batting_team(self, soup):
        batters = list()

        elements = soup.findAll("td", {'class':'batsman-cell'})
        if not elements:
            return None

        for i in elements:
            link = i.find("a")["href"]
            playerID = link[link.rindex('/') + 1 : link.rindex('.')]
            name = i.text
            batter = Batsman(playerID, name, self.date)
            batters.append(batter)

        return batters

    def get_bowling_team(self, soup):
        bowlers = list()

        elements = soup.find("table", {'class':'table bowler'})
        if not elements:
            return None

        bowler_rows = elements.findAll("td", {'class':'text-nowrap'})

        for i in bowler_rows:
            name = i.text
            link = i.find("a")["href"]
            playerID = link[link.rindex('/') + 1 : link.rindex('.')]
            bowler = Bowler(playerID, name, self.date)
            bowlers.append(bowler)

        return bowlers

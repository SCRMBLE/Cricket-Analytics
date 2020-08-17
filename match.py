import requests
from bs4 import BeautifulSoup
import dateutil.parser as dparser
from ground import Ground
from player import Batsman
from player import Bowler

class Match(object):
    def __init__(self, series_id, match_id):
        self.url = "https://www.espncricinfo.com/series/{}/scorecard/{}".format(series_id, match_id)
        print(self.url)
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.series_id = series_id
        self.match_id = match_id
        self.date = self.get_date(soup)
        self.runs = self.get_runs(soup)

        if self.runs is None:
            self.valid = False
            return
        else:
            self.valid = True

        self.deliveries = self.get_deliveries(soup)
        self.wickets = self.get_wickets(soup)
        print(self.deliveries)
        print(self.wickets)

        if self.deliveries < 300 and self.wickets is not 10:
            self.valid = False
            print("invalid")
            print(self.deliveries)
            print(self.wickets)
            return

        self.ground = self.get_ground_average(soup)
        self.ground_average = self.get_ground_average(soup)
        self.bowling_team = self.get_bowling_team(soup)
        self.batting_team = self.get_batting_team(soup)

        if self.runs is not None and self.deliveries is not None:
            self.strike_rate = self.runs / self.deliveries
        else:
            self.strike_rate = None

    def __repr__(self):
        form = "{},{},{}"
        
        bat_repr = ""
        for batter in self.batting_team:
            bat_repr = bat_repr + str(batter)

        bowl_repr = ""
        for bowler in self.bowling_team[0 : 4]:
            bowl_repr = bowl_repr + str(bowler)
        
        return form.format(self.date, bat_repr, bowl_repr)

    def get_runs(self, soup):
        score = soup.find("div", {"class":"score-run font-weight-bold score-run-gray"})
        if score is None:
            return None

        return int(score.text.split("/")[0])

    def get_deliveries(self, soup):
        batsman_table = soup.find("table", {"class":"table batsman"})
        if batsman_table is None:
            return None

        footer = batsman_table.find("tfoot")
        information = footer.findAll("td")[1].text
        overs = float(information.strip('(').split(' ')[0])
        deliveries = (overs % 1) * 5 / 3 + (overs // 1) * 6
        return deliveries

    def get_wickets(self, soup):
        score = soup.find("div", {"class":"score-run font-weight-bold score-run-gray"})
        if score is None:
            return None

        if len(score.text.split("/")) is 1:
            return 10
        
        return score.text.split("/")[1]

    def get_ground_average(self, soup):
        element = soup.find("td", {"class":"font-weight-bold match-venue"})
        ground_info = element.find("a")
        first = ground_info["href"].rfind('/')
        last = ground_info["href"].rfind('.')
        return Ground(ground_info["href"][first + 1 : last], self.date)

    def get_date(self, soup):
        element = soup.find("div", {'class':'desc text-truncate'})
        print(element)
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

        extra = soup.findAll("table", {"class":"table batsman"})
        footer = extra.find("tfoot")
        if footer is not None and footer.find("strong", text="Did not bat:"):
            links = footer.findAll("a")
            for link in links:
                url = link["href"]
                playerID = url[url.rindex('/') + 1 : url.rindex('.')]
                name = link.text
                batter = Batsman(playerID, name, self.date)
                batters.append(batter)
                print("DNB")
                print(playerID)
                print(name)

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


import requests
from bs4 import BeautifulSoup
from player import get_summary_table
from player import get_index_table
from player import parse_number
from player import get_data_index

base = "https://stats.espncricinfo.com/ci/engine/ground/{}.html?class=2;spanmax1={};spanval1=span;template=results;type=aggregate"
class Ground(object):
    def __init__(self, ground_id, date):
        url = base.format(ground_id, date)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.summary = get_summary_table(soup)
        self.index_table = get_index_table(soup)
        self.average = self.get_average()

    def get_average(self):
        index_matches = get_data_index(self.index_table, "Mat")
        index_runs = get_data_index(self.index_table, "Runs")
    
        matches = parse_number(False, self.summary.findAll("td")[index_matches].text)
        runs = parse_number(False, self.summary.findAll("td")[index_runs].text)
        if matches is None:
            return None
        
        return runs / matches / 2

    def get_strike_rate(self):
        index_balls = get_data_index(self.index_table, "Balls")
        index_runs = get_data_index(self.index_table, "Runs")

        balls = parse_number(False, self.summary.findAll("td")[index_balls].text)
        runs = parse_number(False, self.summary.findAll("td")[index_runs].text)

        if balls is None:
            return None
        
        return balls / runs
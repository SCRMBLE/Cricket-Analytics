import requests
from bs4 import BeautifulSoup
from enum import IntEnum
import dateparser
import calendar

base = "https://stats.espncricinfo.com/ci/engine/player/{}.html?class={};spanmax1={};spanval1=span;template=results;type={}"
game_type = "2"

class Batsman(object):
    def __init__(self, playerID, name, date):
        query = base.format(playerID, game_type, date_parser(date), "batting")
        page = requests.get(query)
        soup = BeautifulSoup(page.text, 'html.parser')
        summary = get_summary_table(soup)
        index = get_index_table(soup)

        self.name = name.strip()
        self.innings = self.get_innings(summary, index)
        self.runs = self.get_runs(summary, index)
        self.average = self.get_average(summary, index)
        self.strike_rate = self.get_strike_rate(summary, index)
    
    def __repr__(self):
        form = "{},{},{},{},{}"
        return form.format(self.name, self.innings, self.runs, self.average, self.strike_rate)

    def __str__(self):
        return repr(self)

    def get_innings(self, soup, index_table):
        index = get_data_index(index_table, "Inns")
        return parse_number(False,soup.findAll("td")[index].text)

    def get_runs(self, soup, index_table):
        index = get_data_index(index_table, "Runs")
        return parse_number(False,soup.findAll("td")[index].text)

    def get_average(self, soup, index_table):
        index = get_data_index(index_table, "Ave")
        return parse_number(False,soup.findAll("td")[index].text)

    def get_strike_rate(self, soup, index_table):
        index = get_data_index(index_table, "SR")
        return parse_number(False,soup.findAll("td")[index].text)


class Bowler(object):
    def __init__(self, playerID, name, date):
        query = base.format(playerID, game_type, "date", "bowling")
        page = requests.get(query)
        soup = BeautifulSoup(page.text, 'html.parser')
        summary = get_summary_table(soup)
        index = get_index_table(soup)

        self.name = name.strip()
        self.innings = self.get_innings(summary, index)
        self.deliveries = self.get_deliveries(summary, index)
        self.runs = self.get_runs(summary, index)
        self.wickets = self.get_wickets(summary, index)
        self.average = self.get_average(summary, index)
        self.economy = self.get_economy(summary, index)
        self.strike_rate = self.get_strike_rate(summary, index)

    def __repr__(self):
        form = "{},{},{},{},{},{},{},{}"
        return form.format(self.name, self.innings, self.runs, self.average, self.strike_rate, self.economy, self.wickets, self.deliveries)

    def __str__(self):
        return repr(self)

    def get_innings(self, soup, index_table):
        index = get_data_index(index_table, "Inns")
        return parse_number(False, soup.findAll("td")[index].text)

    def get_runs(self, soup, index_table):
        index = get_data_index(index_table, "Runs")
        return parse_number(False, soup.findAll("td")[index].text)

    def get_deliveries(self, soup, index_table):
        index = get_data_index(index_table, "Overs")
        return parse_number(False, soup.findAll("td")[index].text) * 6

    def get_wickets(self, soup, index_table):
        index = get_data_index(index_table, "Wkts")
        return parse_number(False, soup.findAll("td")[index].text)

    def get_average(self, soup, index_table):
        index = get_data_index(index_table, "Ave")
        return parse_number(False, soup.findAll("td")[index].text)

    def get_economy(self, soup, index_table):
        index = get_data_index(index_table, "Econ")
        return parse_number(False, soup.findAll("td")[index].text)

    def get_strike_rate(self, soup, index_table):
        index = get_data_index(index_table, "SR")
        return parse_number(False, soup.findAll("td")[index].text)

def date_parser(date):
    form = "{}+{}+{}"
    return form.format(date.day, calendar.month_abbr[date.month], date.year)

def get_summary_table(soup):
    tables = soup.findAll("table", {'class':'engineTable'})
    for table in tables:
        row = table.find("tr", {'class':'data1'})
        if row:
            return row

def get_index_table(soup):
    tables = soup.findAll("table", {'class':'engineTable'})
    for table in tables:
        row = table.find("tr", {'class':'head'})
        if row:
            return row

def get_data_index(index_table, name):
    rows = index_table.findAll("th")
    i = 0
    for row in rows:
        if row.text == name:
            return i 
        i = i + 1

def parse_number(isInt, value):
    value.strip('*')
    if isInt:
        try:
            return int(value)
        except:
            pass
    else:
        try:
            return float(value)
        except:
            pass
    
    return None


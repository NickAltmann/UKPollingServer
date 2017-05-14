# -*- coding: utf-8 -*-
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict


month_map = {datetime.date(2016, x, 1).strftime("%b"): x for x in range(1, 13)}
def get_month(ss):
    """Get the month as an int from string"""
    return int(month_map[ss[:3]])


def get_frame_from_wiki(url, years):
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for year in years:
        table = soup.find('span', id=str(year)).parent.findNextSibling('table')

        header = table.find('tr')
        cols = [x.text for x in header.find_all('th')]

        def starts_with_index(s, l):
            for i, x in enumerate(l):
                if x.startswith(s):
                    return i
            return -1

        sw_map = OrderedDict([('Con', 'Con'), ('Lab', 'Lab'), ('Lib', 'LD'), ('UKIP', 'UKIP'), ('Green', 'Green')])
        col_index = OrderedDict([(sw_map[x], starts_with_index(x, cols)) for x in sw_map.keys()])
        date_index = starts_with_index('Date', cols)
        pollster_index = starts_with_index('Polling', cols)

        data = []
        dates = []
        pollsters = []
        for row in table.find_all('tr'):
            try:
                cells = list(row.find_all('td'))
                if len(cells) != len(cols):
                    continue

                def parse_value(x):
                    try:
                        return float(x.replace("%", ""))
                    except:
                        return 0
                row_data = [parse_value(cells[i].text) for i in col_index.values()]

                date_text = cells[date_index].text
                if u"–" in date_text:
                    date_text = date_text.split(u"–")[1]
                if u"-" in date_text:
                    date_text = date_text.split(u"-")[1]

                polling_text = cells[pollster_index].text
                pollster = polling_text.split('/')[0].lower().strip()

                row_day, row_mn = date_text.split(" ")
                month = get_month(row_mn)
                day = int(row_day)
                row_date = datetime.date(year, month, day)

                data.append(row_data)
                dates.append(row_date)
                pollsters.append(pollster)

                df = pd.DataFrame(data, columns=sw_map.values())
                df.insert(0, "Pollster", pollsters)
                df.insert(0, "Date", dates)
            except:
                continue
        results.append(df)

    full = pd.concat(results)

    return full.sort_values("Date")

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time


def month_from_string(ss):
    try:
        pat = '.*?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*.*'
        m = re.match(pat, ss)
        month = m.groups()[0]
        month_num = int(time.strptime(month,'%b').tm_mon)
    except:
        month_num = 0
    return month_num


def dataframe_from_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all("table")

    results = list()
    year = None
    month = None

    for table in tables:
        try:
            hh = table.find('thead').find('tr').find(["th", "td"])
            year = int(hh.text.strip())
        except:
            try:
                year = int(table['id'])
            except:
                # Case where there's an extra table for a year but no id.
                pass
        header = table.find('thead').find('tr')

        col = 0
        header_names = dict()
        for th in header.find_all(['th', 'td']):
            span = int(th.get('colspan', 1))
            text = th.contents[0]
            if col > 0:
                header_names[col] = text.strip(u'\xa0').strip(u' ')
            col += span

        rows = table.find('tbody').find_all('tr')
        for row in rows:
            col = 0
            ratings = dict()
            for td in row.find_all(['td', 'th']):
                text = td.text.strip(u'\xa0').strip(u' ')
                span = int(td.get('colspan', 1))
                if len(text):
                    if td.name == 'th':
                        header_names[col] = text
                    else:
                        if col == 0:
                            month = None
                            if text:
                                month = month_from_string(text)
                        else:
                            try:
                                rating = int(text)
                            except:
                                rating = None
                            if rating:
                                ratings[col] = rating
                col += span

            if month:
                for i in header_names.keys():
                    item = header_names[i]
                    if i in ratings and i+1 in ratings:
                        sat = ratings[i]
                        dis = ratings[i+1]

                        day = datetime.date(year, month, 1)
                        results.append([day, item, sat, dis])

    df = pd.DataFrame(results, columns=['Date', 'Item', 'Sat', 'Dis'])
    return df


def get_data():

    urls = [r'https://www.ipsos.com/ipsos-mori/en-uk/political-monitor-satisfaction-ratings-1997-present',
            r'https://www.ipsos.com/ipsos-mori/en-uk/political-monitor-satisfaction-ratings-1988-1997',
            r'https://www.ipsos.com/ipsos-mori/en-uk/political-monitor-satisfaction-ratings-1977-1987']

    dfs = [dataframe_from_url(url) for url in urls]

    df = pd.concat(dfs).sort_values(['Date', 'Item'])

    return df


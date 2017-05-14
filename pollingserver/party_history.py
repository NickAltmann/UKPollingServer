import datetime
import pandas as pd

from pollingserver.pack import get_frame_from_workbook
from pollingserver.wiki import get_frame_from_wiki

import pollingserver.data_source as ds


def get_data():
    path = ds.get_pack_filepath()
    df1 = get_frame_from_workbook(path)
    max_pack_year = df1.Date.max().year

    years = range(max_pack_year, datetime.datetime.now().year + 1)
    wiki_url = ds.wiki_url
    df2 = get_frame_from_wiki(wiki_url, years)

    df = pd.concat([df1, df2[df2.Date>df1.Date.max()]]).reset_index(drop=True)
    return df


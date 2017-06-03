import os
import sys
import shutil
from enum import Enum
from collections import OrderedDict
import pandas as pd

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

import pollingserver.party_history as hist
import pollingserver.mori



class AvailableData(Enum):
    parties = 1
    leaders = 2
    in_power = 3
    general_elections = 4
    notes = 5


def available_data():
    return [x.name for x in list(AvailableData)]


def filename_from_string(data):
    return "%s.csv" % data


def filename_from_enum(data):
    return filename_from_string(data.name)


def write_excel(frames, filename):
    wb = Workbook()
    ws = None

    for frame in frames.items():
        title = frame[0]
        df = frame[1]
        if ws:
            ws = wb.create_sheet(title=title)
        else:
            ws = wb.active
            ws.title = title
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)

    wb.save(filename=filename)


def write_csvs(target_dir):

    df_mori = pollingserver.mori.get_data()
    mori_filename = os.path.join(target_dir, filename_from_enum(AvailableData.leaders))
    df_mori.to_csv(mori_filename, index=False)

    df_parties = hist.get_data()
    parties_filename = os.path.join(target_dir, filename_from_enum(AvailableData.parties))
    df_parties.to_csv(parties_filename, index=False)

    files_to_copy = [os.path.join(os.path.dirname(os.path.dirname(__file__)), "source", f)
                     for f in [filename_from_enum(AvailableData.general_elections),
                               filename_from_enum(AvailableData.in_power),
                               filename_from_enum(AvailableData.notes)]]
    for f in files_to_copy:
        shutil.copy(f, target_dir)

    names = ['Parties', 'Leaders', 'GeneralElections', 'InPower', 'Notes']
    frames = [df_parties, df_mori] + [pd.read_csv(f) for f in files_to_copy]

    write_excel(OrderedDict(zip(names, frames)), os.path.join(target_dir, "uk_polls.xlsx"))

if __name__ == "__main__":

    if len(sys.argv) == 2:
        target_dir = sys.argv[1]
    else:
        target_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "out")

    write_csvs(target_dir)

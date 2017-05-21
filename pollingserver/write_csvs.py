import os
import sys
import shutil
from enum import Enum

import pollingserver.party_history as hist
import pollingserver.mori


class AvailableData(Enum):
    parties = 1
    leaders = 2
    in_power = 3
    general_elections = 4


def available_data():
    return [x.name for x in list(AvailableData)]


def filename_from_string(data):
    return "%s.csv" % data


def filename_from_enum(data):
    return filename_from_string(data.name)


def write_csvs(target_dir):

    df_mori = pollingserver.mori.get_data()
    mori_filename = os.path.join(target_dir, filename_from_enum(AvailableData.leaders))
    df_mori.to_csv(mori_filename, index=False)

    df_parties = hist.get_data()
    parties_filename = os.path.join(target_dir, filename_from_enum(AvailableData.parties))
    df_parties.to_csv(parties_filename, index=False)

    files_to_copy = [os.path.join(os.path.dirname(os.path.dirname(__file__)), "source", f)
                     for f in [filename_from_enum(AvailableData.general_elections), filename_from_enum(AvailableData.in_power)]]
    for f in files_to_copy:
        shutil.copy(f, target_dir)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        target_dir = sys.argv[1]
    else:
        target_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "out")

    write_csvs(target_dir)

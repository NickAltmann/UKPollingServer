import os
import sys
import shutil

import pollingserver.party_history as hist
import pollingserver.mori


_data_to_filename = {"leaders": "mori.csv",
                     "parties": "parties.csv",
                     "general_elections": "general_elections.csv",
                     "in_power": "power.csv"}


def available_data():
    return _data_to_filename.keys()


def filename(data):
    return _data_to_filename[data]


def write_csvs(target_dir):

    df_mori = pollingserver.mori.get_data()
    mori_filename = os.path.join(target_dir, filename("leaders"))
    df_mori.to_csv(mori_filename, index=False)

    df_parties = hist.get_data()
    parties_filename = os.path.join(target_dir, filename("parties"))
    df_parties.to_csv(parties_filename, index=False)

    files_to_copy = [os.path.join(os.path.dirname(os.path.dirname(__file__)), "source", f)
                     for f in [filename("general_elections"), filename("in_power")]]
    for f in files_to_copy:
        shutil.copy(f, target_dir)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        target_dir = sys.argv[1]
    else:
        target_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "out")

    write_csvs(target_dir)

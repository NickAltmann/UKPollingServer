import os


pack_name = "MarkPack_2017_04.xls"
#wiki_url = 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_next_United_Kingdom_general_election'
wiki_url = 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_United_Kingdom_general_election,_2017'


def data_dir():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "source")


def get_pack_filepath():
    return os.path.join(data_dir(), pack_name)


def get_power_filepath():
    return os.path.join(data_dir(), "in_power.csv")


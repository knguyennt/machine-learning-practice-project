import torch
from bs4 import BeautifulSoup
import requests
from defination import Defination

defination = Defination

class Utils:
    def __init__(self):
        pass

    def get_topic_page(self, site_url, genre):
        final_url = site_url + defination.genre_dict[genre] + '/' + genre
        response = requests.get(final_url)
        if response.status_code != 200:
            print('Status code:', response.status_code)
            raise Exception('Failed to fetch web page ' + final_url)
        return BeautifulSoup(response.text, features="html.parser")

    def load_data(self,data_file):
        pass


    def one_hot_encoding(self, in_features):
        pass

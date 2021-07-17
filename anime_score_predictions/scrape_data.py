# importing libraries
from bs4 import BeautifulSoup
import requests
from utils import Utils
from defination import Defination
from tqdm import tqdm
import logging
import numpy as np
import pandas as pd


anime_defination = Defination()
util = Utils()

def scrape_anime_using_genre():
    print("Scraping anime data from myanimelist genre site")
    anime_genre_site_url = "https://myanimelist.net/anime/genre/"
    # create array to store data
    anime_info_genre_dict = {}
    anime_title_list = []
    anime_genre_list = []
    anime_score_list = []
    for genre in tqdm(anime_defination.genre_dict):
        doc = util.get_topic_page(anime_genre_site_url, genre) # send request to genre site
        # data necessary will need the follow:
        # anime_title
        list_titles = []
        anime_titles = doc.find_all('h2', class_='h2_anime_title') # select top 100 title in that genre
        for anime_title in anime_titles:
            name = anime_title.find('a').text
            list_titles.append(name)
        anime_title_list.append(list_titles)

        # anime_genre
        all_anime_genre_html = doc.find_all('div', class_='genres-inner js-genre-inner') # get html of genre
        anime_current_genre_list = []
        # for each anime in the whole site
        for anime_genres in all_anime_genre_html:
            current_anime_genres = anime_genres.find_all('span', class_="genre") # get all anime genre of site
            current_anime_genres_list = []
            for current_anime_genre in current_anime_genres:
                current_anime_genres_list.append(current_anime_genre.text.strip())
            anime_current_genre_list.append(current_anime_genres_list)
        anime_genre_list.append(anime_current_genre_list)

        # anime_score
        list_scores = []
        anime_scores = doc.find_all('div', class_= 'scormem')
        for score in anime_scores:
            s = score.find('span', class_='score').text.strip()
            list_scores.append(s)
        anime_score_list.append(list_scores)
        anime_info_genre_dict[genre] = [list_titles, anime_current_genre_list, list_scores]

        # optional anime_image for display if using app

    # sanity check
    assert len(anime_score_list) == len(anime_title_list) == len(anime_genre_list) == len(anime_defination.genre_dict)
    logging.info('Assertion pass')
    # the list only use when testing can remove to improve performance time
    return anime_info_genre_dict


def generate_data(genre_list ,anime_info_genre_dict):
    print("Saving data")
    anime_data_frame = []
    for genre in tqdm(genre_list):
        anime_data = np.array(anime_info_genre_dict[genre])
        tmp_df = pd.DataFrame(data=anime_data).T
        tmp_df.to_csv(r'data_dir/{0}{1}.csv'.format(genre, "_genre"), quoting=None , index = False, header = False)
        anime_data_frame.append(tmp_df)
    df = pd.concat(anime_data_frame)
    df.to_csv(r'data_dir/anime_data.csv', index=False, header=False)

def process_data(data_file):
    # load data file
    data = pd.read_csv(data_file)
    # remove repeat data
    data = data.drop_duplicates()
    # remove Nan data
    data = data.dropna()
    # save processed_data
    data.to_csv('data_dir/anime_processed.csv', quoting=None, index=None, header=None)
    return data



if __name__ == "__main__":
    genre_list = anime_defination.genre_dict # or you can specify any genre here
    # scrape data
    anime_info_genre_dict = scrape_anime_using_genre()
    # saving data
    generate_data(genre_list, anime_info_genre_dict)
    # process data
    data = process_data('data_dir/anime_data.csv')


from utils import Utils

site_url = "https://myanimelist.net/anime/genre/"
my_util = Utils()
doc = my_util.get_topic_page(site_url, "Action")
titles = doc.find_all('h2', class_ = 'h2_anime_title')
images = doc.find_all('div', class_='image')
ratings = doc.find_all('div', class_= 'scormem')
genres_dt = doc.find_all('div', class_ = 'genres-inner js-genre-inner')
genre_list = []
anime_genre = []
i = 0
for genres in genres_dt:
    anime_genres = genres.find_all('span', class_ = "genre")
    genre_list = []
    for genre in anime_genres:
        genre_list.append(genre.text.strip())
    anime_genre.append(genre_list)
print(anime_genre)



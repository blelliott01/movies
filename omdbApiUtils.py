import requests

def getMoviData(imdb_id):
    url = f'http://www.omdbapi.com/?i={imdb_id}&apikey=c103f3f9'
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        movie_data_list = response.json()
        return movie_data_list
    else:
        return None
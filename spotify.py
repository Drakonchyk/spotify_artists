"""finding general info about artist"""
import base64
import requests

CLIENT_ID = 'b2d4daf524d44f81a1d5902946f765ce'
CLIENT_SECRET = '2390f673b70f4e398cbb41b716c4208e'

def get_token():
    """
    finds token
    """
    auth_code = f'{CLIENT_ID}:{CLIENT_SECRET}'
    coded_credentials = base64.b64encode(auth_code.encode()).decode()
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {'grant_type': 'client_credentials'}
    auth_headers = {'Authorization': f'Basic {coded_credentials}'}
    response = requests.post(auth_url, data = auth_data, headers = auth_headers, timeout=10)
    access_token = response.json().get('access_token')

    return access_token

def auth_header(token):
    """
    makes request header
    """
    request_headers = {'Authorization': f'Bearer {token}'}
    return request_headers

def search_artist(token, artist_name):
    """
    finds info about given artist
    """
    base_url = 'https://api.spotify.com/v1/search/'

    request_params = {
        'query': artist_name,
        'type': 'artist'
    }
    response = requests.get(base_url, headers = auth_header(token),
                            params=request_params, timeout=10)

    response_data = response.json()

    most_popular_artist = response_data.get('artists').get('items')[0]

    return most_popular_artist

def best_song(token, artist_id):
    """
    finds the most popular artist's song
    """
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UA'
    headers = auth_header(token)
    response = requests.get(url, headers = headers, timeout = 5)
    response_data = response.json()
    most_popular_song = response_data.get('tracks')[0]
    return most_popular_song

def song_markets(token, id_song):
    """
    finds available markets
    """
    url = f'https://api.spotify.com/v1/tracks/{id_song}?country=UA'
    headers = auth_header(token)
    response = requests.get(url, headers = headers, timeout = 5)
    response_data = response.json()
    available_markets = response_data.get("available_markets")
    return available_markets

def main():
    """
    communication with user
    """
    artist = input('Write your artist: ')
    token = get_token()
    data = search_artist(token, artist)
    data['best_song'] = best_song(token, data['id'])['name']
    data['available_markets'] = song_markets(token, best_song(token, data['id'])['id'])
    for i in data:
        print(i)
    while True:
        print('Press x to exit or write the name of data which you want to see')
        ans = input()
        if ans == 'x':
            break
        if ans in data:
            print(data[ans])
        else:
            print('You made a mistake')

if __name__ == '__main__':
    main()

"""
small web application tofind song locations
"""
import base64
import requests
from flask import Flask, request
import folium
import pandas

CLIENT_ID = 'b2d4daf524d44f81a1d5902946f765ce'
CLIENT_SECRET = '2390f673b70f4e398cbb41b716c4208e'

app = Flask(__name__)

def get_token():
    """
    makes a token
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
    most_popular_song = response_data.get('tracks')[0].get('id')
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

def generate_map(countries):
    """
    generates a map with countries where this song is played
    """
    song_map = folium.Map()
    data = pandas.read_csv('countries.csv')
    for i in range(len(data['country'])):
        if data['country'][i] in countries:
            song_map.add_child(folium.Marker(location = [data['latitude'][i], data['longitude'][i]],
                                    popup=f'{data["name"][i]}',
                                    icon=folium.Icon(color='pink', icon='info-sign')))
    html_map = song_map._repr_html_()
    return html_map


@app.route('/')
def start_route():
    """
    creates a form
    """
    return '<form action="/draw_map">\
            <label for="fname">Artist:</label><br>\
            <input type="text" name="artist" value="Imagine Dragons"><br>\
            <input type="submit" value="Submit">\
            </form>'


@app.route('/draw_map')
def main():
    """
    gets data about artist and its song, generates map
    """
    artist = request.args.get('artist')
    token = get_token()
    data = search_artist(token, artist)
    art_id = data['id']
    countries = song_markets(token, best_song(token, art_id))
    return generate_map(countries)

if __name__ == '__main__':
    app.run()

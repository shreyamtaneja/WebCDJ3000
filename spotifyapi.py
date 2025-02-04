import base64
import requests
import datetime
from urllib.parse import urlencode
import json
from client_keys import *

client_creds = f"{client_id}:{client_secret}"
encoded_creds = base64.b64encode(client_creds.encode())

global then
then = datetime.datetime.now()

global expires_in
expires_in = 0

def get_token_data():
    token_url = "https://accounts.spotify.com/api/token"
    token_request_header = {
	"Authorization": f"Basic {encoded_creds.decode()}"
    }
    token_request_data = {
	    "grant_type": "client_credentials"
    }
    r = requests.post(token_url, data=token_request_data, headers=token_request_header)
    if (r.status_code in range(200, 299)):
        return r.json()

def spotify_request(search_request_url):

    global then, expires_in
    #if (datetime.datetime.now() >= then + datetime.timedelta(seconds=expires_in)):
        #token_data = get_token_data()

    token_data = get_token_data()

    access_token = token_data['access_token']
    expires_in = token_data['expires_in']
    then = datetime.datetime.now()

    search_request_header = {
        "Authorization": f"Bearer {access_token}"
    }

    r = requests.get(search_request_url, headers=search_request_header)
    print(r.status_code)
    if(r.status_code in range(200,299)):
        return r

def search(name):
    search_request_data = urlencode(
        {
            "q": name,
            "type": "track",
            "limit": 5
        }
    )

    endpoint = "https://api.spotify.com/v1/search"
    search_request_url = f"{endpoint}?{search_request_data}"

    request_result = spotify_request(search_request_url)
    song_name = request_result.json()['tracks']['items'][0]['name']
    song_id = request_result.json()['tracks']['items'][0]['id']
    get_key(song_name, song_id)

def get_key(song_name, song_id):

    endpoint = "https://api.spotify.com/v1/audio-features/"
    search_request_url = f"{endpoint}{song_id}"
    request_result = spotify_request(search_request_url)
    song_key = request_result.json()['key']
    key_mode = request_result.json()['mode']

    mode_convert = {
        1: "Major",
        0: "Minor"
    }
    
    convert_musical = {
        0: "C",
        1: "C#/D♭",
        2: "D",
        3: "D#/E♭",
        4: "E",
        5: "F",
        6: "F#/G♭",
        7: "G",
        8: "G#/A♭",
        9: "A",
        10: "A#/B♭",
        11: "B",
    }

    camelot_mode = f"{song_key}{key_mode}"

    convert_camelot = {
        "01": "8B",
        "11": "3B",
        "21": "10B",
        "31": "5B",
        "41": "12B",
        "51": "7B",
        "61": "2B",
        "71": "9B",
        "81": "4B",
        "91": "11B",
        "101": "6B",
        "111": "1B",
        "00": "5A",
        "10": "12A",
        "20": "7A",
        "30": "2A",
        "40": "9A",
        "50": "4A",
        "60": "11A",
        "70": "6A",
        "80": "1A",
        "90": "8A",
        "100": "3A",
        "110": "10A",

    }

    key_musical = f"{convert_musical[song_key]} {mode_convert[key_mode]}"
    key_camelot = f"{convert_camelot[camelot_mode]}"

    print(f"Track: {song_name}, Reported Key: {song_key}, Musical Key: {key_musical}, Camelot Key: {key_camelot}")

search("clarity")

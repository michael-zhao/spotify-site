import pprint
import sys

import spotipy
import spotipy.util as util
import json

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = input("please enter your username id: ")

scope = 'user-top-read'
token = util.prompt_for_user_token(username,scope,client_id='4b69524b7c0e42c5b92d120b02ca6f17',client_secret='601b8d254c8b4b688918e6d4d1d5cd7d',redirect_uri='https://google.com/')

if token:
    sp = spotipy.Spotify(auth=token)
    searchQuery = input("Search for a song to see its audio features: ")
    artistQuery = input("filter search by artist if desired (blank if not): ")
    limitQuery = input("how many results do you want shown (default = 10)? ")
    if limitQuery == "":
        limitQuery = 10

    res = sp.search(q=searchQuery, limit=limitQuery, type='track')
    for item in res['tracks']['items']: 
        if artistQuery == "":
            print("Song name: " + color.BLUE + item['name'] + color.END + "; Artist: " + color.RED + item['album']['artists'][0]['name'] + color.END + "; ID: " + color.BOLD + item['id'] + color.END)
            print(sp.audio_features(item['id']))
        else:
            if artistQuery.lower() in item['album']['artists'][0]['name'].lower():
                print("Song name: " + color.BLUE + item['name'] + color.END + "; Artist: " + color.RED + item['album']['artists'][0]['name'] + color.END + "; ID: " +\
                    color.BOLD + item['id'] + color.END)
                print(sp.audio_features(item['id']))
    
else:
    print("Can't get token for", username)

    
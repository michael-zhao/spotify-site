import pprint
import sys

import spotipy
import spotipy.util as util
import json

class Color:
    BLUE = '\033[94m'
    END = '\033[0m'

def main():
    """Main method."""
    username = get_username(sys.argv)
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope)
    features = []
    done = False
    if token:
        sp = spotipy.Spotify(auth=token)
        search_query = input("Search for a song to see its audio features: ")
        artist_query = input("filter search by artist if desired (blank if not): ")
        limit_query = input("how many results do you want shown (default = 10)? ")
        
        first_pass = True
        while not done:
            feature_query = input("What features do you want to see (default = all)? Features include " +\
                "danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, " +\
                    "liveness, valence, tempo, and time signature \n")
            if feature_query.strip() == "" and first_pass:
                features = ["danceability", "energy", "key", "loudness", "mode", "speechiness", \
                    "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time signature"]
                done = True
            elif feature_query.strip() == "" and not first_pass:
                done = True
            else:
                features.append(feature_query)
                checker = input(f"features now include: {features}. type 'done' to finish input, or return to continue entering features \n")
                if checker == "done":
                    done = True
            first_pass = False

        if limit_query == "":
            limit_query = 10

        res = sp.search(q=search_query, limit=limit_query, type='track')
        get_results(sp, res, artist_query, features)      
    else:
        print(f"Can't get token for {username}")  

def get_username(arg):
    """
    Returns a username based on the first non-file input of the system command, or takes in input
    for username.

    arg -- sys.argv, or the system input
    """
    if len(arg) > 1:
        username = arg[1]
    else:
        username = input("please enter your username id: ")
    return username

# def get_danceability(sp, item):
#     return item[0]['danceability']

# def get_energy(sp, item):
#     return item[0]['energy']

# def get_key(sp, item):
#     return item[0]['key']

# def get_loudness(sp, item):
#     return item[0]['loudness']

# def get_mode(sp, item):
#     return item[0]['mode']

# def get_speechiness(sp, item):
#     return item[0]['speechiness']

# def get_acousticness(sp, item):
#     return item[0]['acousticness']

# def get_instrumentalness(sp, item):
#     return item[0]['instrumentalness']

# def get_liveness(sp, item):
#     return item[0]['liveness']

# def get_valence(sp, item):
#     return item[0]['valence']

# def get_tempo(sp, item):
#     return item[0]['tempo']

# def get_time_signature(sp, item):
#     return item[0]['time_signature']

def print_requested_features(sp, item, feature_input):
    """
    Prints results and user's desired features.

    sp -- Spotify object using an authentication token.
    item -- all of the results given a search query.
    feature_input -- the list of features desired by the user.
    """
    for feature in feature_input:
        if feature in item[0]:
            print(f"{feature}: {item[0][feature]}")

def get_results(sp, res, artist_query, feature_input):
    dct_print = {}
    for item in res['tracks']['items']: 
        features = sp.audio_features(item['id'])
        if artist_query.strip() == "":
            print("Song name: " + Color.BLUE + item['name'] + Color.END + "; Artist: " +\
                 item['album']['artists'][0]['name'] + "; ID: " + item['id'])
            # print(features)
            # print(f"Danceability: {get_danceability(sp, features)}")
            print("Genre:", get_genre(sp, item))
            print_requested_features(sp, features, feature_input)
        else:
            if artist_query.lower() in item['album']['artists'][0]['name'].lower():
                print("Song name: " + item['name'] + "; Artist: " +\
                     item['album']['artists'][0]['name'] + "; ID: " + item['id'])
                # print(features)
                print_requested_features(sp, features, feature_input)

def get_genre(sp, track):
    track_album = sp.album(track['album']["external_urls"]["spotify"])
    print(track_album)
    return track_album["genres"]

main()

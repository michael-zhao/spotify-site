"""
Module allows user to look up album art and start playback of chosen tracks on their device(s).
"""

import os
import sys
import json #keep for a commented out piece of code
from json.decoder import JSONDecodeError #keep for commented out code?
import webbrowser
import spotipy
import spotipy.util as util

def main():
    """Main method."""
    username = sys.argv[1]
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'
    token = get_token(username, scope)
    spotify = create_spotify_object(token)
    devices = get_devices(spotify)

    user = get_user_info(spotify)
    display_name = user[1]
    followers = user[2]

    while True:
        print()
        print('>>> Welcome to Spotipy, ' + display_name + '!')
        print(">>> You have " + str(followers) + " followers!")
        print()
        print("0 - Search for an artist")
        print("1 - exit")
        print()
        choice = input("Your choice: ")

        if choice == "0":
            print("0")
            search_query = input("What is the artist's name? ")
            print()

            #get search results
            search_results = spotify.search(search_query, 1, 0, "artist")
            #print(json.dumps(searchResults, sort_keys=True, indent=4))

            artist = search_results['artists']['items'][0]
            print("Artist: " + artist['name'])
            print("Followers: " + (str(artist['followers']['total']) + " followers"))
            print("Genres: ", end="")
            for x in range(len(artist['genres'])):
                print(artist['genres'][x], end="")
                if x < len(artist['genres'])-1:
                    print(", ", end="")
            print()
            webbrowser.open(artist['images'][0]['url'])
            artist_id = artist['id']

            #album & track details
            track_uris = []
            track_art = []
            z = 0

            #extract album data
            album_results = spotify.artist_albums(artist_id)
            album_results = album_results['items']
            for item in album_results:
                print("ALBUM: " + item['name'])
                album_id = item['id']
                album_art = item['images'][0]['url']

                #extract track data
                track_results = spotify.album_tracks(album_id)
                track_results = track_results['items']
                for track in track_results:
                    print(str(z) + ": " + track['name'])
                    track_uris.append(track['uri'])
                    track_art.append(album_art)
                    z += 1
                print()#see album art
            while True:
                song_selection = input("Enter a song number to see album art (if none, 'x'): ")
                if song_selection == "x":
                    break
                track_selection_list = []
                track_selection_list.append(track_uris[int(song_selection)])
                spotify.start_playback(devices[1], None, track_selection_list)
                webbrowser.open(track_art[int(song_selection)])

                #end program
        if choice == "1":
            break
    #print(json.dumps(VARIABLE,sort_keys=true,indent=4))

def get_token(username, scope):
    """Returns a token given a username and scope."""
    #user ID: 1219415681
    #erase cache, prompt user permission
    try:
        token = util.prompt_for_user_token(
            username, scope, client_id='4b69524b7c0e42c5b92d120b02ca6f17',
            client_secret='601b8d254c8b4b688918e6d4d1d5cd7d', redirect_uri='https://google.com/')
    except: #not sure what exception type to specify
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope)
    return token

#create spotify object
def create_spotify_object(token):
    """Creates a Spotify object."""
    spotify_object = spotipy.Spotify(auth=token)
    return spotify_object

def get_devices(sp):
    """Returns a pair of devices and device ID."""
#get current device
    devices = sp.devices()
    #print(json.dumps(devices,sort_keys=True,indent=4))
    devices_id = devices['devices'][0]['id']
    return devices, devices_id

def get_current_track_and_artist(sp):
    """Returns a tuple consisting of the track and artist currently playing."""
    #current track info
    track = sp.current_user_playing_track()
    #print(json.dumps(track,sort_keys=True,indent=4))
    print()
    #print(track)
    artist = track['item']['artists'][0]['name']
    track = track['item']['name']

    if artist != "":
        print("Playing: " + artist + " - " + track)
    return track, artist

def get_user_info(sp):
    """Returns a 3-tuple of user, display name, and followers."""
    #user info
    user = sp.me()
    display_name = user['display_name']
    followers = user['followers']['total']
    return user, display_name, followers

main()

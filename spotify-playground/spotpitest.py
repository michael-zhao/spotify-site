import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

def main():
    """Main method."""
    username = sys.argv[1]
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'
    token = get_token(username, scope)
    spotify = create_spotify_object(token)
    devices = get_devices(spotify)

def get_token(username, scope):
    """Returns a token given a username and scope."""
    #user ID: 1219415681
    #erase cache, prompt user permission
    try:
        token = util.prompt_for_user_token(
            username, scope, client_id='4b69524b7c0e42c5b92d120b02ca6f17',
            client_secret='601b8d254c8b4b688918e6d4d1d5cd7d', redirect_uri='https://google.com/')
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope)
    return token

#create spotify object
def create_spotify_object(token):
    spotify_object = spotipy.Spotify(auth=token)
    return spotify_object

def get_devices(sp):
#get current device
    devices = sp.devices()
    #print(json.dumps(devices,sort_keys=True,indent=4))
    devices_id = devices['devices'][0]['id']
    return devices

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

while True:
    print()
    print('>>> Welcome to Spotipy, ' + displayName + '!')
    print(">>> You have " + str(followers) + " followers!")
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    print()
    choice = input("Your choice: ")

    #Search for artist
    if choice == "0":
        print("0")
        searchQuery = input("What is the artist's name? ")
        print()

        #get search results
        searchResults = spotifyObject.search(searchQuery, 1,0,"artist")
        #print(json.dumps(searchResults, sort_keys=True, indent=4))

        artist = searchResults['artists']['items'][0]
        print("Artist: " + artist['name'])
        print("Followers: " + (str(artist['followers']['total']) + " followers"))
        print("Genres: ", end="")
        for x in range(len(artist['genres'])):
            print(artist['genres'][x], end="")
            if (x < len(artist['genres'])-1):
                print(", ", end="")
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        #album & track details
        trackURIs = []
        trackArt = []
        z = 0

        #extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']
        
        for item in albumResults:
            print("ALBUM: " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            #extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z += 1
            print()

        #see album art
        while True:
            songSelection = input("Enter a song number to see album art (if none, 'x'): ")
            if songSelection == "x":
                break
            trackSelectionList = []
            trackSelectionList.append(trackURIs[int(songSelection)])
            spotifyObject.start_playback(devicesID,None,trackSelectionList)
            webbrowser.open(trackArt[int(songSelection)])

    #end program
    if choice == "1":
        break
#print(json.dumps(VARIABLE,sort_keys=true,indent=4))

main()

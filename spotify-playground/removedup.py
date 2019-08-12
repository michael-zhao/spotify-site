import sys
import spotipy
import webbrowser
import json
import spotipy.util as util

#get username
username = sys.argv[1]

#modify scope of operations
scope = 'user-library-modify playlist-modify-public'
#token
token = util.prompt_for_user_token(username,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    plists = sp.user_playlists(username,limit=10)
    assign = {}
    for x in range(len(plists['items'])):
        print(plists['items'][x]['name'], plists['items'][x]['uri'])
        uri = plists['items'][x]['uri'].index("playlist:") + len("playlist:")
        assign['x'] = plists['items'][x]['uri'][uri:]
        print(x + 1, assign[x])
    inp = int(input("Choose a playlist: "))
    songInList = sp.user_playlist_tracks(username,inp)
    while True:
        sp.trace = False



import pprint
import sys

import spotipy  # figured out linting error (module spotipy not found) by changing .vscode/settings.json path
import spotipy.util as util
import json

#user id: 1219415681

#used powershell, $env:SPOTIPY_CLIENT_ID...='...'
# $env:SPOTIPY_CLIENT_SECRET='...'
# $env:SPOTIPY_REDIRECT_URI='...'

def main():
    #get username from terminal, or else ask for user input username
    username = get_username(sys.argv)
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope)
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        ranges = ['short_term','medium_term','long_term']
        track_or_artist = str.lower(input("Do you want to see your top tracks or top artists? "))
        if track_or_artist == "tracks":
            get_tracks(token, sp, ranges)
        elif track_or_artist == "artists":
            get_artists(token, sp, ranges)
    else:
        print("Can't get token for", username)

def get_username(arg):
    if len(arg) > 1:
        username = arg[1]
    else:
        username = input("please enter your username id: ")
    return username

def get_tracks(token, sp, ranges):
    term = str.lower(input("What range do you want (short, medium, long)? "))
    if term != "short" or term != "medium" or term != "long":
        term = str.lower(input("Please enter a valid range: short, medium, or long: "))
    print()
    track_range_i = input("How many artists do you want to show? Enter a number 1-50 (default 10): ")
    try:
        track_range = int(track_range_i)
    except ValueError:
        track_range = 10
    leng = track_range
    print()

    if term == "short":
        print()
        avg = 0
        print("Range: Short term")
        results = sp.current_user_top_tracks(time_range=ranges[0],limit=leng)
        for i, item in enumerate(results['items'],1):
            avg += item['popularity']
            print(str(i) + ")", item['name'] + " - " + item['album']['artists'][0]['name'], end="" if len(item['album']['artists']) > 1 else " - popularity: " + str(item['popularity']) + "\n")
            for x in range(1,len(item['album']['artists'])):
                print(", " + item['album']['artists'][x]['name'], end="" if x+1 < len(item['album']['artists']) else " - popularity: " + str(item['popularity']) + "\n")
        print("average popularity of music listened to: " + str(avg/leng))
        print()

    elif term == "medium":
        print()
        avg = 0
        print("Range: Medium term")
        results = sp.current_user_top_tracks(time_range=ranges[1],limit=leng)
        for i, item in enumerate(results['items'],1):
            avg += item['popularity']
            print(str(i) + ")", item['name'] + " - " + item['album']['artists'][0]['name'], end="" if len(item['album']['artists']) > 1 else " - popularity: " + str(item['popularity']) + "\n")
            for x in range(1,len(item['album']['artists'])):
                print(", " + item['album']['artists'][x]['name'], end="" if x+1 < len(item['album']['artists']) else " - popularity: " + str(item['popularity']) + "\n")
        print("average popularity of music listened to: " + str(avg/leng))
        print()

    elif term == "long":
        print()
        avg = 0
        print("Range: Long term")
        results = sp.current_user_top_tracks(time_range=ranges[2],limit=leng)
        for i, item in enumerate(results['items'],1):
            avg += item['popularity']
            print(str(i) + ")", item['name'] + " - " + item['album']['artists'][0]['name'], end="" if len(item['album']['artists']) > 1 else " - popularity: " + str(item['popularity']) + "\n")
            for x in range(1,len(item['album']['artists'])):
                print(", " + item['album']['artists'][x]['name'], end="" if x+1 < len(item['album']['artists']) else " - popularity: " + str(item['popularity']) + "\n")
        print("average popularity of music listened to: " + str(avg/leng))
        print()

def get_artists(token, sp, ranges):
    term = str.lower(input("What range do you want (short, medium, long)? "))
    if term != "short" or term != "medium" or term != "long":
        term = str.lower(input("Please enter a valid range: short, medium, or long: "))
    print()
    artist_range_i = input("How many artists do you want to show? Enter a number 1-50 (default 10): ")
    try:
        artist_range = int(artist_range_i)
    except ValueError:
        artist_range = 10
    leng = artist_range
    print()

    if term == "short" or term == "s":
        print("Range: Short term")
        results =sp.current_user_top_artists(time_range=ranges[0],limit=leng)
        for i, item in enumerate(results['items'],1):
            popu = " - popularity: " + str(item['popularity'])
            with_genre = item['name'] + popu + "; genres: " + item['genres'][0] if len(item['genres']) > 0 else item['name'] + popu
            print(str(i) + ")", with_genre, end="" if len(item['genres']) > 1 else "\n")
            for x in range(1,len(item['genres'])):
                print(", " + item['genres'][x], end="" if x+1 < len(item['genres']) else "\n")
        print()

    elif term == "medium" or term == "m" or term == "med":
        print("Range: Medium term")
        results = sp.current_user_top_artists(time_range=ranges[1],limit=leng)
        for i, item in enumerate(results['items'],1):
            withGenre = item['name'] + "; genres: " + item['genres'][0] if len(item['genres']) > 0 else item['name']
            print(str(i)+ ")", withGenre, end="" if len(item['genres']) > 1 else "\n")
            for x in range(1,len(item['genres'])):
                print(", " + item['genres'][x], end="" if x+1 < len(item['genres']) else "\n")
        print()

    elif term == "long" or term == "l":
        print("Range: Long term")
        results = sp.current_user_top_artists(time_range=ranges[2],limit=leng)
        for i, item in enumerate(results['items'],1):
            withGenre = item['name'] + "; genres: " + item['genres'][0] if len(item['genres']) > 0 else item['name']
            print(str(i) + ")", withGenre, end="" if len(item['genres']) > 1 else "\n")
            for x in range(1,len(item['genres'])):
                print(", " + item['genres'][x], end="" if x+1 < len(item['genres']) else "\n")
        print()


main()

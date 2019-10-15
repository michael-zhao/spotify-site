import pprint
import sys

import spotipy  # figure out how to get rid of the dumb intellicode warning
import spotipy.util as util
import json

#user id: 1219415681

#get username from terminal, or else ask for user input username
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = input("please enter your username id: ")

scope = 'user-top-read'
token = util.prompt_for_user_token(username,scope,client_id='4b69524b7c0e42c5b92d120b02ca6f17',client_secret='601b8d254c8b4b688918e6d4d1d5cd7d',redirect_uri='https://google.com/')

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    ranges = ['short_term','medium_term','long_term']
    track_or_artist = str.lower(input("Do you want to see your top tracks or top artists? "))

    if track_or_artist == "tracks":
        term = str.lower(input("What range do you want (short, medium, long)? "))
        print()
        leng = int(input("How many songs do you want to show (1-50)? "))
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
            print("average popularity: " + str(avg/leng))
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
            print("average popularity: " + str(avg/leng))
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
            print("average popularity: " + str(avg/leng))
            print()

    if track_or_artist == "artists":
        term = str.lower(input("What range do you want (short, medium, long)? "))
        print()
        artists_range = input("How many artists do you want to show? Enter a number 1-50 (default 10)")
        leng = int(artists_range) if isinstance(artists_range, int) else 10
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
else:
    print("Can't get token for", username)




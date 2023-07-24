"""
Module for finding the top Spotify artists for a user.
"""
import sys
import types

import spotipy  # figured out linting error (module spotipy not found) by changing .vscode/settings.json path
import spotipy.util as util

# user id: 1219415681

# used powershell, $env:SPOTIPY_CLIENT_ID...='...'
# $env:SPOTIPY_CLIENT_SECRET='...'
# $env:SPOTIPY_REDIRECT_URI='...'

consts = types.SimpleNamespace()
consts.SHORT_TERM = "short"
consts.MEDIUM_TERM = "medium"
consts.LONG_TERM = "long"

def main():
    """
    Main method to run in cli
    """

    # get username from terminal, or else ask for user input username
    username = get_username(sys.argv)
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope)
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        ranges = ['short_term', 'medium_term', 'long_term']
        track_or_artist = str.lower(input("Do you want to see your top tracks or top artists? "))
        while track_or_artist:
            if track_or_artist == "tracks":
                get_tracks(token, sp, ranges)
            elif track_or_artist == "artists":
                get_artists(token, sp, ranges)
            else:
                track_or_artist = str.lower(input("Please enter a valid parameter: tracks or artists "))

    else:
        print("Can't get token for", username)

def get_username(arg):
    """
    Retrieve username from input
    """

    if len(arg) > 1:
        username = arg[1]
    else:
        username = input("please enter your username id: ")
    return username

def get_tracks(token, sp, ranges):
    """
    Retrieve the top tracks based on input from user
    """
    valid_responses = {"short", "medium", "long"}
    term = str.lower(input("What range do you want (short, medium, long)? "))
    while term not in valid_responses:
        term = str.lower(input("Please enter a valid range: short, medium, or long: "))
    print()
    track_range_i = input("How many artists do you want to show? Enter a number 1-50 (default 10): ")
    try:
        track_range = int(track_range_i)
    except ValueError:
        track_range = 10
    leng = track_range
    print()

    match term:
        case consts.SHORT_TERM as time_range:
            print(time_range)
            results = sp.current_user_top_tracks(time_range=ranges[0], limit=leng)
            print_popularity(results, leng)
        case consts.MEDIUM_TERM as time_range:
            print(time_range)
            results = sp.current_user_top_tracks(time_range=ranges[1], limit=leng)
            print_popularity(results, leng)
        case consts.LONG_TERM as time_range:
            print(time_range)
            results = sp.current_user_top_tracks(time_range=ranges[2], limit=leng)
            print_popularity(results, leng)
        case _:
            print("Invalid input - how did you get here?")
    print()

def get_artists(token, sp, ranges):
    """
    Retrieve top artists based on input from user.
    """
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

    match term:
        case consts.SHORT_TERM as time_range:
            print(time_range)
            results = sp.current_user_top_artists(time_range=ranges[0], limit=leng)
            print_artists_helper(results)
        case consts.MEDIUM_TERM as time_range:
            print(time_range)
            results = sp.current_user_top_artists(time_range=ranges[1], limit=leng)
            print_artists_helper(results)
        case consts.LONG_TERM as time_range:
            print(time_range)
            results = sp.current_user_top_artists(time_range=ranges[2], limit=leng)
            print_artists_helper(results)
        case _:
            print("How did you get here?")
    print()

def print_popularity(results, leng):
    """
    Helper method to find and print the popularity of an artist.
    """
    sum_for_avg = 0
    for i, item in enumerate(results['items'], 1):
        sum_for_avg += item['popularity']
        print(str(i) + ")", item['name'] + " - " + item['album']['artists'][0]['name'],
                    end="" if len(item['album']['artists']) > 1 else " - popularity: " + str(item['popularity']) + "\n")
        for x in range(1, len(item['album']['artists'])):
            print(", " + item['album']['artists'][x]['name'],
                    end="" if x + 1 < len(item['album']['artists']) else " - popularity: " + str(
                        item['popularity']) + "\n")
    print("average popularity of music listened to: " + str(sum_for_avg / leng))
    print()

def print_artists_helper(results):
    """
    Helper method to find and print the top artists of a user.
    """
    for i, item in enumerate(results['items'], 1):
        with_genre = item['name'] + "; genres: " + item['genres'][0] if len(item['genres']) > 0 else item['name']
        print(str(i) + ")", with_genre, end="" if len(item['genres']) > 1 else "\n")
        for x in range(1, len(item['genres'])):
            print(", " + item['genres'][x], end="" if x + 1 < len(item['genres']) else "\n") 


main()

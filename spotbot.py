#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import spotipy.util as util
import sys
from dotenv import load_dotenv
from os.path import join, dirname
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)


def search_tool(sp):
    query = ''
    result = sp.search(query)
    try:
        album_cover = result['tracks']['items'][1]['album']['images'][0]['url']
        print album_cover
    # album_name = result['tracks']['items'][0]['album']['name']
    # print album_name

    # print result['tracks']['items'][0]
    # for i in range(11):
    #     print '\n', '\n', '\n', result['tracks']['items'][i]['album']
    #     print album_name
    #     print album_cover

    # top_results = result['tracks']['items'][0]['artists'][0]['external_urls']['spotify']
    # print top_results
    except Exception as e:
        print('We have an error!\n', type(e), '\n', e)


def artist_top_10(sp):
    """Led Zeppelin top hits"""
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
    # lz_uri = 'spotify:artist:', + artist_id
    results = sp.artist_top_tracks(lz_uri)

    for track in results['tracks']:
        # print track
        print 'song          : ' + track['name']
        print 'preview_audio : ' + track['preview_url']
        print 'album cover   : ' + track['album']['images'][0]['url']
        print


# View specific user playlists
def get_playlists(sp):
    # pulls All my playlists
    playlists = sp.user_playlists('hutman64')

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" %
                  (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


# get_playlists(sp)
# artist_top_10(sp)
search_tool(sp)

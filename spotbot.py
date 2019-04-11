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
import sys
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)


def search_tool(sp):
    result = sp.search('Spotify')
    return result['tracks']['items'][0]['artists'][0]['external_urls']['spotify']


def artist_top_10(sp):
    """Led Zeppelin top hits"""
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    results = sp.artist_top_tracks(lz_uri)

    for track in results['tracks']:
        return ('song          : ' + track['name'] + 'preview_audio : ' +
                track['preview_url'] + 'album cover   : ' + track['album']['images'][0]['url'])


def get_playlists(sp):
    playlists = sp.user_playlists('hutman64')

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            return ("%4d %s %s" %
                    (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

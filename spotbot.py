
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '793dac3770d04c0592dc253c056988c2'
client_secret = 'f63d13bf765547dd8fc7742bf3d25949'

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 1. View specific user playlists
playlists = sp.user_playlists('hutman64')

while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" %
              (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

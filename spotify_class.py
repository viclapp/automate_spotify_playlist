#Import class
import os
import spotipy
import requests
import base64
import webbrowser
from flask import Flask, request, redirect

class SpotifyManager:

    def __init__(self, client_id, client_secret, playlist_name):
        self.client_id = client_id
        self.client_secret = client_secret
        self.playlist_name = playlist_name
        self.conn = None
        self.app = Flask(__name__)
        self.redirect_uri = 'http://localhost:8080/callback'
        self.auth_url = (
            f'https://accounts.spotify.com/authorize?response_type=code'
            f'&client_id={self.client_id}&redirect_uri={self.redirect_uri}'
            f'&scope=playlist-modify-private playlist-modify-public user-read-playback-state user-modify-playback-state'
        )

    def login_to_spotify(self):
        self.conn = spotipy.Spotify(
            auth_manager = spotipy.SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri='http://localhost:8080',
                scope='user-read-playback-state,user-modify-playback-state,playlist-modify-private'
            )
        )

        return self.conn
    
    def create_playlist(self):
        if not self.conn:
            raise ValueError("Not connected to Spotify, Call login_to_spotify() first")
        
        user = self.conn.current_user()
        playlist = self.conn.user_playlist_create(user['id'], public=False, name=self.playlist_name)
        return playlist

    def get_spotify_token(self):
        sp_oauth = spotipy.SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope='playlist-modify-private playlist-modify-public')
        
        token_info = sp_oauth.get_access_token()
        access_token = token_info['access_token']
        return access_token

    # def get_spotify_token(self):
    #     @self.app.route('/')
    #     def login():
    #         webbrowser.open(self.auth_url)
    #         return 'Please authorize the application in the browser.'

    #     @self.app.route('/callback')
    #     def callback():
    #         code = request.args.get('code')
    #         token_url = 'https://accounts.spotify.com/api/token'
    #         auth_header = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()
    #         headers = {
    #             'Authorization': f'Basic {auth_header}',
    #             'Content-Type': 'application/x-www-form-urlencoded'
    #         }
    #         data = {
    #             'grant_type': 'authorization_code',
    #             'code': code,
    #             'redirect_uri': self.redirect_uri
    #         }
    #         response = requests.post(token_url, headers=headers, data=data)
    #         token_info = response.json()
    #         access_token = token_info['access_token']
    #         return f'Access Token: {access_token}'

    #     self.app.run(port=8080)
    
    
    def search_track_in_spotify(self,track,album,artist,token):
        search_url = 'https://api.spotify.com/v1/search'
        headers = {'Authorization': f'Bearer {token}'}
        query = f'track:{track} artist:{artist} album:{album}'
        params = {'q': query, 'type': 'track', 'limit': 1}
        search_res = requests.get(search_url, headers=headers, params=params)
        search_res.raise_for_status()
        return search_res.json()
    
    
    # def add_track_to_playlist(self, track_uri, token, playlist_id):
    #     add_track_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    #     headers = {
    #         'Authorization': f'Bearer {token}',
    #         'Content-Type': 'application/json'
    #     }
    #     data = {'uris': [track_uri]}
    #     response = requests.post(add_track_url, headers=headers, json=data)
    #     response.raise_for_status()
    #     return response.status_code
    
    def add_track_to_playlist(self, playlist_id, track_id):
        sp_oauth = spotipy.SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope='playlist-modify-private playlist-modify-public')
        
        token_info = sp_oauth.get_access_token()
        access_token = token_info['access_token']
        sp = spotipy.Spotify(auth=access_token)
        sp.user_playlist_add_tracks(user=sp.current_user()['id'], playlist_id=playlist_id, tracks=track_id)
        return 
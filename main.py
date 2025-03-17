from prompt import prompt
from spotify_class import SpotifyManager
from mistral_class import MistralAgent
import os
import json

API_KEY = os.getenv('MISTRAL_API_KEY')
client_id=os.getenv('SPOTIFY_CLIENT_ID')
client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')

def main():

    #Etape 1: demander au chat de sortir un json avec une liste de 30 morceaux, artistes, albums

    mistral = MistralAgent(prompt, API_KEY)

    print("Step 1: Getting the tracks from Mistral AI")
    json_file = mistral.ask_le_chat()


    #Etape 3: créer 3 listes avec le contenu du json

    print("Step 2: Creating the lists from the JSON file")
    title = [track['titre'] for track in json_file]
    artist = [track['artiste'] for track in json_file]
    album = [track['album'] for track in json_file]

    #Etape 4: créer la playlist 
 
    print("Step 3: Connecting to Spotify")
    spotify = SpotifyManager(client_id=client_id, client_secret=client_secret, playlist_name="")
    spotify.playlist_name = "AI playlist"
    spotify.conn = spotify.login_to_spotify()

    print("Step 4: Creating playlist in Spotify")
    spotify_playlist = spotify.create_playlist()

    playlist_id = spotify_playlist['id']
    print(playlist_id)

    #spotify_token = spotify.get_spotify_token()

    #Etape 5: chercher pour chaque morceau l'uri spotify

    res_search_json = ['3GCdLUSnKSMJhs4Tj6CV3s']

    print("Step 6: getting the uri for titles")
    for i in range(len(title)):
        track_name = title[i]
        track_artist = artist[i]
        track_album = album[i]

        spotify_token = spotify.get_spotify_token()

        track_uri_json = spotify.search_track_in_spotify(track_name, track_album, track_artist, spotify_token)

        if track_uri_json['tracks']['total'] > 0:
            track_uri = track_uri_json['tracks']['items'][0]['uri']
            uri = track_uri.split(':')[-1]
            #res_search_json.append(uri)
    print(res_search_json)        

    #Etape 6: ajouter uri par uri les morceaux à la playlist
    print("Last step: adding tracks into the playlist")
    for i in range(len(res_search_json)):
        track_json = res_search_json[i]
        spotify.add_track_to_playlist(playlist_id, track_json)

    print("Job done, you can now listen to your new playlist!")

    return


if __name__ == '__main__':
    main()
# automate_spotify_playlist
The objective of this project is to automate the creation of a playlist using a LLM.

How does it work (basicaly)?
Using this code, you'll just need to ask the LLM to find new songs based on what you like and it will create a new playlist!

## Information about the project

### Use of OOP
The OOP (Object Oriented Programation) is used in this project in order to have specific agents that works on specific topic.
In this project, we have a SpotifyAgent (python class with all Spotify API functions) and a MistralAgent (python class with all Mistral AI API functions).

### MistralAgent class
The MistralAgent class is a simple class that I created in order to connect to the Mistral AI API and get the list of all new songs from the LLM.
In this project, we are using the model mistral-tiny. Why this model? Because it is simple of use and free. 
Get all information of the models here: https://docs.mistral.ai/getting-started/models/models_overview/

```
def ask_le_chat(self):
        model = self.model
        client = Mistral(api_key=self.api_key)
        chat_res = client.chat.complete(
            model=model,
            messages=[
                {
                    "role":"user",
                    "content":self.prompt
                }
            ]
        )
        try:
            chat_res = chat_res.json()
            chat_res_json = json.loads(chat_res)
            res = chat_res_json['choices'][0]['message']['content']
            start_index = res.find('[')
            end_index = res.find(']')
            res_json = res[start_index:end_index+1].strip()
            res_json = json.loads(res_json)
            return res_json
        except ValueError:
            print("JSON format is not valid")
```

### SpotifyAgent class
The SpotifyAgent class is the more complex part of this project. In this class, we create all the functions that we will use to interact with the Spotify API.
Before starting, check the documentation here: https://developer.spotify.com/documentation/web-api
In this class, we have several function.
- login_to_spotify(): Obviously you need credentials to connect to the API and to your app
```
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
```
- create_playlist(): It will creates a new playlist (empty) for your user
```
def create_playlist(self):
        if not self.conn:
            raise ValueError("Not connected to Spotify, Call login_to_spotify() first")
        
        user = self.conn.current_user()
        playlist = self.conn.user_playlist_create(user['id'], public=False, name=self.playlist_name)
        return playlist
```
- get_spotify_token(): You'll nedd this function to get a token from the API in order to add songs to your playlist
```
def get_spotify_token(self):
        sp_oauth = spotipy.SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope='playlist-modify-private playlist-modify-public')
        
        token_info = sp_oauth.get_access_token()
        access_token = token_info['access_token']
        return access_token
```
- search_track_in_spotify(): After the LLM gave you songs, you need to find the IDs of those songs in Spotify
```
def search_track_in_spotify(self,track,album,artist,token):
        search_url = 'https://api.spotify.com/v1/search'
        headers = {'Authorization': f'Bearer {token}'}
        query = f'track:{track} artist:{artist} album:{album}'
        params = {'q': query, 'type': 'track', 'limit': 1}
        search_res = requests.get(search_url, headers=headers, params=params)
        search_res.raise_for_status()
        return search_res.json()
```
- add_track_to_playlist(): The final function, the one that will add all the songs to your new playlist
```
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
```

### The prompt
In your prompt, you can give the model any type of songs you would like to have in your playlist. The only thing you need to have, is an example of the JSON format you want, so that the LLM creates a well formated response to your request.


## How does it work?

### API connection
First thing first, you need to create developers accounts for both Mistral and Spotify. You can find information on the links above.

To create the API key for mistral, go to https://console.mistral.ai/api-keys and click on Create a new key. Once you created it, you'll see it in your space:
![Capture d’écran 2025-03-28 à 14 13 21](https://github.com/user-attachments/assets/ca401ca2-494e-4fcb-a32c-2ae8c2cde654)

To create the Spotify key, you first need to create a Spotify developer account (https://developer.spotify.com/).
Once you have your account, go to your_space > dashboard. Now you can create a Spotify app (mandatory step). Here is the setup of the app:
![Capture d’écran 2025-03-28 à 14 15 56](https://github.com/user-attachments/assets/c14183cf-5224-4741-a169-05d0ff4ece13)

In the dashboard page, you can check some info about the app your created:
![Capture d’écran 2025-03-28 à 14 16 27](https://github.com/user-attachments/assets/0b3034c0-4f56-4681-81ba-066fdad5d95c)



### Step 1
You connect to the Mistral AI API using the MistralAgent class. 
You can update the prompt to get the type of music you want :)

### Step 2
Once the Mistral model has find some new songs to get and create a JSON with the information about these songs, you will create lists from the JSON with the songs, artists and album (you will need it to find the song IDs in Spotify)

### Step 3
Once you have information about the songs, you'll need to create the playlist, find the songs and add them to your playlist.
I want my playlist name to be simple, so I called it 'AI Playlist' but feel free to named it as you want!
You need to keep the playlist_id in a variable for later.
The script will connect to the Spotify API and create an new empty playlist:
![Capture d’écran 2025-03-28 à 14 08 37](https://github.com/user-attachments/assets/a1062cb2-4cdb-4b5f-aee6-9858dc2cf331)


### Step 4
Now that the playlist is created, you need to find the songs in Spotify using their uri. 
For each songs of the list, you'll look for them in Spotify using all the information you have, and take their uri.
You save all the uri in a list and wait for the last step to start, add the songs to the playlist!

### Step 5
Let's recap a bit, you asked a LLM for new songs to listen, you connected to Spotify and craeted a new playlist and finally got the uris of all the songs suggested by the model.
Impressive, but you still can't listen to them. The final step of this code, is to add the songs to your playlist. For this, you will call the function add_track_to_playlist() of the SpotifyAgent class.
For each uri in the list, this function will add the corresponded song to your playlist.
And voilà! You have a new playlist built automatically using a LLM!

--insert image--

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

### SpotifyAgent class
The SpotifyAgent class is the more complex part of this project. In this class, we create all the functions that we will use to interact with the Spotify API.
Before starting, check the documentation here: https://developer.spotify.com/documentation/web-api
In this class, we have several function.
- login_to_spotify(): Obviously you need credentials to connect to the API and to your app
- create_playlist(): It will creates a new playlist (empty) for your user
- get_spotify_token(): You'll nedd this function to get a token from the API in order to add songs to your playlist
- search_track_in_spotify(): After the LLM gave you songs, you need to find the IDs of those songs in Spotify
- add_track_to_playlist(): The final function, the one that will add all the songs to your new playlist

### The prompt
In your prompt, you can give the model any type of songs you would like to have in your playlist. The only thing you need to have, is an example of the JSON format you want, so that the LLM creates a well formated response to your request.


## How does it work?

### API connection
First thing first, you need to create developers accounts for both Mistral and Spotify. You can find information on the links above.

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

--insert image--

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

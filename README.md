## PlaylistShift
Python script that allows you to migrate your Spotify playlists to YouTube

- `pip install -r requirements.txt`
- `python spin_server.py` This will run a server which is needed to perform login with your gmail auth to get authorization code
- `python spotify2yt.py` Here visit the url that's shown in terminal after it runs and paste the authorization code

### Update config file
- firstly rename the file to config.json
- update all the values

- "spotify_access_token": "", [Follow this](https://developer.spotify.com/documentation/web-api)
- "spotify_playlist_id": "", Copy playlist url there the end part is id only
- "youtube_api_key": "", [Follow here](https://console.cloud.google.com/apis)
- "youtube_playlist_id": "", Copy playlist url there the end part is id only
- "client_id": "", To get YouTube client id use OAuth Client Id from [here](https://console.cloud.google.com/apis/credentials) and use web
- "client_secret": "" Frome above step

Make sure test user is created in OAuth consent screen, user is owner of the YT Playlist

---------------------------

I simply wanted to have my own playlist on YouTube, and also wanted to experiment with ChatGPT for coding, which led me to create this tool quickly. I must say that using GPT-4 felt like coding on steroids!

---------------------------
import requests
from urllib.parse import urlencode
import json

with open('config.json') as f:
    config = json.load(f)

SPOTIFY_API_ENDPOINT = "https://api.spotify.com/v1"
YOUTUBE_API_ENDPOINT = "https://www.googleapis.com/youtube/v3"


def get_spotify_playlist_tracks(playlist_id: str, access_token: str) -> list:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    playlist_tracks_endpoint = f"{SPOTIFY_API_ENDPOINT}/playlists/{playlist_id}/tracks"

    response = requests.get(playlist_tracks_endpoint, headers=headers)

    if response.status_code == 200:
        playlist_tracks = response.json()["items"]
        return playlist_tracks
    else:
        print(f"Failed to get playlist tracks: {response.text}")
        return []


def search_youtube_track(query: str, api_key: str) -> dict:
    params = {
        "part": "id",
        "q": query,
        "type": "video",
        "key": api_key
    }

    response = requests.get(YOUTUBE_API_ENDPOINT + "/search", params=params)

    if response.status_code == 200:
        search_results = response.json()["items"]
        if search_results:
            first_result = search_results[0]
            video_id = first_result["id"]["videoId"]
            return {
                "title": query,
                "video_id": video_id
            }
        else:
            return {}
    else:
        print(f"Failed to search YouTube for '{query}': {response.text}")
        return {}

def get_authorization_code(client_id, redirect_uri):
    url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/youtube.force-ssl",
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = url + "?" + urlencode(params)
    print(f"Please go to this URL and authorize the application: {auth_url}")
    return input("Enter the authorization code: ")

def get_youtube_access_token(client_id, client_secret, redirect_uri):
    url = "https://oauth2.googleapis.com/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    authorization_code = get_authorization_code(client_id, redirect_uri)
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": authorization_code,
        "grant_type": "authorization_code"
    }
    response = requests.post(url, headers=headers, data=data)
    response_json = response.json()
    access_token = response_json.get("access_token", None)
    return access_token

def add_youtube_video_to_playlist(video_id: str, playlist_id: str, access_token: str) -> bool:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }

    response = requests.post(YOUTUBE_API_ENDPOINT + "/playlistItems?part=snippet", headers=headers, json=body)

    if response.status_code == 200:
        print(f"Added video '{video_id}' to YouTube playlist '{playlist_id}'")
        return True
    else:
        print(f"Failed to add video '{video_id}' to YouTube playlist '{playlist_id}': {response.text}")
        return False


def main():
    # Spotify credentials
    spotify_access_token = config['spotify_access_token'] #"YOUR_SPOTIFY_ACCESS_TOKEN"
    spotify_playlist_id = config['spotify_playlist_id'] #"YOUR_SPOTIFY_PLAYLIST_ID"

    # YouTube credentials
    youtube_api_key = config['youtube_api_key'] #"YOUR_YOUTUBE_API_KEY"
    youtube_playlist_id = config['youtube_playlist_id'] #"YOUR_YOUTUBE_PLAYLIST_ID"

    # Get tracks from Spotify playlist
    playlist_tracks = get_spotify_playlist_tracks(spotify_playlist_id, spotify_access_token)

    youtube_access_token = get_youtube_access_token(config['client_id'], config['client_secret'], 'http://localhost:8000/')
    
    # Search for each track on YouTube and add it to the YouTube playlist
    for playlist_track in playlist_tracks:
        track_name = playlist_track["track"]["name"]
        track_artist = playlist_track["track"]["artists"][0]["name"]
        query = f"{track_name} {track_artist} official audio"
        search_result = search_youtube_track(query, youtube_api_key)
        if search_result:
            video_id = search_result["video_id"]
            add_youtube_video_to_playlist(video_id, youtube_playlist_id, youtube_access_token)


if __name__ == "__main__":
    main()

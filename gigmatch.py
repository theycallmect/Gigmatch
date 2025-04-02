import sys
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-read-private",
    cache_path=".cache",
    open_browser=True
))

def search_festival(query):
    response = requests.get(f"https://clashfinder.com/list/?qs={query}", 
                           headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    if link := soup.find("a", class_="cfTitle"):
        return link.text.strip(), link['href']
    return None

def get_festival_artists(url):
    slug = url.rstrip("/").split("/")[-1]
    response = requests.get(f"https://clashfinder.com/data/event/{slug}.json", 
                           headers={"User-Agent": "Mozilla/5.0", "Referer": "https://clashfinder.com/"})
    data = response.json()

    return [event["name"] for loc in data.get("locations", []) 
            for event in loc.get("events", [])]

def get_spotify_artists():
    artists_by_playlist = {}
    for playlist in tqdm(sp.current_user_playlists()['items'], desc="Loading Spotify playlists"):
        tracks = []
        for item in sp.playlist_tracks(playlist['id'])['items']:
            if track := item.get('track'):
                if artists := track.get('artists'):
                    tracks.append({
                        "artist": artists[0]['name'],
                        "song": track.get('name')
                    })
        if tracks:
            artists_by_playlist[playlist['name']] = tracks
    return artists_by_playlist

def export_to_csv(data, filename):
    rows = sorted([
        [track["artist"], track["song"], playlist]
        for playlist, tracks in data.items()
        for track in tracks
    ], key=lambda x: x[0])
    

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Artist", "Song", "Playlist"])
        writer.writerows(rows)
    print(f"Exported Spotify data to {filename}")

if __name__ == "__main__":
    query = input("Enter the festival you want to search for: ").strip()
    if not (result := search_festival(query)):
        print("No festival found.")
        sys.exit(0)
        
    fest_name, fest_url = result
    print(f"Found festival: {fest_name} ({fest_url})")
    if input("Does this look correct? (Y/N): ").strip().lower() not in ("y", "yes"):
        print("Exiting.")
        sys.exit(0)


    print("Loading festival data... please wait.")
    festival_artists = get_festival_artists(fest_url)
    print("Festival data loaded.")

    print("Loading Spotify data... please wait.")
    spotify_data = get_spotify_artists()
    print("Spotify data loaded.")


    user_artists = {track["artist"] for tracks in spotify_data.values() for track in tracks}
    matching_artists = user_artists.intersection(festival_artists)

    if not matching_artists:
        print("\nYou have no artists that match for this festival :(")
        sys.exit(0)

    print("\nMatching results:")
    print(f"Unique artists in your Spotify: {len(user_artists)}")
    print(f"Festival artists: {len(festival_artists)}")
    print(f"Matching artists: {len(matching_artists)}")
    print("Matching artist names:")
    print(list(matching_artists))


    if input("Export Spotify data to CSV? (Y/N): ").strip().lower() in ("y", "yes"):
        export_to_csv(spotify_data, "spotify_data.csv")
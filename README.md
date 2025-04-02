# Gigmatch

Find which artists from your Spotify playlists are playing at festivals.

## Setup

### 1. Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Spotify API

1. Create an app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Add a redirect URI (e.g., `http://127.0.0.1:8080/callback`).
3. Create a `.env` file in the project root:

```env
SPOTIPY_CLIENT_ID="your_client_id"
SPOTIPY_CLIENT_SECRET="your_client_secret"
SPOTIPY_REDIRECT_URI="http://127.0.0.1:8080/callback"
```

## Usage

Run the script:

```bash
python gigmatch.py
```

### Workflow

1. **Search for a festival**: Enter the name when prompted.
   ```
   Enter the festival you want to search for: Glastonbury
   ```

2. **Confirm your selection**: Type 'Y' if correct.
   ```
   Found festival: Glastonbury 2023 (https://clashfinder.com/s/glastonbury2023/)
   Does this look correct? (Y/N):
   ```

3. **View your matches**: The program will show artists that appear in both your playlists and the festival lineup.
   ```
   Matching results:
   Unique artists in your Spotify: 1523
   Festival artists: 432
   Matching artists: 28
   ```

4. **Export data** (optional): Export your Spotify playlist data to CSV for further analysis.

## How It Works

Gigmatch uses the Spotify API to analyze your playlists and Clashfinder.com to get festival lineups. It then finds the intersection between these two sets to show you which artists you know are performing.
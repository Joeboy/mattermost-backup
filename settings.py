from pathlib import Path

# You'll want to edit these three:
MATTERMOST_DOMAIN = "mattermost.some.domain"
LOGIN_ID = "your@login.id"
PASSWORD = "abetterpasswordthanthis"

THIS_FOLDER = Path(__file__).parent
CACHE_FOLDER = THIS_FOLDER / "cache"
USERS_FILE = CACHE_FOLDER / "users.json"
CHANNELS_FOLDER = CACHE_FOLDER / "channels"
PARSED_CHANNELS_FOLDER = THIS_FOLDER / "parsed_channels"
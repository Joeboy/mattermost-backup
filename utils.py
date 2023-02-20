import json
from collections import defaultdict
from pathlib import Path
from mattermostdriver import Driver
from settings import USERS_FILE, MATTERMOST_DOMAIN, LOGIN_ID, PASSWORD, CHANNELS_FOLDER


def get_driver() -> Driver:
    if not hasattr(get_driver, "_driver"):
        get_driver._driver = Driver(
            {
                "url": MATTERMOST_DOMAIN,
                "login_id": LOGIN_ID,
                "password": PASSWORD,
                "port": 443,
                #    'token': 'YourPersonalAccessToken',
            }
        )
        get_driver._driver.login()
    return get_driver._driver


def get_user_data() -> list[dict]:
    if USERS_FILE.exists():
        with open(USERS_FILE) as f:
            user_data = json.load(f)
    else:
        driver = get_driver()
        user_data = driver.users.get_users()
        with open(USERS_FILE, "w") as f:
            json.dump(user_data, f)
    return user_data


def get_users_by_id() -> dict[str, dict]:
    return {u["id"]: u for u in get_user_data()}


def load_cached_channels_data() -> tuple[dict[str, dict], dict[str, int]]:
    channels_data = defaultdict(list)
    latest_completed_pages = {}
    for folder in Path(CHANNELS_FOLDER).iterdir():
        if not folder.is_dir():
            continue
        channel_name = folder.stem
        # Folder should contain a file for each page: 0.json, 1.json etc...
        files = sorted(folder.glob("*.json"))
        if files:
            latest_file = files[
                -1
            ]  # Most recent file contains *all* data, not just last page
            latest_completed_pages[channel_name] = int(latest_file.stem)
            with latest_file.open() as f:
                channels_data[channel_name] = json.load(f)
    return dict(channels_data), latest_completed_pages


def underline(s) -> None:
    print(s)
    print("=" * len(s))

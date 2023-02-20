import itertools
import json
from pathlib import Path

from utils import get_driver, get_users_by_id, underline, load_cached_channels_data
from settings import LOGIN_ID, CHANNELS_FOLDER


def add_post_to_existing_channel_data(channel_data, post) -> None:
    if post["root_id"]:
        # It belongs in the root_id's thread
        try:
            channel_data[post["root_id"]].append(post)
        except KeyError:
            channel_data[post["root_id"]] = [post]
    else:
        # Standalone message, give it its own "thread"
        channel_data[post["id"]] = [post]


def fetch_channels_data() -> None:
    driver = get_driver()
    user = driver.users.get_user_by_email(LOGIN_ID)
    user_id = user["id"]
    users_by_id = get_users_by_id()

    channels_data, latest_completed_pages = load_cached_channels_data()
    for team in driver.teams.get_user_teams(user_id):
        print("TEAM:", team["display_name"])
        channels = driver.channels.get_channels_for_user(user_id, team["id"])
        for channel in channels:
            channel_name = channel["display_name"]
            # NB channel_name will be an empty string for one-to-one channels
            underline("Grabbing '{}'".format(channel_name or "user conversation"))
            channel_data = channels_data.get(channel_name, {})
            latest_completed_page = latest_completed_pages.get(channel_name, 0)
            for page in range(latest_completed_page, int(1e22)):
                print(f"Page {page}")
                channel_options = {
                    "per_page": 200,
                    "page": page,
                }

                posts = driver.posts.get_posts_for_channel(
                    channel["id"], channel_options
                )

                print(f"Got {len(posts['posts'])} posts")
                for post_id, post in posts["posts"].items():
                    add_post_to_existing_channel_data(channel_data, post)

                if not len(posts["posts"]) or (page and not page % 50):
                    all_posts = list(itertools.chain(*channel_data.values()))
                    if len(all_posts):
                        if channel_name:
                            channel_folder = Path(CHANNELS_FOLDER / channel_name)
                        else:
                            channel_user_ids = set([p["user_id"] for p in all_posts])
                            channel_user_ids.remove(user_id)
                            # I think this will error if you started a one-to-one
                            # chat and never got a reply:
                            (channel_user_id,) = channel_user_ids
                            channel_username = users_by_id[channel_user_id]["username"]
                            channel_folder = Path(CHANNELS_FOLDER / channel_username)
                        if not channel_folder.exists():
                            channel_folder.mkdir()
                        if len(posts["posts"]):
                            filename = channel_folder / f"{page}.json"
                        else:
                            filename = channel_folder / f"{page - 1}.json"
                        print(f"Writing data to {filename}")
                        with open(filename, "w") as f:
                            json.dump(channel_data, f, indent=3)
                if not len(posts["posts"]):
                    break


if __name__ == "__main__":
    fetch_channels_data()

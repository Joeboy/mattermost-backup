import sys

from datetime import datetime
from utils import get_users_by_id, load_cached_channels_data, underline

from settings import PARSED_CHANNELS_FOLDER

def write_post(post, fp):
    dt = datetime.utcfromtimestamp(post["create_at"] / 1000)
    user_data = users_by_id[post["user_id"]]
    fp.write(f"{dt} {user_data['username']}: {post['message']}\n")


def earliest_post_time(thread_tuple: tuple[str, list]) -> int:
    _, posts = thread_tuple
    return min([p["create_at"] for p in posts])


channels_data, _ = load_cached_channels_data()
users_by_id = get_users_by_id()

for channel_name, channel_data in channels_data.items():
    with open(PARSED_CHANNELS_FOLDER / f"{channel_name}.txt", "w") as f:
        underline(channel_name)
        sorted_channel_data = sorted(channel_data.items(), key=earliest_post_time)

        for post_id, posts in sorted_channel_data:
            posts = sorted(posts, key=lambda _post: _post["create_at"])
            if len(posts) == 1:
                write_post(posts[0], sys.stdout)
                write_post(posts[0], f)
            else:
                print("=== Thread starts ===")
                for post in sorted(posts, key=lambda _post: _post["create_at"]):
                    write_post(post, sys.stdout)
                    write_post(post, f)
                print("=== Thread ends ===")

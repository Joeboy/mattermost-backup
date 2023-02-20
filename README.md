# Mattermost-Backup

Apparently the Mattermost server we use at work is being decommissioned, so I wrote a script to download all messages via the API. I stopped at the point I was able to download all my messages, it might not be the most robust script ever. YMMV but why not give it a whirl?

To set it up:

    git clone git@github.com:Joeboy/mattermost-backup.git
    cd mattermost-backup
    python -m venv venv # I think you need at least python 3.10 or thereabouts
    pip install -r requirements.txt

Then edit `settings.py` with your Mattermost domain and credentials.

To download messages into the cache folder as json data:

    python download_data.py

If that worked right, you can now do:

    python parse_downloaded_data.py

which will display the downloaded messages to your screen, and also write each channel into a relatively readable text file in the `parsed_channels` folder.
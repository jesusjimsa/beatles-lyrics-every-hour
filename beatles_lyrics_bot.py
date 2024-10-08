"""Beatles lyrics bot module"""
import random
import logging
from datetime import datetime, timezone
import tweepy
import requests
from mastodon import Mastodon
from masto_auth import ACCESS_TOKEN_MASTODON
from bluesky_auth import BLUESKY_HANDLE, BLUESKY_APP_PASSWORD
from auth import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET_KEY

logging.basicConfig(filename='beatles.log', level=logging.DEBUG)

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

mastodon = Mastodon(access_token=ACCESS_TOKEN_MASTODON, api_base_url="https://mastodon.world")


def random_line(afile):
    """
    Get a random line from a given file.

    Parameters
    ----------
    afile : int
        File handle to get the random line from.
    Returns
    -------
    line : str
        Random line from the file.
    """
    line = next(afile)

    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue

        line = aline

    return line


def bluesky_post(text):
    """
    Send a post to BlueSky.

    Parameters
    ----------
    text : str
        Text to send to BlueSky
    """
    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
        timeout=10,
    )
    resp.raise_for_status()
    session = resp.json()

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    hashtag = "#TheBeatles"
    hashtag_start = text.find(hashtag)
    hashtag_end = hashtag_start + len(hashtag)

    post = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": now,
        "facets": [
            {
                "index": {
                    "byteStart": hashtag_start,
                    "byteEnd": hashtag_end
                },
                "features": [
                    {
                        "$type": "app.bsky.richtext.facet#tag",
                        "tag": "TheBeatles"
                    }
                ]
            }
        ]
    }
    post["langs"] = ["en-US"]

    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": "Bearer " + session["accessJwt"]},
        json={
            "repo": session["did"],
            "collection": "app.bsky.feed.post",
            "record": post,
        },
        timeout=10,
    )
    resp.raise_for_status()


try:
    with open('data/lyrics.txt', 'r', encoding="UTF-8") as f:
        rline = random_line(f).split('\n')[0]
        rline = f'{rline} #TheBeatles'

        # print(rline)
        try:
            mastodon.toot(rline)
            bluesky_post(rline)
            client.create_tweet(text=rline)
        except tweepy.errors.TweepyException as tw:
            logging.error("Couldn't send the tweet: %s", tw)
except OSError:
    logging.error("Couldn't open lyrics file")

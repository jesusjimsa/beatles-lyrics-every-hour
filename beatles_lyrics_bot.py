"""Beatles lyrics bot module"""
import random
import logging
import tweepy
from mastodon import Mastodon
from masto_auth import ACCESS_TOKEN_MASTODON
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


try:
    with open('data/lyrics.txt', 'r', encoding="UTF-8") as f:
        rline = random_line(f).split('\n')[0]
        rline = f'{rline} #TheBeatles'

        # print(rline)
        try:
            mastodon.toot(rline)
            client.create_tweet(text=rline)
        except tweepy.errors.TweepyException as tw:
            logging.error("Couldn't send the tweet: %s", tw)
except OSError:
    logging.error("Couldn't open lyrics file")

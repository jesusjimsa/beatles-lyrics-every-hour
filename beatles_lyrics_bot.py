"""Beatles lyrics bot module"""
import random
import logging
from twython import Twython
from twython import TwythonError
from auth import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET_KEY

logging.basicConfig(filename='beatles.log', level=logging.DEBUG)

twitter = Twython(
    API_KEY,
    API_SECRET_KEY,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)


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

        # print(rline)
        try:
            twitter.update_status(status=rline)
        except TwythonError as e:
            logging.error("Couldn't send the tweet: %s", e)
except OSError:
    logging.error("Couldn't open lyrics file")

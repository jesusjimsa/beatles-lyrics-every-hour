"""Beatles lyrics bot module"""
import random


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


with open('data/lyrics.txt', 'r', encoding="UTF-8") as f:
    rline = random_line(f).split('\n')[0]

    print(rline)

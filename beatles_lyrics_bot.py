import random


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line


with open('data/lyrics.txt', 'r') as f:
    rline = random_line(f).split('\n')[0]

    print(rline)

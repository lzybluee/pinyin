import os
import random
import re
import time

import pyttsx3
from pygame import mixer

NUM = 20
LOOP = 3

tone_table = {
    'a': 'āáǎà',
    'e': 'ēéěè',
    'i': 'īíǐì',
    'o': 'ōóǒò',
    'u': 'ūúǔù',
    'ü': 'ǖǘǚǜ'
}


def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 100)
    engine.say(text)
    engine.runAndWait()
    del engine


def play(file):
    mixer.music.load(file)
    mixer.music.set_volume(0.5)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)


def convert(name):
    def repl(match, tone):
        text = list(match.group(0))
        if len(text) > 1 and (text[0] in ['i', 'u', 'ü']):
            tone_index = 1
        else:
            tone_index = 0
        text[tone_index] = tone_table[text[tone_index]][tone - 1]
        return ''.join(text)

    return re.sub(r'[aeiouü]+', lambda m: repl(m, int(name[-1])), name[:-1])


def main():
    mixer.init()

    files = random.sample(os.listdir('audio'), NUM)

    for i, file in enumerate(files):
        print(f'{i + 1}: {convert(file[:file.index('.')])}')

    for n in range(LOOP):
        for i in range(NUM):
            say(str(i + 1))
            play(os.path.join('audio', files[i]))
            time.sleep(1)
        time.sleep(1)


if __name__ == '__main__':
    main()

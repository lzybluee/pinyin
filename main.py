import os
import random
import re
import time
from datetime import datetime

import pyttsx3
from pygame import mixer

INTERVAL = 4
NUM = 20
LOOP = 2
FOLDER = 'audio'
FILTER = [  # 'a', 'e', 'i', 'o', 'u', 'ü',
    'ba', 'bo', 'bi', 'bu', 'pa', 'po', 'pi', 'pu', 'ma', 'mo', 'mi', 'mu', 'fa', 'fo', 'fu',
    'da', 'de', 'di', 'du', 'ta', 'te', 'ti', 'tu', 'na', 'ne', 'ni', 'nu', 'nü', 'la', 'le', 'li', 'lu', 'lü',
    'ga', 'ge', 'gu', 'ka', 'ke', 'ku', 'ha', 'he', 'hu', 'gua', 'kua', 'hua', 'guo', 'kuo', 'huo',
    'ji', 'qi', 'xi', 'jia', 'qia', 'xia', 'ju', 'qu', 'xu',
    'za', 'ze', 'zu', 'zuo', 'ca', 'ce', 'cu', 'cuo', 'sa', 'se', 'su', 'suo', 'zi', 'ci', 'si'
]

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


def filter_file(files):
    if not FILTER:
        return files

    filtered = []
    for file in files:
        if result := re.match(r'(\w+)\d.*', file):
            if result[1] in FILTER:
                filtered.append(file)
    return filtered


def main():
    if not os.path.exists('log'):
        os.mkdir('log')

    files = random.sample(filter_file(os.listdir(FOLDER)), NUM)

    mixer.init()
    play('ready.mp3')
    time.sleep(2)

    with open(os.path.join('log', datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.txt'), 'w') as log:
        for i, file in enumerate(files):
            text = f'{i + 1}: {convert(file[:file.index('.')])}'
            print(text)
            log.write(text + '\n')

    for n in range(LOOP):
        for i in range(NUM):
            say(str(i + 1))
            play(os.path.join(FOLDER, files[i]))
            time.sleep(INTERVAL)
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()

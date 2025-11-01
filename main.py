import os
import random
import re
import time
from datetime import datetime

import pyttsx3
from pygame import mixer

INTERVAL = 6
NUM = 20
LOOP = 2
FOLDER = 'audio'
FILTER = [  # 'a', 'e', 'i', 'o', 'u', 'ü',
    # 'ba', 'bo', 'bi', 'bu',
    # 'pa', 'po', 'pi', 'pu',
    # 'ma', 'mo', 'mi', 'mu',
    # 'fa', 'fo', 'fu',
    # 'da', 'de', 'di', 'du',
    # 'ta', 'te', 'ti', 'tu',
    # 'na', 'ne', 'ni', 'nu', 'nü',
    # 'la', 'le', 'li', 'lu', 'lü',
    # 'ga', 'ge', 'gu', 'gua', 'guo',
    # 'ka', 'ke', 'ku', 'kua', 'kuo',
    # 'ha', 'he', 'hu', 'hua', 'huo',
    # 'ji', 'jia', 'ju',
    # 'qi', 'qia', 'qu',
    # 'xi', 'xia', 'xu',
    # 'zi', 'za', 'ze', 'zu', 'zuo',
    # 'ci', 'ca', 'ce', 'cu', 'cuo',
    # 'si', 'sa', 'se', 'su', 'suo',
    # 'zhi', 'zha', 'zhe', 'zhu', 'zhua', 'zhuo',
    # 'chi', 'cha', 'che', 'chu', 'chuo',
    # 'shi', 'sha', 'she', 'shu', 'shua', 'shuo',
    # 'ri', 're', 'ru', 'ruo',
    # 'yi', 'ya', 'yu',
    # 'wu', 'wa', 'wo',
    # 'gai', 'guai', 'tai', 'kai', 'cai', 'huai', 'kuai',
    'lei', 'bei', 'pei', 'fei', 'gei', 'wei', 'hei',
    'tui', 'hui', 'dui', 'chui', 'zui', 'sui', 'rui',
    # 'niao', 'shao', 'yao', 'rao', 'tiao', 'zao',
    # 'tou', 'lou', 'you', 'zou', 'shou', 'kou', 'rou',
    'qiu', 'diu', 'liu', 'niu', 'xiu', 'jiu'
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

    with open(os.path.join('log', datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.txt'), 'w') as log:
        for i, file in enumerate(files):
            text = f'{i + 1}: {convert(file[:file.index('.')])}'
            print(text)
            log.write(text + '\n')

    mixer.init()
    play('ready.mp3')
    time.sleep(2)

    for n in range(LOOP):
        for i in range(NUM):
            say(str(i + 1))
            play(os.path.join(FOLDER, files[i]))
            time.sleep(INTERVAL)
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()

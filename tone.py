import os
import random

FOLDER = 'audio'


def main():
    double_vowels = {}

    for file in os.listdir(FOLDER):
        if '1' in file:
            name = file[:-5]
            vowels = [name.index(i) for i in ['a', 'e', 'i', 'o', 'u', 'ü'] if i in name]
            if len(vowels) > 1:
                key = name[min(vowels):]
                double_vowels[key] = double_vowels.get(key, []) + [name]

    for k, v in double_vowels.items():
        print(' '.join(random.choice(v)))


if __name__ == '__main__':
    main()

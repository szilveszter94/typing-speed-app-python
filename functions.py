import random
import csv
import json


# return formatted array from "words_to_write" csv file
def create_word_list():
    unformatted_word_list = []
    with open(file='words_to_write') as file:
        data = csv.reader(file)
        for i in data:
            unformatted_word_list.append(i)
    return unformatted_word_list[0]


# return a random sapmle array from formatted words list array
def create_random_word_list():
    word_list = create_word_list()
    random_word_list = []
    random_word_indexes = random.sample(range(0, len(word_list) - 1), 5)
    for i in random_word_indexes:
        random_word_list.append(word_list[i])
    return random_word_list

# read and return cpm the highscore data from highscore.json file
def cpm_highscore():
    with open('highscore.json') as json_file:
        jsfile = json.load(json_file)
        cpm_h_score = int(jsfile['CPM Highscore:'])
    return cpm_h_score

# read and return the wpm highscore data from highscore.json file
def wpm_highscore():
    with open('highscore.json') as json_file:
        jsfile = json.load(json_file)
        wpm_h_score = int(jsfile['WPM Highscore:'])
    return wpm_h_score

import json
import os
import re


test_data_path = r'./eigen_task/test_docs/'
stored_data_path = r'./json_data/'

'''
@dataclass
class Word:
    word: str
    count: int
    sentances: list
    documents: list
'''

def get_file_paths(directory):
    files = []

    for dirpath, _, file_names in os.walk(directory):
        for f in file_names:
            if '.txt' in f:
                files.append(os.path.abspath(os.path.join(dirpath, f)))

    return files

def create_json_file(file_name, file_data):
    with open(file=file_name, mode='w', encoding='utf-8') as f:
        json.dump(file_data, f)

def get_word_count(file_object):
    word_count = {}

    for word in f.read().split():
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
    return word_count

def find_sentance_containing_word(data, word):
    search = r"([^.]*?" + word + r"[^.]*\.)"
    sentances = re.findall(search, data)

    return sentances

def word_in_document(word, document):
    pass

for one_file in get_file_paths(test_data_path):
    file_name = stored_data_path + os.path.basename(one_file).split('.')[0] + '.json'

    with open(file=one_file, mode='r', encoding='utf-8') as f:
        # create_json_file(file_name, get_word_count(f))
        
        final_data = find_sentance_containing_word(f.read(), 'Let')
        print(final_data)

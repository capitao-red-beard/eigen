import json
import os
import pprint
import re


TEST_DATA_PATH = r'./eigen_task/test_docs/'
STORED_DATA_PATH = r'./json_data/'

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

def load_data():
    list_of_data = []

    for one_file in get_file_paths(TEST_DATA_PATH):
        with open(file=one_file, mode='r', encoding='utf-8') as f:
            list_of_data.append(
                {os.path.splitext(os.path.basename(one_file))[0]: f.read()}
            )
    
    return list_of_data

def create_json_file(file_name, file_data):
    with open(file=file_name, mode='w', encoding='utf-8') as f:
        json.dump(file_data, f)

def get_word_count(list_of_data_dicts):
    word_count = {}

    for data_dict in list_of_data_dicts:
        for k, v in data_dict.items():
            for word in v.split():
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1
    return word_count

def get_sentances_containing_word(data, word):
    search = r"([^.]*?" + word + r"[^.]*\.)"
    sentances = re.findall(search, data)

    return sentances

def word_in_document(word, documents):
    pass

data = load_data()

word_count = get_word_count(data)

word = {
    word: '',
    appears_in: '',
    count: 0,
    sentances: ''
    }

for d in data:
    for k, v in d.items():
        print(k, get_sentances_containing_word(v, 'American'))



'''
if __name__ == '__main__':
    paths = get_file_paths()
'''
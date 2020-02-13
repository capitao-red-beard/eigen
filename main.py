import json
import os
import pprint
import re
from dataclasses import dataclass

TEST_DATA_PATH = r"./eigen_task/test_docs/"
STORED_DATA_PATH = r"./json_data/"

pp = pprint.PrettyPrinter(indent=4)


@dataclass
class Word:
    word: str
    count: int
    documents: list
    sentances: list


def get_file_paths(directory):
    files = []

    for dirpath, _, file_names in os.walk(directory):
        for f in file_names:
            if ".txt" in f:
                files.append(os.path.abspath(os.path.join(dirpath, f)))

    return files


def load_data():
    data = []

    for one_file in get_file_paths(TEST_DATA_PATH):
        with open(file=one_file, mode="r", encoding="utf-8") as f:
            data.append({os.path.splitext(os.path.basename(one_file))[0]: f.read()})

    return data


def output_data_to_json_file(file_name, data):
    with open(file=file_name, mode="w", encoding="utf-8") as f:
        json.dump(data, f)


def get_word_count(data):
    word_count = {}

    for d in data:
        for k, v in d.items():
            for word in v.split():
                if word not in word_count:
                    word_count[word] = 0
                word_count[word] += 1

    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_word_count


def get_sentances_containing_word(word, data):
    sentances = re.findall(r"([^.]*? %s [^.]*\.)" % word, data)

    return sentances


def get_word_in_document(word, data):
    docs = []

    for d in data:
        for k, v in d.items():
            for w in v.split():
                if w == word and k not in docs:
                    docs.append(k)

    return docs


if __name__ == "__main__":

    final_data = []

    word_list = [
        "audacity",
        "homegrown",
        "lobbyists",
        "generation",
        "humility",
        "freedom",
        "party",
        "time",
        "progress",
        "corruption",
        "promise",
        "Iraq",
        "recommendation",
    ]

    loaded_data = load_data()
    word_count = get_word_count(loaded_data)

    for w in word_count:
        if w[0] in word_list:
            sentances = []
            word = w[0]
            count = w[1]

            documents = get_word_in_document(w[0], loaded_data)

            for d in loaded_data:
                for k, v in d.items():
                    s = get_sentances_containing_word(w[0], v)
                    if len(s) != 0:
                        sentances.append(s)

            final_data.append(Word(word, count, documents, sentances))

    for f in final_data:
        pp.pprint(f)

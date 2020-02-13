import os
import re
import string
from dataclasses import dataclass
from typing import Dict, List, Tuple

TEST_DATA_PATH = r"./eigen_task/test_docs/"


@dataclass
class Word:
    """
    This is a dataclass which encapsulates the data associated with a word from the test data.
    """

    word: str
    count: int
    documents: list
    sentences: list


def get_file_paths(directory: str) -> List[str]:
    """
    This function takes a directory path as parameter and finds all the files with `.txt` extension
    which are in that directory.
    """

    files: List = []

    for dirpath, _, file_names in os.walk(directory):
        for f in file_names:
            if ".txt" in f:
                files.append(os.path.abspath(os.path.join(dirpath, f)))

    return files


def load_data(path=TEST_DATA_PATH) -> List[Dict[str, str]]:
    """
    This function takes as default the location of the test files as parameter, it then collects the
    data inside of the files and adds them to a list of dictionary objects.
    """

    data: List = []

    for f in get_file_paths(path):
        with open(file=f, mode="r", encoding="utf-8") as fp:
            # The dict keys in this case are the names of the files and the values are the contents.
            data.append({os.path.splitext(os.path.basename(f))[0]: fp.read()})

    return data


def get_word_count(data: List[Dict[str, str]]) -> List[Tuple[str, int]]:
    """
    This function finds the number of times a word was used in a list of dicts containing data.

    The number of times a word was used is then returned in a sorted way.
    """

    word_count: Dict[str, int] = {}

    for d in data:
        for k, v in d.items():
            # Split based on words only, remove the punctuation from the text, lower-case.
            s = re.split(r"\W+", v.translate(str.maketrans("", "", string.punctuation)).lower())
            for word in s:
                if word not in word_count:
                    word_count[word] = 0
                word_count[word] += 1

    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_word_count


def get_sentences_containing_word(word: str, data: List[Dict[str, str]]) -> List[str]:
    """
    This function finds all of the sentences a word appears in across a given list of dicts of data.
    """

    sentences: List[List[str]] = []
    regex = fr"([^.]*?{word}[^.]*\.)"

    for d in data:
        for k, v in d.items():
            sentences.append(re.findall(regex, v.lower()))

    # Because we are looping through a list to create one we end up with a kind of 2D structure,
    # we can use list comprehension to "flatten" it out; i.e. [[str], [str]] -> [str, str].
    flat_list = [sub for sub_list in sentences for sub in sub_list]

    return flat_list


def get_document_names_containing_word(
    word: str, data: List[Dict[str, str]]
) -> List[str]:
    """
    This function is used to get the names of all the documents which contain a given word.
    """

    docs: List[str] = []
    seen = set(docs)

    for d in data:
        for k, v in d.items():
            # Split based on words only, remove the punctuation from the text, lower-case.
            s = re.split(r"\W+", v.translate(str.maketrans("", "", string.punctuation)).lower())
            for w in s:
                # We want to prevent that the name of the document will get added multiple times.
                if w == word and k not in seen:
                    # We use a set here because it is more efficient than checking the list,
                    # using `in` for a list runs in O(n) as opposed to O(1) for sets.
                    seen.add(k)
                    docs.append(k)

    return docs


if __name__ == "__main__":

    final_data: List[Word] = []

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
        "iraq",
        "recommendation",
    ]

    loaded_data = load_data()
    word_count = get_word_count(loaded_data)

    for w in word_count:
        if w[0] in word_list:
            word = w[0]
            count = w[1]

            documents = get_document_names_containing_word(w[0], loaded_data)
            sentences = get_sentences_containing_word(w[0], loaded_data)

            final_data.append(Word(word, count, documents, sentences))

    for i, f in enumerate(final_data):
        print(i, f)

import string
from stemming.porter2 import stem
from collections import Counter


def text_to_words(text):
    """
    Converts text to list of words, no digits, no punctuation, lover case
    :param text:
    :return:
    """
    for c in string.punctuation + " " + "\n":
        text = text.replace(c, ".")

    text = text.lower().strip().split(".")
    text = filter(None, text)

    no_digits = []
    for w in text:
        try:
            int(w)
        except ValueError:
            no_digits.append(w)
    text = no_digits
    return text


def words_analysis(words_list, threeLetters, onlyBase, known_words):
    """
    Analyzes words in list. Sorts them by input criteria. Counts frequency of new words in text
    :param words_list:
    :param threeLetters:
    :param onlyBase:
    :param known_words:
    :return:
    """
    known_in_text = []
    cnt = Counter()
    for word in words_list:
        word.strip()
        if not word or word == " ":
            continue
        elif len(word) == 1:
            continue
        elif threeLetters and len(word) <= 2:
            continue
        elif onlyBase:
            word = stem(word)
        elif word not in known_words:
            cnt[word] += 1
        if word in known_in_text:
            continue
        if word in known_words:
            known_in_text.append(word)
    return known_in_text, cnt



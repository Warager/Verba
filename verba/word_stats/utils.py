import string
from django.template.loader import render_to_string
from sendgrid import sendgrid
from stemming.porter2 import stem
from collections import Counter
from verba.settings import sg


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
        elif onlyBase == 'checked':
            word = stem(word)
        elif word not in known_words:
            cnt[word] += 1
        if word in known_in_text:
            continue
        if word in known_words:
            known_in_text.append(word)
    return known_in_text, cnt


def send_email(user, my_email):
    """
    Sends welcome message on user's email
    :param user:
    :param my_email:
    :return:
    """
    message = sendgrid.Mail()
    message.add_to(my_email)
    message.set_subject('Welcome!')
    message.set_html(render_to_string('word_stats/welcome_email.html', {'user': user}))
    message.set_from('fomin.dritmy@gmail.com')
    status, msg = sg.send(message)
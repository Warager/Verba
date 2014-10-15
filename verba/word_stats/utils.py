import string
from django.template.loader import render_to_string
from sendgrid import sendgrid, Mail
from stemming.porter2 import stem
from collections import Counter
from verba.settings import DEFAULT_EMAIL, SENDGRID_USERNAME, SENDGRID_PASSWORD


def text_to_words(text):
    """
    Converts text to list of words, no digits, no punctuation, lover case
    :param text:
    :return:
    """
    for c in string.punctuation + string.digits + " " + "\n":
        text = text.replace(c, ".")

    text = text.lower().strip().split(".")
    text = filter(None, text)
    return text


def words_analysis(words_list, three_letters, only_base, known_words):
    """
    Analyzes words in list. Sorts them by input criteria. Counts frequency
    of new words in text
    :param words_list:
    :param three_letters:
    :param only_base:
    :param known_words:
    :return:
    """
    known_in_text = []
    cnt = Counter()
    for word in words_list:
        word.strip()
        if not word or word == " ":
            continue
        if len(word) == 1:
            continue
        if word in known_in_text:
            continue
        if only_base:
            word = stem(word)
        if three_letters and len(word) <= 2:
            continue
        if word in known_words:
            known_in_text.append(word)
        else:
            cnt[word] += 1
    return known_in_text, cnt


def send_welcome_email(user, my_email):
    """
    Sends welcome message on user's email
    :param user:
    :param my_email:
    :return:
    """
    sg = sendgrid.SendGridClient(SENDGRID_USERNAME, SENDGRID_PASSWORD)
    message = Mail(to=my_email,
                   subject='Welcome',
                   html=render_to_string('accounts/welcome_email.html', {
                       'user': user}),
                   from_email=DEFAULT_EMAIL)
    status, msg = sg.send(message)

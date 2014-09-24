from collections import Counter
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.template.loader import render_to_string
from stemming.porter2 import stem
from verba.settings import sg
import string
import sendgrid

# Create your views here.
from verba.word_stats.models import UserDictionary


def input_form(request):
    data = {
        "current_page": 'home'
    }
    return render(request, 'word_stats/input_form.html', data)


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


def process(request):
    """
    Main computation of words entered by user
    :param request:
    :return:
    """
    #All computations will be produces only if user is authenticated
    if request.user.is_authenticated():
        text = request.POST.get('text', "")
        threeLetters = request.POST.get('threeLetters') == 'checked'
        onlyBase = request.POST.get('onlyBase') == 'checked'

        if request.user.is_authenticated:
            known_words = UserDictionary.objects.values_list('word', flat=True).filter(user=request.user)
        else:
            known_words = []

        words_list = text_to_words(text)
        _, cnt = words_analysis(words_list, threeLetters, onlyBase, known_words)
        known_in_text, _ = words_analysis(words_list, threeLetters, onlyBase, known_words)

        data = {
            "words": sorted(cnt.items()),
            "known_words": sorted(known_words),
            "known_in_text": sorted(known_in_text)
        }
        return render(request, 'word_stats/analysis.html', data)
    #If user is not authenticated, access on the /process url will be ignored and it will be redirected on the main page
    else:
        return redirect("/")


#This is site register function
def signup(request):
    my_email = request.POST.get('login', "")
    my_password = request.POST.get('password', "")
    my_pass_conf = request.POST.get('confirm', "")

    #Checking if user with this name already exists
    if User.objects.filter(username=my_email).count():
        return HttpResponse('Error')

    #Checking if email is not empty
    if my_email == "":
        return HttpResponse('EmptyUser')

    if my_password == "":
        return HttpResponse('EmptyPassword')

    #Checking of password confirmation
    if my_password != my_pass_conf:
        return HttpResponse('Wrong')

    #Creating new user
    user = User.objects.create_user(username=my_email, email=my_email)
    user.set_password(my_password)
    user.save()
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    #Sending greetings email
    message = sendgrid.Mail()
    message.add_to(my_email)
    message.set_subject('Welcome!')
    message.set_html(render_to_string('word_stats/welcome_email.html'))
    message.set_from('fomin.dritmy@gmail.com')
    status, msg = sg.send(message)
    return HttpResponse('OK')


#This is site login function
def login(request):
    my_email = request.POST.get('login', "")
    my_password = request.POST.get('password', "")

    #Checking if user is exist
    try:
        user = User.objects.get(email__iexact=my_email, is_active=True)
    except User.DoesNotExist:
        return HttpResponse('Error')
    #Checking of user password
    if not user.check_password(my_password):
        return HttpResponse('Error')
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    return HttpResponse('OK')


#This function used to logout and redirect on the main page
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


#This function adds word to user's dictionary by click on the button if this word does not exist there
def add_word(request):
    word = request.POST.get('word', "")
    user_dictionary, _ = UserDictionary.objects.get_or_create(user=request.user, word=word)
    return HttpResponse('OK')


#This function removes selected word from the dictionary
def rem_word(request):
    word_to_rem = request.POST['wordToRem']
    try:
        UserDictionary.objects.filter(user=request.user, word=word_to_rem).delete()
    except UserDictionary.DoesNotExist:
        return HttpResponse('DoesNotExist')
    return HttpResponse('OK')


#This function makes main computation in user's personal dictionary
def my_dictionary(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            new_words = request.POST.get('words', "")

            new_words = text_to_words(new_words)

            for word in new_words:
                word.strip()
                if not word or word == " ":
                    continue
                elif len(word) == 1:
                    continue
                user_dictionary, _ = UserDictionary.objects.get_or_create(user=request.user, word=word)
            return redirect("/my_dictionary")

        known_words = set()
        for user_dictionary in UserDictionary.objects.filter(user=request.user):
            known_words.add(user_dictionary.word)

        data = {
            "known_words": sorted(known_words),
            "current_page": "my_dictionary"
        }
        return render(request, "word_stats/my_dictionary.html", data)
    #If user is not authenticated, access on the /my_dictionary url will be ignored and redirected on the main page
    else:
        return redirect("/")
from collections import Counter
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from stemming.porter2 import stem
import string

# Create your views here.
from verba.word_stats.models import UserDictionary


def input_form(request):
    return render(request, 'word_stats/input_form.html')


def process(request):
    """
    :param request:
    :return:
    """
    text = request.POST['text']
    threeDigits = request.POST.get('threeDigits') == 'checked'
    onlyRoot = request.POST.get('onlyRoot') == 'checked'

    # if onlyRoot == 'checked':
    #     pass

    for c in string.punctuation + " " + "\n":
        text = text.replace(c, ".")

    text = text.lower().strip().split(".")
    text = filter(None, text)

    no_nums = []
    for w in text:
        try:
            type(int(w)) == int
        except ValueError:
            no_nums.append(w)
    text = no_nums

    known_words = set()
    for user_dictionary in UserDictionary.objects.filter(user=request.user):
        known_words.add(user_dictionary.word)

    known_in_text = []
    cnt = Counter()
    for word in text:
        word.strip()
        # for s in string.punctuation+" ":
        #     word = word.replace(s, " ")
        if not word or word == " ":
            continue
        elif len(word) == 1:
            continue
        elif threeDigits and len(word) <= 2:
            continue
        elif onlyRoot:
            word = stem(word)
        try:
            UserDictionary.objects.get(word=word)
            known_in_text.append(word)
        except UserDictionary.DoesNotExist:
            cnt[word] += 1
        # cnt[word] += 1
    a = cnt.items()
    a.sort(key=lambda x: x[1], reverse=True)
    data = {
        "words": sorted(a),
        "known_words": sorted(known_words),
        "known_in_text": sorted(known_in_text)
    }
    return render(request, 'word_stats/analysis.html', data)


def signup(request):
    my_email = request.POST['login']
    my_password = request.POST['password']
    my_pass_conf = request.POST['confirm']

    try:
        User.objects.get(email=my_email)
    except User.DoesNotExist:
        user = User.objects.create_user(username=my_email, email=my_email)
        user.set_password(my_password)
        user.save()
        user.backend = "django.contrib.auth.backends.ModelBackend"
        auth_login(request, user)
        return HttpResponse('OK')
    if my_password != my_pass_conf:
        return HttpResponse('Wrong')
    return HttpResponse('Error')


def accounts(request):
    my_email = request.POST['login']
    my_password = request.POST['password']

    try:
        user = User.objects.get(email__iexact=my_email, is_active=True)
    except User.DoesNotExist:
        return HttpResponse('Error')
    if not user.check_password(my_password):
        return HttpResponse('Error')
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    return HttpResponse('OK')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('http://127.0.0.1:8000/')


def add_word(request):
    word = request.POST.get('word', False)
    try:
        UserDictionary.objects.get(word=word)
        # UserDictionary.order_by('word')
    except UserDictionary.DoesNotExist:
        user_dictionary = UserDictionary(user=request.user, word=word)
        user_dictionary.save()
        # UserDictionary.objects.order_by('word')
        # ordered_dict.save()
        # ordered_dict = UserDictionary.order_by('word')
        return HttpResponse('OK')
    return HttpResponse('Exist')


def rem_word(request):
    word_to_rem = request.POST['wordToRem']
    # UserDictionary.objects.filter(word=word_to_rem).delete()
    try:
        UserDictionary.objects.filter(word=word_to_rem).delete()
        # word_delete.save()
    except UserDictionary.DoesNotExist:
        return HttpResponse('DoesNotExist')
    return HttpResponse('OK')


def my_dictionary(request):

    known_words = set()
    for user_dictionary in UserDictionary.objects.filter(user=request.user):
        known_words.add(user_dictionary.word)

    data = {
        "known_words": sorted(known_words)
    }
    return render(request, "word_stats/my_dictionary.html", data)


def my_dict_new_words(request):

    n_words = request.POST.get('words', False)

    for c in string.punctuation + " " + "\n":
        n_words = n_words.replace(c, ".")

    n_words = n_words.lower().strip().split(".")
    n_words = filter(None, n_words)

    no_nums = []
    for w in n_words:
        try:
            type(int(w)) == int
        except ValueError:
            no_nums.append(w)
    n_words = no_nums

    for word in n_words:
        word.strip()
        if not word or word == " ":
            continue
        elif len(word) == 1:
            continue
        try:
            UserDictionary.objects.get(word=word)
        except UserDictionary.DoesNotExist:
            user_dictionary = UserDictionary(user=request.user, word=word)
            user_dictionary.save()

    return my_dictionary(request)


#   The same method
#    user_dictionary = UserDictionary()
#    user_dictionary.user = request.user
#    user_dictionary.save()

#     user_dictionary = UserDictionary(user = request.user)
#     user_dictionary.save()



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
from hello.word_stats.models import UserDictionary


def input_form(request):
    return render(request, 'word_stats/input_form.html')


def process(request):
    text = request.POST['text']

    threeDigits = request.POST.get('threeDigits') == 'checked'
    onlyRoot = request.POST.get('onlyRoot') == 'checked'

    if onlyRoot == 'checked':
        pass

    for c in string.punctuation:
        text = text.replace(c, " ")

    text = text.lower().split(' ')

    cnt = Counter()

    for word in text:
        if not word:
            continue
        elif threeDigits and len(word) <= 2:
            continue
        elif onlyRoot:
            word = stem(word)
        cnt[word] += 1

    a = cnt.items()
    a.sort(key=lambda x: x[1], reverse=True)
    data = {
        "words": a
    }

    return render(request, 'word_stats/analysis.html', data)


def signup(request):
    my_email = request.POST['login']
    my_password = request.POST['password']
    my_pass_conf = request.POST['confirm']
    try:
        user = User.objects.get(email=my_email)
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
    word = request.POST['word']
    UserDictionary(user=request.user, word=word)
    # user_dict = UserDictionary.objects.create(user=request.user, word=word)
    # user_dict.save()

#   The same method
#    user_dictionary = UserDictionary()
#    user_dictionary.user = request.user
#    user_dictionary.save()

    return HttpResponse('OK')

from collections import Counter
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from stemming.porter2 import stem
import string
import sendgrid

# Create your views here.
from verba.word_stats.models import UserDictionary


def input_form(request):
    data = {
        "current_page": 'home'
    }
    return render(request, 'word_stats/input_form.html', data)


#This function makes main computation of words entered by user
def process(request):
    """
    :param request:
    :return:
    """
    #All computations will be produces only if user is authenticated
    if request.user.is_authenticated():
        #This part used to import text and extra check parameters and assign them to variables
        text = request.POST.get('text', "")
        threeDigits = request.POST.get('threeDigits') == 'checked'
        onlyRoot = request.POST.get('onlyRoot') == 'checked'

        # This part of code counts through punctuation symbols finds them in text and replaces if find on .
        for c in string.punctuation + " " + "\n":
            text = text.replace(c, ".")

        # This part of code makes all symbols in text lower case, removes blank lines before and after text and makes
        # list of words, dividing them by .
        text = text.lower().strip().split(".")
        text = filter(None, text)

        #This part count through the list of words and check if there any digits. Then it makes new list without digits
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
            if not word or word == " ":
                continue
            elif len(word) == 1:
                continue
            elif threeDigits and len(word) <= 2:
                continue
            elif onlyRoot:
                word = stem(word)
            try:
                UserDictionary.objects.get(user=request.user, word=word)
                known_in_text.append(word)
            except UserDictionary.DoesNotExist:
                cnt[word] += 1
        a = cnt.items()
        # a.sort(key=lambda x: x[1], reverse=True)
        data = {
            "words": sorted(a),
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
    #This part of code specify sendgrig client, which sends greetings email after registration
    sg = sendgrid.SendGridClient('warager', 'cfyahfywbcrj!')

    try:
        User.objects.get(email=my_email)
    except User.DoesNotExist:
        user = User.objects.create_user(username=my_email, email=my_email)
        user.set_password(my_password)
        user.save()
        user.backend = "django.contrib.auth.backends.ModelBackend"
        auth_login(request, user)
        message = sendgrid.Mail()
        message.add_to(my_email)
        message.set_subject('Welcome!')
        message.set_text("Thank you for registration on my site!")
        message.set_from('fomin.dritmy@gmail.com')
        status, msg = sg.send(message)
        return HttpResponse('OK')
    #Checking of password confirmation
    if my_password != my_pass_conf:
        return HttpResponse('Wrong')
    return HttpResponse('Error')


#This is site login function
def login(request):
    my_email = request.POST.get('login', "")
    my_password = request.POST.get('password', "")

    try:
        user = User.objects.get(email__iexact=my_email, is_active=True)
    except User.DoesNotExist:
        return HttpResponse('Error')
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
    user_dictionary.save()
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
            n_words = request.POST.get('words', "")

            for c in string.punctuation + " " + "\n":
                n_words = n_words.replace(c, ".")

            n_words = n_words.lower().strip().split(".")
            n_words = filter(None, n_words)

            no_nums = []
            for w in n_words:
                try:
                    int(w) == int
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
                    UserDictionary.objects.get(user=request.user, word=word)
                except UserDictionary.DoesNotExist:
                    user_dictionary = UserDictionary(user=request.user, word=word)
                    user_dictionary.save()
            return redirect("/my_dictionary")

        known_words = set()
        for user_dictionary in UserDictionary.objects.filter(user=request.user):
            known_words.add(user_dictionary.word)

        data = {
            "known_words": sorted(known_words),
            "current_page": "my_dictionary"
        }
        return render(request, "word_stats/my_dictionary.html", data)
    else:
        return redirect("/")


#   The same method
#    user_dictionary = UserDictionary()
#    user_dictionary.user = request.user
#    user_dictionary.save()

#     user_dictionary = UserDictionary(user = request.user)
#     user_dictionary.save()

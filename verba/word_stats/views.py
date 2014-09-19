from collections import Counter
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
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

        #Creating list of known words
        known_words = UserDictionary.objects.values_list('word', flat=True)

        known_in_text = []
        cnt = Counter()
        for word in text:
            word.strip()
            if not word or word == " ":
                continue
            if len(word) == 1:
                continue
            if threeDigits and len(word) <= 2:
                continue
            if onlyRoot:
                word = stem(word)
            if word not in known_words:
                cnt[word] += 1
            if word in known_in_text:
                continue
            if word in known_words:
                known_in_text.append(word)
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
    message.set_text("Thank you for registration on my site!")
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

            for c in string.punctuation + " " + "\n":
                new_words = new_words.replace(c, ".")

            new_words = new_words.lower().strip().split(".")
            new_words = filter(None, new_words)

            no_nums = []
            for word in new_words:
                try:
                    int(word)
                except ValueError:
                    continue
                no_nums.append(word)
            new_words = no_nums

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


#   The same method
#    user_dictionary = UserDictionary()
#    user_dictionary.user = request.user
#    user_dictionary.save()

#     user_dictionary = UserDictionary(user = request.user)
#     user_dictionary.save()

# try:
#     UserDictionary.objects.get(user=request.user, word=word)
#     known_in_text.append(word)
# except UserDictionary.DoesNotExist:
#     cnt[word] += 1

#This part of code specify sendgrig client, which sends greetings email after registration
# sg = sendgrid.SendGridClient('warager', 'cfyahfywbcrj!')


# try:
#     User.objects.get(email=my_email)
# except User.DoesNotExist:
#
#     user = User.objects.create_user(username=my_email, email=my_email)
#     user.set_password(my_password)
#     user.save()
#     user.backend = "django.contrib.auth.backends.ModelBackend"
#     auth_login(request, user)
#     message = sendgrid.Mail()
#     message.add_to(my_email)
#     message.set_subject('Welcome!')
#     message.set_text("Thank you for registration on my site!")
#     message.set_from('fomin.dritmy@gmail.com')
#     status, msg = sg.send(message)
#     return HttpResponse('OK')
# #Checking of password confirmation
# if my_password != my_pass_conf:
#     return HttpResponse('Wrong')
# return HttpResponse('Error')
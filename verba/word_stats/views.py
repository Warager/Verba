from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.template.loader import render_to_string
from verba.settings import sg
from verba.word_stats.utils import text_to_words, words_analysis
import sendgrid


from verba.word_stats.models import UserDictionary


def input_form(request):
    """
    Renders start page
    :param request:
    :return:
    """
    data = {
        "current_page": 'home'
    }
    return render(request, 'word_stats/input_form.html', data)


def process(request):
    """
    Main computation of words entered by user
    :param request:
    :return:
    """
    if request.method != "POST":
        return redirect("/")
    text = request.POST.get('text', "")
    threeLetters = request.POST.get('threeLetters') == 'checked'
    onlyBase = request.POST.get('onlyBase') == 'checked'

    try:
        known_words = UserDictionary.objects.values_list('word', flat=True).filter(user=request.user)
    except TypeError:
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


def signup(request):
    """
    Site registration function
    :param request:
    :return:
    """
    my_email = request.POST.get('login', "")
    my_name = request.POST.get('name', 'Stranger')
    my_password = request.POST.get('password', "")
    my_pass_conf = request.POST.get('confirm', "")

    if User.objects.filter(username=my_email).count():
        return HttpResponse('Error')
    if my_email == "":
        return HttpResponse('EmptyUser')
    if my_password == "":
        return HttpResponse('EmptyPassword')
    if my_password != my_pass_conf:
        return HttpResponse('Wrong')

    #Creating new user
    user = User.objects.create_user(username=my_email, email=my_email)
    user.set_password(my_password)
    user.set_first_name(my_name)
    user.save()
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    #Sending greetings email
    message = sendgrid.Mail()
    message.add_to(my_email)
    message.set_subject('Welcome!')
    message.set_html(render_to_string('word_stats/welcome_email.html', {'user': user}))
    message.set_from('fomin.dritmy@gmail.com')
    status, msg = sg.send(message)
    return HttpResponse('OK')


def login(request):
    """
    Site log in function
    :param request:
    :return:
    """
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


@login_required
def logout(request):
    """
    Site logout function
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect('/')


def add_word(request):
    """
    Adds words to the user's personal dictionary
    :param request:
    :return:
    """
    word = request.POST.get('word', "")
    if word == "":
        return HttpResponse('Error')
    user_dictionary, _ = UserDictionary.objects.get_or_create(user=request.user, word=word)
    return HttpResponse('OK')


def rem_word(request):
    """
    Remover words from user's personal dictionary
    :param request:
    :return:
    """
    word_to_rem = request.POST['wordToRem']
    try:
        UserDictionary.objects.filter(user=request.user, word=word_to_rem).delete()
    except UserDictionary.DoesNotExist:
        return HttpResponse('DoesNotExist')
    return HttpResponse('OK')


#This function makes main computation in user's personal dictionary
def my_dictionary(request):

    if not request.user.is_authenticated():
        return redirect("/")

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
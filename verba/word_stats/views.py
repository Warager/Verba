from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from verba.word_stats.utils import text_to_words, words_analysis, send_email
from verba.word_stats.models import UserDictionary


def input_form(request):
    """
    Renders start page
    """
    data = {
        "current_page": 'home'
    }
    return render(request, 'word_stats/input_form.html', data)


@csrf_exempt
def process(request):
    """
    Main computation of words entered by user
    """
    if request.method != "POST":
        return redirect("/")
    text = request.POST.get('text', "")
    three_letters = request.POST.get('threeLetters') == 'true'
    only_base = request.POST.get('onlyBase') == 'true'

    if request.user.is_authenticated():
        known_words = UserDictionary.objects.values_list(
            'word', flat=True).filter(user=request.user)
    else:
        known_words = []

    words_list = text_to_words(text)
    _, cnt = words_analysis(words_list, three_letters, only_base, known_words)
    known_in_text, _ = words_analysis(words_list, three_letters, only_base,
                                      known_words)

    return JsonResponse({'success': True,
                         'analysis': render_to_string(
                             'analysis.html', {
                                 "words": sorted(cnt.items()),
                                 "known_words": sorted(known_words),
                                 "known_in_text": sorted(known_in_text)
                             })})


# def signup(request):
#     """
#     Site registration function
#     """
#     my_email = request.POST.get('login', "")
#     my_name = request.POST.get('name', 'Stranger')
#     my_password = request.POST.get('password', "")
#     my_pass_conf = request.POST.get('confirm', "")
#
#     if User.objects.filter(username=my_email).count():
#         return JsonResponse({'success': False, 'error': 'error'})
#     if my_email == "":
#         return JsonResponse({'success': False, 'error': 'empty_user'})
#     if my_password == "":
#         return JsonResponse({'success': False, 'error': 'empty_password'})
#     if my_password != my_pass_conf:
#         return JsonResponse({'success': False, 'error': 'wrong'})
#
#     user = User.objects.create_user(username=my_email, email=my_email)
#     user.set_password(my_password)
#     user.first_name = my_name
#     user.save()
#     user.backend = "django.contrib.auth.backends.ModelBackend"
#     auth_login(request, user)
#     # send_email(user, my_email)
#     return JsonResponse({'success': True, 'headline': render_to_string(
#         'headline.html', {'user': user})})
#
#
# def login(request):
#     """
#     Site log in function
#     """
#     my_email = request.POST.get('login', "")
#     my_password = request.POST.get('password', "")
#
#     try:
#         user = User.objects.get(email__iexact=my_email, is_active=True)
#     except User.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'error'})
#
#     if not user.check_password(my_password):
#         return JsonResponse({'success': False, 'error': 'error'})
#     user.backend = "django.contrib.auth.backends.ModelBackend"
#     auth_login(request, user)
#     return JsonResponse({'success': True, 'headline': render_to_string(
#         'headline.html', {'user': user})})
#
#
# @login_required
# def logout(request):
#     """
#     Site logout function
#     """
#     auth.logout(request)
#     return redirect('/')


def add_word(request):
    """
    Adds words to the user's personal dictionary
    """
    if not request.user.is_authenticated():
        return JsonResponse({'success': False})
    word = request.POST.get('word', "")
    user_dictionary, _ = UserDictionary.objects.get_or_create(
        user=request.user,
        word=word)
    return JsonResponse({'success': True})


def rem_word(request):
    """
    Remover words from user's personal dictionary
    """
    word_to_rem = request.POST['wordToRem']
    try:
        UserDictionary.objects.filter(user=request.user,
                                      word=word_to_rem).delete()
    except UserDictionary.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'does_not_exist'})
    return JsonResponse({'success': True})


def my_dictionary(request):
    """
    Main computation in user's dictionary
    """
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
            user_dictionary, _ = UserDictionary.objects.get_or_create(
                user=request.user,
                word=word)
        return redirect("/my_dictionary")

    known_words = set()
    for user_dictionary in UserDictionary.objects.filter(user=request.user):
        known_words.add(user_dictionary.word)

    data = {
        "known_words": sorted(known_words),
        "current_page": "my_dictionary"
    }
    return render(request, "word_stats/my_dictionary.html", data)
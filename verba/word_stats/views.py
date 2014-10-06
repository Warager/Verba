from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from verba.word_stats.utils import text_to_words, words_analysis
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
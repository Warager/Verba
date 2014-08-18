from collections import Counter
from django.shortcuts import render
import string

# Create your views here.
def input_form(request):
    return render(request, 'word_stats/input_form.html')

def process(request):
    text = request.POST['text']

    for c in string.punctuation:
        text = text.replace(c, "")
    text = text.lower().split(' ')
    cnt = Counter()

    for word in text:
        cnt[word] += 1

    a = cnt.items()
    a.sort(key=lambda x: x[1], reverse=True)
    data = {
        "words": a
    }
    return render(request, 'word_stats/analysis.html', data)
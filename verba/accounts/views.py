from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.template.loader import render_to_string
from verba.word_stats.utils import send_welcome_email


def signup(request):
    """
    Site registration function
    """
    my_email = request.POST.get('login', "")
    my_name = request.POST.get('name', 'Stranger')
    my_password = request.POST.get('password', "")
    my_pass_conf = request.POST.get('confirm', "")

    if User.objects.filter(username=my_email).count():
        return JsonResponse({'success': False, 'error': 'error'})
    if my_email == "":
        return JsonResponse({'success': False, 'error': 'empty_user'})
    if my_password == "":
        return JsonResponse({'success': False, 'error': 'empty_password'})
    if my_password != my_pass_conf:
        return JsonResponse({'success': False, 'error': 'wrong'})

    user = User.objects.create_user(username=my_email, email=my_email)
    user.set_password(my_password)
    user.first_name = my_name
    user.save()
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    send_welcome_email(user, my_email)
    return JsonResponse({'success': True, 'headline': render_to_string(
        'headline.html', {'user': user})})


def login(request):
    """
    Site log in function
    """
    my_email = request.POST.get('login', "")
    my_password = request.POST.get('password', "")

    try:
        user = User.objects.get(email__iexact=my_email, is_active=True)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'error'})

    if not user.check_password(my_password):
        return JsonResponse({'success': False, 'error': 'error'})
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    return JsonResponse({'success': True, 'headline': render_to_string(
        'headline.html', {'user': user})})


@login_required
def logout(request):
    """
    Site logout function
    """
    auth.logout(request)
    return redirect('/')

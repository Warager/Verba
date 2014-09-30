from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login




def signup(request):
    """
    Site registration function
    """
    my_email = request.POST.get('login', "")
    my_name = request.POST.get('name', 'Stranger')
    my_password = request.POST.get('password', "")
    my_pass_conf = request.POST.get('confirm', "")

    if User.objects.filter(username=my_email).count():
        return JsonResponse({'reply': 'Error'})
    if my_email == "":
        return JsonResponse({'reply': 'EmptyUser'})
    if my_password == "":
        return JsonResponse({'reply': 'EmptyPassword'})
    if my_password != my_pass_conf:
        return JsonResponse({'reply': 'Wrong'})

    user = User.objects.create_user(username=my_email, email=my_email)
    user.set_password(my_password)
    user.first_name = my_name
    user.save()
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    # send_email(user, my_email)
    return JsonResponse({'reply': 'OK'})


def login(request):
    """
    Site log in function
    """
    my_email = request.POST.get('login', "")
    my_password = request.POST.get('password', "")

    try:
        user = User.objects.get(email__iexact=my_email, is_active=True)
    except User.DoesNotExist:
        return JsonResponse({'reply': 'Error'})

    if not user.check_password(my_password):
        return JsonResponse({'reply': 'Error'})
    user.backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user)
    return JsonResponse({'reply': 'OK', 'navhead': '.navhead'})


@login_required
def logout(request):
    """
    Site logout function
    """
    auth.logout(request)
    return redirect('/')
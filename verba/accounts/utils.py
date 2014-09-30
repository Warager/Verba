from django.template.loader import render_to_string
from sendgrid import sendgrid
from verba.settings import sg, DEFAULT_EMAIL


def send_email(user, my_email):
    """
    Sends welcome message on user's email
    :param user:
    :param my_email:
    :return:
    """
    message = sendgrid.Mail(
        to=my_email,
        subject='Welcome',
        html=render_to_string('accounts/welcome_email.html',
                              {'user': user}),
        from_email=DEFAULT_EMAIL)
    status, msg = sg.send(message)
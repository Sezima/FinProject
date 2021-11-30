

from django.core.mail import send_mail



def send_welcome_email(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""
    Thank you for registrate in our Online Hospital!
    To activate your account click here {activation_url}
    """

    send_mail('Online hospital account activation',message,'admin@admin.com', [email, ], fail_silently=False, )


def send_welcome_mail(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""
    To reset your password click here {activation_code}
"""

    send_mail('Onlne Hospital password reset',message,'admin@admin.com', [email, ], fail_silently=False, )
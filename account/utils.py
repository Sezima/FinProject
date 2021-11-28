from django.core.mail import send_mail

def send_welcome_email(email):
    message = f'Thanks for registration in our site Online Hospital!'
    send_mail(
        'Welcome to Online Hospital!',
        message,
        'admin@gmail.com',
        [email],
        fail_silently=False
    )





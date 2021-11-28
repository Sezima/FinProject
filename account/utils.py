from django.core.mail import send_mail

def send_welcome_email(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""Thanks for registration in our site Online Hospital!
    Activate your email with link: {activation_url}'
"""
    send_mail(
        'Welcome to Online Hospital!',
        message,
        'admin@gmail.com',
        [email],
        fail_silently=False
    )





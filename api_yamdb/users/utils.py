from django.core.mail import send_mail


def send_email_with_code(email, confirmation_code):
    message = 'Your confirmation code: ' + str(confirmation_code)
    send_mail(
        'Confirmation code',
        message,
        'from@example.com',
        [email],
        fail_silently=False,
    )

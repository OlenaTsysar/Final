from django.conf import settings

def email_context(request):
    return {
        'EMAIL_HOST_USER': settings.EMAIL_HOST_USER
    }

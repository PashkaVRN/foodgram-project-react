from random import randint

from django.conf import settings
from django.core.mail import send_mail


def get_confirmation_code():
    """Генерирует 6-тизначный код."""
    return randint(
        settings.CONFIRMATION_CODE_MIN_VALUE,
        settings.CONFIRMATION_CODE_MAX_VALUE
    )


def send_confirmation_code(user):
    """
    Отправляет код для регистрации на почту.
    В качестве аргумента принимает проверенные данные сериализатора
    и объект пользователя.
    """
    send_mail(
        subject='Регистрация на foodgram',
        message=(
            'Для завершения регистрации на Yamdb отправьте запрос '
            f'с именем пользователя {user.username} и '
            f'кодом подтверждения {user.confirmation_code} '
            'на эндпойнт /api/v1/auth/token/.'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )

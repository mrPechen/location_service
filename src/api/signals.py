import random
import string

from django.db.models.signals import pre_save
from django.dispatch import receiver

from api.models import Car


def generate_unique_number():
    unique_num = random.randint(1000, 9999)
    letter = random.choice(string.ascii_uppercase)
    result = f'{unique_num}{letter}'
    return result


def get_unique_num():
    result = generate_unique_number()
    check_unique_num = Car.objects.filter(number=result).exists()
    while check_unique_num:
        result = generate_unique_number()

    return result


@receiver(pre_save, sender=Car)
def save_user_profile(sender, instance, **kwargs):
    instance.number = get_unique_num()

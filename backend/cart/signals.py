from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Cart


@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    """
    Yangi User yaratilganda avtomatik ravishda uning Cart'i ham yaratiladi.
    Shu tufayli Cart yaratish uchun alohida kod yozish shart emas.
    """
    if created:
        Cart.objects.get_or_create(user=instance)

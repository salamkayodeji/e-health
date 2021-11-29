from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Medical_History, UserProfile
from django.dispatch import receiver



@receiver(post_save, sender=UserProfile)
def create_medical_history(sender, instance, created, **kwargs):
    if created:
        Medical_History.objects.create(email=instance)


@receiver(post_save, sender=User)
def save_medical_history(sender, instance, **kwargs):
    instance.medical_history.save()
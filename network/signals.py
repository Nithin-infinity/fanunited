from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def updateProfile(sender, instance, created, **kwargs):
    if not created:
        instance.profile.save()

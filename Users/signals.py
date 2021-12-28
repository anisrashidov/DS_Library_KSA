from django.db.models.signals import post_save
from .models import Student, Profile
from django.dispatch import receiver

@receiver(post_save, sender=Student)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=Student)
def save_profile(sender, instance, **kwargs):
		instance.profile.save()
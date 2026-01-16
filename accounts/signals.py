from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance: User, created: bool, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            metadata={
                "company": "Carlsberg Koprivnica",
                "created_by": "IT Department",
            }
        )
    else:
        UserProfile.objects.get_or_create(user=instance)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    github = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True, verbose_name='Profil Fotoğrafı')
    bio = models.TextField(max_length=300, blank=True, null=True, verbose_name='Biyografi')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class NewsletterEmail(models.Model):
    email = models.EmailField(unique=True, verbose_name='E-posta')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

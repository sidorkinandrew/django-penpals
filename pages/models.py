from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)
    first = models.CharField(max_length=200, blank=True, null=True)
    last = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(
        default='user.png', upload_to='photos/%y/%m',  blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)
    speaks = models.CharField(max_length=200, blank=True, null=True)
    learns = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['-id']


def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)
        print(f"profile created for {instance}")


post_save.connect(create_profile, sender=User)

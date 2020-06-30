from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    QUESTION_CHOICE = [('UG', (
        ('CS', 'Comp. Sci/ IT Engg.'),
        ('ECE', 'Electrical & Comm Engg.'),
        ('EEE', 'Electrical Engg.'),
        ('MH', 'Mechanical Engg'),
        ('GN', 'General'))
    ), ('N', 'None')]
    field = models.CharField(max_length=3, choices=QUESTION_CHOICE, default='N')
    CHOICE = [
        (True, 'Notify Me'),
        (False, 'Don\'t Notify Me')
    ]
    notifications = models.BooleanField(choices=CHOICE, default=True)
    image = models.ImageField(upload_to='profile pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username}\'s profile'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            resize = (300, 300)
            img.thumbnail(resize)
            img.save(self.image.path)


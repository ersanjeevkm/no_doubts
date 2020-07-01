from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.core.mail import send_mail
from .models import Questions
from users.models import Profile

request = None
def crnt_request(current_request):
    global request
    request = current_request

@receiver(post_save, sender=Questions)
def create_profile(sender, instance, created, **kwargs):
    if created:
        message = f'''
                   *** This is an no-reply notification message from NO DOUBTS ***

                   Hello,
                   '{instance.author.username}' has an Doubt based on your field({instance.get_category_display()}) : '{instance.title}'

                    Check this link to find out {request.build_absolute_uri(reverse('post_detail', kwargs={'slug': instance.slug}))}

                   If this isn't you please ignore this. Sorry for the inconvenience.

                   If you didn't like to receive any such notifications select "Don't Notify Me" option under Notification panel here {request.build_absolute_uri(reverse('account'))}

                   From, NO DOUBTS team.
               '''
        receivers = []
        profiles = Profile.objects.filter(field=instance.category)
        for profile in profiles:
            if profile.notifications:
                if profile.user != request.user:
                    receivers.append(profile.user.email)

        send_mail(
            subject=f"Someone has an Doubt based on your field",
            message=message,
            from_email='noreply.nodoubts@gmail.com',
            recipient_list=receivers,
            fail_silently=False,
        )

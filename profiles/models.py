from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from .utils import code_generator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
# Create your models here.
User=settings.AUTH_USER_MODEL

class ProfileManager(models.Manager):
    def toggle_follow(self,request_user,username_to_toggle):
        profile_=Profile.objects.get(user__username__iexact=username_to_toggle)
        user=request_user
        is_following=False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following=True
        return profile_,is_following
class Profile(models.Model):
    user=   models.OneToOneField(User)
    followers=  models.ManyToManyField(User,related_name='is_following',blank=True)
    #following=  models.ManyToManyField(User,related_name='following',blank=True)

    activation_key=models.CharField(max_length=120,blank=True,null=True)
    activated=  models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    objects=ProfileManager()


    def __str__(self):
        return self.user.username
    #challenge code
    def send_activation_email(self):
        if not self.activated:
            self.activation_key=code_generator()
            path_=reverse('activate',kwargs={"code": self.activation_key})
            subject = 'Activate account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: {path_}'
            recipient_list = ['mytest@gmail.com', 'you@email.com']
            html_message = f'<h1>Activate your account here: {path_}</h1>'
            self.save()
            print(html_message)
            #send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
            sent_mail=False
            return sent_mail

def post_save_user_receiver(sender,instance,created,*args,**kwargs):
    if created:
        profile,is_created=Profile.objects.get_or_create(user=instance)
        default_user_profile=Profile.objects.get_or_create(user__id=1)[0]
        default_user_profile.followers.add(instance)

def pre_save_user_receiver(sender,instance,**kwargs):
    instance.is_active=True

pre_save.connect(pre_save_user_receiver,sender=User)
post_save.connect(post_save_user_receiver,sender=User)

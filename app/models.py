from __future__ import unicode_literals
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings


# create Blog as soon as User is created
@receiver(post_save, sender=User)
def create_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance)


class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

    def get_absolute_url(self):
        return reverse('blog', kwargs={'pk': self.blog.user.pk})

    def __unicode__(self):
        return self.name


# Send message as soon as new Post in Feed was created
@receiver(post_save, sender=Post)
def send_mail_if_post(sender, instance, created, **kwargs):
    if created:
        blog = instance.blog
        subscriptions = Subscription.objects.filter(blog=blog)
        to = [subscription.user.email for subscription in subscriptions]
        mail = send_mail(
            subject='New Post from user {}'.format(blog.user.username),
            message='New Post http://127.0.0.1:8000/post/{}'.format(instance.pk),
            recipient_list=to,
            from_email=settings.EMAIL_HOST_USER
        )


class Subscription(models.Model):
    """
    Subscription of a user to blogs
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name="blog", on_delete=models.CASCADE)


class FinishedPost(models.Model):
    """
    Read post by a user
    """
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post", on_delete=models.CASCADE)
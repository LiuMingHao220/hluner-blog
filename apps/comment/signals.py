import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from notifications.signals import notify
from .models import Comment
#

@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    if instance.reply_to is None:
        # 评论
        recipient = instance.content_object.get_user()
        if instance.content_type.model == 'article':
            article = instance.content_object
            verb = '{0} 评论了你的文章《{1}》'.format(instance.user.username, article.title)
        else:
            raise Exception('unkown comment object type')
    else:
        # 回复
        recipient = instance.reply_to
        verb = '{0} 回复了你的评论“{1}”'.format(
            instance.user.username,
            strip_tags(instance.parent.comment_text)
        )
    url = instance.content_object.get_absolute_url() + "#comment_" + str(instance.pk)
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance,url = url)
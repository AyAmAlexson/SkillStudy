from django.db import models
from users.models import CustomUser

from django.shortcuts import reverse

from .misc import AD_STATUS_CHOICES, RES_STATUS_CHOICES, GENERAL
from embed_video.fields import EmbedVideoField
from markdownx.models import MarkdownxField

from ckeditor.fields import RichTextField

class Ad(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET(GENERAL))
    title = models.CharField(max_length=50)
    body = RichTextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    status = models.CharField(max_length=2,choices=AD_STATUS_CHOICES, default='TR')
    reject_comment = models.CharField(max_length=50, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('adboard:detail_ad_view', args=[str(self.id)])


class Response(models.Model):
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices= RES_STATUS_CHOICES, default='SB')


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='ads_main_image/')
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)


class Video(models.Model):
    video = EmbedVideoField()
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE)
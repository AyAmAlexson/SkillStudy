from .models import Ad, Category, Image, Video
from django import forms
from embed_video.fields import EmbedVideoFormField
from markdownx.models import MarkdownxFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class AdForm(forms.ModelForm):
    title = forms.CharField(max_length=50, label="Title")
    body = RichTextUploadingFormField()
    category = forms.ModelChoiceField(
        label="Category",
        widget=forms.Select,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Ad
        fields = [
            'title',
            'body',
            'category',
        ]


class ImageForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = Image
        fields = [
            #'ad',
            'image',
        ]


class VideoForm(forms.ModelForm):
    video = EmbedVideoFormField()
    class Meta:
        model = Video
        fields = [
            #'ad',
            'video',
        ]


class AdCreationForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    video = EmbedVideoFormField(required=False)

    class Meta:
        model = Ad
        fields = ['title', 'body', 'category', 'image', 'video']

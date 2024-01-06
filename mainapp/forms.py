from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Posts, Responses


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Текст')

    class Meta:
        model = Posts
        fields = [
            'title',
            'category',
            'content',
            'author'
        ]
        labels = {
            'category': 'Категория',
            'title': 'Название',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = [
            'post',
            'text',
            'author',
        ]
        labels = {
            'post': 'Пост',
            'text': 'Текст отклика',
        }
        widgets = {
            'post': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

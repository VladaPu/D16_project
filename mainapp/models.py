from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.urls import reverse


class Posts(models.Model):
    TYPE = (
        ('tanks', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=64)
    content = RichTextUploadingField(verbose_name='Содержание')
    category = models.CharField(max_length=12, choices=TYPE, default='tanks', verbose_name='Категория')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title.title()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Responses(models.Model):
    CONDITION = (
        ('U', 'Undefined'),
        ('A', 'Accepted'),
        ('D','Deleted')
    )
    author = models.ForeignKey(User, verbose_name='Автор отклика', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст отклика', default='')
    post = models.ForeignKey(Posts, verbose_name='Пост', on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Состояние отклика', max_length=1,choices=CONDITION, default='U')

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return f'{self.text[:12]}'
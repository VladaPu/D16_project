from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Posts, Responses
from .forms import PostForm, ResponseForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect

class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Posts
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Posts
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Posts
    # и новый шаблон, в котором используется форма.
    template_name = 'post_create.html'


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ResponseList(LoginRequiredMixin, ListView):
    model = Responses
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        self.selected_post_id = self.request.GET.get('post_id')
        replies = Responses.objects.filter(post__author=self.request.user)
        if self.selected_post_id:
            return replies.filter(post__id=self.selected_post_id)
        else:
            return replies

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_post_id'] = int(self.selected_post_id) if self.selected_post_id else None
        return context

    def post(self, request, *args, **kwargs):
        response_pk = request.POST.get('pk')
        response = Responses.objects.get(pk=response_pk)

        if 'accepted' in request.POST:
            response.status = 'A'
        elif 'deleted' in request.POST:
            response.status = 'D'

        response.save()

        mail = send_mail(
            subject=f"Реакция на ваш отклик по объявлению '{response.post}'",
            message=f"{response.author}!\n\nВаш отклик '{response.text}' на объявление '{response.post.title}' "
                    f"{response.get_status_display().lower()}!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.author.email]
        )
        print(mail)
        return redirect(self.request.path_info)


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Responses
    template_name = 'response_create.html'
    success_url = reverse_lazy('post_list')



from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator

from .models import Post
from .filters import PostFilter
from .forms import PostForm

from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView


class Posts(LoginRequiredMixin, ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-id']
    paginate_by = 1  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # получили весь контекст из класса-родителя
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()  # добавили новую контекстную переменную is_not_authors
        return context

class PostSearch(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context

class PostDetailView(DetailView):
    template_name = 'flatpages/post_detail.html'
    queryset = Post.objects.all()

class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post')


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm
    queryset = Post.objects.all()
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post')


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'flatpages/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post')


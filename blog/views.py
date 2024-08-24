from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.models import Articles
from dentistry.forms import ArticlesModeratorForm


# Контроллер для просмотра статей
class ArticlesListView(ListView):
    model = Articles


# Контроллер для создания статей статей
class ArticlesCreateView(CreateView):
    model = Articles
    form_class = ArticlesModeratorForm
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_object = form.save()
            new_object.save()

        return super().form_valid(form)


# Контроллер для просмотра выбранной статьи
class ArticlesDetailView(DetailView):
    model = Articles

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


# Контроллер для редактирования статьи
class ArticlesUpdateView(UpdateView):
    model = Articles
    form_class = ArticlesModeratorForm
    success_url = reverse_lazy('blog:blog_list')




# Контроллер для удаления врача
class ArticlesDeleteView(DeleteView):
    model = Articles
    success_url = reverse_lazy('blog:blog_list')

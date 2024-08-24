from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import ArticlesListView, ArticlesCreateView, ArticlesUpdateView, ArticlesDeleteView, ArticlesDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(60)(ArticlesListView.as_view()), name='blog_list'),
    path('blog_create/', ArticlesCreateView.as_view(), name='blog_create'),
    path('blog_detail/<int:pk>', ArticlesDetailView.as_view(), name='blog_detail'),
    path('blog_update/<int:pk>', ArticlesUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>', ArticlesDeleteView.as_view(), name='blog_delete'),
]
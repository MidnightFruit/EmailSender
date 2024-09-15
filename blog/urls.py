from blog.views import BlogPostListView, BlogPostDetailView
from blog.apps import BlogConfig
from django.urls import path

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', BlogPostListView.as_view(), name='blog'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='read_post'),
]

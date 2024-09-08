from blog.views import BlogPostCreateView, BlogPostListView, BlogPostDetailView, BlogPostUpdateView, BlogPostDeleteView
from blog.apps import BlogConfig
from django.urls import path

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', BlogPostListView.as_view(), name='blog'),
    path('create/', BlogPostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='read_post'),
    path('update/<int:pk>/', BlogPostUpdateView.as_view(), name='update_post'),
    path('delite/<int:pk>/', BlogPostDeleteView.as_view(), name='delete_post'),
]

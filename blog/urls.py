from blog.views import BlogPostListView
from blog.apps import BlogConfig
from django.urls import path

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', BlogPostListView.as_view(), name='blog'),

]

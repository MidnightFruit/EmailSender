import random

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import BlogPost
from sender.models import Sender, Client


class BlogPostListView(ListView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        number_senders = Sender.objects.all()
        number_of_active_senders = 0
        for score in number_senders:
            if score.status == Sender.STATUSES[2][0]:
                number_of_active_senders += 1

        context_data['number_senders'] = len(number_senders)
        context_data['number_of_active_senders'] = number_of_active_senders

        number_clients = Client.objects.all()
        context_data['number_clients'] = len(number_clients)

        posts = BlogPost.objects.all()
        first_post, second_post, third_post = random.sample(range(1, len(posts) + 1), 3)
        context_data['first_post'] = first_post
        context_data['second_post'] = second_post
        context_data['third_post'] = third_post

        return context_data


    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'content', 'is_published')
    success_url = reverse_lazy('blog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ('title', 'content', 'is_published')
    # success_url = reverse_lazy('blog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:read_post', args=[self.kwargs.get('pk')])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog:blog")


class BlogPostDetailView(DetailView):
    model = BlogPost

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = None

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.viewed += 1
        self.object.save()
        return self.object

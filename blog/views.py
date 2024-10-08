import random

from django.views.generic import ListView

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
        try:
            first_post, second_post, third_post = random.sample(range(1, len(posts) + 1), 3)
        except:
            first_post = None
            second_post = None
            third_post = None
        context_data['first_post'] = first_post
        context_data['second_post'] = second_post
        context_data['third_post'] = third_post

        return context_data

from django.urls import path
from django.views.decorators.cache import cache_page

from sender.apps import SenderConfig

from sender.views import SenderCreateView, SenderListView, SenderTemplateView, ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView, ClientTemplateView, MessageListView, MessageCreateView, MessageDeleteView, \
    MessageUpdateView, MessageTemplateView, AttemptsListView

app_name = SenderConfig.name

urlpatterns = [
    path('create_sender/', SenderCreateView.as_view(), name='create_sender'),
    path('', SenderListView.as_view(), name='sender_list'),
    path('sender/<int:pk>/', SenderTemplateView.as_view(), name='sender_view'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('add_client/', ClientCreateView.as_view(), name='create_client'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('client/<int:pk>/', ClientTemplateView.as_view(), name='client'),
    path('messages_templates/', MessageListView.as_view(), name='message_list'),
    path('create_messages/', MessageCreateView.as_view(), name='create_message'),
    path('update_message/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
    path('message/<int:pk>/', cache_page(60)(MessageTemplateView.as_view()), name='message'),
    path('attempts_list/', AttemptsListView.as_view(), name='attempts_list')
]
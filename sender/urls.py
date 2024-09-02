from django.urls import path

from sender.apps import SenderConfig

from sender.views import SenderCreateView, SenderListView, SenderTemplateView, ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView, ClientTemplateView

app_name = SenderConfig.name

urlpatterns = [
    path('create_sender/', SenderCreateView.as_view(), name='create_sender'),
    path('', SenderListView.as_view(), name='sender_list'),
    path('sender/<int:pk>/', SenderTemplateView.as_view(), name='sender_view'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('add_client/', ClientCreateView.as_view(), name='create_client'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('client/<int:pk>/', ClientTemplateView.as_view(), name='client')
]
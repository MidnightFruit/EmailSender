from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView

from sender.forms import SenderForm, ClientForm
from sender.models import Sender, Client


class ClientTemplateView(TemplateView):
    template_name = 'sender/client.html'

    def get(self, request, pk):
        context = {'object': Client.objects.get(pk=pk)}
        return render(request, self.template_name, context)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    model = Client
    fields = ('name', 'surname', 'patronymic', 'email', 'comment')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    model = Client
    success_url = reverse_lazy('sender:client_list')


class ClientCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    model = Client
    success_url = reverse_lazy('sender:client_list')
    form_class = ClientForm

    def form_valid(self, form):
        client = form.save()
        client.company = self.request.user
        client.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class ClientListView(ListView):
    model = Client
    template_name = 'sender/client_list.html'


class SenderCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    model = Sender
    success_url = reverse_lazy('sender:sender_list')
    form_class = SenderForm

    def form_valid(self, form):
        sender = form.save()
        sender.company = self.request.user
        sender.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class SenderUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    model = Sender
    fields = ('title', 'clients', 'frequency', 'status')


class SenderTemplateView(TemplateView):
    template_name = 'sender/sender_view.html'

    def get(self, request, pk):
        context = {'object': Sender.objects.get(pk=pk)}
        return render(request, self.template_name, context)


class SenderListView(ListView):
    model = Sender


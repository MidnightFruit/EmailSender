from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView

from sender.forms import SenderForm, ClientForm, MessageForm
from sender.models import Sender, Client, Message, DeliveryAttempt


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
        sender.status = Sender.STATUSES[1][0]
        sender.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class SenderUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    model = Sender
    fields = ('title', 'clients', 'frequency', 'status', 'message')


class SenderTemplateView(TemplateView):
    template_name = 'sender/sender_view.html'

    def get(self, request, pk):
        context = {'object': Sender.objects.get(pk=pk)}
        return render(request, self.template_name, context)


class SenderListView(ListView):
    model = Sender


class MessageListView(ListView):
    model = Message
    template_name = 'sender/message_list.html'


class MessageTemplateView(TemplateView):
    template_name = 'sender/message.html'

    def get(self, request, pk):
        context = {'object': Message.objects.get(pk=pk)}
        return render(request, self.template_name, context)


class MessageCreateView(CreateView):
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    model = Message
    success_url = reverse_lazy('sender:message_list')
    form_class = MessageForm

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('sender:message_list')
    model = Message
    form_class = MessageForm


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    model = Message
    success_url = reverse_lazy('sender:message_list')


class AttemptsListView(LoginRequiredMixin, ListView):
    model = DeliveryAttempt
    template_name = 'sender/attempt_list.html'
    login_url = reverse_lazy('company:login')
    redirect_field_name = 'redirect_to'
    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        logs = DeliveryAttempt.objects.all()
        users_logs = []
        for log in logs:
            if log.sender.company == self.request.user:
                users_logs.append(log)
        context_data['logs'] = users_logs
        return context_data
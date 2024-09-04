from django import forms

from sender.models import Sender, Client, Message


class SenderForm(forms.ModelForm):

    class Meta:
        model = Sender
        fields = '__all__'
        exclude = ('company',)


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('company',)


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'
        exclude = ('owner',)
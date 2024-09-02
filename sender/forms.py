from django import forms

from sender.models import Sender, Client


class SenderForm(forms.ModelForm):

    class Meta:
        model = Sender
        fields = '__all__'
        exclude = ('clients',)


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('company',)

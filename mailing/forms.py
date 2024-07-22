from django.forms import BooleanField
from django import forms
from mailing.models import Client, MailingSettings


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'first_name', 'last_name', 'comment')


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from blog.models import Blog
from mailing.models import MailingSettings, Client, MailingMessage, MailingLog
from mailing.forms import MailingSettingsForm, ClientForm


def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print(f'{name} ({email}: {message})')

    return render(request, 'mailing/start_page.html')


class ContactsTemplateView(TemplateView):
    template_name = 'mailing/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingSettings

    def get_queryset(self):
        if self.request.user.is_superuser:
            return MailingSettings.objects.all()
        elif self.request.user.is_authenticated:
            return MailingSettings.objects.filter(owner=self.request.user)
        raise PermissionDenied


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    # success_url = reverse_lazy('mailing:start_page')
    form_class = MailingSettingsForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:setting_list')
    fields = '__all__'


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:setting_list')


class MailingMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage
    fields = '__all__'

    def get_queryset(self):
        return MailingMessage.objects.filter(owner=self.request.user)


class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    fields = '__all__'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingMessageDetailView(LoginRequiredMixin, DetailView):
    model = MailingMessage
    fields = '__all__'
    success_url = reverse_lazy('mailing:message_detail')


class MailingMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingMessage
    fields = '__all__'
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        object = super().get_object()
        if object.owner == self.request.user:
            return object
        return PermissionDenied


class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    fields = '__all__'
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        object = super().get_object()
        if object.owner == self.request.user:
            return object
        return PermissionDenied


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Список клиентов'
    }

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_detail')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        object = super().get_object()
        if object.owner == self.request.user:
            return object
        return PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        object = super().get_object()
        if object.owner == self.request.user:
            return object
        return PermissionDenied


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    template_name = 'mailing/start_page.html'
    reverse_url = reverse_lazy('mailing:start_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список рассылок'
        context['mailings_all'] = len(MailingSettings.objects.all())
        context['mailings_active'] = len(MailingSettings.objects.filter(status='started'))
        context['clients_unique'] = len(Client.objects.all().distinct())
        context['blog'] = Blog.objects.all()[:3]
        return context
    # def get_queryset(self):
    #     return MailingLog.objects.filter(owner=self.request.user)

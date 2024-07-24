from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.views import ContactsTemplateView, MailingListView, index, MailingSettingsCreateView, \
    MailingSettingsDetailView, MailingSettingsUpdateView, MailingSettingsDeleteView, MailingMessageListView, \
    MailingMessageCreateView, MailingMessageDetailView, MailingMessageUpdateView, MailingMessageDeleteView, \
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, MailingLogListView
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    # path('', index, name='start_page'),
    path('', MailingLogListView.as_view(), name='start_page'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('message/', MailingMessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MailingMessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MailingMessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MailingMessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MailingMessageDeleteView.as_view(), name='message_delete'),

    path('mailing', MailingListView.as_view(), name='setting_list'),
    path('settings/<int:pk>/', MailingSettingsDetailView.as_view(), name='setting_detail'),
    path('settings/create/', MailingSettingsCreateView.as_view(), name='setting_create'),
    path('settings/update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='setting_update'),
    path('settings/delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='setting_delete'),

]

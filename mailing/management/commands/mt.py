from django.core.management import BaseCommand

from mailing.services.serv_send_mail import send_all_mails


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_all_mails()

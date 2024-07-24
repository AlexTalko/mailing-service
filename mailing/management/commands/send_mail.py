from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from mailing.services.serv_send_mail import send_all_mails


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = 'Runs APScheduler.'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_all_mails,
            trigger=CronTrigger(second='*/30'),
            id='sendmail',
            max_instances=10,
            replace_existing=True,
        )

        try:
            print('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            print("Stopped scheduler")
            scheduler.shutdown()
            print("Success!")

from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.core.serializers.json import DjangoJSONEncoder
import json

schedule, _ = CrontabSchedule.objects.get_or_create(
    minute='0',
    hour='0',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)


PeriodicTask.objects.create(
    crontab=schedule,
    name='Send daily newsfeed',
    task='celery_tasks.tasks.send_daily_newsfeed_to_console',
    args=json.dumps([]),
    kwargs=json.dumps({}),
    expires=None,
    enabled=True,
    one_off=False
)

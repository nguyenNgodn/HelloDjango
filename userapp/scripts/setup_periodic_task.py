import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HelloPython.settings")
django.setup()

from django_celery_beat.models import PeriodicTask, IntervalSchedule

schedule, _ = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.MINUTES,
)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    name='Check new users and notify admin',
    task='userapp.services.mail_service.check_new_users_and_notify',
    defaults={'kwargs': json.dumps({})}
)

print("✅ Đã đăng ký task định kỳ.")

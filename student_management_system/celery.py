# student_management_system/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')

# Создаем экземпляр Celery
app = Celery('student_management_system')
app.conf.worker_pool = 'solo'

# Настройка из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи
app.autodiscover_tasks()

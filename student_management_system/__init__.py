# student_management_system/__init__.py
from __future__ import absolute_import, unicode_literals

# Инициализация Celery при запуске Django
from .celery import app as celery_app

__all__ = ('celery_app',)

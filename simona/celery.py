# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps 

# Thiết lập biến môi trường cho Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simona.settings')

# Tạo instance của Celery
app = Celery('Simona')

# Sử dụng chuỗi trong cấu hình, không phải các giá trị tương ứng
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động phát hiện các tasks trong các ứng dụng đã cài đặt
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

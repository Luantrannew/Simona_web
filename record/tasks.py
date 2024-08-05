from celery import shared_task
from django.conf import settings
from .models import Customer, Order
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

channel_layer = get_channel_layer()


@shared_task
def lookup_customer_info(channel_name, customer_code):
    print("Task: lookup_customer_info started")
    print(f"Channel Name: {channel_name}")
    print(f"Customer Code: {customer_code}")
    
    customer = Customer.objects.filter(code=customer_code).last()
    orders = Order.objects.filter(customer=customer).values_list('order_code', flat=True)

    if customer:
        response = {
            'status': 'success',
            'data': {
                'customer_code': customer.code,
                'customer_name': customer.name,
                'customer_segment': customer.seg.seg_name,
                'orders': list(orders),
            }
        }
    else:
        response = {
            'status': 'error',
            'message': 'Không tìm thấy khách hàng.'
        }

    print(f"Response: {response}")

    
    async_to_sync(channel_layer.send)(channel_name, {
        'type': 'chat.message',
        'message': json.dumps(response)
    })

    print("Task: lookup_customer_info completed")

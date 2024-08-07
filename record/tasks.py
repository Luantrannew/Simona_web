from celery import shared_task
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from time import sleep
from django.utils import timezone

from .models import Customer, Order, OrderLine, Product


channel_layer = get_channel_layer()


@shared_task
def lookup_customer_info(channel_name, customer_code):
    
    customer = Customer.objects.filter(code=customer_code).last()
    orders = Order.objects.filter(customer=customer).values_list('order_code', flat=True)

    if customer:
        response = {
            'status': 'success',
            'command' : 'lookup',
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
            'command' : 'lookup',
            'message': 'Không tìm thấy khách hàng.'
        }

    print(f"Response: {response}")

    sleep(2)
    async_to_sync(channel_layer.send)(channel_name, {
        'type': 'chat.message',
        'message': json.dumps(response)
    })

    print("Task: lookup_customer_info completed")


@shared_task
def place_order(channel_name, customer_code, orderlines):
    response = {}
    try:
        # Tìm khách hàng
        customer = Customer.objects.filter(code=customer_code).last()

        # Tạo mã đơn hàng mới
        last_order = Order.objects.last()
        new_order_number = (int(last_order.order_code.split('ORD')[1]) + 1) if last_order else 1
        order_code = f'ORD{new_order_number:07d}'

        # Tạo đối tượng Order
        order = Order.objects.create(
            order_code=order_code,
            customer=customer,
            time=timezone.now()
        )

        # Tạo các dòng sản phẩm (OrderLine)
        for line in orderlines:
            product_code = line.get('product_code')
            quantity = line.get('quantity')
            product = Product.objects.filter(code=product_code).last()
            if not product:
                raise Product.DoesNotExist(f"Product with code {product_code} does not exist.")
            
            OrderLine.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

        response = {
            'status': 'success',
            'command': 'order',
            'message': f"Đơn hàng {order_code} đã được tạo thành công cho khách hàng {customer.name}.",
            'order_id': order_code
        }
    except Customer.DoesNotExist:
        response = {
            'status': 'error',
            'command': 'order',
            'message': 'Không tìm thấy khách hàng.'
        }
    except Product.DoesNotExist as e:
        response = {
            'status': 'error',
            'command': 'order',
            'message': str(e)
        }
    except Exception as e:
        response = {
            'status': 'error',
            'command': 'order',
            'message': f'Có lỗi xảy ra: {str(e)}'
        }

    # Gửi phản hồi về WebSocket
    async_to_sync(channel_layer.send)(channel_name, {
        'type': 'chat.message',
        'message': json.dumps(response)
    })


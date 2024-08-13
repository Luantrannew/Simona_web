import re
import json
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import requests

COMMANDS = {
    'help': {
        'help': 'Thông tin trợ giúp các lệnh.',
    },
    'lookup': {
        'args': 1,
        'help': 'Tra cứu thông tin khách hàng, ví dụ: `lookup <mã khách hàng>`.',
        'task': 'lookup_customer_info'
    },
    'order': {
        'args': 3,
        'help': 'Đặt hàng, ví dụ: `order <mã khách hàng> <mã sản phẩm> <số lượng> <mã sản phẩm 2> <số lượng sp 2>`.',
        'task': 'place_order'
    },
}

class ShopBotConsumer(WebsocketConsumer):

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        response_message = 'Vui lòng nhập `help` để xem danh sách các lệnh có thể sử dụng.'

        command_match = re.match(r'(\w+)', message)
        if command_match:
            command = command_match.group(1).lower()
            if command == 'help':
                response_message = 'Các lệnh hỗ trợ:\n' + '\n'.join(
                    [f'{command} - {params["help"]}' for command, params in COMMANDS.items()])
            elif command in COMMANDS:
                required_args = COMMANDS[command]['args']
                if command == 'order':
                    # Sử dụng regex để trích xuất mã khách hàng, mã sản phẩm và số lượng
                    order_match = re.match(r'order\s+(\w+)\s+(.+)', message)
                    if order_match:
                        customer_code = order_match.group(1)
                        order_details = order_match.group(2)
                        orderlines = re.findall(r'(\w+)\s+(\d+)', order_details)
                        if not orderlines:
                            response_message = 'Lệnh `order` yêu cầu các cặp mã sản phẩm và số lượng.'
                        else:
                            orderlines = [{'product_code': code, 'quantity': qty} for code, qty in orderlines]
                            task_name = COMMANDS[command]['task']
                            url = "http://127.0.0.1:8000/home/chatbot/handle-task/"
                            data = {
                                'task_name': task_name,
                                'channel_name': self.channel_name,
                                'args': [customer_code, orderlines]
                            }
                            response = requests.post(url, json=data)
                            response_message = f'Đã nhận `{message}`, đang xử lý...'
                else:
                    args_match = re.match(r'\w+\s+(.*)', message)
                    if args_match:
                        args = args_match.group(1).split()
                        if len(args) != required_args:
                            response_message = f'Lệnh `{command}` yêu cầu {required_args} tham số, vui lòng kiểm tra lại.'
                        else:
                            task_name = COMMANDS[command]['task']
                            url = "http://127.0.0.1:8000/home/chatbot/handle-task/"
                            data = {
                                'task_name': task_name,
                                'channel_name': self.channel_name,
                                'args': args
                            }
                            response = requests.post(url, json=data)
                            response_message = f'Đã nhận `{message}`, đang xử lý...'

        self.send(text_data=json.dumps({
            'message': response_message
        }))

    def chat_message(self, event):
        message = json.loads(event.get('message', '{}'))
        response_messages = []
        command = message.get('command', 'unknown')

        if message.get('status') == 'success':
            data = message.get('data', {})
            if command == 'lookup':
                response_messages.append(f"Mã Khách hàng: {data.get('customer_code')}")
                response_messages.append(f"Họ và tên khách hàng: {data.get('customer_name')}")
                response_messages.append(f"Phân khúc: {data.get('customer_segment')}")
                response_messages.append("Số đơn hàng của khách: " + ', '.join(data.get('orders', [])))
            elif command == 'order':
                response_messages.append(f"Mã đơn hàng: {data.get('order_id')}")
                response_messages.append(f"Khách hàng: {data.get('customer_name')}")
                for line in data.get('orderlines', []):
                    response_messages.append(f"Sản phẩm: {line.get('product_name')}, Số lượng: {line.get('quantity')}")
            else:
                response_messages.append('Lệnh không xác định.')
        else:
            response_messages.append(message.get('message', 'Unknown error'))

        for response in response_messages:
            self.send(text_data=json.dumps({
                'message': response
            }))

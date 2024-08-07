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
        message_parts = message.split()

        response_message = 'Vui lòng nhập `help` để xem danh sách các lệnh có thể sử dụng.'

        if message_parts:
            command = message_parts[0].lower()
            if command == 'help':
                response_message = 'Các lệnh hỗ trợ:\n' + '\n'.join(
                    [f'{command} - {params["help"]}' for command, params in COMMANDS.items()])
            elif command in COMMANDS:
                required_args = COMMANDS[command]['args']
                if command == 'order':
                    # Command 'order' không có số lượng tham số cố định, cần kiểm tra số lượng cặp sản phẩm và số lượng
                    if len(message_parts[2:]) % 2 != 0:
                        response_message = 'Lệnh `order` yêu cầu các cặp mã sản phẩm và số lượng.'
                    else:
                        customer_code = message_parts[1]
                        orderlines = []
                        for i in range(2, len(message_parts), 2):
                            product_code = message_parts[i]
                            quantity = message_parts[i + 1]
                            orderlines.append({'product_code': product_code, 'quantity': quantity})

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
                    if len(message_parts[1:]) != required_args:
                        response_message = f'Lệnh `{command}` yêu cầu {required_args} tham số, vui lòng kiểm tra lại.'
                    else:
                        task_name = COMMANDS[command]['task']
                        # Gửi yêu cầu tới view để xử lý task
                        url = "http://127.0.0.1:8000/home/chatbot/handle-task/"
                        data = {
                            'task_name': task_name,
                            'channel_name': self.channel_name,
                            'args': message_parts[1:]
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
                response_messages.append(f"Mã đơn hàng: {data.get('order')}")
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

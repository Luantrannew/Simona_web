import json
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

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
        'help': 'Đặt hàng, ví dụ: `order <mã khách hàng> <mã sản phẩm> <số lượng>`.',
        'task': 'place_order'
    },
}

class ShopBotConsumer(WebsocketConsumer):
    
    def receive(self, text_data):
        print("WebSocket message received")
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        print(f"Received message: {message}")

        response_message = 'Vui lòng nhập `help` để xem danh sách các lệnh có thể sử dụng.'
        message_parts = message.split()

        if message_parts:
            command = message_parts[0].lower()
            if command == 'help':
                response_message = 'Các lệnh hỗ trợ:\n' + '\n'.join(
                    [f'{command} - {params["help"]}' for command, params in COMMANDS.items()])
            elif command in COMMANDS:
                required_args = COMMANDS[command]['args']
                if len(message_parts[1:]) != required_args:
                    response_message = f'Lệnh `{command}` yêu cầu {required_args} tham số, vui lòng kiểm tra lại.'
                else:
                    task_name = COMMANDS[command]['task']
                    # Gửi yêu cầu tới view để xử lý task
                    import requests
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

        print(f"Sent response message: {response_message}")

    def chat_message(self, event):
        print("Event received: chat_message")
        message = event.get('message')
        print(f"Message from task: {message}")
        self.send(text_data=json.dumps({
            'message': f'[Chatbot]: {message}'
        }))
        print("Sent message to WebSocket")


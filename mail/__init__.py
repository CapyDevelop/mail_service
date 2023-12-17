import os

from mail.verify import send_verify_message
import pika
import json
from dotenv import load_dotenv

load_dotenv()


def callback(ch, method, properties, body):
    message_body = body.decode('utf-8')
    data = json.loads(message_body)
    print(f" [x] Received {data}")
    send_verify_message(data["user"], data["code"])




credentials = pika.PlainCredentials(username=os.getenv("RABBITMQ_USERNAME"), password=os.getenv("RABBITMQ_PASSWORD"))
connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"), os.getenv("RABBITMQ_PORT"), credentials=credentials))
channel = connection.channel()

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit, press CTRL+C')
# Запуск бесконечного цикла для ожидания новых сообщений
channel.start_consuming()
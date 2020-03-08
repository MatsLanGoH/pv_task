"""
PV Simulator
"""
import time

import pika


class BrokerReceiver:
    def __init__(self, broker_host: str, queue: str):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(broker_host)
        )
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=queue, durable=True)


def callback(ch, method, properties, body):
    print(f" [x] Received {body} watt.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    QUEUE = "task_queue"
    BROKER_HOST = "broker"
    receiver = BrokerReceiver(broker_host=BROKER_HOST, queue=QUEUE)
    receiver.channel.basic_qos(prefetch_count=1)
    receiver.channel.basic_consume(queue=QUEUE, on_message_callback=callback)
    try:
        print("PV Simulator...")
        receiver.channel.start_consuming()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

"""
Meter simulator
"""
import random

import time
import pika


class BrokerSender:
    def __init__(self, broker_host: str, queue: str):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(broker_host)
        )
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=queue, durable=True)


class Meter:
    @staticmethod
    def generate_value():
        return random.randint(0, 9000)


def main():
    QUEUE = "task_queue"
    BROKER_HOST = "broker"
    sender = BrokerSender(broker_host=BROKER_HOST, queue=QUEUE)
    meter = Meter()
    try:
        while True:
            msg = str(meter.generate_value())
            sender.channel.basic_publish(
                exchange="",
                routing_key=QUEUE,
                body=msg,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            print(f" [x] Sent {msg} watts.")
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

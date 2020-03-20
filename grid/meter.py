"""
Meter simulator
"""
import random
import time

import pika
from retry import retry

from message_broker.connection import ConnectionManager


class Meter:
    def __init__(self, broker_host: str, queue: str) -> None:
        self.broker_host = broker_host
        self.queue = queue

    def start(self) -> None:
        conn_manager = ConnectionManager(broker_host=self.broker_host, queue=self.queue)
        channel = conn_manager.start_channel()
        try:
            # TODO: Consider abstracting this so Meter doesn't have to worry about pika implementation details
            while True:
                msg = str(self.generate_value())
                channel.basic_publish(
                    exchange="",
                    routing_key=self.queue,
                    body=msg,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
                print(f" [x] Meter: {msg} kW.")
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    @staticmethod
    def generate_value() -> int:
        return random.randint(0, 9000)

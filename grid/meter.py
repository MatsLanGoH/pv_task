"""
Meter simulator
"""
import random
import time

import pika

from message_broker.connection import ConnectionManager


class Meter:
    def __init__(self, broker_host: str, queue: str) -> None:
        self.broker_host = broker_host
        self.queue = queue
        self.consumption = 0

    def start(self) -> None:
        conn_manager = ConnectionManager(broker_host=self.broker_host, queue=self.queue)
        channel = conn_manager.start_channel()
        try:
            while True:
                self.generate_consumption()
                msg = str(self.consumption)
                conn_manager.publish_message(channel, msg=msg)
                print(f" [x] Meter: {msg} kW.")
                time.sleep(5)
        except KeyboardInterrupt:
            pass

    def generate_consumption(self) -> int:
        last_consumption = self.consumption
        next_limit = min(
            max(0, random.choice([last_consumption + 500, last_consumption - 500])),
            9000,
        )
        next_range = (last_consumption, next_limit)

        self.consumption = random.randint(min(next_range), max(next_range))

"""
Meter simulator
"""
import random
import time
from datetime import datetime

from message_broker.connection import ConnectionManager
from grid.config import (
    INTERVAL_SECONDS,
    MIN_CONSUMPTION_KW,
    MAX_CONSUMPTION_KW,
)


class Meter:
    def __init__(self, broker_host: str, queue: str) -> None:
        self.broker_host = broker_host
        self.queue = queue
        self.consumption = random.randint(MIN_CONSUMPTION_KW, MAX_CONSUMPTION_KW)

    def start(self) -> None:
        """Starts a regular meter.
        This generates a consumption value and sends it to the message queue.
        The process is repeated every N seconds until the program is interrupted manually.
        """

        conn_manager = ConnectionManager(broker_host=self.broker_host, queue=self.queue)
        channel = conn_manager.start_channel()
        try:
            print("Starting regular meter...")
            while True:
                self.generate_consumption()
                msg = str(self.consumption)
                conn_manager.publish_message(channel, msg=msg)
                print(f" [x] Meter: {msg} kW.")
                time.sleep(INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("Exiting...")
            pass

    def start_timelapse(self) -> None:
        """Starts a timelapse.
        This simulates a series of generated power consumption values.
        Values are generated for a 24-hour span, with 5 minute intervals.
        """
        conn_manager = ConnectionManager(broker_host=self.broker_host, queue=self.queue)
        channel = conn_manager.start_channel()
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        print("Starting timelapse...")
        for h in range(0, 24):
            for m in range(0, 60, 5):
                dt = current_date.replace(hour=h, minute=m)
                timestamp = int(time.mktime(dt.timetuple()))

                self.generate_consumption()
                msg = str(self.consumption)
                conn_manager.publish_message(channel, msg=msg, timestamp=timestamp)
                print(f" [x] Timestamp: {dt}\tMeter: {msg} kW.")
        print("Exiting...")

    def generate_consumption(self) -> int:
        """Generates a pseudo-random consumption value.
        This uses the last produced value as a base value to ensure that 
        the next value is within a certain distance of the previous value.
        """
        last_consumption = self.consumption
        next_limit = min(
            max(MIN_CONSUMPTION_KW, random.choice([last_consumption + 500, last_consumption - 500])),
            MAX_CONSUMPTION_KW,
        )
        next_range = (last_consumption, next_limit)

        self.consumption = random.randint(min(next_range), max(next_range))

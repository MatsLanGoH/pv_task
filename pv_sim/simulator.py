"""
PV Simulator
"""
import csv
from dataclasses import asdict, dataclass
from datetime import datetime
from pprint import pprint
import pathlib
import time

import pika

from message_broker.connection import ConnectionManager


@dataclass
class PVMeterReportItem:
    """Class for keeping track of a PV Meter reading.
    """

    timestamp: str
    pv_meter: int
    pv_photovoltaic: int

    def pv_total_meter_photovoltaic(self) -> int:
        return self.pv_meter + self.pv_photovoltaic


def generate_report(report_item: PVMeterReportItem) -> None:
    """
    NOTE: 
    We want the result to be saved 
    - [x] in a file with 
    - [ ] timestamped filename
    at least 
    - [x] a timestamp
    - [x] meter power value
    - [x] PV power value
    - [x] the sum of the powers (meter power and pv power value)
    """
    with open("/results/output.csv", "a") as csvfile:
        fieldnames = [
            "timestamp",
            "pv_meter",
            "pv_photovoltaic",
            "pv_total_meter_photovoltaic",
        ]
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        report_dict = asdict(report_item)
        report_dict[
            "pv_total_meter_photovoltaic"
        ] = report_item.pv_total_meter_photovoltaic()
        csvwriter.writerow(report_dict)


def get_current_timestamp():
    current_time = datetime.now()
    return current_time.isoformat()


class PVSimulator:
    def __init__(self, broker_host: str, queue: str) -> None:
        self.broker_host = broker_host
        self.queue = queue

    def start(self) -> None:
        conn_manager = ConnectionManager(broker_host=self.broker_host, queue=self.queue)
        channel = conn_manager.start_channel()
        channel.basic_consume(queue=self.queue, on_message_callback=self.callback)

        try:
            print("PV Simulator...")
            channel.start_consuming()
        except KeyboardInterrupt:
            pass

    @staticmethod
    def callback(ch, method, properties, body):
        print(f" [x] Received {str(body)} kW.")

        report_item = PVMeterReportItem(
            timestamp=get_current_timestamp(), pv_meter=int(body), pv_photovoltaic=0,
        )
        generate_report(report_item)

        ch.basic_ack(delivery_tag=method.delivery_tag)

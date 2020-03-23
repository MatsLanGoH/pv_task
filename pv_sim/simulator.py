"""
PV Simulator
"""
import csv
import pathlib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from suntime import Sun

from message_broker.connection import ConnectionManager
from pv_sim.config import LATITUDE, LONGITUDE, PV_MAX_TOTAL_OUTPUT_KW


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
    date_string = report_item.timestamp.split("T")[0]
    filename = pathlib.Path("/results", f"{date_string}.csv")
    with open(filename, "a") as csvfile:
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
        print(report_dict)
        csvwriter.writerow(report_dict)


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

        try:
            timestamp = properties.timestamp
            current_time = datetime.utcfromtimestamp(timestamp).replace(
                tzinfo=timezone.utc
            )
        except AttributeError:
            current_time = datetime.now().replace(tzinfo=timezone.utc)

        pv_photovoltaic = generate_pv_output(current_time)

        report_item = PVMeterReportItem(
            timestamp=current_time.isoformat(),
            pv_meter=int(body),
            pv_photovoltaic=pv_photovoltaic,
        )
        generate_report(report_item)

        ch.basic_ack(delivery_tag=method.delivery_tag)


def is_sunny(dt: datetime, sunrise: datetime, sunset: datetime) -> bool:
    return sunrise <= dt <= sunset


def calculate_pv_output(dt: datetime, sunrise: datetime, sunset: datetime) -> int:
    distance_to_zenith = (sunset - sunrise) / 2
    zenith = sunrise + distance_to_zenith
    dist_to_zenith_seconds = distance_to_zenith.total_seconds()

    zenith_percentage = abs(zenith - dt).total_seconds() / dist_to_zenith_seconds

    sun_intensity = zenith_percentage ** 2
    output = PV_MAX_TOTAL_OUTPUT_KW - (PV_MAX_TOTAL_OUTPUT_KW * sun_intensity)

    return int(output)


def generate_pv_output(dt: datetime) -> int:
    sun = Sun(LATITUDE, LONGITUDE)

    sunrise = sun.get_sunrise_time()
    sunset = sun.get_sunset_time()

    if not is_sunny(dt, sunrise, sunset):
        return 0

    return calculate_pv_output(dt, sunrise, sunset)

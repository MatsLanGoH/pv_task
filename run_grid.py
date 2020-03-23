import fire

from grid.meter import Meter


def main(timelapse: bool = False):
    meter = Meter(broker_host="broker", queue="task_queue")
    if timelapse:
        meter.start_timelapse()
    else:
        meter.start()


if __name__ == "__main__":
    fire.Fire(main)

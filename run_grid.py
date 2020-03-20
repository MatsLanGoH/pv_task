from grid.meter import Meter


if __name__ == "__main__":
    meter = Meter(broker_host="broker", queue="task_queue")
    meter.start()

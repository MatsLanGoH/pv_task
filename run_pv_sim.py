from pv_sim.simulator import PVSimulator


if __name__ == "__main__":
    pv_sim = PVSimulator(broker_host="broker", queue="task_queue")
    pv_sim.start()

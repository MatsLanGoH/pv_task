# PV Simulator

## How to run

- Prerequisites: A working `docker` / `docker-compose` installation.
- Clone this repository and run the following commands from inside the directory.

## Standard execution (live simulation)

This starts a continuous meter/PV simulation. The services run until halted manually by the user.

1. Build the images using `$ docker-compose build`
1. Run the services with `$ docker-compose up -d`
1. The calculated results can be shown using `$ tail -f results/YYYY-DD-MM.csv`
1. The services can be inspected using `$docker-compose logs [pv_sim|grid]`
1. To stop the services, use `$ docker-compose down`
1. Execution parameters can be changed in each modules `config.py` file.

## Timelapse execution

This generates a simulation of values for 24 hours with 5 minute intervals.

1. Uncomment the `#TIMELAPSE=True` line in `grid.env`, then restart the services using the same steps as in `Standard execution`.

NOTE: This implementaiton uses the same naming scheme for the CSV file, so if you test both `live` and `timelapse` simulations it's probably best to delete the ouput files inbetween.

## Notes

- The Meter and PV generation logic probably won't hold up in the real-world. Both methods are designed to be `replaceable`, so that we can swap them out with real-world generated values - or possibly data we get from live sensor interfaces.
- No tests yet - `pytest` with `tox`, hooked up to a CI would be nice to have :)
- Usually I don't push directly to `master`, but use tickets/issues and feature branches...

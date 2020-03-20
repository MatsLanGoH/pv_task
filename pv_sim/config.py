"""
Configuration options for PV simulator.
"""

# Solar panel configuration
PV_MAX_PANEL_OUTPUT_KW = 320
PV_NUM_PANELS = 10
PV_MAX_TOTAL_OUTPUT_KW = PV_MAX_PANEL_OUTPUT_KW * PV_NUM_PANELS

# Set location to calculate sunrise/sunset
LATITUDE, LONGITUDE = (48.1351, 11.5820)  # Munich, Germany

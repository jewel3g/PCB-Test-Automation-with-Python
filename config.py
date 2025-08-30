# config.py
# GPIO pins for relays controlling each PCB test point
RELAY_PINS = [17, 18, 27, 22, 23]  # BCM numbering
# GPIO pins for digital inputs (if any)
DIGITAL_PINS = [5, 6, 13, 19, 26]

# Sensor limits (min, max) for pass/fail
SENSOR_LIMITS = [
    (0, 100),
    (0, 200),
    (0, 500),
    (0, 1000),
    (0, 1500)
]

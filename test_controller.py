import time
import csv
import random  # for simulation, remove for real hardware
# import RPi.GPIO as GPIO  # Uncomment for Raspberry Pi

from config import RELAY_PINS, SENSOR_LIMITS

CSV_LOG_FILE = "logs/pcb_test_results.csv"

def setup_gpio():
    # GPIO.setmode(GPIO.BCM)
    # for pin in RELAY_PINS:
    #     GPIO.setup(pin, GPIO.OUT)
    pass  # simulation

def measure_sensor(index):
    """Simulate analog/digital measurement"""
    # Replace with actual reading code
    value = random.uniform(SENSOR_LIMITS[index][0]-20, SENSOR_LIMITS[index][1]+20)
    return round(value, 2)

def test_point(index):
    """Activate relay, measure sensor, return value and pass/fail"""
    # GPIO.output(RELAY_PINS[index], GPIO.HIGH)
    time.sleep(0.2)  # wait for stabilization
    value = measure_sensor(index)
    low, high = SENSOR_LIMITS[index]
    passed = low <= value <= high
    # GPIO.output(RELAY_PINS[index], GPIO.LOW)
    return value, passed

def run_full_test():
    setup_gpio()
    results = []
    overall_pass = True
    for i in range(len(RELAY_PINS)):
        val, passed = test_point(i)
        overall_pass = overall_pass and passed
        results.append((i+1, val, "PASS" if passed else "FAIL"))
    log_results(results, overall_pass)
    return results, overall_pass

def log_results(results, overall_pass):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        row = [timestamp] + [val for _, val, _ in results] + ["PASS" if overall_pass else "FAIL"]
        writer.writerow(row)

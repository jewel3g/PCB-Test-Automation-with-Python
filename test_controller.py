import spidev
import RPi.GPIO as GPIO
import time
import csv
from config import RELAY_PINS, DIGITAL_PINS, ADC_CHANNELS, VREF

# SPI setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
for pin in DIGITAL_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# CSV log file
LOG_FILE = "logs/pcb_test_results.csv"

# Read analog channel
def read_adc(channel):
    adc = spi.xfer2([1, (8+channel)<<4, 0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

# Convert ADC to voltage
def adc_to_voltage(adc_val):
    return round((adc_val * VREF)/1023, 2)

# Test a single point
def test_point(relay_pin, digital_pin, adc_channel, min_v=0.0, max_v=3.3):
    GPIO.output(relay_pin, GPIO.HIGH)
    time.sleep(0.5)
    digital_status = GPIO.input(digital_pin)
    voltage = adc_to_voltage(read_adc(adc_channel))
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    result = "PASS" if min_v <= voltage <= max_v and digital_status==1 else "FAIL"

    # Log results
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([relay_pin, digital_pin, adc_channel, digital_status, voltage, result, timestamp])
    
    GPIO.output(relay_pin, GPIO.LOW)
    return {"relay": relay_pin, "digital": digital_status, "voltage": voltage, "result": result, "time": timestamp}

# Run full test sequence
def run_full_test():
    results = []
    for i in range(len(RELAY_PINS)):
        res = test_point(RELAY_PINS[i], DIGITAL_PINS[i%len(DIGITAL_PINS)], ADC_CHANNELS[i%len(ADC_CHANNELS)])
        results.append(res)
    return results

# Cleanup
def cleanup():
    GPIO.cleanup()
    spi.close()

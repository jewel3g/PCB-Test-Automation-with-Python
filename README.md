PCB Test Automation with Raspberry Pi & Python

A full-featured PCB test automation system built with Python and Raspberry Pi, designed for electronics engineers and test engineers. This project allows automated testing of PCB test points, including digital and analog measurements, pass/fail evaluation, relay-controlled switching, and a web-based dashboard for real-time monitoring.

Features

Sequential testing of PCB test points using relays.

Analog voltage measurements via MCP3008 ADC.

Digital continuity testing using GPIO pins.

Automated pass/fail evaluation for each test point.

Web dashboard built with Flask to display live test results.

CSV logging for documentation and traceability.

Modular design for easy expansion: HiL testing, additional sensors, or IoT integration.

Hardware Requirements

Raspberry Pi (any model with GPIO and SPI)

MCP3008 ADC (for analog measurements)

Relay module for switching test points

PCB or test board with accessible test points

Jumper wires and breadboard (for prototyping)

Software Requirements

Python 3.x

Flask (pip install flask)

RPi.GPIO (pip install RPi.GPIO)

spidev (pip install spidev)

Directory Structure
pcb_test_automation/
│
├── app.py                # Web dashboard and test controller
├── test_controller.py    # Core test routines
├── config.py             # Hardware configuration
├── templates/
│   └── dashboard.html    # Web dashboard template
├── static/
│   └── style.css         # Optional styling
└── logs/
    └── pcb_test_results.csv  # Test results log


Clone the repository:

git clone https://github.com/yourusername/pcb_test_automation.git
cd pcb_test_automation


Install required Python packages:

pip install flask RPi.GPIO spidev


Connect hardware:

Wire MCP3008 to Raspberry Pi SPI pins.

Connect relay module to GPIO pins as defined in config.py.

Connect digital test points to GPIO inputs.

Run the web dashboard:

python3 app.py


Access dashboard:
Open a browser and go to http://<raspberry_pi_ip>:5000 to view test results in real-time.

Usage

Each test point is automatically switched using relays.

Analog and digital measurements are taken and evaluated against pass/fail criteria.

Results are logged in logs/pcb_test_results.csv.

To clean up GPIO and SPI after testing:

http://<raspberry_pi_ip>:5000/cleanup

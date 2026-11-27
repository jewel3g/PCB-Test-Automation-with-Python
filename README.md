# ⚡ PCB Test Automation with Raspberry Pi & Python  

> 🛠️ A full-featured **PCB test automation system** built with Python and Raspberry Pi, designed for electronics engineers and test engineers.  
> This project enables **automated testing of PCB test points**, including **digital/analog measurements**, **pass/fail evaluation**, **relay-controlled switching**, and a **web-based dashboard** for real-time monitoring.  

---

## ✨ Features  

✅ **Sequential PCB testing** using relay switching  
✅ **Analog voltage measurements** via MCP3008 ADC  
✅ **Digital continuity testing** using GPIO pins  
✅ **Automated pass/fail evaluation** for each test point  
✅ **Web dashboard (Flask)** for live monitoring  
✅ **CSV logging** for traceability and documentation  
✅ **Modular design** – extend with HiL testing, sensors, or IoT integration  

---
![PCB Test Dashboard](Screenshot%202025-08-30%20034800.png)

## 🖼️ System Overview  

```
Raspberry Pi  ──>  UART ──> PCB Test Points
       │
       ├── MCP3008 (ADC) ──> Analog Measurements
       ├── GPIO ──────────> Digital Continuity Tests
       │
   Flask Web App ──> Dashboard + Logging
```

---

## 🔧 Hardware Requirements  

- Raspberry Pi (any model with GPIO + SPI)  
- MCP3008 ADC (for analog input)  
- Relay module (to switch test points)  
- PCB or test board with accessible test pads  
- Jumper wires & breadboard (for prototyping)  

---

## 💻 Software Requirements  

- Python **3.x**  
- [Flask](https://flask.palletsprojects.com/) → `pip install flask`  
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) → `pip install RPi.GPIO`  
- [spidev](https://pypi.org/project/spidev/) → `pip install spidev`  

---

## 📂 Directory Structure  

```
pcb_test_automation/
│
├── app.py                # Web dashboard + test controller
├── test_controller.py    # Core test routines
├── config.py             # Hardware pin mapping + test configs
│
├── templates/
│   └── dashboard.html    # Web UI for results
│
├── static/
│   └── style.css         # Dashboard styling
│
└── logs/
    └── pcb_test_results.csv  # Test results log
```

---

## 🚀 Getting Started  

### 1️⃣ Clone Repository  
```bash
git clone https://github.com/jewel3g/PCB-Test-Automation-with-Python.git
cd PCB-Test-Automation-with-Python
```

### 2️⃣ Install Dependencies  
```bash
pip install flask RPi.GPIO spidev
```

### 3️⃣ Connect Hardware  
- Wire **MCP3008** to Raspberry Pi SPI pins  
- Connect **relay module** to GPIO (see `config.py`)  
- Connect **PCB test points** to relay outputs + GPIO inputs  

### 4️⃣ Run the App  
```bash
python3 app.py
```

### 5️⃣ Open Dashboard  
Navigate to:  
👉 `http://<raspberry_pi_ip>:5000`  

Live test results will appear in real-time.  

---

## ⚙️ Usage  

- Each test point is **sequentially switched** using relays  
- **Analog & digital values** are measured  
- Results are evaluated **against pass/fail thresholds**  
- Test outcomes are **logged to CSV** (`logs/pcb_test_results.csv`)  

👉 To **clean up GPIO & SPI after testing**:  
```
http://<raspberry_pi_ip>:5000/cleanup
```

---

## 📊 Example Dashboard  

✅ **Real-time PCB test results**  
✅ **Pass/Fail indicators**  
✅ **Traceable CSV logging**  

*(Add a screenshot here when available)*  

---

## 🤝 Contributing  

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to add.  

---

## 📜 License  

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  

---

⚡ Happy Testing! Automate your PCB validation workflow with Raspberry Pi & Python 🚀

## Engineering context and validation

Verify ADC calibration, fixture voltage limits, relay isolation and measurement repeatability.

[Engineering portfolio](https://jewel3g.github.io). Production readiness is not independently verified.

## Verification and fixture engineering

| Test category | Acceptance evidence |
|---|---|
| Analog measurement | Known reference voltages, ADC calibration, uncertainty budget |
| Relay switching | Break-before-make behavior, settling time and safe startup state |
| Digital measurement | Voltage compatibility and known open/short fixture cases |
| Logging | DUT serial number, fixture revision, software commit and timestamp |

Recommended evolution: isolate hardware access behind a testable interface, store limits in versioned configuration, add simulated fixtures for CI, and ensure outputs return to a safe state on timeout or exception. Do not connect energized DUT nodes directly to GPIO or ADC inputs without suitable protection and scaling.

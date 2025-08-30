import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import random

# Optional: uncomment if using real serial data
# import serial

# ============================
# Serial / Dummy Config
# ============================
SERIAL_PORT = "/dev/ttyAMA0"  # Change to /dev/ttyUSB0 if needed
BAUD_RATE = 9600
use_dummy = True  # True = simulate data, False = use real UART

# Test limits (min, max) for each sensor
SENSOR_LIMITS = [
    (0, 100),   # Sensor 1
    (0, 200),   # Sensor 2
    (0, 500),   # Sensor 3
    (0, 1000),  # Sensor 4
    (0, 1500)   # Sensor 5
]

# Global variables
ser = None
running = False
thread = None

# ============================
# Serial / Dummy Reader
# ============================
def read_serial():
    global running
    while running:
        try:
            if use_dummy:
                # Generate dummy sensor values
                dummy_values = [
                    round(random.uniform(0, 120), 2),
                    round(random.uniform(150, 250), 2),
                    round(random.uniform(400, 600), 2),
                    round(random.uniform(900, 1100), 2),
                    round(random.uniform(1400, 1600), 2),
                ]
                line = ",".join(map(str, dummy_values))

                # Insert raw data into text box
                text_box.after(0, lambda l=line: text_box.insert(tk.END, l + "\n"))
                text_box.after(0, lambda: text_box.see(tk.END))

                # Process data for sensor labels & pass/fail
                process_data(line)

                time.sleep(2)  # slow enough to read updates
            else:
                if ser and ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        text_box.after(0, lambda l=line: text_box.insert(tk.END, l + "\n"))
                        text_box.after(0, lambda: text_box.see(tk.END))
                        process_data(line)
        except Exception as e:
            process_data(f"[ERROR] {e}")
            time.sleep(0.5)

# ============================
# Process Data
# ============================
def process_data(msg):
    if "," in msg:
        try:
            values = msg.split(",")
            overall_pass = True
            for i, val in enumerate(values):
                if i < len(sensor_labels):
                    try:
                        v = float(val)
                        low, high = SENSOR_LIMITS[i]
                        if low <= v <= high:
                            color = "green"
                            status = "PASS"
                        else:
                            color = "red"
                            status = "FAIL"
                            overall_pass = False
                        sensor_labels[i].after(
                            0,
                            lambda v=v, idx=i, c=color, s=status:
                            sensor_labels[idx].config(
                                text=f"Sensor {idx+1}: {v:.2f} ({s})",
                                foreground=c
                            )
                        )
                    except ValueError:
                        sensor_labels[i].after(
                            0, lambda idx=i:
                            sensor_labels[idx].config(text=f"Sensor {idx+1}: ERROR", foreground="red")
                        )
                        overall_pass = False
            # Update status bar
            status_bar.after(
                0,
                lambda: status_bar.config(
                    text="✅ TEST PASSED" if overall_pass else "❌ TEST FAILED",
                    foreground="green" if overall_pass else "red"
                )
            )
        except Exception as e:
            text_box.after(0, lambda: text_box.insert(tk.END, f"[ERROR] Parsing data: {e}\n"))

# ============================
# Start / Stop
# ============================
def start_serial():
    global running, ser, thread
    try:
        if not use_dummy:
            # Uncomment for real UART
            # ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            pass
        running = True
        thread = threading.Thread(target=read_serial)
        thread.daemon = True
        thread.start()
        start_btn.config(state=tk.DISABLED)
        stop_btn.config(state=tk.NORMAL)
        status_bar.config(text="Connected, waiting for data...", foreground="black")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open serial port: {e}")

def stop_serial():
    global running, ser
    running = False
    if thread:
        thread.join(timeout=1.0)
    if ser and ser.is_open:
        ser.close()
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)
    status_bar.config(text="Not connected", foreground="black")

def reset_sensors():
    text_box.delete(1.0, tk.END)
    for i, lbl in enumerate(sensor_labels):
        lbl.config(text=f"Sensor {i+1}: 0.00 (PASS)", foreground="green")
    status_bar.config(text="Reset to default", foreground="black")

def on_closing():
    stop_serial()
    root.destroy()

# ============================
# GUI Setup
# ============================
root = tk.Tk()
root.title("PCB Tester GUI")
root.geometry("700x500")
root.protocol("WM_DELETE_WINDOW", on_closing)

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(frame, text="PCB Sensor Readings", font=("Arial", 14, "bold"))
title_label.pack(pady=5)

sensor_frame = ttk.LabelFrame(frame, text="Sensor Values", padding=10)
sensor_frame.pack(fill=tk.X, pady=5)

sensor_labels = []
for i in range(5):
    lbl = ttk.Label(sensor_frame, text=f"Sensor {i+1}: 0.00 (PASS)", font=("Arial", 10), foreground="green")
    lbl.pack(anchor="w", pady=2)
    sensor_labels.append(lbl)

text_frame = ttk.LabelFrame(frame, text="Raw Serial Data", padding=5)
text_frame.pack(fill=tk.BOTH, expand=True, pady=5)

text_box = scrolledtext.ScrolledText(text_frame, height=15, width=80, font=("Consolas", 9))
text_box.pack(fill=tk.BOTH, expand=True)

btn_frame = ttk.Frame(frame)
btn_frame.pack(pady=10)

start_btn = ttk.Button(btn_frame, text="Start Reading", command=start_serial)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = ttk.Button(btn_frame, text="Stop Reading", command=stop_serial, state=tk.DISABLED)
stop_btn.grid(row=0, column=1, padx=5)

clear_btn = ttk.Button(btn_frame, text="Clear Data", command=reset_sensors)
clear_btn.grid(row=0, column=2, padx=5)

quit_btn = ttk.Button(btn_frame, text="Quit", command=on_closing)
quit_btn.grid(row=0, column=3, padx=5)

status_bar = ttk.Label(root, text="Not connected", relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)
test_btn = ttk.Button(btn_frame, text="Run Full Test", command=run_test_automation)
test_btn.grid(row=0, column=4, padx=5)
root.mainloop()

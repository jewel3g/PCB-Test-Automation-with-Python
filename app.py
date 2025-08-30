from test_controller import run_full_test

def run_test_automation():
    results, overall = run_full_test()
    text_box.insert(tk.END, "=== Running Full PCB Test ===\n")
    for idx, val, status in results:
        text_box.insert(tk.END, f"Sensor {idx}: {val:.2f} ({status})\n")
        sensor_labels[idx-1].config(text=f"Sensor {idx}: {val:.2f} ({status})",
                                     foreground="green" if status=="PASS" else "red")
    status_bar.config(text="✅ TEST PASSED" if overall else "❌ TEST FAILED",
                      foreground="green" if overall else "red")
    text_box.see(tk.END)

import tkinter as tk
import subprocess

root = tk.Tk()

root.title("Appartment Management System")
root.geometry("400x300")

flats_process = None
om_process = None

def open_flats():
    global flats_process
    if flats_process is None or flats_process.poll() is not None:
       flats_process = subprocess.Popen(["python", "flats.py"])

def open_om():
    global om_process
    if om_process is None or om_process.poll() is not None:
       om_process = subprocess.Popen(["python", "om.py"])

def on_close():
    if flats_process and flats_process.poll() is None:
        flats_process.terminate()
    
    if om_process and om_process.poll() is None:
        om_process.terminate()
    
    root.destroy()

tk.Button(root, text="Flats Details", width=20, command=open_flats).pack(pady=20)

tk.Button(root, text="O&M charges", width=20, command=open_om).pack(pady=20)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
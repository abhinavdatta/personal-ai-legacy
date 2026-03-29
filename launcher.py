import webview
import subprocess
import time
import requests
import sys
import os
import socket
import tkinter as tk
from tkinter import messagebox

# ==================================================
# CONFIG
# ==================================================
OLLAMA_PORT = 11434
STREAMLIT_PORT = 8501

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OLLAMA_PATHS = [
    r"C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama.exe",
    r"C:\Program Files\Ollama\ollama.exe",
]

# ==================================================
# UTILS
# ==================================================
def expand(path):
    return os.path.expandvars(path)


def find_ollama():
    for p in OLLAMA_PATHS:
        full = expand(p)
        if os.path.exists(full):
            return full
    return None


def port_open(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except:
        return False


# ==================================================
# OLLAMA CONTROL
# ==================================================
def start_ollama():
    ollama_exe = find_ollama()
    if not ollama_exe:
        return False

    subprocess.Popen(
        [ollama_exe, "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    return True


# ==================================================
# STREAMLIT CONTROL
# ==================================================
def wait_for_streamlit():
    for _ in range(20):
        try:
            requests.get(f"http://localhost:{STREAMLIT_PORT}", timeout=1)
            return True
        except:
            time.sleep(1)
    return False


# ==================================================
# MAIN
# ==================================================

# ---- Ensure Ollama ----
if not port_open(OLLAMA_PORT):
    if not start_ollama():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Ollama Not Found",
            "Ollama is required to run Study AI.\n\n"
            "Please install it from:\nhttps://ollama.com"
        )
        sys.exit(1)

    # wait for ollama
    for _ in range(15):
        if port_open(OLLAMA_PORT):
            break
        time.sleep(1)

# ---- Start Streamlit with SAME Python ----
process = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py",
        "--server.headless=true",
        "--server.port=8501",
        "--browser.gatherUsageStats=false"
    ],
    cwd=BASE_DIR,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW
)

if not wait_for_streamlit():
    messagebox.showerror(
        "Startup Error",
        "Failed to start the Study AI interface."
    )
    process.terminate()
    sys.exit(1)

# ---- Native Window ----
webview.create_window(
    "Study AI",
    f"http://localhost:{STREAMLIT_PORT}",
    width=1200,
    height=800,
    resizable=True
)

webview.start()

# ---- Clean shutdown ----
process.terminate()

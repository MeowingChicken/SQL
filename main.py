import tkinter as tk
from tkinter import messagebox, ttk
import requests
from multiprocessing import Process
from flask import Flask, request, jsonify
import sqlite3
import time

# -----------------------------
# Flask API
# -----------------------------
API_HOST = "127.0.0.1"
API_PORT = 5000
DB_FILE = "user_database.db"

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users (Username, Password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Registration successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE Username=? AND Password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

def run_api():
    init_db()
    print(f"🚀 API server running at http://{API_HOST}:{API_PORT}")
    app.run(debug=False, host=API_HOST, port=API_PORT)

# -----------------------------
# Tkinter GUI
# -----------------------------
API_URL = f"http://{API_HOST}:{API_PORT}"

def create_main_app_gui(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Quadruple View GUI")
    root.geometry("1920x1080")

    for r in range(2):
        root.grid_rowconfigure(r, weight=1, uniform="row")
    for c in range(2):
        root.grid_columnconfigure(c, weight=1, uniform="col")

    frame_tl = ttk.Frame(root, relief="solid", borderwidth=1)
    frame_tl.grid(row=0, column=0, sticky="nsew")
    label_video1 = tk.Label(frame_tl, text="Video Stream Placeholder 1", anchor="center")
    label_video1.pack(expand=True, fill="both")

    frame_tr = ttk.Frame(root, relief="solid", borderwidth=1)
    frame_tr.grid(row=0, column=1, sticky="nsew")

    control_frame = ttk.Frame(frame_tr)
    control_frame.pack(expand=True, fill="both")

    for i in range(3):
        control_frame.grid_columnconfigure(i, weight=1)
    for i in range(4):
        control_frame.grid_rowconfigure(i, weight=1)

    ttk.Button(control_frame, text="\u2191").grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(control_frame, text="\u2190").grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(control_frame, text="\u2192").grid(row=1, column=2, padx=5, pady=5)
    ttk.Button(control_frame, text="\u25A0").grid(row=2, column=1, padx=5, pady=5)
    ttk.Button(control_frame, text="\u25B6").grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(control_frame, text="\u2193").grid(row=3, column=1, padx=5, pady=5)

    frame_bl = ttk.Frame(root, relief="solid", borderwidth=1)
    frame_bl.grid(row=1, column=0, sticky="nsew")
    label_video2 = tk.Label(frame_bl, text="Video Stream Placeholder 2", anchor="center")
    label_video2.pack(expand=True, fill="both")

    frame_br = ttk.Frame(root, relief="solid", borderwidth=1)
    frame_br.grid(row=1, column=1, sticky="nsew")
    log_text = tk.Text(frame_br, wrap="word")
    log_text.pack(expand=True, fill="both")
    log_text.insert(tk.END, "User Log:\n")

def create_login_gui(root):
    root.title("Login/Registration System")
    root.geometry("300x300")

    username_label = tk.Label(root, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    def user_login():
        username = username_entry.get()
        password = password_entry.get()
        try:
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                messagebox.showinfo("Success", response.json().get("message"))
                create_main_app_gui(root)
            else:
                messagebox.showerror("Error", response.json().get("message"))
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Cannot connect to API server.")

    def user_register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty.")
            return
        try:
            response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
            if response.status_code == 201:
                messagebox.showinfo("Success", response.json().get("message"))
            else:
                messagebox.showerror("Error", response.json().get("message"))
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Cannot connect to API server.")

    login_button = tk.Button(root, text="Login", command=user_login)
    login_button.pack(pady=5)
    register_button = tk.Button(root, text="Register", command=user_register)
    register_button.pack(pady=5)

# -----------------------------
# Run API and GUI together
# -----------------------------
def start_app():
    api_process = Process(target=run_api)
    api_process.start()
    time.sleep(1)  # small delay to let API start
    root = tk.Tk()
    create_login_gui(root)
    root.mainloop()
    api_process.terminate()  # stop API when GUI closes

start_app()

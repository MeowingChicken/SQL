import tkinter as tk
from tkinter import messagebox, ttk
import requests

API_URL = "http://127.0.0.1:5000"  # must match api.py

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

root = tk.Tk()
create_login_gui(root)
root.mainloop()

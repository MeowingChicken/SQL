import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def setup_database():
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, c

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

    btn_up = ttk.Button(control_frame, text="\u2191")
    btn_up.grid(row=0, column=1, padx=5, pady=5)
    btn_left = ttk.Button(control_frame, text="\u2190")
    btn_left.grid(row=1, column=0, padx=5, pady=5)
    btn_right = ttk.Button(control_frame, text="\u2192")
    btn_right.grid(row=1, column=2, padx=5, pady=5)
    btn_stop = ttk.Button(control_frame, text="\u25A0")
    btn_stop.grid(row=2, column=1, padx=5, pady=5)
    btn_play = ttk.Button(control_frame, text="\u25B6")
    btn_play.grid(row=1, column=1, padx=5, pady=5)
    btn_down = ttk.Button(control_frame, text="\u2193")
    btn_down.grid(row=3, column=1, padx=5, pady=5)

    frame_bl = ttk.Frame(root, relief="solid", borderwidth=1)
    frame_bl.grid(row=1, column=0, sticky="nsew")
    label_video2 = tk.Label(frame_bl, text="Video Stream Placeholder 2", anchor="center")
    label_video2.pack(expand=True, fill="both")

    frame_br = ttk.Frame(root, relief="solid", borderwidth=1)
    frame_br.grid(row=1, column=1, sticky="nsew")
    log_text = tk.Text(frame_br, wrap="word")
    log_text.pack(expand=True, fill="both")
    log_text.insert(tk.END, "User Log:\n")

def create_login_gui(root, conn, c):
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

        c.execute("SELECT * FROM users WHERE Username=? AND Password=?", (username, password))
        user = c.fetchone()

        if user:
            messagebox.showinfo("Success", "Login successful!")
            create_main_app_gui(root)  # Call the function to show the main app GUI
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def user_register():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty.")
            return

        try:
            c.execute("INSERT INTO users (Username, Password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")

    login_button = tk.Button(root, text="Login", command=user_login)
    login_button.pack(pady=5)

    register_button = tk.Button(root, text="Register", command=user_register)
    register_button.pack(pady=5)

root = tk.Tk()
conn, c = setup_database()

create_login_gui(root, conn, c)

root.mainloop()
conn.close()
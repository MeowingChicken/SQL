from tkinter import *
from tkinter import messagebox
import user_db
import GUI

# Main login window
app = Tk()
app.title("Robot Control Login")
app.geometry("800x600")

def register():
    """
    Register a new user.
    """
    uname = username_entry.get().strip()
    pwd = password_entry.get().strip()

    if not uname or not pwd:
        messagebox.showwarning("Error", "Both fields are required.")
        return

    if user_db.create_user(uname, pwd):
        messagebox.showinfo("Success", f"User '{uname}' created successfully.")
    else:
        messagebox.showerror("Error", "Username already exists.")

def login():
    """
    Authenticate user and open robot control GUI.
    """
    uname = username_entry.get().strip()
    pwd = password_entry.get().strip()

    if user_db.verify_user(uname, pwd):
        GUI.launch_gui(uname)
        app.withdraw()
    else:
        if messagebox.askyesno("Login Failed", "User not found. Create account?"):
            register()

# UI Elements
Label(app, text="Username:").pack(pady=10)
username_entry = Entry(app)
username_entry.pack(pady=5)

Label(app, text="Password:").pack(pady=10)
password_entry = Entry(app, show="*")
password_entry.pack(pady=5)

Button(app, text="Login", command=login).pack(pady=10)
Button(app, text="Signup", command=register).pack(pady=5)

app.mainloop()

from tkinter import *
import requests

API_ENDPOINT = "http://127.0.0.1:5000"

def launch_gui(username):
    """
    Open the robot control interface with a D-pad layout.
    Play and Stop are stacked in the center of the arrows.
    """
    win = Toplevel()
    win.title(f"Robot Controller - {username}")
    win.geometry("1200x800")

    # Grid layout for 2x2 main sections
    for i in range(2):
        win.grid_rowconfigure(i, weight=1)
        win.grid_columnconfigure(i, weight=1)

    # Frames for video, controller, and logs
    frame_video1 = Frame(win, bd=2, relief="ridge")
    frame_controller = Frame(win, bd=2, relief="ridge")
    frame_video2 = Frame(win, bd=2, relief="ridge")
    frame_log = Frame(win, bd=2, relief="ridge")

    frame_video1.grid(row=0, column=0, sticky="nsew")
    frame_controller.grid(row=0, column=1, sticky="nsew")
    frame_video2.grid(row=1, column=0, sticky="nsew")
    frame_log.grid(row=1, column=1, sticky="nsew")

    Label(frame_video1, text="Video Feed 1", font=("Helvetica", 16)).pack(pady=5)
    Label(frame_controller, text="Controls", font=("Helvetica", 16)).pack(pady=5)
    Label(frame_video2, text="Video Feed 2", font=("Helvetica", 16)).pack(pady=5)
    Label(frame_log, text="User Logs", font=("Helvetica", 16)).pack(pady=5)

    # Control frame centered inside controller frame
    control_frame = Frame(frame_controller)
    control_frame.place(relx=0.5, rely=0.5, anchor="center")

    arrow_style = ("Helvetica", 24)

    def send_command(direction):
        """
        Send movement command to the API.
        """
        requests.post(f"{API_ENDPOINT}/move/{direction}")

    # Configure 3x3 grid for D-pad
    for r in range(3):
        control_frame.grid_rowconfigure(r, weight=1)
    for c in range(3):
        control_frame.grid_columnconfigure(c, weight=1)

    # Directional arrows
    up_btn = Button(control_frame, text="↑", font=arrow_style, command=lambda: send_command("forward"))
    down_btn = Button(control_frame, text="↓", font=arrow_style, command=lambda: send_command("backward"))
    left_btn = Button(control_frame, text="←", font=arrow_style, command=lambda: send_command("left"))
    right_btn = Button(control_frame, text="→", font=arrow_style, command=lambda: send_command("right"))

    up_btn.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
    left_btn.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
    right_btn.grid(row=1, column=2, sticky="nsew", padx=2, pady=2)
    down_btn.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)

    # Center stack for Play and Stop buttons
    center_frame = Frame(control_frame)
    center_frame.grid(row=1, column=1, sticky="nsew")
    center_frame.grid_rowconfigure(0, weight=1)
    center_frame.grid_rowconfigure(1, weight=1)
    center_frame.grid_columnconfigure(0, weight=1)

    play_btn = Button(center_frame, text="Play", font=arrow_style)
    stop_btn = Button(center_frame, text="Stop", font=arrow_style)

    play_btn.grid(row=0, column=0, sticky="nsew", padx=2, pady=(0,2))
    stop_btn.grid(row=1, column=0, sticky="nsew", padx=2, pady=(2,0))




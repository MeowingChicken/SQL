import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Quadruple View GUI")
root.geometry("1920x1080")

for r in range(2):
    root.grid_rowconfigure(r, weight=1, uniform="row")
for c in range(2):
    root.grid_columnconfigure(c, weight=1, uniform="col")

# Top Left Quadrant (Video 1)
frame_tl = ttk.Frame(root, relief="solid", borderwidth=1)
frame_tl.grid(row=0, column=0, sticky="nsew")
label_video1 = tk.Label(frame_tl, text="Video Stream Placeholder 1", anchor="center")
label_video1.pack(expand=True, fill="both")

# Top Right Quadrant (Controls)
frame_tr = ttk.Frame(root, relief="solid", borderwidth=1)
frame_tr.grid(row=0, column=1, sticky="nsew")

control_frame = ttk.Frame(frame_tr)
control_frame.pack(expand=True, fill="both")

for i in range(3):
    control_frame.grid_columnconfigure(i, weight=1)
for i in range(4):
    control_frame.grid_rowconfigure(i, weight=1)

# Directional buttons
btn_up = ttk.Button(control_frame, text="\u2191")
btn_up.grid(row=0, column=1, padx=5, pady=5)

btn_left = ttk.Button(control_frame, text="\u2190")
btn_left.grid(row=1, column=0, padx=5, pady=5)

btn_right = ttk.Button(control_frame, text="\u2192")
btn_right.grid(row=1, column=2, padx=5, pady=5)

btn_stop = ttk.Button(control_frame, text="\u25A0")
btn_stop.grid(row=2, column=1, padx=5, pady=5)

# Play and Stop buttons
btn_play = ttk.Button(control_frame, text="\u25B6")
btn_play.grid(row=1, column=1, padx=5, pady=5)

btn_down = ttk.Button(control_frame, text="\u2193")
btn_down.grid(row=3, column=1, padx=5, pady=5)

# Bottom Left Quadrant (Video 2)
frame_bl = ttk.Frame(root, relief="solid", borderwidth=1)
frame_bl.grid(row=1, column=0, sticky="nsew")
label_video2 = tk.Label(frame_bl, text="Video Stream Placeholder 2", anchor="center")
label_video2.pack(expand=True, fill="both")

# Bottom Right Quadrant (User Log)
frame_br = ttk.Frame(root, relief="solid", borderwidth=1)
frame_br.grid(row=1, column=1, sticky="nsew")

log_text = tk.Text(frame_br, wrap="word")
log_text.pack(expand=True, fill="both")
log_text.insert(tk.END, "User Log:\n")

root.mainloop()
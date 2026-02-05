import tkinter as tk
from ui import build_ui
from utils import center_window

window = tk.Tk()
window.withdraw()

build_ui(window)

center_window(window)
window.deiconify()
window.mainloop()

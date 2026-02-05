import tkinter as tk

def custom_popup(parent, title, message):
    """
    Creates a modal confirmation dialog.
    Returns True if OK is clicked, otherwise False.
    """

    result = {"value": False}

    popup = tk.Toplevel(parent)
    popup.title(title)
    popup.transient(parent)
    popup.grab_set()
    popup.resizable(False, False)

    tk.Label(
        popup,
        text=message,
        justify="left",
        padx=20,
        pady=20
    ).pack()

    button_frame = tk.Frame(popup)
    button_frame.pack(pady=10)

    def on_ok():
        result["value"] = True
        popup.destroy()

    def on_cancel():
        popup.destroy()

    tk.Button(button_frame, text="OK", width=10, command=on_ok).pack(side="left", padx=5)
    tk.Button(button_frame, text="Cancel", width=10, command=on_cancel).pack(side="left", padx=5)

    # Center popup over parent
    popup.update_idletasks()
    px, py = parent.winfo_x(), parent.winfo_y()
    pw, ph = parent.winfo_width(), parent.winfo_height()
    w, h = popup.winfo_width(), popup.winfo_height()

    popup.geometry(f"{w}x{h}+{px + pw//2 - w//2}+{py + ph//2 - h//2}")

    parent.wait_window(popup)
    return result["value"]

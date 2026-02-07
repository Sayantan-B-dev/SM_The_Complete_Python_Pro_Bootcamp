import tkinter as tk
import webbrowser


class GraphView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.url = None

        self.label = tk.Label(self, text="View your Pixela graph")
        self.label.pack()

        self.btn = tk.Button(self, text="Open Graph", state="disabled", command=self.open)
        self.btn.pack()

    def set_graph_url(self, url: str):
        self.url = url
        self.btn.config(state="normal")

    def open(self):
        if self.url:
            webbrowser.open(self.url)

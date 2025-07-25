from tkinter import *
import tkinter as tk
from tkinter import ttk
from utils.flashcard_classes import FlashCardApp

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashCardApp(root)
    root.mainloop()
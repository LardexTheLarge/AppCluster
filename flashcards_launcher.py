from tkinter import *
from tkinter import ttk
from utils.flashcard_classes import FlashCardApp

# Main application
if __name__ == "__main__":
    root = Tk()
    app = FlashCardApp(root)
    root.mainloop()
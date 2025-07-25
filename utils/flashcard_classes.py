import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
import math
import json

class FlashCardApp:
    def __init__(self, root):
        s = ttk.Style()
        s.theme_use('classic')
        # winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'

        #Root
        root.minsize(800,800)
        root.title("Flash Cards")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.FLASHCARD_DIR = "flashcard_collections"

        #Main Container
        self.content = ttk.Frame(root, padding=10)
        self.content.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)

        #Title grid
        self.title_frame = ttk.Frame(self.content)
        self.title_frame.grid(row=0, sticky=(N,E,W), pady=5)
        self.title_frame.columnconfigure(0, weight=1)
        self.title_frame.columnconfigure(1, weight=1)
        self.title_frame.columnconfigure(2, weight=1)

        #Flash card collection grid
        self.collection_frame = ttk.Frame(self.content, relief="ridge", borderwidth=1)
        self.collection_frame.grid(row=1, sticky=(tk.N, tk.E, tk.W))
        self.collection_frame.columnconfigure(0, weight=1)
        self.collection_frame.rowconfigure(1, weight=2)

        self.refresh_collections()

    def refresh_collections(self):
        #Clears the existing widgets
        for w in self.collection_frame.winfo_children():
            w.destroy()

        files = self.get_flash_collection()
        names = list(files.keys())
        count = len(names)
        if count == 0:
            ttk.Label(self.collection_frame, text="No collections found.").grid()
            return
        
        #find grid dimensions
        self.cols = math.ceil(math.sqrt(count))
        self.rows = math.ceil(count / self.cols)

        #Expands the items in the grid evenly
        for c in range(self.cols):
            self.collection_frame.columnconfigure(c, weight=1)
        for r in range(self.rows):
            self.collection_frame.rowconfigure(r, weight=1)

        #put a file name in a label item
        for idx, filename in enumerate(names):
            r, c = divmod(idx, self.cols)

            lbl = ttk.Label(
                self.collection_frame,
                text=filename,
                width=20,
                relief="solid",
                borderwidth=1,
                cursor="hand2",
                wraplength=150,
                background="lightblue",
                anchor="center",
            )
            lbl.grid(row=r, column=c, padx=5, pady=5, sticky=(N,S,E,W))

            lbl.bind("<Button-1>", lambda e, fn=filename: self.open_collection(fn))

        btn_row = self.rows
        create_btn = ttk.Button(
            self.collection_frame,
            text="Create Collection",
            command="",
        )

        create_btn.grid(
            row=btn_row,
            column=0,
            columnspan=self.cols,
            pady=(5),
            sticky=(E,W)
        )


    def get_flash_collection(self):
        """Fetch flash cards collection from storage"""
        collections = {}

        # Checks for directory
        os.makedirs(self.FLASHCARD_DIR, exist_ok=True)

        for filename in os.listdir(self.FLASHCARD_DIR):
            if filename.endswith(".json"):
                path = os.path.join(self.FLASHCARD_DIR, filename)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        collection_name = os.path.splitext(filename)[0]
                        collections[collection_name] = data
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode {filename}")
        return collections
        
    # def save_flashcards(self, data, path="flashcards.json"):
    #     with open(path, "w") as file:
    #         json.dump(data, file, indent=4)

    def show_collections(self):
        """Returns to flash card collection grid"""
        #clears the widgets on the collection frame
        for widget in self.collection_frame.winfo_children():
            widget.destroy()
        self.refresh_collections()

    def open_collection(self, title):
        """Opens the collection that the user clicks on"""
        #clears the widgets on the collection frame
        for widget in self.collection_frame.winfo_children():
            widget.destroy()

        # title of the flash card using a text box
        opened_collection_title = ttk.Label(self.title_frame, text=title, anchor="center")
        opened_collection_title.grid(row=0, column=1)

        #List of flash card objects from the json file
        flashcards = self.get_card_content(title)

        #For loop that assigns a row and flashcard form the flashcards list
        for row_index, flashcard in enumerate(flashcards):
            q_lbl = ttk.Label(self.collection_frame, text=flashcard["question"])
            a_lbl = ttk.Label(self.collection_frame, text=flashcard["answer"])

            q_lbl.grid(row=row_index, column=0, sticky=(N,W), padx=5, pady=2)
            a_lbl.grid(row=row_index, column=1, sticky=(N,W), padx=5, pady=2)

        #Button to go back to flash card collections
        back_btn = ttk.Button(
            self.collection_frame,
            text = "Back",
            command=self.show_collections
        )
        back_btn.grid(pady=5, sticky=(E,W))

    def get_card_content(self, title):
        """Gets the json objects from json files in flashcard collection folder"""

        filename = f"{title}.json"
        path = os.path.join(self.FLASHCARD_DIR, filename)

        if not os.path.exists(path):
            print(f"Collection '{title}' not found.")
            return []
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    print(f"Invalid format in {filename}. Expected a list.")
                    return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {filename}: {e}")
            return []
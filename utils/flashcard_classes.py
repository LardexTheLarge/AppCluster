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
        self.content = ttk.Frame(root, padding=(5,0))
        self.content.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)

        #Title grid
        self.title_frame = ttk.Frame(self.content, relief="ridge", borderwidth=1)
        self.title_frame.grid(row=0, sticky=(N,E,W), pady=5)
        self.title_frame.columnconfigure(0, weight=1)
        self.title_frame.columnconfigure(1, weight=1)
        self.title_frame.columnconfigure(2, weight=1)

        #Frame that will hold the single card's study material
        self.card_frame = ttk.Frame(self.content, relief="groove", borderwidth=2)
        self.card_frame.grid(row=1, column=0, sticky=(N,S,W,E))
        self.card_frame.columnconfigure(0, weight=1)
        self.card_frame.columnconfigure(1, weight=1)
        self.card_frame.columnconfigure(2, weight=1)

        self.card_frame.rowconfigure(0, weight=1)
        self.card_frame.rowconfigure(1, weight=1)
        self.card_frame.rowconfigure(2, weight=1)

        #Flash card collection grid
        self.collection_frame = ttk.Frame(self.content, relief="sunken", borderwidth=10)
        self.collection_frame.grid(row=1, column=0, sticky=(tk.N, tk.E, tk.W))
        self.collection_frame.columnconfigure(0, weight=1)
        self.collection_frame.rowconfigure(1, weight=2)

        #Buttons grid
        self.btn_frame = ttk.Frame(self.content)
        self.btn_frame.grid(row=2, sticky=(S,E,W))
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.rowconfigure(2, weight=1)

        self.refresh_collections()

    def refresh_collections(self):
        #Clears the existing widgets
        self.wipe_ui()

        #Brings back the grid after it's forgotten
        self.collection_frame.grid(row=1, column=0, sticky=(tk.N, tk.E, tk.W))

        #Shows what ui the user is viewing and centering the title
        title = ttk.Label(self.title_frame, text="Flash Card Collections")
        title.grid(row=0, column=1)

        #Gets the collection file and puts each file into a list with a length of the list
        files = self.get_flash_collection()
        names = list(files.keys())
        count = len(names)
        #Counts to see if there are files in the list
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

            lbl = tk.Label(
                self.collection_frame,
                text=filename,
                width=20,
                height=2,
                relief="solid",
                borderwidth=1,
                cursor="hand2",
                wraplength=150,
                background="lightblue",
                anchor="center",
            )
            lbl.grid(row=r, column=c, padx=5, pady=5, sticky=(N,S,E,W))

            #Each label is bound by a function and will bring up the flash cards when clicked
            lbl.bind("<Button-1>", lambda e, fn=filename: self.study_collection(fn))

        btn_row = self.rows
        create_btn = ttk.Button(
            self.btn_frame,
            text="Create Collection",
            command="",
        )

        create_btn.grid(
            row=btn_row,
            column=0,
            columnspan=self.cols,
            pady=(5),
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

    def show_collections(self):
        """Returns to flash card collection grid"""
        #clears the widgets on the collection frame
        self.wipe_ui()
        self.refresh_collections()

    def open_collection(self, title):
        """Opens the collection that the user clicks on"""
        #clears the widgets on the collection frame
        self.wipe_ui()

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
            self.btn_frame,
            text = "Back",
            command=self.show_collections
        )
        back_btn.grid(pady=5)

    def study_collection(self, title):
        """Allows the user to start studying the Flash cards in the collection"""
        #Clears the UI
        self.wipe_ui()
        self.collection_frame.grid_forget()

        # Title of the collection
        collection_title = ttk.Label(self.title_frame, text=title)
        collection_title.grid(row=0, column=1)

        #List of flash card objects from the json file
        flashcards = self.get_card_content(title)
        
        #Iterates through the list of objects and assigns them to a label 
        for flashcard in flashcards:
            card_front = tk.Label(self.card_frame, text=flashcard["question"], width=80, height=20, relief="raised", borderwidth=5)
            card_back = tk.Label(self.card_frame, text=flashcard["answer"], width=80, height=20, relief="raised", borderwidth=5)

        #overlaps the labels and puts the front card first
        card_front.grid(row=1, column=1, sticky=(N,S,W,E))
        card_back.grid(row=1, column=1, sticky=(N,S,E,W))
        card_front.lift()

        #Binded functionality to each label to bring one to the front
        card_front.bind("<Button-1>", lambda e: card_back.lift())
        card_back.bind("<Button-1>", lambda e: card_front.lift())

        #Buttons for cycling cards and backing out of the study mode
        back_btn = ttk.Button(self.btn_frame, text="Back", command=self.refresh_collections)
        cycle_forward = ttk.Button(self.btn_frame, text="Forward", width=50)
        cycle_back = ttk.Button(self.btn_frame, text="Backward", width=50)

        back_btn.grid(row=0, column=0, sticky=(W))
        cycle_forward.grid(row=0, column=2, columnspan=2)
        cycle_back.grid(row=0, column=1)

        #Cycle buttons functionality
        # cycle_forward.bind("<Button-1>", lambda e:)
        # cycle_back.bind("<Button-1>", lambda e:)


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

    def wipe_ui(self):
        """Destroys all widgets when the ui changes"""
        for w in self.collection_frame.winfo_children():
            w.destroy()
        for b in self.btn_frame.winfo_children():
            b.destroy()
        for t in self.title_frame.winfo_children():
            t.destroy()
        for c in self.card_frame.winfo_children():
            c.destroy()

    # def save_flashcards(self, data, path="flashcards.json"):
    #     with open(path, "w") as file:
    #         json.dump(data, file, indent=4)
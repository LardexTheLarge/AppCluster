import os
from tkinter import *
from tkinter import ttk
import json

class FlashCardApp:
    def __init__(self, root):
        s = ttk.Style()
        s.theme_use('classic')
        # winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'
        root.title("Flash Cards")
        # root.maxsize(800, 800)
        # root.minsize(800, 800)
        self.FLASHCARD_DIR = "flashcard_collections"

        self.main = ttk.Frame(root)
        self.collection_frame = ttk.Frame(self.main, relief="ridge", borderwidth=1)

        flashCardCollection = self.get_flash_collection()
        
        # for loop to handle the collections and their respective labels
        for i, collection_title in enumerate(flashCardCollection):
            row = i // 5
            col = i % 5

            flashCardCollectionLabel = ttk.Label(
                self.collection_frame,
                text=collection_title,
                width=20,
                # height=6,
                relief="solid",
                borderwidth=1,
                cursor="hand2",
                wraplength=250,
                background="lightblue",
                )

            flashCardCollectionLabel.grid(row=row, column=col, padx=5, pady=5, columnspan=2, rowspan=2)

            flashCardCollectionLabel.bind("<Button-1>", lambda event, lbl=flashCardCollectionLabel, title=collection_title: self.open_collection(title))

        createCollectionBtn = ttk.Button(self.collection_frame, text="Create Collection", command="")

        self.main.grid(column=0, row=0, columnspan=10, rowspan=10)
        self.collection_frame.grid(column=5, row=5, columnspan=10, rowspan=10)
        createCollectionBtn.grid(column=5, row=10, columnspan=2)


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

    def open_collection(self, title):
        """Opens the collection that the user clicks on"""

        for widget in self.collection_frame.winfo_children():
            widget.destroy()

        opened_collection_title = ttk.Entry(self.collection_frame)
        opened_collection_title.insert(0, title)

        flashcards = self.get_card_content(title)
        extracted = []

        for card in flashcards:
            if isinstance(card, dict):
                values = list(card.values())
                extracted.append(values)

        for value in extracted:
            card_title = ttk.Entry(self.collection_frame)
            card_title.insert(1, value[0])

            card_text = ttk.Entry(self.collection_frame)
            card_text.insert(1, value[1])

            row = len(extracted)

        card_title.grid(column=0, row=row, columnspan=4)
        card_text.grid(column=5, row=row, columnspan=5)

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
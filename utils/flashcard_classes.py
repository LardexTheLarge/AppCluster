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
        root.maxsize(800, 800)
        root.minsize(800, 800)

        main = ttk.Frame(root)
        collection_frame = ttk.Frame(main, relief="ridge", borderwidth=5, width=800, height=800)

        flashCardCollection = self.get_flash_collection()
                
        for i, collection_title in enumerate(flashCardCollection):
            row = i // 5
            col = i % 5

            flashCardCollectionLabel = ttk.Label(
                collection_frame,
                text=collection_title,
                width=20,
                # height=6,
                relief="solid",
                borderwidth=1,
                cursor="hand2",
                wraplength=250,
                background="blue",
                )

            flashCardCollectionLabel.grid(row=row, column=col, padx=5, pady=5)

            flashCardCollectionLabel.bind("<Button-1>", lambda event, lbl=flashCardCollectionLabel, title=collection_title: self.select_note(lbl, title))


        main.grid(column=0, row=0)
        collection_frame.grid(column=0, row=0, columnspan=10, rowspan=10)
        


    def get_flash_collection(self):
        """Fetch flash cards collection from storage"""
        collections = {}

        # Checks for directory
        os.makedirs("flashcard_collections", exist_ok=True)

        for filename in os.listdir("flashcard_collections"):
            if filename.endswith(".json"):
                path = os.path.join("flashcard_collections", filename)
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
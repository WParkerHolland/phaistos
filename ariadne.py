import tkinter as tk
from tkinter import filedialog
from src import scansion
import os
import sys

# Function Defintions
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        script_dir = os.path.dirname(os.path.abspath(__file__)) + "\\src"
        print(script_dir)
        sys.path.append(script_dir)
        abs_path = os.path.abspath(file_path)
        scans = scansion.greekToScansion(abs_path)
        print(scansion.makePresentable(scans[0]))


# Window Declaration
window = tk.Tk()
window.title("Ariadne")
window.geometry("800x600")

# Title Label
label = tk.Label(text="Ariadne Scansion Tool", font=("Arial", 24))
label.pack()

# File Input

openFileButton = tk.Button(text="Select File to Scan", command=open_file)
openFileButton.pack()

window.mainloop()
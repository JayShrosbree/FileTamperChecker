import hashlib
import tkinter as tk
from tkinter import filedialog
import json
import os

def calculate_checksum(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash

def store_checksum():
    filename = filedialog.askopenfilename()
    if filename:
        checksum = calculate_checksum(filename)
        with open('checksums.json', 'r+') as f:
            checksums = json.load(f)
            checksums[filename] = checksum
            f.seek(0)
            json.dump(checksums, f)
        print(f"Stored checksum for {filename}")

def verify_checksum():
    filename = filedialog.askopenfilename()
    if filename:
        with open('checksums.json', 'r') as f:
            checksums = json.load(f)
        if filename in checksums:
            current_checksum = calculate_checksum(filename)
            if current_checksum == checksums[filename]:
                print("The file has not been tampered with.")
            else:
                print("WARNING: The file has been tampered with.")
        else:
            print("No stored checksum for this file.")

def main():
    if not os.path.exists('checksums.json'):
        with open('checksums.json', 'w') as f:
            json.dump({}, f)

    root = tk.Tk()
    store_button = tk.Button(root, text="Store Checksum", command=store_checksum)
    store_button.pack()
    verify_button = tk.Button(root, text="Verify Checksum", command=verify_checksum)
    verify_button.pack()
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import messagebox
import os
import re
import unicodedata
import subprocess
import pyperclip

BETTING_FOLDER = "C:\dev\scommesse"

def normalize_text(text):
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("ASCII")
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text

def check_no_uncommitted_changes():
    try:
        # Run 'git status --porcelain' to check for changes
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

        # Check if the output is non-empty
        if result.stdout.strip():
            print("Uncommitted changes detected.")
            return False
        else:
            print("No uncommitted changes.")
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error while running git status: {e}")
        return False
    
def get_current_branch():
    try:
        # Run 'git rev-parse --abbrev-ref HEAD' to get the current branch
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
        
        # Capture and return the branch name
        branch_name = result.stdout.strip()
        return branch_name
    except subprocess.CalledProcessError as e:
        print(f"Error while getting current branch: {e}")
        return None    

def process_input_clipboard():
    cliptext = pyperclip.paste()
    splitted = cliptext.split("/")
    entry.delete(0, tk.END)  # Clear the existing text
    branchname = ''.join(splitted[1]).split("_")
    entry.insert(0, branchname[0])
    entry_feature.insert(0, branchname[2:])
    entry_branch_name.insert(0, cliptext)
    return

def process_create_branch():
    os.chdir(BETTING_FOLDER)
    if check_no_uncommitted_changes():
        branch = entry_branch_name.get()
        reset = checkbox_var.get()
        if reset:
            os.system("git reset --hard")
            os.system("git clean -f")
        os.system(f"git checkout develop")
        os.system(f"git pull")
        os.system(f"git checkout -b {branch}")
        current_branch = get_current_branch()
        messagebox.showinfo("Input Processed", f'swithced to branch\n{current_branch}')
    else:
        current_branch = get_current_branch()
        messagebox.showinfo("Input Processed", f'there are uncommitted changes in the current branch\n{current_branch}')
    return

def process_input():
    danb = entry.get().split(",")

    folder = ""
    if danb[0].startswith("STRY"):
        folder = "feature"
    elif danb[0].startswith("BUGT"):
        folder = "fix"
    else:
        folder = input("Enter FEATURE or FIX: ").lower()
        validInput = False
        for possibleAction in ["fix", "feature"]:
            if folder == possibleAction:
                validInput = True
                break
        if validInput == False:
            print("Invalid command")
            print()
            print()
            return

    feature =  normalize_text(entry_feature.get()).lower()
    
    if (feature.strip() == ""):
        messagebox.showinfo("missing data","please enter the feature name" )        
        return

    branch = f'{folder}/{"_".join(danb).replace(" ", "")}_BOZZONI_{feature}'
    pyperclip.copy(branch)

    entry_branch_name.delete(0, tk.END)
    entry_branch_name.insert(0, branch)

    print(f"Copied into clipboard: {branch}")

app = tk.Tk()
app.title("Sisal Git branch creator")

frame = tk.Frame(app, padx=30, pady=20)
frame.pack(fill="both", expand=True)

app.iconbitmap("branch_creator.ico")

label = tk.Label(frame, text="Enter SN number (if more than one, separated by comma): ")
label.pack()

entry = tk.Entry(frame)
entry.pack(fill="x")

label = tk.Label(frame, text="Enter feature description: ")
label.pack()

entry_feature = tk.Entry(frame)
entry_feature.pack(fill="x")

button = tk.Button(frame, text="Create branch name", command=process_input)
button.pack()

spacer = tk.Label(frame, text="", height=1)  # height=2 for vertical space (you can adjust this)
spacer.pack()

label = tk.Label(frame, text="branch name:")
label.pack()

entry_branch_name = tk.Entry(frame)
entry_branch_name.pack(fill="x")

btnFromClipBoard = tk.Button(frame, text="get from Clipboard", command=process_input_clipboard)
btnFromClipBoard.pack()

spacer = tk.Label(frame, text="", height=1)  # height=2 for vertical space (you can adjust this)
spacer.pack()


checkbox_var = tk.IntVar()
checkbox = tk.Checkbutton(app, text="Reset hard if there are uncommitted changes", variable=checkbox_var)
checkbox.pack()

btnFromClipBoard = tk.Button(frame, text="create branch", command=process_create_branch)
btnFromClipBoard.pack()

app.update()  # Force a layout update
app.geometry('')  # Tell Tkinter to auto-size based on content

app.mainloop()
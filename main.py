import tkinter as tk
from tkinter import messagebox
import os
import re
import unicodedata
import subprocess
import pyperclip

BETTING_FOLDER = "C:\dev\scommesse"
USERNAME = "BOZZONI"

class App:
    def __init__(self, root):
        self.root = root
        root.title("Sisal Git branch creator")

        self.frame = tk.Frame(self.root, padx=30, pady=20)
        self.frame.pack(fill="both", expand=True)

        self.root.iconbitmap("branch_creator.ico")

        self.label = tk.Label(self.frame, text="Enter SN number (if more than one, separated by comma): ")
        self.label.pack()

        self.entry = tk.Entry(self.frame)
        self.entry.pack(fill="x")

        self.label = tk.Label(self.frame, text="Enter feature description: ")
        self.label.pack()

        self.entry_feature = tk.Entry(self.frame)
        self.entry_feature.pack(fill="x")

        self.button = tk.Button(self.frame, text="Create branch name", command=self.process_input)
        self.button.pack()

        spacer = tk.Label(self.frame, text="", height=1)  # height=2 for vertical space (you can adjust this)
        spacer.pack()

        self.label = tk.Label(self.frame, text="branch name:")
        self.label.pack()

        self.entry_branch_name = tk.Entry(self.frame)
        self.entry_branch_name.pack(fill="x")

        self.btnFromClipBoard = tk.Button(self.frame, text="get from Clipboard", command=self.process_input_clipboard)
        self.btnFromClipBoard.pack()

        self.spacer = tk.Label(self.frame, text="", height=1)  # height=2 for vertical space (you can adjust this)
        self.spacer.pack()

        self.checkbox_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(self.root, text="Reset hard if there are uncommitted changes", variable=self.checkbox_var)
        self.checkbox.pack()

        self.btnFromClipBoard = tk.Button(self.frame, text="create branch", command=self.process_create_branch)
        self.btnFromClipBoard.pack()

        self.root.update()  # Force a layout update
        self.root.geometry('')  # Tell Tkinter to auto-size based on content

    def normalize_text(self,text):
        text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("ASCII")
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        text = re.sub(r"\s+", "-", text)
        return text

    def no_uncommitted_changes(self):
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
        
    def there_are_uncommitted_changes(self):
        return not self.check_no_uncommitted_changes()    
        
    def get_current_branch(self):
        try:
            # Run 'git rev-parse --abbrev-ref HEAD' to get the current branch
            result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
            
            # Capture and return the branch name
            branch_name = result.stdout.strip()
            return branch_name
        except subprocess.CalledProcessError as e:
            print(f"Error while getting current branch: {e}")
            return None    

    def process_input_clipboard(self):
        cliptext = pyperclip.paste()
        splitted = cliptext.split("/")
        self.entry.delete(0, tk.END)  # Clear the existing text
        branchname = ''.join(splitted[1]).split("_")
        self.entry.insert(0, branchname[0])
        self.entry_feature.insert(0, branchname[2:])
        self.entry_branch_name.insert(0, cliptext)
        return

    def process_create_branch(self):
        os.chdir(BETTING_FOLDER)
        
        reset = self.checkbox_var.get()
        if self.there_are_uncommitted_changes() and reset:
            os.system("git reset --hard")
            os.system("git clean -f")

        if self.no_uncommitted_changes():
            branch = self.entry_branch_name.get()
            os.system(f"git checkout develop")
            os.system(f"git pull")
            os.system(f"git checkout -b {branch}")
            current_branch = self.get_current_branch()
            messagebox.showinfo("Input Processed", f'swithced to branch\n{current_branch}')
        else:
            current_branch = self.get_current_branch()
            messagebox.showinfo("Input Processed", f'there are uncommitted changes in the current branch\n{current_branch}')
        return

    def process_input(self):
        danb = self.entry.get().split(",")

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

        feature =  self.normalize_text(self.entry_feature.get()).lower()
        
        if (feature.strip() == ""):
            messagebox.showinfo("missing data","please enter the feature name" )        
            return

        branch = f'{folder}/{"_".join(danb).replace(" ", "")}_{USERNAME}_{feature}'
        pyperclip.copy(branch)

        self.entry_branch_name.delete(0, tk.END)
        self.entry_branch_name.insert(0, branch)

        print(f"Copied into clipboard: {branch}")

def main():    
    root = tk.Tk()  #starts the GUI library
    app = App(root) #create the object app and passes the root of the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
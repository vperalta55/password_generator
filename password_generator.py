import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import keyboard
import threading

# Function to generate a random password
def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    if not (use_upper or use_lower or use_digits or use_symbols):
        raise ValueError("At least one character type must be selected.")

    character_pool = ""
    if use_upper:
        character_pool += string.ascii_uppercase
    if use_lower:
        character_pool += string.ascii_lowercase
    if use_digits:
        character_pool += string.digits
    if use_symbols:
        character_pool += string.punctuation

    password = ''.join(random.choice(character_pool) for _ in range(length))
    return password

# Function to copy text to clipboard
def copy_to_clipboard(text):
    pyperclip.copy(text)

# Function to handle password generation and copying
def handle_generate():
    try:
        length = int(length_var.get())
        use_upper = upper_var.get()
        use_lower = lower_var.get()
        use_digits = digits_var.get()
        use_symbols = symbols_var.get()

        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        password_var.set(password)
        copy_to_clipboard(password)
        messagebox.showinfo("Password Generated", "Password has been copied to clipboard.")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", "An error occurred while generating the password.")

# Function to set up the hotkey
def set_hotkey():
    hotkey = hotkey_var.get()
    if hotkey:
        try:
            # Unregister previous hotkeys to prevent duplicates
            keyboard.unhook_all_hotkeys()
            keyboard.add_hotkey(hotkey, handle_generate)
            messagebox.showinfo("Hotkey Set", f"Hotkey '{hotkey}' has been set.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set hotkey: {e}")
    else:
        messagebox.showwarning("No Hotkey", "Please enter a valid hotkey.")

# Function to run the keyboard listener in a separate thread
def run_hotkey_listener():
    keyboard.wait()  # This will block, so run it in a separate thread

# Initialize the main window
root = tk.Tk()
root.title("Python Password Generator")
root.geometry("400x350")
root.resizable(False, False)

# Variables
length_var = tk.StringVar(value="12")
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)
password_var = tk.StringVar()
hotkey_var = tk.StringVar()

# Styling
style = ttk.Style()
style.configure('TLabel', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))
style.configure('TCheckbutton', font=('Arial', 10))

# Layout
padding = {'padx': 10, 'pady': 10}

# Password Length
length_label = ttk.Label(root, text="Password Length:")
length_label.grid(column=0, row=0, sticky='W', **padding)

length_entry = ttk.Entry(root, textvariable=length_var, width=10)
length_entry.grid(column=1, row=0, sticky='W', **padding)

# Character Types
char_types_label = ttk.Label(root, text="Include Characters:")
char_types_label.grid(column=0, row=1, sticky='W', **padding)

upper_check = ttk.Checkbutton(root, text="Uppercase (A-Z)", variable=upper_var)
upper_check.grid(column=0, row=2, sticky='W', **padding)

lower_check = ttk.Checkbutton(root, text="Lowercase (a-z)", variable=lower_var)
lower_check.grid(column=0, row=3, sticky='W', **padding)

digits_check = ttk.Checkbutton(root, text="Digits (0-9)", variable=digits_var)
digits_check.grid(column=0, row=4, sticky='W', **padding)

symbols_check = ttk.Checkbutton(root, text="Symbols (!@#...)", variable=symbols_var)
symbols_check.grid(column=0, row=5, sticky='W', **padding)

# Generate Button
generate_button = ttk.Button(root, text="Generate Password", command=handle_generate)
generate_button.grid(column=0, row=6, columnspan=2, **padding)

# Generated Password Display
password_label = ttk.Label(root, text="Generated Password:")
password_label.grid(column=0, row=7, sticky='W', **padding)

password_display = ttk.Entry(root, textvariable=password_var, width=40, state='readonly')
password_display.grid(column=0, row=8, columnspan=2, **padding)

# Hotkey Setting
hotkey_label = ttk.Label(root, text="Set Hotkey (e.g., ctrl+shift+p):")
hotkey_label.grid(column=0, row=9, sticky='W', **padding)

hotkey_entry = ttk.Entry(root, textvariable=hotkey_var, width=25)
hotkey_entry.grid(column=0, row=10, sticky='W', **padding)

set_hotkey_button = ttk.Button(root, text="Set Hotkey", command=set_hotkey)
set_hotkey_button.grid(column=1, row=10, sticky='W', **padding)

# Start the hotkey listener in a separate thread
listener_thread = threading.Thread(target=run_hotkey_listener, daemon=True)
listener_thread.start()

# Run the application
root.mainloop()

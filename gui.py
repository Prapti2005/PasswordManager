import tkinter as tk
from tkinter import ttk, messagebox
import os
import secrets
import string

from auth import setup_master_password, verify_master_password, get_salt
from crypto_utils import encrypt_password, decrypt_password
from vault import add_entry, get_entry, delete_entry, load_vault


class PasswordManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure Password Manager")
        self.root.geometry("650x650")
        self.root.configure(bg="#1e1e2e")

        self.master_password = None

        if os.path.exists("master.json"):
            self.login_screen()
        else:
            self.setup_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_screen(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Create Master Password",
            font=("Segoe UI", 22, "bold"),
            bg="#1e1e2e",
            fg="white"
        ).pack(pady=30)

        self.setup_password = tk.Entry(self.root, show="*", width=35)
        self.setup_password.pack(pady=10)

        tk.Button(
            self.root,
            text="Create Vault",
            command=self.create_master_password
        ).pack(pady=10)

    def create_master_password(self):
        password = self.setup_password.get()

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return

        setup_master_password(password)
        messagebox.showinfo("Success", "Master Password Created")
        self.login_screen()

    def login_screen(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Secure Login",
            font=("Segoe UI", 22, "bold"),
            bg="#1e1e2e",
            fg="white"
        ).pack(pady=30)

        self.login_password = tk.Entry(self.root, show="*", width=35)
        self.login_password.pack(pady=10)

        tk.Button(
            self.root,
            text="Login",
            command=self.login
        ).pack(pady=10)

    def login(self):
        password = self.login_password.get()

        if verify_master_password(password):
            self.master_password = password
            self.dashboard()
        else:
            messagebox.showerror("Login Failed", "Incorrect Master Password")

    def dashboard(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Password Manager Dashboard",
            font=("Segoe UI", 18, "bold"),
            bg="#1e1e2e",
            fg="white"
        ).pack(pady=15)

        tk.Label(self.root, text="Website").pack()
        self.site_entry = tk.Entry(self.root, width=40)
        self.site_entry.pack(pady=5)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root, width=40)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, width=40, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Generate Password", command=self.generate_password).pack(pady=5)
        tk.Button(self.root, text="Add Entry", command=self.add_password).pack(pady=5)
        tk.Button(self.root, text="Retrieve Entry", command=self.retrieve_password).pack(pady=5)
        tk.Button(self.root, text="Delete Entry", command=self.delete_password).pack(pady=5)
        tk.Button(self.root, text="Show Sites", command=self.search_sites).pack(pady=5)

        self.result_box = tk.Text(self.root, height=10, width=70)
        self.result_box.pack(pady=10)

    def generate_password(self):
        chars = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(chars) for _ in range(16))

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def add_password(self):
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not site or not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        encrypted = encrypt_password(password, self.master_password, get_salt())
        add_entry(site, username, encrypted)

        messagebox.showinfo("Success", "Password Saved")

    def retrieve_password(self):
        site = self.site_entry.get().strip()

        entry = get_entry(site)

        if not entry:
            messagebox.showerror("Not Found", "Entry does not exist")
            return

        password = decrypt_password(
            entry["password"],
            self.master_password,
            get_salt()
        )

        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(
            tk.END,
            "Website: " + site + "\n"
            + "Username: " + entry["username"] + "\n"
            + "Password: " + password
        )

    def delete_password(self):
        site = self.site_entry.get().strip()
        delete_entry(site)
        messagebox.showinfo("Deleted", "Entry deleted")

    def search_sites(self):
        data = load_vault()

        self.result_box.delete("1.0", tk.END)

        for site in data.keys():
            self.result_box.insert(tk.END, site + "\n")

    def run(self):
        self.root.mainloop()

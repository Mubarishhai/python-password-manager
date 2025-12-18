# ----------------------------------------------------------
# Project: Smart Password Manager - DB Version
# Author: Shaikh Mubarish
# Date: 2025
# ----------------------------------------------------------

import sqlite3
from cryptography.fernet import Fernet
import os
import getpass

DB_NAME = "passwords.db"
KEY_FILE = "key.key"

# ---------------------------
# Load or generate encryption key
# ---------------------------
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as file:
            file.write(key)
        return key

key = load_key()
fernet = Fernet(key)

# ---------------------------
# Initialize DB
# ---------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------------------------
# Save new password
# ---------------------------
def save_password():
    website = input("Enter Website: ")
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password (hidden): ")

    encrypted_password = fernet.encrypt(password.encode()).decode()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
              (website, username, encrypted_password))
    conn.commit()
    conn.close()

    print("✔ Password saved securely!\n")

# ---------------------------
# View passwords
# ---------------------------
def view_passwords():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM passwords")
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("No passwords saved yet TRY AGAIN.\n")
        return

    print("\n🔐 Saved Passwords:DONT WORRY YOUR PASSWORD IS SAFE")
    for row in rows:
        try:
            decrypted = fernet.decrypt(row[3].encode()).decode()
        except Exception:
            decrypted = "Error decrypting!"
        print(f"ID: {row[0]} | Website: {row[1]} | Username: {row[2]} | Password: {decrypted}")
    print("")

# --------------------------
# Delete password
# --------------------------
def delete_password():
    view_passwords()
    try:
        idx = int(input("Enter ID of password to delete: "))
    except ValueError:
        print("❌ Invalid input!\n")
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM passwords WHERE id=?", (idx,))
    row = c.fetchone()
    if row:
        confirm = input(f"Are you sure you want to delete '{row[1]}'? (y/n): ")
        if confirm.lower() == 'y':
            c.execute("DELETE FROM passwords WHERE id=?", (idx,))
            conn.commit()
            print(f"🗑 Deleted: {row[1]}\n")
        else:
            print("Deletion cancelled.\n")
    else:
        print("❌ ID not found!\n")
    conn.close()

# ---------------------------
# Search password by website
# ---------------------------
def search_password():
    website = input("Enter website to search: ").lower()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM passwords WHERE LOWER(website) LIKE ?", ('%'+website+'%',))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("No passwords found for this website.\n")
        return

    print(f"\n🔎 Search Results for '{website}':")
    for row in rows:
        try:
            decrypted = fernet.decrypt(row[3].encode()).decode()
        except Exception:
            decrypted = "Error decrypting!"
        print(f"ID: {row[0]} | Website: {row[1]} | Username: {row[2]} | Password: {decrypted}")
    print("")

# ---------------------------
# Menu system
# ---------------------------
def menu():
    init_db()
    while True:
        print("\n----------------------------")
        print(" 🔐 SMART PASSWORD MANAGER ")
        print("----------------------------")
        print("1. Save New Password")
        print("2. View Saved Passwords")
        print("3. Delete Password")
        print("4. Search Password")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            save_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            delete_password()
        elif choice == "4":
            search_password()
        elif choice == "5":
            print("Bye! 👋")
            break
        else:
            print("❌ Invalid choice! Try again.\n")

if __name__ == "__main__":
    menu()

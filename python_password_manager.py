# ----------------------------------------------------------
# Project: Smart Password Manager
# Author: Shaikh Mubarish
# Date: 2025
# ----------------------------------------------------------
from cryptography.fernet import Fernet
import os

# ---------------------------
# Generate or load encryption key
# ---------------------------
def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as file:
            file.write(key)
        return key

key = load_key()
fernet = Fernet(key)

# ---------------------------
# Save Password
# ---------------------------
def save_password(website, username, password):
    encrypted_password = fernet.encrypt(password.encode())
    with open("passwords.txt", "ab") as file:
        file.write(f"{website} | {username} | {encrypted_password.decode()}\n".encode())
    print("✔ Password saved securely!")

# ---------------------------
# View Passwords
# ---------------------------
def view_passwords():
    print("\n🔐 Saved Passwords:")
    if not os.path.exists("passwords.txt"):
        print("No passwords saved yet.\n")
        return

    with open("passwords.txt", "rb") as file:
        for line in file.readlines():
            website, username, encrypted_password = line.decode().split(" | ")
            decrypted = fernet.decrypt(encrypted_password.strip().encode()).decode()
            print(f"🌐 Website: {website} | 👤 Username: {username} | 🔑 Password: {decrypted}")

# ---------------------------
# Menu System
# ---------------------------
def menu():
    while True:
        print("\n----------------------------")
        print(" 🔐 SMART PASSWORD MANAGER ")
        print("----------------------------")
        print("1. Save New Password")
        print("2. View Saved Passwords")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            save_password(website, username, password)

        elif choice == "2":
            view_passwords()

        elif choice == "3":
            print("Bye!   have a nice day!👋")
            break

        else:
            print("Invalid choice! Try again  Choose better.")

menu()

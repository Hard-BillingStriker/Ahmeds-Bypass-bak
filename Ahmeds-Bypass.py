import os
import tkinter as tk
from tkinter import filedialog
import requests
import zipfile
import rarfile
import py7zr
from tkinter import ttk
import threading
import webbrowser

# GitHub repository details
REPO_URL = "https://github.com/Ahmeds-tool/Ahmeds-Bypass"
API_URL = "https://api.github.com/repos/Ahmeds-tool/Ahmeds-Bypass/contents/Bypasses"
GITHUB_TOKEN = 'TOKKEN' 

def check_drive(directory):
    """Check if the directory is on C or D drive."""
    drive = os.path.splitdrive(directory)[0]
    return drive.upper() in ['C:', 'D:']

def download_file(url, save_dir, status_label):
    """Downloads a file from a URL and saves it to the specified directory."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Authorization": f"token {GITHUB_TOKEN}"
        }
        status_label.config(text="⏳ Download in progress...")  # General download message
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        filename = os.path.basename(url)
        save_path = os.path.join(save_dir, filename)

        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"✅ Downloaded: {save_path}")
        extract_archive(save_path, save_dir, status_label)

    except requests.exceptions.RequestException as e:
        status_label.config(text=f"❌ Download error: {e}")

def extract_archive(file_path, extract_to, status_label):
    """Extracts ZIP, RAR, or 7z files."""
    try:
        status_label.config(text=f"📂 Extracting files...")  # General extraction message
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
            print(f"📂 ZIP extracted: {extract_to}")

        elif rarfile.is_rarfile(file_path):
            with rarfile.RarFile(file_path, "r") as rar_ref:
                rar_ref.extractall(extract_to)
            print(f"📂 RAR extracted: {extract_to}")

        elif file_path.lower().endswith(".7z"):
            with py7zr.SevenZipFile(file_path, "r") as seven_z_ref:
                seven_z_ref.extractall(extract_to)
            print(f"📂 7Z extracted: {extract_to}")

        else:
            print("⚠️ Not an archive, skipping extraction.")

    except (zipfile.BadZipFile, rarfile.BadRarFile, py7zr.Bad7zFile) as e:
        status_label.config(text=f"❌ Extraction failed: {e}")
    except Exception as e:
        status_label.config(text=f"❌ Unexpected error: {e}")

def get_github_files():
    """Fetches the list of directories (games) from the GitHub repository."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Authorization": f"token {GITHUB_TOKEN}"
        }
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        files = response.json()

        game_names = []
        for file in files:
            if file['type'] == 'dir':  # Check only directories under 'Bypasses' folder
                game_names.append(file['name'])

        return game_names
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        raise

def download_github_folder(folder_path, save_dir, status_label):
    """Downloads all files from a GitHub folder."""
    folder_url = f"{API_URL}/{folder_path}"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Authorization": f"token {GITHUB_TOKEN}"
        }
        response = requests.get(folder_url, headers=headers)
        response.raise_for_status()
        files = response.json()

        # Track number of files to download
        total_files = len([file for file in files if file["type"] == "file"])
        downloaded_files = 0

        for file in files:
            if file["type"] == "file":
                download_file(file["download_url"], save_dir, status_label)
                downloaded_files += 1

        if downloaded_files == total_files:
            status_label.config(text="✅ successfull!")

    except requests.exceptions.RequestException as e:
        status_label.config(text=f"❌ Download failed: {e}")
        raise

def browse_folder():
    """Let the user choose a directory for saving files."""
    folder = filedialog.askdirectory()
    if folder:
        save_directory.set(folder)

def start_download(status_label):
    """Start downloading based on selected game."""
    selected_folder = game_choice.get()

    if check_drive(save_directory.get()):
        try:
            status_label.config(text="🌀 Bypass in progress...")
            threading.Thread(target=download_github_folder, args=(selected_folder, save_directory.get(), status_label)).start()
        except Exception as e:
            status_label.config(text=f"❌ Download failed: {str(e)}")
    else:
        status_label.config(text="❌ Select a folder on C or D drive.")

def update_game_options():
    """Update the game options from GitHub repository."""
    try:
        game_names = get_github_files()
        if game_names:
            game_choice.set(game_names[0])  # Set the first option as the default
        return game_names
    except Exception as e:
        status_label.config(text=f"❌ Failed to fetch game list: {str(e)}")
        return []

def create_gui():
    """Create the GUI with smooth animation and glowing buttons."""
    root = tk.Tk()
    root.title("Ahmeds-Bypass")
    root.geometry("800x600")  # Window size
    root.config(bg="#2E2E2E")  # Dark background color

    global save_directory
    save_directory = tk.StringVar()

    frame = tk.Frame(root, bg="#2E2E2E")
    frame.pack(padx=20, pady=20, expand=True)

    # Title label
    title_label = tk.Label(frame, text="Ahmeds-Bypass V 1.0", font=("Helvetica", 24, "bold"), fg="white", bg="#2E2E2E")
    title_label.pack(pady=20)

    # Subtitle label
    subtitle_label = tk.Label(frame, text="Select a Game to Bypass:", font=("Helvetica", 14), fg="white", bg="#2E2E2E")
    subtitle_label.pack(pady=10)

    global game_choice
    game_choice = tk.StringVar()

    # Fetch game options and update dropdown
    game_names = update_game_options()

    if game_names:
        game_choice.set(game_names[0])  # Set the first option as the default

    # Dropdown menu with game names
    game_menu = ttk.Combobox(frame, textvariable=game_choice, values=game_names, font=("Helvetica", 12), state="readonly")
    game_menu.config(width=40)
    game_menu.pack(pady=10)

    # Directory selection
    directory_label = tk.Label(frame, text="Select Game directory:", font=("Helvetica", 12), fg="white", bg="#2E2E2E")
    directory_label.pack(pady=10)

    # Directory entry field
    directory_entry = tk.Entry(frame, textvariable=save_directory, font=("Helvetica", 12), width=40, relief="flat")
    directory_entry.pack(pady=10)

    # Browse button with glowing effect
    browse_button = tk.Button(frame, text="Browse...", font=("Helvetica", 12), bg="#444444", fg="white", relief="flat", command=browse_folder)
    browse_button.pack(pady=10)

    # Glowing start download button
    start_button = tk.Button(frame, text="Start Bypass", font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat", command=lambda: start_download(status_label))
    start_button.pack(pady=20)

    # Glowing effect when hovering
    def on_enter(event):
        event.widget.config(bg="#5cb85c")

    def on_leave(event):
        event.widget.config(bg="#4CAF50")

    start_button.bind("<Enter>", on_enter)
    start_button.bind("<Leave>", on_leave)

    # Discord button
    discord_button = tk.Button(frame, text="Join Discord", font=("Helvetica", 12), bg="#7289DA", fg="white", relief="flat", command=lambda: webbrowser.open("https://discord.gg/sv6EGxCRnC"))
    discord_button.pack(pady=10)

    # YouTube button
    youtube_button = tk.Button(frame, text="YouTube channel", font=("Helvetica", 12), bg="#FF0000", fg="white", relief="flat", command=lambda: webbrowser.open("https://www.youtube.com/@Ahmedsscript"))
    youtube_button.pack(pady=10)

    # Status label to display progress
    status_label = tk.Label(frame, text="Select a game and directory to start.", font=("Helvetica", 12), fg="white", bg="#2E2E2E")
    status_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

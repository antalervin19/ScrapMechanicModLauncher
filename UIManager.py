# /* UIManager.py */ #

# COPYRIGHT (C) 2025 antalervin19
# I do NOT give ANYONE permission to copy, modify or redistribute code in this file!
# If you want to use code from this in your own project(s), you HAVE to ask me for permission first!
# Contacts:
# Discord: antalervin19
# Web: https://www.iggames.eu

import json
import asyncio
import shutil
import customtkinter as ctk
from pathlib import Path
from FileManager import install_mod, uninstall_mod
from GameManager import scan_and_get_game_path, run_gameprocess
from LogManager import log
import tkinter.messagebox as messagebox
from PIL import Image
import webbrowser

MODS_DIR = Path("./Mods")
CACHE_FILE = Path(".cache")
INSTALLED_MODS_FILE = MODS_DIR / "installed_mods.json"

if CACHE_FILE.exists():
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        GAME_DIR = Path(json.load(f)['game_path'])
else:
    result = messagebox.askyesno("Error!", "Scrap Mechanic Installation Not found!\nDo you want to run the game to automatically get the installation path?")
    if result:
        run_gameprocess()
        GAME_DIR = scan_and_get_game_path()
        if GAME_DIR:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump({"game_path": str(GAME_DIR)}, f, indent=2)
        else:
            messagebox.showerror("Error", "Failed to detect Scrap Mechanic path.")
            exit(1)
    else:
        exit(1)

WORKSHOP_MODS_DIR = GAME_DIR.parent.parent / "workshop" / "content" / "387990"

if INSTALLED_MODS_FILE.exists():
    with open(INSTALLED_MODS_FILE, "r", encoding="utf-8") as f:
        installed_mods = set(json.load(f))
else:
    installed_mods = set()

def save_installed_mods():
    with open(INSTALLED_MODS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(installed_mods), f, indent=2)

def load_valid_mods(mods_root: Path):
    mods = []
    for mod_dir in mods_root.iterdir():
        content_file = mod_dir / "mod.content"
        if mod_dir.is_dir() and content_file.exists():
            with open(content_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["folder"] = mod_dir.name
                mods.append(data)
    return mods

def load_workshop_mods():
    if not WORKSHOP_MODS_DIR.exists():
        return []
    return load_valid_mods(WORKSHOP_MODS_DIR)

def toggle_mod(mod, button):
    mod_path = MODS_DIR / mod['folder']
    if mod['folder'] in installed_mods:
        log(f"Uninstalling {mod['title']}")
        asyncio.run(uninstall_mod(mod_path, GAME_DIR))
        installed_mods.remove(mod['folder'])
        button.configure(text="Install", fg_color="#5a189a")
    else:
        log(f"Installing {mod['title']}")
        asyncio.run(install_mod(mod_path, GAME_DIR))
        installed_mods.add(mod['folder'])
        button.configure(text="Uninstall", fg_color="#7209b7")
    save_installed_mods()

def download_workshop_mod(mod, button):
    src_path = WORKSHOP_MODS_DIR / mod['folder']
    dest_path = MODS_DIR / mod['folder']
    log(f"Copying {mod['title']} from Workshop to Mods...")

    if dest_path.exists():
        shutil.rmtree(dest_path)

    shutil.copytree(src_path, dest_path)

    button.configure(text="Remove", fg_color="#7209b7", command=lambda: remove_downloaded_mod(mod, button))


def remove_downloaded_mod(mod, button):
    mod_path = MODS_DIR / mod['folder']
    if mod_path.exists():
        log(f"Removing downloaded mod: {mod['title']}")
        shutil.rmtree(mod_path)

    button.configure(text="Download", fg_color="#5a189a", command=lambda: download_workshop_mod(mod, button))


class ModManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ScrapMechanic Mod Launcher")
        self.geometry("900x600")
        self.configure(fg_color="#0b0b0f")

        self.sidebar = ctk.CTkFrame(self, width=48, fg_color="#1e1e2f", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.my_mods_icon = ctk.CTkImage(Image.open("./Resources/home_dark.png"), size=(22, 22))
        self.workshop_icon = ctk.CTkImage(Image.open("./Resources/workshop.png"), size=(22, 22))
        self.settings_icon = ctk.CTkImage(Image.open("./Resources/settings_dark.png"), size=(22, 22))
        self.refresh_icon = ctk.CTkImage(Image.open("./Resources/refresh.png"), size=(22, 22))

        self.my_mods_button = ctk.CTkButton(self.sidebar, image=self.my_mods_icon, text="", width=24, height=24,
            fg_color="#5a189a", hover_color="#3a0ca3", corner_radius=6, command=self.open_my_mods)
        self.my_mods_button.pack(pady=(10, 2), padx=10, anchor="center")

        self.workshop_button = ctk.CTkButton(self.sidebar, image=self.workshop_icon, text="", width=24, height=24,
            fg_color="#5a189a", hover_color="#3a0ca3", corner_radius=6, command=self.open_workshop)
        self.workshop_button.pack(pady=2, padx=10, anchor="center")

        self.settings_button = ctk.CTkButton(self.sidebar, image=self.settings_icon, text="", width=24, height=24,
            fg_color="#5a189a", hover_color="#3a0ca3", corner_radius=6, command=self.open_settings)
        self.settings_button.pack(pady=2, padx=10, anchor="center")

        self.refresh_button = ctk.CTkButton(self.sidebar, image=self.refresh_icon, text="", width=24, height=24,
            fg_color="#5a189a", hover_color="#3a0ca3")

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#0b0b0f")
        self.scroll_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.about_button = None
        self.created_by_label = None
        self.thanks_label = None

        self.mods = load_valid_mods(MODS_DIR)
        self.create_mod_cards(self.mods)
        self.open_my_mods()

    def clear_settings_widgets(self):
        if self.about_button:
            self.about_button.destroy()
            self.about_button = None
        if self.created_by_label:
            self.created_by_label.destroy()
            self.created_by_label = None
        if self.thanks_label:
            self.thanks_label.destroy()
            self.thanks_label = None

    def create_mod_cards(self, mods, from_workshop=False):
        for mod in mods:
            frame = ctk.CTkFrame(self.scroll_frame, corner_radius=15, fg_color="#1e1e2f")
            frame.pack(pady=5, padx=10, fill="x")

            title = ctk.CTkLabel(frame, text=mod["title"], font=("Segoe UI", 18, "bold"), text_color="white")
            title.pack(anchor="w", padx=10, pady=(8, 0))

            desc = ctk.CTkLabel(frame, text=mod["description"], font=("Segoe UI", 12), text_color="#dddddd", wraplength=650)
            desc.pack(anchor="w", padx=10, pady=(2, 5))

            meta = f"Author: {mod['author']} | Version: {mod['version']} | Game: {mod['GameVersion']} | Date: {mod['date']}"
            meta_label = ctk.CTkLabel(frame, text=meta, font=("Segoe UI", 12), text_color="#aaaaaa")
            meta_label.pack(anchor="w", padx=10, pady=(0, 8))

            if from_workshop:
                is_downloaded = (MODS_DIR / mod['folder']).exists()
                is_installed = mod['folder'] in installed_mods
                btn_text = "Remove" if is_downloaded else "Download"
                btn_color = "#7209b7" if is_downloaded else "#5a189a"

                button = ctk.CTkButton(
                    frame,
                    text=btn_text,
                    fg_color=btn_color,
                    hover_color="#3a0ca3",
                    width=100,
                    height=30,
                    state="disabled" if is_installed else "normal"
                )
                button.pack(anchor="e", padx=10, pady=(0, 10))

                if is_installed:
                    tooltip = ctk.CTkLabel(
                        frame,
                        text="Cannot be removed while the mod is installed",
                        text_color="#bbbbbb",
                        font=("Segoe UI", 10),
                    )
                    tooltip.place(in_=button, relx=-1.025, rely=-0.2, anchor="sw")
                elif is_downloaded:
                    button.configure(command=lambda m=mod, b=button: remove_downloaded_mod(m, b))
                else:
                    button.configure(command=lambda m=mod, b=button: download_workshop_mod(m, b))
            else:
                toggle_text = "Uninstall" if mod['folder'] in installed_mods else "Install"
                toggle_color = "#7209b7" if toggle_text == "Uninstall" else "#5a189a"
                button = ctk.CTkButton(frame, text=toggle_text, fg_color=toggle_color, hover_color="#3a0ca3",
                                        width=100, height=30)
                button.pack(anchor="e", padx=10, pady=(0, 10))
                button.configure(command=lambda m=mod, b=button: toggle_mod(m, b))

    def refresh_mods(self):
        log("Refreshing mod list...")
        self.mods = load_valid_mods(MODS_DIR)
        self.open_my_mods()

    def refresh_workshop(self):
        log("Refreshing workshop mods...")
        self.open_workshop()

    def open_workshop(self):
        log("Workshop tab opened")
        self.clear_settings_widgets()
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        workshop_mods = load_workshop_mods()
        self.create_mod_cards(workshop_mods, from_workshop=True)
        self.refresh_button.configure(command=self.refresh_workshop)
        self.refresh_button.pack(side="bottom", pady=10, padx=10)

    def open_my_mods(self):
        log("My Mods tab opened")
        self.clear_settings_widgets()
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.create_mod_cards(self.mods)
        self.refresh_button.configure(command=self.refresh_mods)
        self.refresh_button.pack(side="bottom", pady=10, padx=10)

    def open_settings(self):
        log("Settings tab opened")
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.refresh_button.pack_forget()
        self.clear_settings_widgets()

        self.about_button = ctk.CTkButton(
            self,
            text="About Me",
            fg_color="#5a189a",
            hover_color="#3a0ca3",
            command=lambda: webbrowser.open("https://github.com/antalervin19")
        )
        self.about_button.place(relx=1.0, rely=1.0, anchor="se", x=-50, y=-90)

        self.created_by_label = ctk.CTkLabel(
            self,
            text="Created by: antalervin19",
            text_color="#aaaaaa",
            font=("Segoe UI", 12)
        )
        self.created_by_label.place(relx=1.0, rely=1.0, anchor="se", x=-55, y=-60)

        self.thanks_label = ctk.CTkLabel(
            self,
            text="Huge Thanks to: CrackX02",
            text_color="#de0707",
            font=("Segoe UI", 12)
        )
        self.thanks_label.place(relx=1.0, rely=1.0, anchor="se", x=-55, y=-35)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = ModManagerApp()
    app.mainloop()

# /* GameManager.py */ #

# COPYRIGHT (C) 2025 antalervin19
# I do NOT give ANYONE permission to copy, modify or redistribute code in this file!
# If you want to use code from this in your own project(s), you HAVE to ask me for permission first!
# Contacts:
# Discord: antalervin19
# Web: https://www.iggames.eu

import psutil
import webbrowser
from pathlib import Path
import time
from LogManager import log
import win32api

def kill_gameprocess():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == "ScrapMechanic.exe".lower():
                proc.kill()
                log("Killed SM Process!")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            log(f"Could not kill game process! {e}")

def run_gameprocess():
    steamurl = "steam://rungameid/387990"
    try:
        webbrowser.open(steamurl)
        log("Launching ScrapMechanic!")
    except Exception as e:
        log(f"Failed to launch ScrapMechanic: {e}")

def scan_and_get_game_path():
    game_path = None
    while not game_path:
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['name'].lower() == "ScrapMechanic.exe".lower():
                    game_path = Path(proc.info['exe']).resolve().parent.parent
                    log(f"Game path detected: {game_path}")
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                log(f"Could not access process: {e}")

        if not game_path:
            log("Waiting for Scrap Mechanic to launch...")
            time.sleep(2)

    kill_gameprocess()
    time.sleep(2)

    return game_path

def get_exe_version_info(file_path):
    try:
        info = win32api.GetFileVersionInfo(file_path, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        file_version_full = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"

        pms = info['ProductVersionMS']
        pls = info['ProductVersionLS']
        product_version_full = f"{pms >> 16}.{pms & 0xFFFF}.{pls >> 16}.{pls & 0xFFFF}"

        file_version = ".".join(file_version_full.split(".")[:3])
        product_version = ".".join(product_version_full.split(".")[:3])

        return file_version, product_version
    except Exception as e:
        print(f"Failed to get version info: {e}")
        return None, None

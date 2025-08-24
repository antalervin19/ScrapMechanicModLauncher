# /* FileManager.py */ #

# COPYRIGHT (C) 2025 antalervin19
# I do NOT give ANYONE permission to copy, modify or redistribute code in this file!
# If you want to use code from this in your own project(s), you HAVE to ask me for permission first!
# Contacts:
# Discord: antalervin19
# Web: https://www.iggames.eu

import asyncio
import aiofiles
import os
from pathlib import Path
from LogManager import log
import requests

async def copy_file(src_path: Path, dest_path: Path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(src_path, 'rb') as src_file:
        content = await src_file.read()
    async with aiofiles.open(dest_path, 'wb') as dest_file:
        await dest_file.write(content)

async def install_mod(mod_folder: Path, game_folder: Path):
    mod_files_path = mod_folder / "ModFiles"
    tasks = []
    for root, dirs, files in os.walk(mod_files_path):
        dirs[:] = [d for d in dirs if not d.startswith("IGNORE#")]
        for file in files:
            if file.startswith("IGNORE#"):
                continue
            src_file_path = Path(root) / file
            relative_path = src_file_path.relative_to(mod_files_path)
            dest_file_path = game_folder / relative_path
            tasks.append(copy_file(src_file_path, dest_file_path))
    await asyncio.gather(*tasks)
    log("✅ Mod installed successfully.")

async def uninstall_mod(mod_folder: Path, game_folder: Path):
    uninstall_path = mod_folder / "Uninstall"
    mod_files_path = mod_folder / "ModFiles"
    tasks = []
    for root, _, files in os.walk(mod_files_path):
        for file in files:
            mod_file_path = Path(root) / file
            relative_path = mod_file_path.relative_to(mod_files_path)
            game_file_path = game_folder / relative_path
            uninstall_file_path = uninstall_path / relative_path

            if uninstall_file_path.exists():
                tasks.append(copy_file(uninstall_file_path, game_file_path))
            else:
                if game_file_path.exists():
                    log(f"🗑️ Deleting modded file: {game_file_path}")
                    game_file_path.unlink()
    await asyncio.gather(*tasks)
    log("Mod uninstalled successfully.")


# ——— Network Checksum Disabler Download Helper ——— #

def get_latest_asset_download_url(owner: str, repo: str, asset_name: str) -> str:
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    resp = requests.get(api_url)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch latest release: HTTP {resp.status_code}")
    release = resp.json()
    for asset in release.get("assets", []):
        if asset.get("name") == asset_name:
            return asset["browser_download_url"]
    raise FileNotFoundError(f"Asset '{asset_name}' not found in latest release.")

def download_file(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    log(f"Downloading {url} -> {dest}")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    log(f"Downloaded successfully: {dest}")

def ensure_network_checksum_disabler(resources_dir: Path):
    owner = "ScrappySM"
    repo = "Network-Checksum-Disabler"
    asset_name = "NetworkChecksumDisabler.dll"

    core_dir = resources_dir / "Core"
    dll_path = core_dir / asset_name

    if not dll_path.exists():
        log("NetworkChecksumDisabler.dll not found. Creating Core/ and downloading latest version.")
        download_url = get_latest_asset_download_url(owner, repo, asset_name)
        download_file(download_url, dll_path)
    else:
        log("NetworkChecksumDisabler.dll already present; skipping download.")

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

async def copy_file(src_path: Path, dest_path: Path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(src_path, 'rb') as src_file:
        content = await src_file.read()
    async with aiofiles.open(dest_path, 'wb') as dest_file:
        await dest_file.write(content)

async def install_mod(mod_folder: Path, game_folder: Path):
    mod_files_path = mod_folder / "ModFiles"
    tasks = []

    for root, _, files in os.walk(mod_files_path):
        for file in files:
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
# ScrapMechanicModLauncher

A Work-In-Progress mod loader and launcher for the game **Scrap Mechanic**.

---

## Table of Contents

- [Download and Install](#download-install)
- [Mod Creation](#mod-creation)
  - [Mod Content Structure](#mod-content-structure)
  - [File and Folder Structure](#file-and-folder-structure)

---

## Download and Install

To get started with the **ScrapMechanicModLauncher**, follow these steps:

1. **Download** the latest release from the [releases section](https://github.com/antalervin19/ScrapMechanicModLauncher/releases).
2. **Unzip** the downloaded file to a desired location on your computer.
3. Run the `ScrapMechanicModLauncher.exe` file.


---

## Mod Creation

If you'd like to create your own mods, follow the steps below to set up your mod folder and its contents.

### Mod Content Structure

1. Create a folder in the `./Mods/` directory for your mod. This will be the base folder for your mod.
   
2. Inside the new mod folder, create a **`Mod.content`** file with the following structure:

```json
{
    "title": "ModName",
    "description": "Mod Description",
    "author": "YourName",
    "date": "year-month-day",
    "version": "1.0.0",
    "GameVersion": "0.7.3"
}

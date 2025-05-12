# ScrapMechanicModLauncher

A Work-In-Progress mod loader and launcher for the game **Scrap Mechanic**.

---

## Table of Contents

- [Download and Install](#download-and-install)
- [Mod Creation](#mod-creation)
  - [Mod Content Structure](#mod-content-structure)
  - [File and Folder Structure](#file-and-folder-structure)

---

## Download and Install

To get started with the **ScrapMechanicModLauncher**, follow these steps:

1. **Download** the latest release from the [releases section](https://github.com/antalervin19/ScrapMechanicModLauncher/releases)
2. **Unzip** the downloaded file to a desired location on your computer.
3. Run the `ScrapMechanicModLauncher.exe` file.

---

## Mod Creation

If you'd like to create your own mods, follow the steps below to set up your mod folder and its contents.

### Mod Content Structure

1. Create a folder in the `./Mods/` directory for your mod. This will be the base folder for your mod.
2. Inside the new mod folder, create a `Mod.content` file with the following content:

```json
{
  "title": "ModName",
  "description": "Mod Description",
  "author": "YourName",
  "date": "year-month-day",
  "version": "1.0.0",
  "GameVersion": "0.7.3"
}
```

### File and Folder Structure

Once the `Mod.content` file is created, you can start adding the actual files that make up your mod.

The launcher expects mods to follow the same folder structure as the game. Your mod should include:

```plaintext
Mods/
└── ExampleMod/
    ├── ModFiles/       # Here are your mod files
    └── Uninstall/      # Original files of the game
```

- `ModFiles/`: This folder should contain all the files that make up your mod, such as scripts, textures, etc.
- `Uninstall/`: This folder contains the original files of the game that will be restored when uninstalling the mod.

**Example:**

If your mod is called `AwesomeMod`, the structure would look like this:

```plaintext
Mods/
└── AwesomeMod/
    ├── ModFiles/
    │   └── Survival/
    │       └── Scripts/
    │           └── game/
    │               └── SurvivalGame.lua # Modified File
    └── Uninstall/
        └── Survival/
            └── Scripts/
                └── game/
                    └── SurvivalGame.lua #Original File
```

Once this is set up, you can load your mod using the ScrapMechanicModLauncher.

## License

COPYRIGHT (C) 2025 antalervin19
I do NOT give ANYONE permission to copy, modify or redistribute code in this file!
If you want to use code from this in your own project(s), you HAVE to ask me for permission first!
Contacts:
Discord: antalervin19
Web: https://www.iggames.eu
---

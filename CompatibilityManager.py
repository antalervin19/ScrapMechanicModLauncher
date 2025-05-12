import win32api

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

exe_path = r"./ScrapMechanic.exe"
fv, pv = get_exe_version_info(exe_path)
print(f"File Version: {fv}")
print(f"Product Version: {pv}")

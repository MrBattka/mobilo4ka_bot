from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from tkinter import messagebox

GITHUB_USER = "MrBattka"
GITHUB_REPO = "mobilo4ka_bot"

REMOTE_VERSION_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.txt"
)

UPDATE_ZIP_URL = (
    f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"
    "/releases/latest/download/Mobilochka.zip"
)


if getattr(sys, "frozen", False):
    # Launcher.exe находится в ...\mobilochka_bot\dist
    LAUNCHER_DIR = Path(sys.executable).resolve().parent
    BASE_DIR = LAUNCHER_DIR.parent
else:
    # launcher.py находится в корне проекта
    BASE_DIR = Path(__file__).resolve().parent

APP_FILE = BASE_DIR / "Mobilo4ka.exe"
LOCAL_VERSION_FILE = BASE_DIR / "version.txt"

PROTECTED_FILES = {
    ".env",
    "Mobilo4kaPrice.exe",
    "Mobilo4kaPrice.exe",
}


def get_version(value: str):
    try:
        return tuple(map(int, value.strip().split(".")))
    except ValueError:
        return (0, 0, 0)


def read_local_version():
    if not LOCAL_VERSION_FILE.exists():
        return "0.0.0"

    return LOCAL_VERSION_FILE.read_text(encoding="utf-8").strip()


def read_remote_version():
    with urllib.request.urlopen(REMOTE_VERSION_URL, timeout=15) as response:
        return response.read().decode("utf-8").strip()


def download_update():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        archive_path = temp_dir / "update.zip"
        extract_dir = temp_dir / "files"

        urllib.request.urlretrieve(UPDATE_ZIP_URL, archive_path)

        with zipfile.ZipFile(archive_path, "r") as archive:
            archive.extractall(extract_dir)

        root_items = list(extract_dir.iterdir())
        root_files = [item for item in root_items if item.is_file()]
        root_folders = [item for item in root_items if item.is_dir()]

        if not root_files and len(root_folders) == 1:
            source_dir = root_folders[0]
        else:
            source_dir = extract_dir

        for source_file in source_dir.rglob("*"):
            if not source_file.is_file():
                continue

            relative_path = source_file.relative_to(source_dir)

            if relative_path.name in PROTECTED_FILES:
                continue

            target_file = BASE_DIR / relative_path
            target_file.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(source_file, target_file)


def start_application():
    if not APP_FILE.exists():
        messagebox.showerror(
            "Ошибка запуска",
            f"Не найден файл:\n{APP_FILE}\n\n"
            "Обновление не было загружено.",
        )
        return False

    subprocess.Popen([str(APP_FILE)], cwd=str(BASE_DIR))
    return True


def main():
    try:
        local_version = read_local_version()
        remote_version = read_remote_version()

        # Скачивать также при отсутствии основного EXE
        update_required = (
            not APP_FILE.exists()
            or get_version(remote_version) > get_version(local_version)
        )

        if update_required:
            download_update()

        if not APP_FILE.exists():
            raise FileNotFoundError(
                f"После обновления не найден файл: {APP_FILE}"
            )

        start_application()

    except Exception as error:
        messagebox.showerror(
            "Ошибка обновления",
            f"{type(error).__name__}: {error}\n\n"
            "Проверьте интернет и наличие Mobilo4ka.exe "
            "в Mobilochka.zip на GitHub Release."
        )

        # Не запускать несуществующий файл
        if APP_FILE.exists():
            start_application()


if __name__ == "__main__":
    main()
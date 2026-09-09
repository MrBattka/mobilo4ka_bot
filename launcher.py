from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

GITHUB_USER = "MrBattka"
GITHUB_REPO = "mobilo4ka_bot"

REMOTE_VERSION_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.txt"
)

UPDATE_ZIP_URL = (
    f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"
    "/releases/latest/download/Mobilochka.zip"
)


BASE_DIR = Path(sys.executable).resolve().parent
APP_FILE = BASE_DIR / "Mobilochka.exe"
LOCAL_VERSION_FILE = BASE_DIR / "version.txt"

PROTECTED_FILES = {
    ".env",
    "suplires_site.json",
    "Launcher.exe",
    "launcher.exe",
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

        # Если архив содержит одну вложенную папку — используем её
        folders = [item for item in extract_dir.iterdir() if item.is_dir()]
        source_dir = folders[0] if len(folders) == 1 else extract_dir

        for source_file in source_dir.rglob("*"):
            if not source_file.is_file():
                continue

            relative_path = source_file.relative_to(source_dir)

            if relative_path.name in PROTECTED_FILES:
                continue

            target_file = BASE_DIR / relative_path
            target_file.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(source_file, target_file)


def main():
    try:
        local_version = read_local_version()
        remote_version = read_remote_version()

        if get_version(remote_version) > get_version(local_version):
            print(f"Обновление: {local_version} -> {remote_version}")
            download_update()

        subprocess.Popen([str(APP_FILE)], cwd=BASE_DIR)

    except Exception as error:
        print(f"Ошибка обновления: {error}")
        subprocess.Popen([str(APP_FILE)], cwd=BASE_DIR)


if __name__ == "__main__":
    main()
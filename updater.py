from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent


def run_git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        if result.stderr:
            print(result.stderr)
        return False

    return True


def get_local_version():
    path = BASE_DIR / "version.txt"

    if not path.exists():
        return "0.0.0"

    return path.read_text(encoding="utf-8").strip()


def get_remote_version():
    result = subprocess.run(
        ["git", "show", "origin/main:version.txt"],
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def main():
    print("Проверка обновлений...")

    if not run_git("fetch", "origin", "main"):
        print("Не удалось проверить обновления.")
        input("Нажмите Enter для выхода...")
        return 1

    local_version = get_local_version()
    remote_version = get_remote_version()

    print(f"Текущая версия: {local_version}")
    print(f"Версия на сервере: {remote_version}")

    if remote_version and remote_version != local_version:
        print("Найдена новая версия. Выполняется обновление...")

        if not run_git("pull", "--ff-only", "origin", "main"):
            print("Обновление не выполнено.")
            input("Нажмите Enter для выхода...")
            return 1

        print("Обновление успешно установлено.")
    else:
        print("Обновлений нет.")

    print("Запуск приложения...")
    return subprocess.call(
        [sys.executable, str(BASE_DIR / "gui_tool.py")],
        cwd=BASE_DIR,
    )


if __name__ == "__main__":
    raise SystemExit(main())
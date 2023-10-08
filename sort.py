import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging

# Створюємо парсер командного рядка за допомогою argparse
parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

# Отримуємо аргументи з командного рядка
args = vars(parser.parse_args())
source = Path(args.get("source"))
output = Path(args.get("output"))

# Створюємо список для зберігання папок
folders = []

# Функція для рекурсивного збору папок із вказаної директорії та її підпапок
def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)

# Функція для копіювання файлів з однієї папки у відповідну підпапку за розширенням
def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            ext_folder = output / ext
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)
                copyfile(el, ext_folder / el.name)
            except OSError as err:
                logging.error(err)

if __name__ == "__main__":
    # Налаштування журналування
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    # Додаємо вхідну папку до списку для обробки
    folders.append(source)
    
    # Запускаємо функцію для збору списку папок
    grabs_folder(source)
    
    # Виводимо список папок, які будуть оброблятися
    print(folders)

    # Створюємо список потоків для обробки папок та копіювання файлів
    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    # Чекаємо завершення роботи всіх потоків
    [th.join() for th in threads]

    # Виводимо повідомлення про завершення та можливість видалення вхідної папки
    print(f"Можна видаляти {source}")

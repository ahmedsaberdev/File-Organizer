import json
import shutil
import time
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', required=True, type=Path, help='The target folder to organize files in')
args = parser.parse_args()

class OrganizeHandler(FileSystemEventHandler):
  def __init__(self, folder: Path):
    self.folder = folder
  
  def on_created(self, event):
    if not event.is_directory:
      time.sleep(1)
      folder_organizer(self.folder)
    
  def on_moved(self, event):
    if not event.is_directory:
      folder_organizer(self.folder)

with open('config.json', 'r') as f:
  config = json.load(f)

IGNORE_EXTENTIONS = config['ignore_extentions']
CATEGORIES = config['categories']

def folder_organizer(folder):
  for entry in folder.iterdir():
    if entry.is_file():
      ext = entry.suffix.lower()
      moved = False

      for category, extentions in CATEGORIES.items():
        if ext in IGNORE_EXTENTIONS:
          break
        if ext in extentions:
          move_file(entry, folder / category)
          moved = True
          break

      if not moved:
        move_file(entry, folder / "Others")

def move_file(file, dest_folder):
  dest_folder.mkdir(exist_ok=True)
  for attemts in range(10):
    try:
      shutil.move(str(file), str(dest_folder / file.name))
      print(f'Moved {file.name} -> {dest_folder.name}')
      return
    except PermissionError:
      print(f'File {file.name} is in use. Retrying in 1s...')
      time.sleep(1)
  print(f'Failed to move {file.name} after multiable attempts.')


if __name__ == "__main__":
  target_folder = args.target
  folder_organizer(target_folder)

  event_handler = OrganizeHandler(target_folder)
  observer = Observer()
  observer.schedule(event_handler, str(target_folder), recursive=False)
  observer.start()

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()

  observer.join()

# Still need to do:
# 1. Exception handling
# 2. Handling of duplicates
# 3. Dry run mode (optional)
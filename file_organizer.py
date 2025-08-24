import re
import json
import shutil
import time
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Parser for adding (-t, --target) argument to the CLI.
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', required=True, type=Path, help='The target folder to organize files in')
args = parser.parse_args()

# Custom Handler to organize new files created of moved dynamicly
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

# Config file
with open('config.json', 'r') as f:
  config = json.load(f)

IGNORE_EXTENTIONS = config['ignore_extentions']
CATEGORIES = config['categories']

# Unique name generator to resolve the duplicate names conflect
def get_unique_name(file: Path, dest_folder: Path):
  base_name = file.stem
  ext = file.suffix

  pattern = re.compile(rf"^{re.escape(base_name)}(?: \((\d+)\))?$", re.IGNORECASE)

  max_num = 0
  for entry in dest_folder.iterdir():
    if entry.is_file() and (entry.suffix.lower() == ext.lower()):
      match = pattern.match(entry.stem)
      if match:
        if match.group(1):
          num = int(match.group(1))
          max_num = max(max_num, num)
        else:
          max_num = max(max_num, 0)
  
  if max_num > 0 or (dest_folder / file.name).exists():
    new_name = f'{base_name} ({max_num + 1}){ext}'
    return dest_folder / new_name
  else:
    return dest_folder / file.name

# Organize and move files to its specified folder 
def folder_organizer(folder: Path):
  for entry in folder.iterdir():
    if entry.is_file():
      ext = entry.suffix.lower()
      moved = False
      ignore = False

      for category, extentions in CATEGORIES.items():
        if ext in IGNORE_EXTENTIONS:
          ignore = True
          break
        if ext in extentions:
          move_file(entry, folder / category)
          moved = True
          break

      if not (moved or ignore):
        move_file(entry, folder / "Others")

# Move files to destination folder with a unique name and waiting time to avoid permission error.
def move_file(file: Path, dest_folder: Path):
  dest_folder.mkdir(exist_ok=True)
  unique_file_name = Path(get_unique_name(file, dest_folder))
  for attemts in range(10):
    try:
      shutil.move(str(file), str(dest_folder / unique_file_name))
      print(f'Moved {unique_file_name} -> {dest_folder.name}')
      return
    except PermissionError:
      print(f'File {unique_file_name} is in use. Retrying in 1s...')
      time.sleep(1)
  print(f'Failed to move {unique_file_name} after multiable attempts.')

# Main program with file not found error handling if the target folder doesn't exist and an observer to update the folder in the case of new files added or moved dynamicly 
if __name__ == "__main__":
  try:
    target_folder = args.target
    if not target_folder.exist():
      raise FileNotFoundError(f'Target folder {target_folder} not found.')
    folder_organizer(target_folder)
  except FileNotFoundError as exception:
    print(exception)

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
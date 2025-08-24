import shutil
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', required=True, type=str, nargs=1, help='The target folder to organize files in')

args = parser.parse_args()

CATEGORIES = {
  "Images" : [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
  "Videos" : [".mp4", ".mkv", ".mov", ".avi"],
  "Documents" : [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
  "Music" : [".mp3", ".wav", ".flac", ".ogg"],
  "Archives" : [".zip", ".rar", ".tar", ".gz"],
  "Scripts" : [".py", ".js", ".sh"],
  "Source Files" : [".cpp", ".c", ".java"],
  "Applications" : [".exe"],
  "Torrents" : [".torrent"],
  "Others" : []
}

TARGET_FOLDER = Path(args.target[0])

def folder_organizer(folder):
  for entry in folder.iterdir():
    if entry.is_file():
      ext = entry.suffix.lower()
      moved = False

      for category, extentions in CATEGORIES.items():
        if ext in extentions:
          move_file(entry, folder / category)
          moved = True
          break

      if not moved:
        move_file(entry, folder / "Others")

def move_file(file, dest_folder):
  dest_folder.mkdir(exist_ok=True)
  shutil.move(str(file), str(dest_folder / file.name))
  print(f'Moved {file.name} -> {dest_folder.name}')


if __name__ == "__main__":
  target = Path(TARGET_FOLDER)
  folder_organizer(target)
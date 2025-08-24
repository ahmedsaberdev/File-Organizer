# File Organizer

A Python script that automatically organizes files into folders based on their extensions.
Supports a customizable configuration file so you can define your own folder structure.

## Features

- Organize files by extentions (e.g., `.jpg`, `.pdf`, `.mp4`, etc.)
- Supports a JSON config file for custom folder mappings
- Handles duplicate file names by adding incremental numbers (e.g., `file (1).txt`)
- Retries moving files if they are in use (automatically handles permission error).

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ahmedsaberdev/File-Organizer
cd File-Organizer
```

2. (Optional) Create a virtual enviroment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install watchdog module (if not already installed)

```base
pip install watchdog
```

## Usage

Run the script with:

```bash
python file_organizer.py --target /path/to/folder
```

P.S. Make sure to run the script using the python version you installed watchdog within (or use a VE).

Example Config (config.json):

```bash
{
    "Images": [".jpg", ".jpeg", ".png"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".avi"]
}
```

## Example

Before:

```bash
Downloads/
  photo.jpg
  report.pdf
  movie.mp4
```

After running:

```bash
Downloads/
  Images/photo.jpg
  Documents/report.pdf
  Videos/movie.mp4
```

## Author

Ahmed Saber - Computer Science student Cairo University.

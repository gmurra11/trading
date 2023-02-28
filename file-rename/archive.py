import os
import shutil

# Original files directory
src_dir = "/home/gmurray/Downloads"

# Archive directory
archive_dir = "/home/gmurray/Downloads/archive"

# Get a list of all files in the source directory
files = os.listdir(src_dir)

# Loop through each file and move it to the archive directory if it starts with "lvt"
for file in files:
    if file.startswith("lvt"):
        # Construct the full path of the file
        src_path = os.path.join(src_dir, file)
        archive_path = os.path.join(archive_dir, file)
        # Move the file to the archive directory
        shutil.copy(src_path, archive_path)

import os
import datetime
import shutil

# Original files directory
src_dir = "/home/gmurray/Downloads"

# Output directory
dst_dir = "/home/gmurray/REPO/trading/data"

# Daily output directory
daily_dir = "/home/gmurray/REPO/trading/data/daily"

# Weekly output directory
weekly_dir = "/home/gmurray/REPO/trading/data/weekly"

# Mapping of old filenames to new filenames
filename_map = {
    "lvt_chart ETH Buy_Sell Volume Last  Month 31MAR23 .csv": "LVT-MONTHLY-31MAR23.csv",
    "lvt_chart ETH Buy_Sell Volume Last  Month 30JUN23 .csv": "LVT-MONTHLY-30JUN23.csv",
    "lvt_chart ETH Buy_Sell Volume Last  Month 29SEP23 .csv": "LVT-MONTHLY-29SEP23.csv",
    "lvt_chart ETH Buy_Sell Volume Last  COMMON.Week 29SEP23 .csv": "LVT-WEEKLY-29SEP23.csv",
    "lvt_chart ETH Buy_Sell Volume Last  COMMON.Week 30JUN23 .csv": "LVT-WEEKLY-30JUN23.csv",
    "lvt_chart ETH Buy_Sell Volume Last  COMMON.Week 31MAR23 .csv": "LVT-WEEKLY-31MAR23.csv"
}

# Get the modification time of the destination directory
dst_dir_stat = os.stat(dst_dir)
dst_dir_mod_time = dst_dir_stat.st_mtime

# Get the current date and time
current_date = datetime.datetime.now().date()

# Clean up old daily files with names starting with "LVT-"
# and move the old files with names starting with "LVT-" to the daily directory
# if the modification time of the destination directory is not today
if datetime.datetime.fromtimestamp(dst_dir_mod_time).date() != current_date:
    for filename in os.listdir(daily_dir):
        if filename.startswith("LVT-"):
            os.remove(os.path.join(daily_dir, filename))

    for filename in os.listdir(dst_dir):
        if filename.startswith("LVT-"):
            src_path = os.path.join(dst_dir, filename)
            dst_path = os.path.join(daily_dir, filename)
            os.rename(src_path, dst_path)

    # Copy daily files to weekly directory if it's Sunday
    if current_date.weekday() == 6:
        for filename in os.listdir(daily_dir):
            if filename.startswith("LVT-"):
                src_path = os.path.join(daily_dir, filename)
                dst_path = os.path.join(weekly_dir, filename)
                shutil.copy2(src_path, dst_path)

# Delete existing files in the destination directory
for filename in os.listdir(dst_dir):
    if filename in filename_map.values():
        os.remove(os.path.join(dst_dir, filename))

# Loop through the files in the source directory
for filename in os.listdir(src_dir):
    # Check if the file is in the mapping
    if filename in filename_map:
        # Construct the source and destination paths
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename_map[filename])

        # Rename the file
        os.rename(src_path, dst_path)

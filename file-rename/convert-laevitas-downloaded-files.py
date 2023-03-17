import os
import datetime
import shutil
import fileinput
import re

# Only Change these Constants when the weekly options change.  Hopefully initially small maintenance.
LESS_THAN_50_DAYS = "28APR23"
LESS_THAN_80_DAYS = "26MAY23"

# Get the current date and time
current_date = datetime.datetime.now().date()

def delete_old_files(directory):
    current_date = datetime.datetime.now().date()

    for filename in os.listdir(directory):
        if filename.startswith("LVT-"):
            filepath = os.path.join(directory, filename)
            modification_time = os.path.getmtime(filepath)
            modification_date = datetime.datetime.fromtimestamp(modification_time).date()

            if modification_date != current_date:
                os.remove(filepath)

def move_files_to_daily_directory(src_directory, dst_directory):
    for filename in os.listdir(src_directory):
        if filename.startswith("LVT-"):
            src_path = os.path.join(src_directory, filename)
            dst_path = os.path.join(dst_directory, filename)
            os.rename(src_path, dst_path)

def copy_files_to_weekly_directory(src_directory, dst_directory):
    for filename in os.listdir(src_directory):
        if filename.startswith("LVT-"):
            src_path = os.path.join(src_directory, filename)
            dst_path = os.path.join(dst_directory, filename)
            shutil.copy2(src_path, dst_path)

def delete_existing_files(directory, filename_map):
    for filename in os.listdir(directory):
        if filename in filename_map.values():
            filepath = os.path.join(directory, filename)
            os.remove(filepath)

def rename_files(src_directory, dst_directory, filename_map):
    for filename in os.listdir(src_directory):
        if filename in filename_map:
            src_path = os.path.join(src_directory, filename)
            dst_path = os.path.join(dst_directory, filename_map[filename])
            os.rename(src_path, dst_path)

def main():
    # Original files directory
    src_dir = "/home/gmurray/Downloads"

    # Output directory quarterly
    dst_dir_options = "/home/gmurray/REPO/trading/data"

    # Output directory skew
    dst_dir_skew_options = "/home/gmurray/REPO/trading/data-skew-test"

    # Daily output directory for quaterly data
    daily_dir_options = "/home/gmurray/REPO/trading/data/daily"

    # Weekly output directory for quaterly data
    weekly_dir_options = "/home/gmurray/REPO/trading/data/weekly"

    # Daily output directory for skew data
    daily_dir_skew_options = "/home/gmurray/REPO/trading/data-skew-test/daily"

    # Weekly output directory for skew data
    weekly_dir_skew_options = "/home/gmurray/REPO/trading/data-skew-test/weekly"

    filename_map_50_or_80_days = {
        f"lvt_chart ETH Buy_Sell Volume Last  Month {LESS_THAN_50_DAYS} .csv": f"LVT-MONTHLY-{LESS_THAN_50_DAYS}-ETH.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  Month {LESS_THAN_80_DAYS} .csv": f"LVT-MONTHLY-{LESS_THAN_80_DAYS}-ETH.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  COMMON.Week {LESS_THAN_50_DAYS} .csv": f"LVT-WEEKLY-{LESS_THAN_50_DAYS}-ETH.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  COMMON.Week {LESS_THAN_80_DAYS} .csv": f"LVT-WEEKLY-{LESS_THAN_80_DAYS}-ETH.csv",
        f"lvt_chart BTC Buy_Sell Volume Last  Month {LESS_THAN_50_DAYS} .csv": f"LVT-MONTHLY-{LESS_THAN_50_DAYS}-BTC.csv",
        f"lvt_chart BTC Buy_Sell Volume Last  Month {LESS_THAN_80_DAYS} .csv": f"LVT-MONTHLY-{LESS_THAN_80_DAYS}-BTC.csv",
        f"lvt_chart BTC Buy_Sell Volume Last  COMMON.Week {LESS_THAN_50_DAYS} .csv": f"LVT-WEEKLY-{LESS_THAN_50_DAYS}-BTC.csv",
        f"lvt_chart BTC Buy_Sell Volume Last  COMMON.Week {LESS_THAN_80_DAYS} .csv": f"LVT-WEEKLY-{LESS_THAN_80_DAYS}-BTC.csv"
    }

    filename_map_skew = {
        f"lvt_chart Skew 25Δ ETH .csv": f"LVT-SKEW25-1D-ETH.csv",
        f"lvt_chart Skew 25Δ ETH  (1).csv": f"LVT-SKEW25-1W-ETH.csv",
        f"lvt_chart Skew 25Δ ETH  (2).csv": f"LVT-SKEW25-1M-ETH.csv",
        f"lvt_chart Skew 25Δ BTC .csv": f"LVT-SKEW25-1D-BTC.csv",
        f"lvt_chart Skew 25Δ BTC  (1).csv": f"LVT-SKEW25-1W-BTC.csv",
        f"lvt_chart Skew 25Δ BTC  (2).csv": f"LVT-SKEW25-1M-BTC.csv",
        f"lvt_chart Time Lapse Skew  ETH .csv": f"LVT-ETH-25DELTA-IV-CHANGE.csv",
        f"lvt_chart Time Lapse Skew  BTC .csv": f"LVT-BTC-25DELTA-IV-CHANGE.csv",
        f"lvt_chart Multi-Expiry Skew ETH .csv": f"LVT-MULTI-EXPIRY-SKEW-ETH.csv",
        f"lvt_chart Multi-Expiry Skew BTC .csv": f"LVT-MULTI-EXPIRY-SKEW-BTC.csv"
    }

    # WEEKLY DIRECTROY CLEAN UP SUNDAY
    if current_date.weekday() == 6:
        # Delete existing files from weekly directory for quarterly data
        delete_existing_files(weekly_dir_options, filename_map_50_or_80_days)
        # Copy files to weekly directory for quarterly data
        copy_files_to_weekly_directory(daily_dir_options, weekly_dir_options)

    # SKEW DIRECTROY CLEAN UP SUNDAY
    if current_date.weekday() == 6:
        # Delete existing files from weekly directory for weekly data
        delete_existing_files(weekly_dir_skew_options, filename_map_skew)
        # Copy files to weekly directory for weekly data
        copy_files_to_weekly_directory(daily_dir_skew_options, weekly_dir_skew_options)

    # Get the modification time of the destination directory, ie:have we run today already or is this a snapshot?
    dst_dir_options_stat = os.stat(dst_dir_options)
    dst_dir_options_mod_time = dst_dir_options_stat.st_mtime
    dst_dir_skew_options_stat = os.stat(dst_dir_skew_options)
    dst_dir_skew_options_mod_time = dst_dir_skew_options_stat.st_mtime

    # Move files to daily directory for volume data
    if datetime.datetime.fromtimestamp(dst_dir_options_mod_time).date() != current_date:
        # Delete old files from daily directory for volume data
        delete_old_files(daily_dir_options)
        move_files_to_daily_directory(dst_dir_options, daily_dir_options)

    # Move files to daily directory for skew data
    if datetime.datetime.fromtimestamp(dst_dir_skew_options_mod_time).date() != current_date:
        # Delete old files from daily directory for weekly data
        delete_old_files(daily_dir_skew_options)
        move_files_to_daily_directory(dst_dir_skew_options, daily_dir_skew_options)

    # Remove files from destination before coping from ~Download
    #delete_existing_files(dst_dir_weekly_options, filename_map_weekly)
    # Rename files in source directory for weekly data
    rename_files(src_dir, dst_dir_options, filename_map_50_or_80_days)

    # Remove files from destination before coping from ~Download
    #delete_existing_files(dst_dir_skew_options, filename_map_skew)
    # Rename files in source directory for skew data
    rename_files(src_dir, dst_dir_skew_options, filename_map_skew)

if __name__ == "__main__":
    main()

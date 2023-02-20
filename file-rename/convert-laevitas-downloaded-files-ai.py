import os
import datetime
import shutil

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
            print(dst_path)
            os.rename(src_path, dst_path)

def main():
    # Original files directory
    src_dir = "/home/gmurray/Downloads"

    # Output directory quarterly
    dst_dir_quarterly_options = "/home/gmurray/REPO/trading/data-quarterly"

    # Output directory weekly
    dst_dir_weekly_options = "/home/gmurray/REPO/trading/data-weekly"

    # Daily output directory for quaterly data
    daily_dir_quarterly_options = "/home/gmurray/REPO/trading/data-quarterly/daily"

    # Weekly output directory for quaterly data
    weekly_dir_quarterly_options = "/home/gmurray/REPO/trading/data-quarterly/weekly"

    # Daily output directory for weekly data
    daily_dir_weekly_options = "/home/gmurray/REPO/trading/data-weekly/daily"

    # Weekly output directory for weekly data
    weekly_dir_weekly_options = "/home/gmurray/REPO/trading/data-weekly/weekly"

    # Only Change these Constants when the weekly options change.  Hopefully initially small maintenance.
    next_fri = "24FEB23"
    follwoing_fri = "03MAR23"
    third_fri = "10MAR23"

    # Get the current date and time
    current_date = datetime.datetime.now().date()

    # Mapping of old filenames to new filenames
    filename_map_quarterly = {
        "lvt_chart ETH Buy_Sell Volume Last  Month 31MAR23 .csv": "LVT-MONTHLY-31MAR23.csv",
        "lvt_chart ETH Buy_Sell Volume Last  Month 30JUN23 .csv": "LVT-MONTHLY-30JUN23.csv",
        "lvt_chart ETH Buy_Sell Volume Last  Month 29SEP23 .csv": "LVT-MONTHLY-29SEP23.csv",
        "lvt_chart ETH Buy_Sell Volume Last  COMMON.Week 29SEP23 .csv": "LVT-WEEKLY-29SEP23.csv",
        "lvt_chart ETH Buy_Sell Volume Last  COMMON.Week 30JUN23 .csv": "LVT-WEEKLY-30JUN23.csv",
        "lvt_chart ETH Buy_Sell Volume Last  COMMON.Week 31MAR23 .csv": "LVT-WEEKLY-31MAR23.csv"
    }

    filename_map_weekly = {
        f"lvt_chart ETH Buy_Sell Volume Last  Month {next_fri} .csv": f"LVT-MONTHLY-{next_fri}.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  Month {follwoing_fri} .csv": f"LVT-MONTHLY-{follwoing_fri}.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  Month {third_fri} .csv": f"LVT-MONTHLY-{third_fri}.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  COMMON.Week {next_fri} .csv": f"LVT-WEEKLY-{next_fri}.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  COMMON.Week {follwoing_fri} .csv": f"LVT-WEEKLY-{follwoing_fri}.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  COMMON.Week {third_fri} .csv": f"LVT-WEEKLY-{third_fri}.csv"
    }


    # WEEKLY DIRECTROY CLEAN UP
    if current_date.weekday() == 6:
        # Delete existing files from weekly directory for quarterly data
        delete_existing_files(weekly_dir_quarterly_options, filename_map_quarterly)
        # Copy files to weekly directory for quarterly data
        copy_files_to_weekly_directory(daily_dir_quarterly_options, weekly_dir_quarterly_options)

    # WEEKLY DIRECTROY CLEAN UP
    if current_date.weekday() == 6:
        # Delete existing files from weekly directory for weekly data
        delete_existing_files(weekly_dir_weekly_options, filename_map_weekly)
        # Copy files to weekly directory for weekly data
        copy_files_to_weekly_directory(daily_dir_weekly_options, weekly_dir_weekly_options)

    # Delete old files from daily directory for quarterly data
    delete_old_files(daily_dir_quarterly_options)

    # Delete old files from daily directory for weekly data
    delete_old_files(daily_dir_weekly_options)

    # Get the modification time of the destination directory, ie:have we run today already and is this a snapshot
    dst_dir_quarterly_options_stat = os.stat(dst_dir_quarterly_options)
    dst_dir_quarterly_options_mod_time = dst_dir_quarterly_options_stat.st_mtime
    dst_dir_weekly_options_stat = os.stat(dst_dir_weekly_options)
    dst_dir_weekly_options_mod_time = dst_dir_weekly_options_stat.st_mtime

    # Move files to daily directory for quarterly data
    if datetime.datetime.fromtimestamp(dst_dir_quarterly_options_mod_time).date() != current_date:
        move_files_to_daily_directory(dst_dir_quarterly_options, daily_dir_quarterly_options)

    # Move files to daily directory for weekly data
    if datetime.datetime.fromtimestamp(dst_dir_weekly_options_mod_time).date() != current_date:
        move_files_to_daily_directory(dst_dir_weekly_options, daily_dir_weekly_options)

    # Rename files in source directory for quarterly data
    rename_files(src_dir, dst_dir_quarterly_options, filename_map_quarterly)

    # Rename files in source directory for weekly data
    rename_files(src_dir, dst_dir_weekly_options, filename_map_weekly)

if __name__ == "__main__":
    main()

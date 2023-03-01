import os
import datetime
import shutil
import fileinput
import re

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
    dst_dir_quarterly_options = "/home/gmurray/REPO/trading/data-quarterly"

    # Output directory weekly
    dst_dir_weekly_options = "/home/gmurray/REPO/trading/data-weekly"

    # Output directory skew
    dst_dir_skew_options = "/home/gmurray/REPO/trading/data-skew"

    # Daily output directory for quaterly data
    daily_dir_quarterly_options = "/home/gmurray/REPO/trading/data-quarterly/daily"

    # Weekly output directory for quaterly data
    weekly_dir_quarterly_options = "/home/gmurray/REPO/trading/data-quarterly/weekly"

    # Daily output directory for weekly data
    daily_dir_weekly_options = "/home/gmurray/REPO/trading/data-weekly/daily"

    # Weekly output directory for weekly data
    weekly_dir_weekly_options = "/home/gmurray/REPO/trading/data-weekly/weekly"

    # Daily output directory for skew data
    daily_dir_skew_options = "/home/gmurray/REPO/trading/data-skew/daily"

    # Weekly output directory for skew data
    weekly_dir_skew_options = "/home/gmurray/REPO/trading/data-skew/weekly"

    # Get the current date and time
    current_date = datetime.datetime.now().date()
    # Format the date to include a leading zero if the day is a single digit; this is a hack.  Strikes are a single digit, Laevitas files are two digits; eg: 3MAR or 03MAR
    formatted_date = current_date.strftime('%d%b%y') if current_date.day > 9 else current_date.strftime('0%d%b%y')

    # Parse the constants into datetime objects
    nearest_fri_date = datetime.datetime.strptime(nearest_fri, '%d%b%y')
    following_fri_date = datetime.datetime.strptime(following_fri, '%d%b%y')

    # Format the parsed constants using the formatted date
    nearest_fri_formatted = nearest_fri_date.strftime('%d%b%y').upper()
    following_fri_formatted = following_fri_date.strftime('%d%b%y').upper()


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
        f"lvt_chart ETH Buy_Sell Volume Last  Month {nearest_fri_formatted} .csv": f"LVT-MONTHLY-{nearest_fri_formatted}.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  Month {following_fri_formatted} .csv": f"LVT-MONTHLY-{following_fri_formatted}.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  COMMON.Week {nearest_fri_formatted} .csv": f"LVT-WEEKLY-{nearest_fri_formatted}.csv",
        f"lvt_chart ETH Buy_Sell Volume Last  COMMON.Week {following_fri_formatted} .csv": f"LVT-WEEKLY-{following_fri_formatted}.csv",
    }

    filename_map_skew = {
        f"lvt_chart Skew 25Δ ETH .csv": f"LVT-SKEW25-1D.csv",
        f"lvt_chart Skew 25Δ ETH  (1).csv": f"LVT-SKEW25-1W.csv",
        f"lvt_chart Skew 25Δ ETH  (2).csv": f"LVT-SKEW25-1M.csv",
        f"lvt_chart Skew 25Δ BTC .csv": f"LVT-SKEW25-1D-BTC.csv",
        f"lvt_chart Skew 25Δ BTC  (1).csv": f"LVT-SKEW25-1W-BTC.csv",
        f"lvt_chart Skew 25Δ BTC  (2).csv": f"LVT-SKEW25-1M-BTC.csv",
        f"lvt_chart Time Lapse Skew  ETH .csv": f"LVT-ETH-25DELTA-IV-CHANGE.csv",
        f"lvt_chart Time Lapse Skew  BTC .csv": f"LVT-BTC-25DELTA-IV-CHANGE.csv",
        f"lvt_chart Multi-Expiry Skew ETH .csv": f"MULTI-EXPIRY-SKEW.csv",
        f"lvt_chart Multi-Expiry Skew BTC .csv": f"MULTI-EXPIRY-SKEW-BTC.csv"
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

    # SKEW DIRECTROY CLEAN UP
    if current_date.weekday() == 6:
        # Delete existing files from weekly directory for weekly data
        delete_existing_files(weekly_dir_skew_options, filename_map_skew)
        # Copy files to weekly directory for weekly data
        copy_files_to_weekly_directory(daily_dir_skew_options, weekly_dir_skew_options)

    # Get the modification time of the destination directory, ie:have we run today already or is this a snapshot?
    dst_dir_quarterly_options_stat = os.stat(dst_dir_quarterly_options)
    dst_dir_quarterly_options_mod_time = dst_dir_quarterly_options_stat.st_mtime
    dst_dir_weekly_options_stat = os.stat(dst_dir_weekly_options)
    dst_dir_weekly_options_mod_time = dst_dir_weekly_options_stat.st_mtime
    dst_dir_skew_options_stat = os.stat(dst_dir_skew_options)
    dst_dir_skew_options_mod_time = dst_dir_skew_options_stat.st_mtime

    # Move files to daily directory for quarterly data
    if datetime.datetime.fromtimestamp(dst_dir_quarterly_options_mod_time).date() != current_date:
        # Delete old files from daily directory for quarterly data
        delete_old_files(daily_dir_quarterly_options)
        move_files_to_daily_directory(dst_dir_quarterly_options, daily_dir_quarterly_options)

    # Move files to daily directory for weekly data
    if datetime.datetime.fromtimestamp(dst_dir_weekly_options_mod_time).date() != current_date:
        # Delete old files from daily directory for weekly data
        delete_old_files(daily_dir_weekly_options)
        move_files_to_daily_directory(dst_dir_weekly_options, daily_dir_weekly_options)

    # Move files to daily directory for skew data
    if datetime.datetime.fromtimestamp(dst_dir_skew_options_mod_time).date() != current_date:
        # Delete old files from daily directory for weekly data
        delete_old_files(daily_dir_skew_options)
        move_files_to_daily_directory(dst_dir_skew_options, daily_dir_skew_options)

    # Only Change these Constants when the weekly options change.  Hopefully initially small maintenance.
    nearest_fri = "17MAR23"
    following_fri = "28APR23"

    previous_nearest_fri = "3MAR23"
    previous_following_fri = "10MAR23"

    #  Update data files with the list of strike using above constants
    pattern = re.compile(r'ETH-{}-\d+'.format(previous_nearest_fri))
    for line in fileinput.input('/home/gmurray/REPO/trading/data-weekly/Nearest-Fri-Options.txt', inplace=True):
        if pattern.search(line):
            line = line.replace(previous_nearest_fri, nearest_fri)
        print(line, end='')

    pattern = re.compile(r'ETH-{}-\d+'.format(previous_following_fri))
    for line in fileinput.input('/home/gmurray/REPO/trading/data-weekly/Following-Fri-Options.txt', inplace=True):
        if pattern.search(line):
            line = line.replace(previous_following_fri, following_fri)
        print(line, end='')

    # Remove files from destination before coping from ~Download
    #delete_existing_files(dst_dir_quarterly_options, filename_map_quarterly)
    # Rename files in source directory for quarterly data
    rename_files(src_dir, dst_dir_quarterly_options, filename_map_quarterly)

    # Remove files from destination before coping from ~Download
    #delete_existing_files(dst_dir_weekly_options, filename_map_weekly)
    # Rename files in source directory for weekly data
    rename_files(src_dir, dst_dir_weekly_options, filename_map_weekly)

    # Remove files from destination before coping from ~Download
    #delete_existing_files(dst_dir_skew_options, filename_map_skew)
    # Rename files in source directory for skew data
    rename_files(src_dir, dst_dir_skew_options, filename_map_skew)

if __name__ == "__main__":
    main()

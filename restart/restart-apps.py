import os

base_dir = "/home/gmurray/REPO/trading/"

options_weekly_script = "options-weekly/deribitIVperExpiryWeekly.py"
options_quarterly_script = "options-quarterly/deribitIVperExpiryQuarterly.py"
laevitas_weekly_script = "laevitas-weekly/blockedTradesWeeklyOptions.py"
laevitas_quarterly_script = "laevitas-quarterly/blockedTradesQuarterlyOptions.py"

# Create a list of the scripts
scripts = [options_weekly_script, options_quarterly_script, laevitas_weekly_script, laevitas_quarterly_script]

# Loop through the scripts and restart them
for script in scripts:
    # Get the full path to the script
    script_path = os.path.join(base_dir, script)
    # Stop the script
    os.system(f"pkill -f {script_path}")
    # Start the script
    os.system(f"python3 {script_path} &")
import os

base_dir = "/home/gmurray/REPO/trading/"

options_weekly_script = "options-weekly/deribitIVperExpiryWeekly.py"
options_quarterly_script = "options-quarterly/deribitIVperExpiryQuarterly.py"
blocked_otc_weekly_script = "blocked-otc-weekly/blockedTradesWeeklyOptions.py"
blocked_otc_quarterly_script = "blocked-otc-quarterly/blockedTradesQuarterlyOptions.py"
dashboard_script = "option-dashboard/dashboard.py"

# Create a list of the scripts
scripts = [options_weekly_script, options_quarterly_script, blocked_otc_weekly_script, blocked_otc_quarterly_script, dashboard_script]

# Loop through the scripts and restart them
for script in scripts:
    # Get the full path to the script
    script_path = os.path.join(base_dir, script)
    # Stop the script
    os.system(f"pkill -f {script_path}")

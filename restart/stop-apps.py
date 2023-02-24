import os

base_dir = "/home/gmurray/REPO/trading/"

options_ivp_weekly_script = "options-ivp-weekly/ivp-weekly.py"
options_ivp_quarterly_script = "options-ivp-quarterly/ivp-quarterly.py"
blocked_otc_weekly_script = "blocked-otc-weekly/blockedTradesWeeklyOptions.py"
blocked_otc_quarterly_script = "blocked-otc-quarterly/blockedTradesQuarterlyOptions.py"
dashboard_script = "option-dashboard/dashboard.py"

# Create a list of the scripts
scripts = [options_ivp_weekly_script, options_ivp_quarterly_script, blocked_otc_weekly_script, blocked_otc_quarterly_script, dashboard_script]

# Loop through the scripts and restart them
for script in scripts:
    # Get the full path to the script
    script_path = os.path.join(base_dir, script)
    # Stop the script
    os.system(f"pkill -f {script_path}")

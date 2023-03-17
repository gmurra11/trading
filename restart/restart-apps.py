import os


base_dir = "/home/gmurray/REPO/trading/"

options_liquidity_eth = "options-liquidity/liquidity-eth.py"
options_liquidity_eth_blocked = "options-liquidity/liquidity-eth-blocked.py"
options_liquidity_btc = "options-liquidity/liquidity-btc.py"
options_liquidity_btc_blocked = "options-liquidity/liquidity-btc-blocked.py"
dashboard_script = "option-skew-dashboard/skew-dashboard.py"

# Create a list of the scripts
scripts = [options_liquidity_eth, options_liquidity_eth_blocked, options_liquidity_btc, options_liquidity_btc_blocked, dashboard_script]

# Loop through the scripts and restart them
for script in scripts:
    # Get the full path to the script
    script_path = os.path.join(base_dir, script)
    # Stop the script
    os.system(f"pkill -f {script_path}")
    # Start the script
    os.system(f"python3 {script_path} &")

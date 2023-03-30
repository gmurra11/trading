import time
import requests

now = int(time.time() * 1000)

def get_options(currency, kind, expired):
    endpoint = "https://www.deribit.com/api/v2/public/get_instruments"
    params = {"currency": currency, "kind": kind, "expired": expired}
    response = requests.get(endpoint, params=params)
    data = response.json()
    return data["result"]

def filter_expiries(data, min_days, max_days):
    expiries = [d for d in data
                if d["expiration_timestamp"] > now
                and d["expiration_timestamp"] - now >= min_days*86400*1000
                and d["expiration_timestamp"] - now <= max_days*86400*1000]
    return expiries

def extract_dates(expiries):
    LESS_50_DAYS = []
    LESS_80_DAYS = []
    for expiry in expiries:
        get_expiry_date_from_instrument = expiry["instrument_name"].split("-")  #format: ETH-28APR23-1900-C; ie: 28APR23
        date_str = get_expiry_date_from_instrument[1]
        timestamp = expiry["expiration_timestamp"] / 1000
        days_until_expiry = (timestamp - now/1000) / 86400
        if days_until_expiry < 50:
            LESS_50_DAYS.append(date_str)
        elif days_until_expiry < 80:
            LESS_80_DAYS.append(date_str)
    return LESS_50_DAYS, LESS_80_DAYS

def find_distinct_expirations(LESS_50_DAYS, LESS_80_DAYS):
    DISTINCT_EXPIRATIONS = set(LESS_50_DAYS).union(set(LESS_80_DAYS))
    return DISTINCT_EXPIRATIONS

def format_instrument_name(instrument):
    currency = instrument['base_currency'].upper()
    expiry_date = instrument['expiration_timestamp']
    expiry_date = time.strftime('%d%b%y', time.localtime(expiry_date / 1000))
    strike = f"{instrument['strike']:.0f}"
    option_type = instrument['option_type'][0].capitalize()    #[0] is C or P for call or put
    return f"{currency}-{expiry_date}-{strike}-{option_type}"

def get_strikes(currency, min_days, max_days, min_strike, max_strike):
    data = get_options(currency, "option", "false")
    expiries = filter_expiries(data, min_days, max_days)
    LESS_50_DAYS, LESS_80_DAYS = extract_dates(expiries)
    DISTINCT_EXPIRATIONS = find_distinct_expirations(LESS_50_DAYS, LESS_80_DAYS)
    expiry_month = list(DISTINCT_EXPIRATIONS)[0]
    options = [instrument for instrument in data
               if expiry_month in instrument['instrument_name'] and min_strike <= instrument['strike'] <= max_strike]
    strikes = [format_instrument_name(instrument) for instrument in options]
    return strikes

# Get the BTC and ETH options data  - USE FOR TESTING
eth_strikes = get_strikes("ETH", 25, 80, 1000, 2500)
#btc_strikes = get_strikes("BTC", 30, 80, 15000, 30000)

# Print the list of ETH and BTC strikes for the first expiry month in the list - USE FOR TESTING
print(f"ETH Options Strikes: {eth_strikes}")
#print(f"BTC Options Strikes: {btc_strikes}")

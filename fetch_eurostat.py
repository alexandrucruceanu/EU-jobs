import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

def fetch_employment():
    # lfsa_egai2d: Employed persons by detailed occupation (ISCO-08 two digit level)
    # geo=EU27_2020, time=2023, sex=T, age=Y15-64
    url = f"{EUROSTAT_BASE}/lfsa_egai2d?geo=EU27_2020&time=2023&sex=T&age=Y15-64"
    logging.info(f"Fetching employment: {url}")
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    d = r.json()
    
    cats = d['dimension']['isco08']['category']['index']
    vals = d['value']
    
    mapping = {}
    for isco_code, idx in cats.items():
        # Eurostat ISCO codes have 'OC' prefix (e.g. 'OC21' for ISCO 21)
        clean_code = isco_code.replace("OC", "")
        if clean_code.isdigit() and len(clean_code) == 2:
            str_idx = str(idx)
            if str_idx in vals:
                # Value is in thousands, so multiply by 1000
                mapping[clean_code] = int(vals[str_idx] * 1000)
    return mapping

def fetch_earnings():
    # earn_ses_hourly: Mean and median hourly earnings by sex, age, occupation (2 digit)
    # We want Median (MED) for EU27_2020 in 2022
    url = f"{EUROSTAT_BASE}/earn_ses_hourly?geo=EU27_2020&time=2022&sex=T&age=TOTAL&sizeclas=GE10&indic_se=ERN_MD_H"
    logging.info(f"Fetching earnings: {url}")
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    d = r.json()
    
    cats = d['dimension']['isco08']['category']['index']
    vals = d['value']
    
    mapping = {}
    for isco_code, idx in cats.items():
        clean_code = isco_code.replace("OC", "")
        if clean_code.isdigit() and len(clean_code) == 2:
            str_idx = str(idx)
            if str_idx in vals:
                # Value is hourly median in Euros
                # Convert to annual assuming 2080 hours
                mapping[clean_code] = int(vals[str_idx] * 2080)
    return mapping

def main():
    try:
        emp = fetch_employment()
        logging.info(f"Got {len(emp)} employment records")
    except Exception as e:
        logging.error(f"Emp error: {e}")
        emp = {}

    try:
        earn = fetch_earnings()
        logging.info(f"Got {len(earn)} earnings records")
    except Exception as e:
        logging.error(f"Earn error: {e}")
        earn = {}

    out = {
        "employment": emp,
        "earnings_annual": earn
    }

    with open("eurostat_real.json", "w") as f:
        json.dump(out, f, indent=2)
    
    print("Successfully wrote eurostat_real.json")

if __name__ == "__main__":
    main()

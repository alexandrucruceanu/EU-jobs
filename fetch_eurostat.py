import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

def fetch_employment(geo="EU27_2020"):
    # lfsa_egai2d: Employed persons by detailed occupation (ISCO-08 two digit level)
    # geo=EU27_2020 (or ES), time=2023, sex=T, age=Y15-64
    url = f"{EUROSTAT_BASE}/lfsa_egai2d?geo={geo}&time=2023&sex=T&age=Y15-64"
    logging.info(f"Fetching employment for {geo}: {url}")
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

def fetch_earnings(geo="EU27_2020"):
    # earn_ses_hourly: Mean and median hourly earnings by sex, age, occupation (2 digit)
    # We want Median (MED) for geo in 2022
    url = f"{EUROSTAT_BASE}/earn_ses_hourly?geo={geo}&time=2022&sex=T&age=TOTAL&sizeclas=GE10&indic_se=ERN_MD_H"
    logging.info(f"Fetching earnings for {geo}: {url}")
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
                # Value is hourly median in Euros (store raw hourly rate)
                mapping[clean_code] = vals[str_idx]
    return mapping

def main():
    geos = {
        "EU": "EU27_2020",
        "AT": "AT", "BE": "BE", "BG": "BG", "CY": "CY", "CZ": "CZ",
        "DE": "DE", "DK": "DK", "EE": "EE", "EL": "EL", "ES": "ES",
        "FI": "FI", "FR": "FR", "HR": "HR", "HU": "HU", "IE": "IE",
        "IT": "IT", "LT": "LT", "LU": "LU", "LV": "LV", "MT": "MT",
        "NL": "NL", "PL": "PL", "PT": "PT", "RO": "RO", "SE": "SE",
        "SI": "SI", "SK": "SK"
    }
    
    out = {}
    
    for label, geo_code in geos.items():
        logging.info(f"Processing region: {label} ({geo_code})")
        try:
            emp = fetch_employment(geo_code)
            logging.info(f"Got {len(emp)} employment records for {label}")
        except Exception as e:
            logging.error(f"Emp error for {label}: {e}")
            emp = {}

        try:
            earn = fetch_earnings(geo_code)
            logging.info(f"Got {len(earn)} earnings records for {label}")
        except Exception as e:
            logging.error(f"Earn error for {label}: {e}")
            earn = {}

        out[label] = {
            "employment": emp,
            "earnings": earn
        }

    with open("eurostat_real.json", "w") as f:
        json.dump(out, f, indent=2)
    
    print("Successfully wrote eurostat_real.json with EU and ES data")

if __name__ == "__main__":
    main()

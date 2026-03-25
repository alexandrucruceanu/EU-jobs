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
    # earn_ses_hourly: Structure of earnings survey - hourly earnings
    # Dataset provides 1-digit ISCO-08 major groups.
    # We use Median earnings in euro (MED_E_EUR) and filter for Full-time (FT).
    
    # Try 2022 first (latest survey), fallback to 2018 if needed
    years = ["2022", "2018"]
    
    for year in years:
        url = f"{EUROSTAT_BASE}/earn_ses_hourly?geo={geo}&time={year}&sex=T&age=TOTAL&nace_r2=B-S_X_O&indic_se=MED_E_EUR&worktime=FT"
        logging.info(f"Fetching earnings for {geo} ({year}): {url}")
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            d = r.json()
            
            cats = d['dimension']['isco08']['category']['index']
            vals = d.get('value', {})
            
            if not vals:
                logging.warning(f"No earnings values for {geo} in {year}")
                continue
                
            mapping = {}
            for isco_code, idx in cats.items():
                clean_code = isco_code.replace("OC", "")
                
                # Handling 1nd-digit major groups (OC1, OC2, ...)
                if clean_code.isdigit() and len(clean_code) == 1:
                    str_idx = str(idx)
                    if str_idx in vals:
                        val = vals[str_idx]
                        # Map to all 2-digit children (e.g. 2 -> 21, 22, 23, 24, 25, 26)
                        for i in range(10):
                            mapping[f"{clean_code}{i}"] = val
                
                # Handling 2nd-digit sub-major groups if available (OC11, OC12, ...)
                elif clean_code.isdigit() and len(clean_code) == 2:
                    str_idx = str(idx)
                    if str_idx in vals:
                        mapping[clean_code] = vals[str_idx]
            
            if mapping:
                logging.info(f"Successfully retrieved {len(mapping)} earnings mappings for {geo} in {year}")
                return mapping
                
        except Exception as e:
            logging.error(f"Error fetching earnings for {geo} in {year}: {e}")
            
    return {}

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

    with open("data/json/eurostat_real.json", "w") as f:
        json.dump(out, f, indent=2)
    
    print("Successfully wrote eurostat_real.json with EU and ES data")

if __name__ == "__main__":
    main()

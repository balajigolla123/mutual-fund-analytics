import requests
import pandas as pd

scheme_code = 125497  # HDFC Top 100 Direct

url = f"https://api.mfapi.in/mf/{scheme_code}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    print("Scheme Name:")
    print(data["meta"]["scheme_name"])

    nav_df = pd.DataFrame(data["data"])

    output_file = "data/raw/hdfc_top100_live_nav.csv"
    nav_df.to_csv(output_file, index=False)

    print(f"\nNAV data saved to: {output_file}")
    print(nav_df.head())
else:
    print("Failed to fetch NAV data")
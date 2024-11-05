import requests
import pandas as pd
from us import states
from io import StringIO
import re

url = "https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt"
response = requests.get(url)

preprocessed_data = ""
for line in response.text.splitlines()[16:16+56]: 

    match = re.match(r"^\s*(\d+)\s+(.*)$", line)
    if match:
        fips_code, state_name = match.groups()
        preprocessed_data += f"{fips_code},{state_name}\n"

fips = pd.read_csv(StringIO(preprocessed_data), names=["FIPS", "State"])

state_abbreviations = {state.name.upper(): state.abbr for state in states.STATES}
fips['Abbr'] = fips['State'].map(state_abbreviations)
fips.loc[fips['State'] == 'DISTRICT OF COLUMBIA', 'Abbr'] = 'DC'

fips.to_csv("fips.csv", index=False)
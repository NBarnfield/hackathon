import requests
from bs4 import BeautifulSoup
import pandas

base_url = "http://www.iba.gov.au/business/finance/business-loan/"
urls = ['business-loan/', 'procurement-loan/', 'producer-loan/', 'start-finance-package/']

# create a list called records - we will use it for pandas
grants_summary = []

for url in urls:

    new_url = base_url + url
    r = requests.get(new_url)
    c = r.content

    soup = BeautifulSoup(c, "html.parser")
    rows = soup.find_all("tr")

    for row in rows:
        # To avoid poorly formatted table rows, skip if number of children is less than 5.
        if len(row) <5 : continue

        grant_details = {}

        grant_name = soup.h1
        feature =  row.find("td")
        details = feature.find_next("td")
        grant_details['Grant'] = grant_name.text.strip()
        grant_details['Details'] = details.text.strip()
        grant_details['Feature'] = feature.text.strip()

        # exporting the dictionary (grant_details) into the list (grants_summary)
        grants_summary.append(grant_details)

# using pandas for data analysis and manipulation
df = pandas.DataFrame(grants_summary)
pandas.set_option('display.max_columns', None)
print(df)

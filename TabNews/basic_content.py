# %%

import requests
import pandas as pd
import datetime
import json
import re
import time

# %%

def get_response(**kwargs):
	url = "https://www.tabnews.com.br/api/v1/contents/"
	resp = requests.get(url, params=kwargs)
	return resp

def save_data(data, option='json'):

	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f").replace(":", "_", -1)
	
	if option == 'json':
		with open(f"data/contents/json/{now}.json", 'w') as open_file:
			json.dump(data, open_file, indent=4)

	elif option == 'parquet':
		df = pd.DataFrame(data)
		df.to_parquet(f"data/contents/parquet/{now}.parquet", index=False)
		
# %%

page = 1

while True:
    print(page)
    resp = get_response(page=1, per_page=100, strategy="new")
    if resp.status_code == 200:     
        data = resp.json()
        save_data(data)
		
        if len(data) < 100:
            break		
		
        page +=1
        time.sleep(10)
		
    else:
        print(resp.status_code)
        print(resp.json())
        time.sleep(60*15)


# %%

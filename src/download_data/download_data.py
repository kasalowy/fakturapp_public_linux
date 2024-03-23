import requests
import pandas as pd
from datetime import datetime
import itertools
from dateutil.relativedelta import relativedelta

import os

# Function current_year_df checks for the size of dataset that has to be downloaded
# In the second step - func builds pandas df and returns it as a pd object.
def current_year_df(api_token: str,  api_url_root: str, api_sufix: str,  data_danych: datetime) -> pd.DataFrame:
    
    print("""
        +--------------------------------------+
        | RESOLVING THE SIZE OF BASE DATAFRAME |
        +--------------------------------------+
        """)
    
    api=f"{api_url_root}/{api_sufix}"
    pg_a=1
    
    while True:
        params = {
            "api_token": api_token,
            "page": pg_a,
            "per_page": 100
        }
        
        response = requests.get(api, params=params).json()
        print(len(response))
        print(type(response))
        if len(response) != 0:
            last_date = datetime.strptime(response[-1]['sell_date'], "%Y-%m-%d")        
            if last_date >= data_danych:
                pg_a=pg_a+1
            else:
                page_range=pg_a+1
                break
        else:
            page_range=pg_a
            break


    full_json=[]
    
    for pg_b in range(page_range):
        params = {
            "api_token": api_token,
            "page": pg_b,
            "per_page": 100
        }

        response = requests.get(api, params=params).json()
        full_json.append(response)
                    
    df = pd.DataFrame(list(itertools.chain.from_iterable(full_json)))
    df['sell_date'] = pd.to_datetime(df['sell_date'])
    df = df[df['sell_date'] >= data_danych]
    
    df.reset_index(drop=True, inplace=True)
    
    return df
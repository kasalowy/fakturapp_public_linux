import os
import datetime
    
from connect_to_db.connect_to_db import connect_to_db
from download_data.download_data import current_year_df
from aggregate_data.aggregate_data import transform_data_1
  
workdir_name = os.getenv('FAKTURAPP_ROOT')
maska_pliku = os.getenv('FILE_MASK')
api_url=os.getenv('API_URL')
api_token=os.getenv('API_TOKEN')

data_danych=datetime.datetime.strptime(os.getenv('DATA_DANYCH'), "%Y-%m-%d")

def run (api_token: str, api_url_root: str, data_danych: datetime.datetime, workdir: str, file_mask: str) -> None:
     
    # Establish connextion to fakturownia and check credentials
    api_sufix="categories.json"
    connect_to_db(api_token, api_url_root, api_sufix)
    
    # Download unprocessed user's financial data
    api_sufix="invoices.json"
    df = current_year_df(api_token, api_url_root, api_sufix, data_danych)

    # Perform desired data aggregation
    df = transform_data_1(df)

    # Save output as a CSV file in a Docker volume
    df.to_csv(f"{workdir}/output_dir/{file_mask}", encoding="utf-8", sep=";", index=False)
        
if __name__ == "__main__":
    run(api_token, api_url, data_danych, workdir_name, maska_pliku)
import requests
import sys

def connect_to_db(api_token: str, api_url_root: str, api_sufix: str) -> dict:    
    
    api_url = f"{api_url_root}/{api_sufix}"
        
    params = {"api_token": api_token}
    response = requests.get(api_url, params=params)

    if response.headers["Status"] == "200 OK":
        print("""
            +-----------------------------------------+
            | CONNECTION TO FAKTUROWNIA.PL SUCCESSFUL |
            +-----------------------------------------+
            """)
        return 0
    else:
        print(f"""
            +------------------------------------+
            | CONNECTION ERROR. ERROR CODE BELOW |
            +------------------------------------+
            """)
        print(f"CODE ERROR: {response.headers['Status']}")
        sys.exit()
    
    
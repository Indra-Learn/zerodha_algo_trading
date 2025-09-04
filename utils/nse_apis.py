import requests

class NSE_APIS:
    base_nse_url = "https://www.nseindia.com/"
    nse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    def __init__(self):
        self.nse_session = requests.Session()
        self.nse_session.headers.update(self.nse_headers)
        self.nse_session.get(self.base_nse_url)

    def get_data(self, api_url):
        full_nse_api_url = self.base_nse_url + api_url
        print(f"calling {full_nse_api_url} ..")
        output = dict()
        try:
            response = self.nse_session.get(full_nse_api_url)
            response.raise_for_status()
        except Exception as e:
            print(f"error from NSE_API.get_data(): {e}")
        else:
            if response.status_code == 200:
                output = response.json()
        return output
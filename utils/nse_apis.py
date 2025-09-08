import requests
import pandas as pd

class NSE_APIS:
    base_nse_url = "https://www.nseindia.com/"
    nse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    def __init__(self):
        self.nse_session = requests.Session()
        self.nse_session.headers.update(self.nse_headers)
        self.nse_session.get(self.base_nse_url, headers=self.nse_headers,  timeout=10)
        self.nse_session.get(self.base_nse_url+"/option-chain", headers=self.nse_headers,  timeout=10)

    def _get_data(self, api_url):
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
    
    def get_large_deal_data(self):
        data = self._get_data("api/snapshot-capital-market-largedeal")
        df = pd.DataFrame(data.get("BULK_DEALS_DATA"))
        grouped_df = df.groupby(["date", "symbol", "name", "buySell"]) \
                        .agg({"qty":[sum], "watp":[max, min]})
        grouped_df.reset_index(inplace=True)
        # .sort_values('qty', ascending=False)
        # df["max_buy"] = 
        # df["min_sell"] = 
        # df = df.groupby(level=0, group_keys=False).apply(lambda g:g.sort_values("qty", ascending=False))
        return grouped_df



if __name__ == "__main__":
    nse_api = NSE_APIS()
    # data = nse_api._get_data("api/snapshot-capital-market-largedeal")
    data = nse_api.get_large_deal_data()
    print(f"data={data}")
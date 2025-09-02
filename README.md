# zerodha_algo_trading
zerodha algo trading


## How To Use:
1. Clone the Git Repo -
    ```shell
    git clone https://github.com/Indra-Learn/zerodha_algo_trading.git
    cd .\zerodha_algo_trading\
    ```
2. Create `.env` file immediate under to `zerodha_algo_trading` folder and add below details inside into it -
    ```shell
    KITE_API_KEY=<KITE API KEY>
    KITE_API_SECRET=<KITE API SECRET>
    ```
3. Create & Activate the Python Environment -
    ```shell
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```
4. Run the Flask app from VS Code terminal - 
    ```shell
    # do not use in production
    flask --app app run --host=0.0.0.0 --port=8080 --debug
    ```

## Reference Docs:
1. Zerodha Kite-Connect Api: https://zerodha.com/products/api/
2. Kite-Connect Api(Python) Doc: https://kite.trade/docs/connect/v3/sdks/
3. Kite-Connect Api(Python) Github: https://github.com/zerodha/pykiteconnect

## Algo Trading:
1. 

## Circular:
1. NSE Circular: https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework

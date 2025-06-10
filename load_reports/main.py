import asyncio

import reports_service

path = "financial_reports_1.db"

tickers_1 = ['AAPL','META', 'NVDA', 'AMD', 'GOOG', "KHC", "FERG"]
tickers_2 = ['XOM', 'MCD', 'KO', 'PFE', 'PG', "PAYX", "STZ"]
tickers_3 = ['MSFT', 'AMZN', 'TSLA', 'GOOGL', 'JPM', "ODFL"]
tickers_4 = ['JNJ', 'V', 'CMCSA', 'PEP', 'T', "CHTR", "WCN"]
tickers_5 = ['CSCO', 'DIS', 'NKE', 'VZ', 'HD', "GWW", "D"]
tickers_6 = ['UNH', 'CRM', 'NFLX', 'INTC', 'BA', "KMI", "AEP"]
tickers_7 = ['MRK', 'LMT', 'GILD', 'SBUX',  "APD", "SRE", "LEN"]
tickers_8 = ['AMGN', 'IBM', 'HON', 'PYPL', 'LRCX', "PCAR", "GEV"]
tickers_9 = ['MDLZ', 'BKNG', 'FDX', 'EOG', 'CIM', "F", "NSC"]
tickers_10 = ['DVN', 'MPC', 'CHK', 'RRC', "MRVL", "HLT", "AZO"]
tickers_11 = ['NOG', 'ADBE', 'CAT', 'QCOM', "DASH", "SLB"]
tickers_12 = ["VRTX", "ETN", "BSX", "MDT", "ADI", "EPD", "CEG"]
tickers_13 = ["ANET", "PANW", "ADP", "KLAC", "DHI", "NEM", "GM"]
tickers_14 = ["BUD", "DE", "MELI", "SHOP", "FI", "CSX", "CRWD"]
tickers_15 = ["BMY", "SO", "SHW", "DUK", "MAR", "ORLY", "CARR"]
tickers_16 = ["CL", "WM", "SNPS", "SCCO", "ZTS", "FCX"]
tickers_17 = ["APH", "DELL", "CTAS", "PH", "CMG"]
tickers_18 = ["ITW", "TGT", "MSI", "MCK", "ECL"]

async def main():
    print("This application downloads financial statements and saves them to the SQlite database")
    api_key = input("Enter API key >>> ")
    await reports_service.load_full_reports(tickers_5, api_key, path)
    print("Reports succesfully saved")

if __name__ == '__main__':
    asyncio.run(main())
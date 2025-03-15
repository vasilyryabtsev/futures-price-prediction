import reports_client, data_classes, repository
import asyncio

async def load_full_reports(tickers, apikey, path):
    full_data = []
    tasks = []
    
    for ticker in tickers:
        tasks.append(load_reports(ticker, apikey, path))
    
    results = await asyncio.gather(*tasks)
    
    for result in results:
        full_data.append(result)
        
    return full_data

async def load_reports(ticker, apikey, path):
    await repository.create_db(path)
    pnl = await load_pnl(ticker, apikey, path)
    bs = await load_bs(ticker, apikey, path)
    cf = await load_cf(ticker, apikey, path)
    return {
        'ticker': ticker,
        'pnl': pnl,
        'balance_sheet': bs,
        'cash_flow': cf,
    }

async def load_pnl(ticker, apikey, path):
    pnl_json = await reports_client.get_income_statement(ticker, apikey)
    pnl = data_classes.IncomeStatement.create_pnl(pnl_json)
    await repository.save_income_statement(pnl, path)
    return pnl

async def load_bs(ticker, apikey, path):
    bs_json = await reports_client.get_balance_sheet(ticker, apikey)
    bs = data_classes.BalanceSheet.create_from_json(bs_json)
    await repository.save_balance_sheet(bs, path)
    return bs

async def load_cf(ticker, apikey, path):
    cf_json = await reports_client.get_cash_flow(ticker, apikey)
    cf = data_classes.CashFlow.create_from_json(cf_json)
    await repository.save_cash_flow(cf, path)
    return cf
import aiosqlite
from dataclasses import asdict

async def candles_save(candles, path):
    async with aiosqlite.connect(path) as conn:
        cursor = await conn.cursor()

        candles_to_insert = [(candle._id, candle._date_time, candle._ticker,
                              candle._size, candle._source, candle._open,
                              candle._max, candle._min, candle._close, candle._volume) for candle in candles]
        try:
            await cursor.executemany('''
                INSERT OR IGNORE INTO candles (id, date_time, ticker, size, source, open, max, min, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', candles_to_insert)
            await conn.commit()
        except aiosqlite.Error as e:
            print(f"Error: {e}")
            await conn.rollback()

async def create_db(path):
    async with aiosqlite.connect(path) as conn:
        cursor = await conn.cursor()
        print('Create tables')
        try:

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS pnl (
                    id VARCHAR(30) PRIMARY KEY,
                    ticker VARCHAR(30) NOT NULL,
                    type VARCHAR(30) NOT NULL,
                    fiscalDateEnding DATE NOT NULL,
                    reportedCurrency VARCHAR(30) NOT NULL,
                    grossProfit REAL,
                    totalRevenue REAL,
                    costOfRevenue REAL,
                    costofGoodsAndServicesSold REAL,
                    operatingIncome REAL,
                    sellingGeneralAndAdministrative REAL,
                    researchAndDevelopment REAL,
                    operatingExpenses REAL,
                    investmentIncomeNet REAL,
                    netInterestIncome REAL,
                    interestIncome REAL,
                    interestExpense REAL,
                    nonInterestIncome REAL,
                    otherNonOperatingIncome REAL,
                    depreciation REAL,
                    depreciationAndAmortization REAL,
                    incomeBeforeTax REAL,
                    incomeTaxExpense REAL,
                    interestAndDebtExpense REAL,
                    netIncomeFromContinuingOperations REAL,
                    comprehensiveIncomeNetOfTax REAL,
                    ebit REAL,
                    ebitda REAL,
                    netIncome REAL
                )
            """)

            await cursor.execute("""CREATE TABLE IF NOT EXISTS balance_sheet (
                    id VARCHAR(30) PRIMARY KEY,
                    ticker VARCHAR(30) NOT NULL,
                    type VARCHAR(30) NOT NULL,
                    fiscalDateEnding DATE NOT NULL,
                    reportedCurrency VARCHAR(30) NOT NULL,
                    totalAssets REAL,
                    totalCurrentAssets REAL,
                    cashAndCashEquivalentsAtCarryingValue REAL,
                    cashAndShortTermInvestments REAL,
                    inventory REAL,
                    currentNetReceivables REAL,
                    totalNonCurrentAssets REAL,
                    propertyPlantEquipment REAL,
                    accumulatedDepreciationAmortizationPPE REAL,
                    intangibleAssets REAL,
                    intangibleAssetsExcludingGoodwill REAL,
                    goodwill REAL,
                    investments REAL,
                    longTermInvestments REAL,
                    shortTermInvestments REAL,
                    otherCurrentAssets REAL,
                    otherNonCurrentAssets REAL,
                    totalLiabilities REAL,
                    totalCurrentLiabilities REAL,
                    currentAccountsPayable REAL,
                    deferredRevenue REAL,
                    currentDebt REAL,
                    shortTermDebt REAL,
                    totalNonCurrentLiabilities REAL,
                    capitalLeaseObligations REAL,
                    longTermDebt REAL,
                    currentLongTermDebt REAL,
                    longTermDebtNoncurrent REAL,
                    shortLongTermDebtTotal REAL,
                    otherCurrentLiabilities REAL,
                    otherNonCurrentLiabilities REAL,
                    totalShareholderEquity REAL,
                    treasuryStock REAL,
                    retainedEarnings REAL,
                    commonStock REAL,
                    commonStockSharesOutstanding REAL
                    );
                """)

            await cursor.execute("""CREATE TABLE IF NOT EXISTS cash_flow (
                    id VARCHAR(255) PRIMARY KEY,
                    ticker VARCHAR(30) NOT NULL,
                    type VARCHAR(30) NOT NULL,
                    fiscalDateEnding DATE NOT NULL,
                    reportedCurrency VARCHAR(30) NOT NULL,
                    operatingCashflow REAL,
                    paymentsForOperatingActivities REAL,
                    proceedsFromOperatingActivities REAL,
                    changeInOperatingLiabilities REAL,
                    changeInOperatingAssets REAL,
                    depreciationDepletionAndAmortization REAL,
                    capitalExpenditures REAL,
                    changeInReceivables REAL,
                    changeInInventory REAL,
                    profitLoss REAL,
                    cashflowFromInvestment REAL,
                    cashflowFromFinancing REAL,
                    proceedsFromRepaymentsOfShortTermDebt REAL,
                    paymentsForRepurchaseOfCommonStock REAL,
                    paymentsForRepurchaseOfEquity REAL,
                    paymentsForRepurchaseOfPreferredStock REAL,
                    dividendPayout REAL,
                    dividendPayoutCommonStock REAL,
                    dividendPayoutPreferredStock REAL,
                    proceedsFromIssuanceOfCommonStock REAL,
                    proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet REAL,
                    proceedsFromIssuanceOfPreferredStock REAL,
                    proceedsFromRepurchaseOfEquity REAL,
                    proceedsFromSaleOfTreasuryStock REAL,
                    changeInCashAndCashEquivalents REAL,
                    changeInExchangeRate REAL,
                    netIncome REAL);
                """)

            await conn.commit()
        except aiosqlite.Error as e:
            print(f"An error occurred: {e}")
            await conn.rollback()


async def save_income_statement(pnl, path):
    async with aiosqlite.connect(path) as conn:
        c = await conn.cursor()

        try:
            for statement in pnl:
                data = asdict(statement)
                data['fiscalDateEnding'] = data['fiscalDateEnding'].isoformat()
                placeholders = ', '.join('?' * len(data))
                columns = ', '.join(data.keys())
                query = f"INSERT OR IGNORE INTO pnl ({columns}) VALUES ({placeholders})"
                await c.execute(query, tuple(data.values()))

            await conn.commit()
        except aiosqlite.Error as e:
            print(f"An error occurred: {e}")

async def save_balance_sheet(bs, path):
    async with aiosqlite.connect(path) as conn:
        c = await conn.cursor()

        try:
            for statement in bs:
                data = asdict(statement)
                data['fiscalDateEnding'] = data['fiscalDateEnding'].isoformat()
                placeholders = ', '.join('?' * len(data))
                columns = ', '.join(data.keys())
                query = f"INSERT OR IGNORE INTO balance_sheet ({columns}) VALUES ({placeholders})"
                await c.execute(query, tuple(data.values()))

            await conn.commit()
        except aiosqlite.Error as e:
            print(f"An error occurred: {e}")

async def save_cash_flow(cf, path):
    async with aiosqlite.connect(path) as conn:
        c = await conn.cursor()

        try:
            for statement in cf:
                data = asdict(statement)
                data['fiscalDateEnding'] = data['fiscalDateEnding'].isoformat()
                placeholders = ', '.join('?' * len(data))
                columns = ', '.join(data.keys())
                query = f"INSERT OR IGNORE INTO cash_flow ({columns}) VALUES ({placeholders})"
                await c.execute(query, tuple(data.values()))

            await conn.commit()
        except aiosqlite.Error as e:
            print(f"An error occurred: {e}")
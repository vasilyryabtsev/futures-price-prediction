from dataclasses import dataclass
from datetime import date


@dataclass
class BalanceSheet:
    id: str
    ticker: str
    type: str
    fiscalDateEnding: date
    reportedCurrency: str
    totalAssets: float = None
    totalCurrentAssets: float = None
    cashAndCashEquivalentsAtCarryingValue: float = None
    cashAndShortTermInvestments: float = None
    inventory: float = None
    currentNetReceivables: float = None
    totalNonCurrentAssets: float = None
    propertyPlantEquipment: float = None
    accumulatedDepreciationAmortizationPPE: float = None
    intangibleAssets: float = None
    intangibleAssetsExcludingGoodwill: float = None
    goodwill: float = None
    investments: float = None
    longTermInvestments: float = None
    shortTermInvestments: float = None
    otherCurrentAssets: float = None
    otherNonCurrentAssets: float = None
    totalLiabilities: float = None
    totalCurrentLiabilities: float = None
    currentAccountsPayable: float = None
    deferredRevenue: float = None
    currentDebt: float = None
    shortTermDebt: float = None
    totalNonCurrentLiabilities: float = None
    capitalLeaseObligations: float = None
    longTermDebt: float = None
    currentLongTermDebt: float = None
    longTermDebtNoncurrent: float = None
    shortLongTermDebtTotal: float = None
    otherCurrentLiabilities: float = None
    otherNonCurrentLiabilities: float = None
    totalShareholderEquity: float = None
    treasuryStock: float = None
    retainedEarnings: float = None
    commonStock: float = None
    commonStockSharesOutstanding: float = None

    @staticmethod
    def create_from_json(json_data):
        reports = []
        for report_type, reports_data in [("annual", json_data["annualReports"]),
                                          ("quarterly", json_data["quarterlyReports"])]:
            for report_data in reports_data:
                report = BalanceSheet(
                    id=json_data["symbol"] + report_data["fiscalDateEnding"] + report_type,
                    ticker=json_data["symbol"],
                    type=report_type,
                    fiscalDateEnding=date.fromisoformat(report_data["fiscalDateEnding"]),
                    reportedCurrency=report_data["reportedCurrency"],
                    totalAssets=float(report_data["totalAssets"]) if report_data["totalAssets"] != "None" else None,
                    totalCurrentAssets=float(report_data["totalCurrentAssets"]) if report_data[
                                                                                       "totalCurrentAssets"] != "None" else None,
                    cashAndCashEquivalentsAtCarryingValue=float(report_data["cashAndCashEquivalentsAtCarryingValue"]) if
                    report_data["cashAndCashEquivalentsAtCarryingValue"] != "None" else None,
                    cashAndShortTermInvestments=float(report_data["cashAndShortTermInvestments"]) if report_data[
                                                                                                         "cashAndShortTermInvestments"] != "None" else None,
                    inventory=float(report_data["inventory"]) if report_data["inventory"] != "None" else None,
                    currentNetReceivables=float(report_data["currentNetReceivables"]) if report_data[
                                                                                             "currentNetReceivables"] != "None" else None,
                    totalNonCurrentAssets=float(report_data["totalNonCurrentAssets"]) if report_data[
                                                                                             "totalNonCurrentAssets"] != "None" else None,
                    propertyPlantEquipment=float(report_data["propertyPlantEquipment"]) if report_data[
                                                                                               "propertyPlantEquipment"] != "None" else None,
                    accumulatedDepreciationAmortizationPPE=float(
                        report_data["accumulatedDepreciationAmortizationPPE"]) if
                    report_data["accumulatedDepreciationAmortizationPPE"] != "None" else None,
                    intangibleAssets=float(report_data["intangibleAssets"]) if report_data[
                                                                                   "intangibleAssets"] != "None" else None,
                    intangibleAssetsExcludingGoodwill=float(report_data["intangibleAssetsExcludingGoodwill"]) if
                    report_data["intangibleAssetsExcludingGoodwill"] != "None" else None,
                    goodwill=float(report_data["goodwill"]) if report_data["goodwill"] != "None" else None,
                    investments=float(report_data["investments"]) if report_data["investments"] != "None" else None,
                    longTermInvestments=float(report_data["longTermInvestments"]) if report_data[
                                                                                         "longTermInvestments"] != "None" else None,
                    shortTermInvestments=float(report_data["shortTermInvestments"]) if report_data[
                                                                                           "shortTermInvestments"] != "None" else None,
                    otherCurrentAssets=float(report_data["otherCurrentAssets"]) if report_data[
                                                                                       "otherCurrentAssets"] != "None" else None,
                    otherNonCurrentAssets=float(report_data["otherNonCurrentAssets"]) if report_data[
                                                                                             "otherNonCurrentAssets"] != "None" else None,
                    totalLiabilities=float(report_data["totalLiabilities"]) if report_data[
                                                                                   "totalLiabilities"] != "None" else None,
                    totalCurrentLiabilities=float(report_data["totalCurrentLiabilities"]) if report_data[
                                                                                                 "totalCurrentLiabilities"] != "None" else None,
                    currentAccountsPayable=float(report_data["currentAccountsPayable"]) if report_data[
                                                                                               "currentAccountsPayable"] != "None" else None,
                    deferredRevenue=float(report_data["deferredRevenue"]) if report_data[
                                                                                 "deferredRevenue"] != "None" else None,
                    currentDebt=float(report_data["currentDebt"]) if report_data["currentDebt"] != "None" else None,
                    shortTermDebt=float(report_data["shortTermDebt"]) if report_data[
                                                                             "shortTermDebt"] != "None" else None,
                    totalNonCurrentLiabilities=float(report_data["totalNonCurrentLiabilities"]) if report_data[
                                                                                                       "totalNonCurrentLiabilities"] != "None" else None,
                    capitalLeaseObligations=float(report_data["capitalLeaseObligations"]) if report_data[
                                                                                                 "capitalLeaseObligations"] != "None" else None,
                    longTermDebt=float(report_data["longTermDebt"]) if report_data["longTermDebt"] != "None" else None,
                    currentLongTermDebt=float(report_data["currentLongTermDebt"]) if report_data[
                                                                                         "currentLongTermDebt"] != "None" else None,
                    longTermDebtNoncurrent=float(report_data["longTermDebtNoncurrent"]) if report_data[
                                                                                               "longTermDebtNoncurrent"] != "None" else None,
                    shortLongTermDebtTotal=float(report_data["shortLongTermDebtTotal"]) if report_data[
                                                                                               "shortLongTermDebtTotal"] != "None" else None,
                    otherCurrentLiabilities=float(report_data["otherCurrentLiabilities"]) if report_data[
                                                                                                 "otherCurrentLiabilities"] != "None" else None,
                    otherNonCurrentLiabilities=float(report_data["otherNonCurrentLiabilities"]) if report_data[
                                                                                                       "otherNonCurrentLiabilities"] != "None" else None,
                    totalShareholderEquity=float(report_data["totalShareholderEquity"]) if report_data[
                                                                                               "totalShareholderEquity"] != "None" else None,
                    treasuryStock=float(report_data["treasuryStock"]) if report_data[
                                                                             "treasuryStock"] != "None" else None,
                    retainedEarnings=float(report_data["retainedEarnings"]) if report_data[
                                                                                   "retainedEarnings"] != "None" else None,
                    commonStock=float(report_data["commonStock"]) if report_data["commonStock"] != "None" else None,
                    commonStockSharesOutstanding=float(report_data["commonStockSharesOutstanding"]) if report_data[
                                                                                                           "commonStockSharesOutstanding"] != "None" else None
                )
                reports.append(report)

        return reports


@dataclass
class CashFlow:
    id: str
    ticker: str
    type: str
    fiscalDateEnding: date
    reportedCurrency: str
    operatingCashflow: float = None
    paymentsForOperatingActivities: float = None
    proceedsFromOperatingActivities: float = None
    changeInOperatingLiabilities: float = None
    changeInOperatingAssets: float = None
    depreciationDepletionAndAmortization: float = None
    capitalExpenditures: float = None
    changeInReceivables: float = None
    changeInInventory: float = None
    profitLoss: float = None
    cashflowFromInvestment: float = None
    cashflowFromFinancing: float = None
    proceedsFromRepaymentsOfShortTermDebt: float = None
    paymentsForRepurchaseOfCommonStock: float = None
    paymentsForRepurchaseOfEquity: float = None
    paymentsForRepurchaseOfPreferredStock: float = None
    dividendPayout: float = None
    dividendPayoutCommonStock: float = None
    dividendPayoutPreferredStock: float = None
    proceedsFromIssuanceOfCommonStock: float = None
    proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet: float = None
    proceedsFromIssuanceOfPreferredStock: float = None
    proceedsFromRepurchaseOfEquity: float = None
    proceedsFromSaleOfTreasuryStock: float = None
    changeInCashAndCashEquivalents: float = None
    changeInExchangeRate: float = None
    netIncome: float = None

    @staticmethod
    def create_from_json(json_data):
        reports = []
        for report_type, reports_data in [("annual", json_data["annualReports"]),
                                          ("quarterly", json_data["quarterlyReports"])]:
            for report_data in reports_data:
                report = CashFlow(
                    id=json_data["symbol"] + report_data["fiscalDateEnding"] + report_type,
                    ticker=json_data["symbol"],
                    type=report_type,
                    fiscalDateEnding=date.fromisoformat(report_data["fiscalDateEnding"]),
                    reportedCurrency=report_data["reportedCurrency"],
                    operatingCashflow=float(report_data["operatingCashflow"]) if report_data[
                                                                                     "operatingCashflow"] != "None" else None,
                    paymentsForOperatingActivities=float(report_data["paymentsForOperatingActivities"]) if report_data[
                                                                                                               "paymentsForOperatingActivities"] != "None" else None,
                    proceedsFromOperatingActivities=float(report_data["proceedsFromOperatingActivities"]) if
                    report_data["proceedsFromOperatingActivities"] != "None" else None,
                    changeInOperatingLiabilities=float(report_data["changeInOperatingLiabilities"]) if report_data[
                                                                                                           "changeInOperatingLiabilities"] != "None" else None,
                    changeInOperatingAssets=float(report_data["changeInOperatingAssets"]) if report_data[
                                                                                                 "changeInOperatingAssets"] != "None" else None,
                    depreciationDepletionAndAmortization=float(report_data["depreciationDepletionAndAmortization"]) if
                    report_data["depreciationDepletionAndAmortization"] != "None" else None,
                    capitalExpenditures=float(report_data["capitalExpenditures"]) if report_data[
                                                                                         "capitalExpenditures"] != "None" else None,
                    changeInReceivables=float(report_data["changeInReceivables"]) if report_data[
                                                                                         "changeInReceivables"] != "None" else None,
                    changeInInventory=float(report_data["changeInInventory"]) if report_data[
                                                                                     "changeInInventory"] != "None" else None,
                    profitLoss=float(report_data["profitLoss"]) if report_data["profitLoss"] != "None" else None,
                    cashflowFromInvestment=float(report_data["cashflowFromInvestment"]) if report_data[
                                                                                               "cashflowFromInvestment"] != "None" else None,
                    cashflowFromFinancing=float(report_data["cashflowFromFinancing"]) if report_data[
                                                                                             "cashflowFromFinancing"] != "None" else None,
                    proceedsFromRepaymentsOfShortTermDebt=float(report_data["proceedsFromRepaymentsOfShortTermDebt"]) if
                    report_data["proceedsFromRepaymentsOfShortTermDebt"] != "None" else None,
                    paymentsForRepurchaseOfCommonStock=float(report_data["paymentsForRepurchaseOfCommonStock"]) if
                    report_data["paymentsForRepurchaseOfCommonStock"] != "None" else None,
                    paymentsForRepurchaseOfEquity=float(report_data["paymentsForRepurchaseOfEquity"]) if report_data[
                                                                                                             "paymentsForRepurchaseOfEquity"] != "None" else None,
                    paymentsForRepurchaseOfPreferredStock=float(report_data["paymentsForRepurchaseOfPreferredStock"]) if
                    report_data["paymentsForRepurchaseOfPreferredStock"] != "None" else None,
                    dividendPayout=float(report_data["dividendPayout"]) if report_data[
                                                                               "dividendPayout"] != "None" else None,
                    dividendPayoutCommonStock=float(report_data["dividendPayoutCommonStock"]) if report_data[
                                                                                                     "dividendPayoutCommonStock"] != "None" else None,
                    dividendPayoutPreferredStock=float(report_data["dividendPayoutPreferredStock"]) if report_data[
                                                                                                           "dividendPayoutPreferredStock"] != "None" else None,
                    proceedsFromIssuanceOfCommonStock=float(report_data["proceedsFromIssuanceOfCommonStock"]) if
                    report_data["proceedsFromIssuanceOfCommonStock"] != "None" else None,
                    proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet=float(
                        report_data["proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet"]) if report_data[
                                                                                                         "proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet"] != "None" else None,
                    proceedsFromIssuanceOfPreferredStock=float(report_data["proceedsFromIssuanceOfPreferredStock"]) if
                    report_data["proceedsFromIssuanceOfPreferredStock"] != "None" else None,
                    proceedsFromRepurchaseOfEquity=float(report_data["proceedsFromRepurchaseOfEquity"]) if report_data[
                                                                                                               "proceedsFromRepurchaseOfEquity"] != "None" else None,
                    proceedsFromSaleOfTreasuryStock=float(report_data["proceedsFromSaleOfTreasuryStock"]) if
                    report_data["proceedsFromSaleOfTreasuryStock"] != "None" else None,
                    changeInCashAndCashEquivalents=float(report_data["changeInCashAndCashEquivalents"]) if report_data[
                                                                                                               "changeInCashAndCashEquivalents"] != "None" else None,
                    changeInExchangeRate=float(report_data["changeInExchangeRate"]) if report_data[
                                                                                           "changeInExchangeRate"] != "None" else None,
                    netIncome=float(report_data["netIncome"]) if report_data["netIncome"] != "None" else None
                )
                reports.append(report)

        return reports


@dataclass
class IncomeStatement:
    id: str
    ticker: str
    type: str
    fiscalDateEnding: date
    reportedCurrency: str
    grossProfit: float = None
    totalRevenue: float = None
    costOfRevenue: float = None
    costofGoodsAndServicesSold: float = None
    operatingIncome: float = None
    sellingGeneralAndAdministrative: float = None
    researchAndDevelopment: float = None
    operatingExpenses: float = None
    investmentIncomeNet: float = None
    netInterestIncome: float = None
    interestIncome: float = None
    interestExpense: float = None
    nonInterestIncome: float = None
    otherNonOperatingIncome: float = None
    depreciation: float = None
    depreciationAndAmortization: float = None
    incomeBeforeTax: float = None
    incomeTaxExpense: float = None
    interestAndDebtExpense: float = None
    netIncomeFromContinuingOperations: float = None
    comprehensiveIncomeNetOfTax: float = None
    ebit: float = None
    ebitda: float = None
    netIncome: float = None

    @staticmethod
    def create_pnl(json_data):
        reports = []
        for report_type, reports_data in [("annual", json_data["annualReports"]),
                                          ("quarterly", json_data["quarterlyReports"])]:
            for report_data in reports_data:
                report = IncomeStatement(
                    id=json_data["symbol"] + report_data["fiscalDateEnding"] + report_type,
                    ticker=json_data["symbol"],
                    type=report_type,
                    fiscalDateEnding=date.fromisoformat(report_data["fiscalDateEnding"]),
                    reportedCurrency=report_data["reportedCurrency"],
                    grossProfit=float(report_data["grossProfit"]) if report_data["grossProfit"] != "None" else None,
                    totalRevenue=float(report_data["totalRevenue"]) if report_data["totalRevenue"] != "None" else None,
                    costOfRevenue=float(report_data["costOfRevenue"]) if report_data[
                                                                             "costOfRevenue"] != "None" else None,
                    costofGoodsAndServicesSold=float(report_data["costofGoodsAndServicesSold"]) if report_data[
                                                                                                       "costofGoodsAndServicesSold"] != "None" else None,
                    operatingIncome=float(report_data["operatingIncome"]) if report_data[
                                                                                 "operatingIncome"] != "None" else None,
                    sellingGeneralAndAdministrative=float(report_data["sellingGeneralAndAdministrative"]) if
                    report_data["sellingGeneralAndAdministrative"] != "None" else None,
                    researchAndDevelopment=float(report_data["researchAndDevelopment"]) if report_data[
                                                                                               "researchAndDevelopment"] != "None" else None,
                    operatingExpenses=float(report_data["operatingExpenses"]) if report_data[
                                                                                     "operatingExpenses"] != "None" else None,
                    investmentIncomeNet=float(report_data["investmentIncomeNet"]) if report_data[
                                                                                         "investmentIncomeNet"] != "None" else None,
                    netInterestIncome=float(report_data["netInterestIncome"]) if report_data[
                                                                                     "netInterestIncome"] != "None" else None,
                    interestIncome=float(report_data["interestIncome"]) if report_data[
                                                                               "interestIncome"] != "None" else None,
                    interestExpense=float(report_data["interestExpense"]) if report_data[
                                                                                 "interestExpense"] != "None" else None,
                    nonInterestIncome=float(report_data["nonInterestIncome"]) if report_data[
                                                                                     "nonInterestIncome"] != "None" else None,
                    otherNonOperatingIncome=float(report_data["otherNonOperatingIncome"]) if report_data[
                                                                                                 "otherNonOperatingIncome"] != "None" else None,
                    depreciation=float(report_data["depreciation"]) if report_data["depreciation"] != "None" else None,
                    depreciationAndAmortization=float(report_data["depreciationAndAmortization"]) if report_data[
                                                                                                         "depreciationAndAmortization"] != "None" else None,
                    incomeBeforeTax=float(report_data["incomeBeforeTax"]) if report_data[
                                                                                 "incomeBeforeTax"] != "None" else None,
                    incomeTaxExpense=float(report_data["incomeTaxExpense"]) if report_data[
                                                                                   "incomeTaxExpense"] != "None" else None,
                    interestAndDebtExpense=float(report_data["interestAndDebtExpense"]) if report_data[
                                                                                               "interestAndDebtExpense"] != "None" else None,
                    netIncomeFromContinuingOperations=float(report_data["netIncomeFromContinuingOperations"]) if
                    report_data["netIncomeFromContinuingOperations"] != "None" else None,
                    comprehensiveIncomeNetOfTax=float(report_data["comprehensiveIncomeNetOfTax"]) if report_data[
                                                                                                         "comprehensiveIncomeNetOfTax"] != "None" else None,
                    ebit=float(report_data["ebit"]) if report_data["ebit"] != "None" else None,
                    ebitda=float(report_data["ebitda"]) if report_data["ebitda"] != "None" else None,
                    netIncome=float(report_data["netIncome"]) if report_data["netIncome"] != "None" else None
                )
                reports.append(report)

        return reports
    

@dataclass
class Company:
    symbol: str
    asset_type: str
    name: str
    description: str
    cik: int
    exchange: str
    currency: str
    country: str
    sector: str
    industry: str
    address: str
    fiscal_year_end: str

    @staticmethod
    def create_company_overview(json):
        company = Company(
            json["Symbol"],
            json["AssetType"],
            json["Name"],
            json["Description"],
            json["CIK"],
            json["Exchange"],
            json["Currency"],
            json["Country"],
            json["Sector"],
            json["Industry"],
            json["Address"],
            json["FiscalYearEnd"]
        )
        return company

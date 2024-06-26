from agency_swarm.tools import BaseTool
from pydantic import Field
import yfinance as yf

class YFinanceTools(BaseTool):
    """
    This tool enables the agent to retrieve financial information about a company using the Yahoo Finance API.
    It accepts a company ticker symbol as input and returns relevant financial data such as revenue, profit margins, debt levels, cash flow, and key financial ratios.
    """

    # Define the fields with descriptions using Pydantic Field
    ticker_symbol: str = Field(
        ..., description="The ticker symbol of the company to retrieve financial information for."
    )

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method retrieves financial information about the specified company using the Yahoo Finance API.
        """
        # Retrieve the financial data using yfinance
        try:
            stock = yf.Ticker(self.ticker_symbol)
            info = stock.info
            financials = stock.financials
            # balance_sheet = stock.balance_sheet
            # cash_flow = stock.cashflow

            # Extract relevant financial data
            financial_data = {
                "company_name": info.get("longName", "N/A"),
                "stock": {
                    "stock_price": info.get("currentPrice", "N/A"),
                    "market_cap": info.get("marketCap", "N/A"),
                    "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                    "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
                    "dividend_yield": info.get("dividendYield", "N/A"),
                    "pe_ratio": info.get("trailingPE", "N/A"),
                    "eps": info.get("trailingEps", "N/A"),
                },
                "revenue": financials.loc["Total Revenue"].to_dict() if "Total Revenue" in financials.index else "N/A",
                "margin": {
                    "gross_profit_margin": info.get("grossMargins", "N/A"),
                    "operating_profit_margin": info.get("operatingMargins", "N/A"),
                    "net_profit_margin": info.get("netMargins", "N/A"),
                },
                # "debt_levels": balance_sheet.loc["Long Term Debt"].to_dict() if "Long Term Debt" in balance_sheet.index else "N/A",
                # "debt_to_equity_ratio": info.get("debtToEquity", "N/A"),
                # "cash_flow": {
                #     "operating_activities": cash_flow.loc["Total Cash From Operating Activities"].to_dict() if "Total Cash From Operating Activities" in cash_flow.index else "N/A",
                #     "investing_activities": cash_flow.loc["Total Cashflows From Investing Activities"].to_dict() if "Total Cashflows From Investing Activities" in cash_flow.index else "N/A",
                #     "financing_activities": cash_flow.loc["Total Cash From Financing Activities"].to_dict() if "Total Cash From Financing Activities" in cash_flow.index else "N/A",
                # },
                # "key_financial_ratios": {
                #     "current_ratio": info.get("currentRatio", "N/A"),
                #     "quick_ratio": info.get("quickRatio", "N/A"),
                #     "return_on_equity": info.get("returnOnEquity", "N/A"),
                #     "return_on_assets": info.get("returnOnAssets", "N/A"),
                # }
            }

            return financial_data
        except Exception as e:
            return f"Error: Unable to retrieve financial data. {str(e)}"

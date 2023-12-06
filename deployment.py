import streamlit as st
import pandas as pd
import yfinance as yf

stats = [
    # "Net income applicable to common shares",
    "Total Assets",
    # "Total cash flow from operating activities",
    # "Long-term debt",
    # "Other liabilities",
    # "Total current assets",
    # "Total current liabilities",
    # "Common stock",
    # "Total revenue",
    # "Gross profit",
]  # change as required

indx = [
    "NetIncome",
    "TotAssets",
    "CashFlowOps",
    "LTDebt",
    "OtherLTDebt",
    "CurrAssets",
    "CurrLiab",
    "CommStock",
    "TotRevenue",
    "GrossProfit",
]

def score_prediction_tab():
    st.write("# Score Prediction Tab")
    tickers = st.text_input("Enter your input:", "Input text here")
    if st.button('Predict Score'):
        # Add your prediction logic here based on the input_text
        #fetching the data
        financials_dict = {}
        for ticker in tickers:
            stock = yf.Ticker(ticker)

            # Fetching income statement data
            income_statement = stock.financials
            income_statement.dropna(axis=0, how="all", inplace=True)
            income_statement = income_statement.iloc[:, :3]
            financials_dict[ticker + "_income_statement"] = income_statement

            # Fetching balance sheet data
            balance_sheet = stock.balance_sheet
            balance_sheet.dropna(axis=0, how="all", inplace=True)
            balance_sheet = balance_sheet.iloc[:, :3]
            financials_dict[ticker + "_balance_sheet"] = balance_sheet

            # Fetching cash flow data
            cash_flow = stock.cashflow
            cash_flow.dropna(axis=0, how="all", inplace=True)
            cash_flow = cash_flow.iloc[:, :3]
            financials_dict[ticker + "_cash_flow"] = cash_flow

            df = pd.DataFrame(columns=cash_flow.columns)
        
        #FIltering 
        def info_filter(df, stats, indx):
            tickers = df.columns
            all_stats = {}
            for ticker in tickers:
                try:
                    temp: pd.Series = df[ticker]
                    ticker_stats = []
                    for stat in stats:
                        ticker_stats.append(temp.loc[stat])
                    all_stats["{}".format(ticker)] = ticker_stats
                except Exception as e:
                    print("can't read data for ", ticker)

            all_stats_df = pd.DataFrame(all_stats, index=indx)

            # cleansing of fundamental data imported in dataframe
            all_stats_df[tickers] = all_stats_df[tickers].replace({",": ""}, regex=True)
            for ticker in all_stats_df.columns:
                all_stats_df[ticker] = pd.to_numeric(
                    all_stats_df[ticker].values, errors="coerce"
                )
            return all_stats_df
        
        
        predicted_score = 0  # Replace with the predicted score
        st.write(f"Predicted Score: {predicted_score}")

def portfolio_optimization_tab():
    st.write("# Portfolio Optimization Tab")
    st.write("Add your portfolio optimization code here.")

tabs = ["Score Prediction", "Portfolio Optimization"]
tab_choice = st.sidebar.radio("Select a tab:", tabs)

if tab_choice == "Score Prediction":
    score_prediction_tab()
elif tab_choice == "Portfolio Optimization":
    portfolio_optimization_tab()

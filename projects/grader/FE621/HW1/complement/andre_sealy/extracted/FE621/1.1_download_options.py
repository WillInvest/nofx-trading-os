from calendar import monthrange
from datetime import date, timedelta

import pandas as pd
import yfinance as yf


def is_third_friday(d):
    """
    Check if a date is the 3rd Friday of its months.
    """

    # getting the first day of the month
    first_day = date(d.year, d.month, 1)

    days_until_first_friday = (4 - first_day.weekday()) % 7
    if days_until_first_friday == 0 and first_day.weekday() != 4:
        days_until_first_friday = 7

    first_friday = first_day + timedelta(days=days_until_first_friday)

    # 3rd Friday is 14 days after the first Friday
    third_friday = first_friday + timedelta(days=14)

    return d == third_friday


if __name__ == "__main__":

    tickers_input = input(
        "Enter option tickers seperated by commas (e.g., SPY,AAPL,JPM,...): "
    )
    ticker_list = [t.strip().upper() for t in tickers_input.split(",")]

    file_name = input("Enter the file name for exporting: ")

    # Get todays's date and calculate the date 3 months from now
    today = date.today()
    three_months_later = today + timedelta(days=90)

    third_friday_expirations = {}

    all_calls = []
    all_puts = []

    for ticker in ticker_list:
        print(ticker)

        option = yf.Ticker(ticker)
        option.option_chain()

        expirations = option._expirations
        print(expirations)

        for exp_date_str, unix_timestamp in expirations.items():
            # Convert expiration date string to date object
            exp_date = date.fromisoformat(exp_date_str)

            # Check if within next 3 months and is 3rd Friday
            if today <= exp_date <= three_months_later and is_third_friday(exp_date):
                third_friday_expirations[exp_date_str] = unix_timestamp

        # print(f"Third Friday expirations for the next 3 months:")
        # print(third_friday_expirations)

        expiration_list = list(third_friday_expirations.keys())

        for expr_date in expiration_list:
            print(expr_date)
            try:
                opt_chain = option.option_chain(expr_date)
                calls = opt_chain.calls.copy()
                puts = opt_chain.puts.copy()

                calls["expirationDate"] = expr_date
                puts["expirationDate"] = expr_date

                all_calls.append(calls)
                all_puts.append(puts)

            except Exception as e:
                print(f"Failed to get date for {expr_date}: {e}")

    calls_df = pd.concat(all_calls, ignore_index=True)
    puts_df = pd.concat(all_puts, ignore_index=True)

    print(calls_df.head())

    merged_df = calls_df.merge(puts_df, how="outer")
    print(merged_df)

    merged_df.to_csv(f"{file_name}", index=False)

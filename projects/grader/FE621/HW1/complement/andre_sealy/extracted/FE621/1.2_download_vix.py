import numpy as np
import pandas as pd
import yfinance as yf

df = pd.read_csv("data2.csv")
df["lastTradeDate"] = pd.to_datetime(df["lastTradeDate"], utc=True, errors="coerce")

expiration_dates = ["2026-02-18", "2026-03-18", "2026-04-15"]

all_calls = []
all_puts = []

option = yf.Ticker("^VIX")
calls_chain_0 = option.option_chain(expiration_dates[0]).calls
calls_chain_0["expirationDate"] = expiration_dates[0]
calls_chain_1 = option.option_chain(expiration_dates[1]).calls
calls_chain_1["expirationDate"] = expiration_dates[1]
calls_chain_2 = option.option_chain(expiration_dates[2]).calls
calls_chain_2["expirationDate"] = expiration_dates[2]

all_calls.append(calls_chain_0)
all_calls.append(calls_chain_1)
all_calls.append(calls_chain_2)

calls_df = pd.concat(all_calls, ignore_index=True)

print(calls_df.tail())

puts_chain_0 = option.option_chain(expiration_dates[0]).puts
puts_chain_0["expirationDate"] = expiration_dates[0]
puts_chain_1 = option.option_chain(expiration_dates[1]).puts
puts_chain_1["expirationDate"] = expiration_dates[1]
puts_chain_2 = option.option_chain(expiration_dates[2]).puts
puts_chain_2["expirationDate"] = expiration_dates[2]

all_puts.append(puts_chain_0)
all_puts.append(puts_chain_1)
all_puts.append(puts_chain_2)

puts_df = pd.concat(all_puts, ignore_index=True)

print(puts_df.tail())

merged_df = calls_df.merge(puts_df, how="outer")

final_df = df.merge(merged_df, how="outer")

final_df.to_csv("data2.csv", index=False)

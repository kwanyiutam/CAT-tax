##### gen_input.py #####
## Code which generates an excel output with a sample transaction

## Modules to input
import math
import random
import yfinance as yf
import numpy as np
import pandas as pd
import time
from datetime import datetime

## Project modules to input
import check_inputs # Modules to check inputs

# Initial referenve values
default_in_type = {"stock_num": int, "stock_val": float, "min_trans": int, "max_trans": int, "step_trans": int, "final_sell": bool}
default_in = list(default_in_type.keys())
default_in.sort()
stock_init = {"META": {"stock_num": 0, "stock_val": 0, "min_trans": 10, "max_trans": 50, "step_trans": 10, "final_sell": True},
              "TSLA": {"stock_num": 0, "stock_val": 0, "min_trans": 20, "max_trans": 20, "step_trans": 10, "final_sell": False}}
time_format = "%Y-%m-%d"

## random_date
## Function: Produces a random date
## Input: start - start date
##        end - end dates
## Output: Return a random date between the start dates
def random_date(start, end):
    # Get random number and initialise time format
    prop = random.random()
    
    # Create the start and end time
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    # Get the proportioned time between the two dates
    ptime = stime + prop * (etime - stime)

    # Convert back to the correct time format and return
    return time.strftime(time_format, time.localtime(ptime))

## net_share
## Function: Gets the net share of each row
## Input: row - row of a dataframe
## Output: Return the quantity (positive = buy, negative = sell)
def net_share(row):
    quantity = row["Quantity"]
    if row["Buy/Sell"] == "Sell":
        return -quantity
    else:
        return quantity

## share_value
## Function: Gets the value of the transaction
## Input: row - row of a dataframe
## Output: Return the value
def share_value(row):
    quantity = row["Quantity"]
    price = row["Unit Price"]
    value = quantity * price
    
    return value

## settlement_calc
## Function: Calculates the settlement amount using the percentage
## Input: row - row of a dataframe
##        p_transact - transaction fee percentage 
## Output: Return the settlement amount (i.e. amount actually paid/received)
def settlement_calc(row, p_transact):
    value = share_value(row)
    
    if row["Buy/Sell"] == "Sell":
        # reduce received amount because of transaction fee
        return (value*(1-p_transact))
    else:
        # increase cost because of transaction fee
        return -(value*(1+p_transact))

## gen_main
## Function: Main function to generate stock inputs
## Inputs: stocks - (mandatory, dict) dictionary of stocks (e.g. TSLA) with the following properties 
##                   stock_num - (int) number of stocks held before first year
##                   stock_val - (float) stock value for the stocks held
##                   min_trans - (int) minimum number of shares to transact
##                   max_trans - (int) maximum number of shares to transact
##                   step_trans - (int) step size for shares
##                   final_sell - (bool) whether final transaction must be a sell off of all shares
##         n_min - (int) minimum number of transactions per year
##         n_max - (int) maximum number of transactions per year
##         p_sd - (float) probability of the transactions being same day
##         n_sdmin - (int) minimum number of same day transactions
##         n_sdmax - (int) maximum number of same day transactions
##         p_buy - (float) probability of buying a stock
##         p_transact - (float) decimal of transaction fee (treated as probability)
##         year_start - (int) tax year start
##         year_end - (int) tax year end
##         export_xlsx - (bool) export final result to excel?
def gen_input_main(stocks = stock_init,
                   n_min = 2,
                   n_max = 100,
                   p_sd = 0.1,
                   n_sdmin = 2,
                   n_sdmax = 5,
                   p_buy = 0.5,
                   p_transact = 0.01,
                   year_start = 2023,
                   year_end = 2024,
                   export_xlsx = False):
    
    # Checks whether the stocks were initialised correctly
    stocks = check_inputs.check_stocks_in(stocks, default_in, default_in_type)
        
    # Checks whether the inputs were integers and raises error if it is not
    n_min = check_inputs.check_shares(n_min)
    n_max = check_inputs.check_shares(n_max)
    n_sdmin = check_inputs.check_shares(n_sdmin)
    n_sdmax = check_inputs.check_shares(n_sdmax)
    year_start = check_inputs.check_int(year_start)
    year_end = check_inputs.check_int(year_end)
    
    # Checks whether it is a valid probability
    p_sd = check_inputs.check_prob(p_sd)
    p_buy = check_inputs.check_prob(p_buy)
    p_transact = check_inputs.check_prob(p_transact)

    # Tax year start and end
    start_date = f"{year_start}-04-06"
    end_date = f"{year_end}-04-05"
    
    # Check whether the excel choice is a bool
    export_xlsx = check_inputs.check_bool(export_xlsx)
    
    # Initialise dataframe to save inptus
    df_stock_transact = pd.DataFrame(columns = ["Date", "Stock ID", "Buy/Sell", "Unit Price", "Quantity", "Settlement Amount", "Net Share", "Cumulative Share"])

    # For each stock listed
    for stock in list(stocks.keys()):
        # Obtain the stock data from Yahoo
        stock_data = yf.Ticker(str(stock))

        # Get stock history from Yahoo
        df_stock = stock_data.history(start = start_date,
                                      end = end_date,
                                      interval = '1d')

        # Return an error if no stock information was found
        if df_stock.empty:
            raise NoSuchStock("No such stock is found during the time period on Yahoo Finance")
        else:         
            # Get the dates of the stocks
            df_stock_dates = [datetime.strftime(pd.to_datetime(str(i)), time_format) for i in df_stock.index.values]

            # Choose number of stock transactions within the stock year
            n_transaction = random.randint(n_min, n_max)
            
            # Get a list of dates
            date_list = []
            price_list = []
            
            # Count number of dates
            n_dates = 0
            
            # While the number of transaction dates are less than the expected number
            while(n_dates < n_transaction):
                # Choose a random date
                date_picked = random_date(start_date, end_date)
                
                ## Random date may not return true, so pick closest date
                # Get the date timestamp
                date_raw = datetime.strptime(date_picked, time_format)

                ## days_between
                ## Function: Calculates difference between dates
                ## Input: d1 - Dates
                ## Output: Return the difference in days
                def days_between(d1):
                    d1 = datetime.strptime(d1, time_format)
                    return abs((date_raw - d1).days)

                # Map to get the difference in days of the list to the date picked
                day_diff = list(map(days_between, df_stock_dates))
                # Get the index of closest matching date and return this
                date_picked = df_stock_dates[day_diff.index(min(day_diff))]
                # Get the highest and lowest price
                df_stock_low = df_stock["Low"][day_diff.index(min(day_diff))]
                df_stock_high = df_stock["High"][day_diff.index(min(day_diff))]
 
                # Initiate number of transactions that day
                n_sd_trans = 1
                n_trans_left = n_transaction - n_dates

                # If the random number is below probability and there are still
                # enough transactions left
                if random.random() < p_sd and n_trans_left > n_sdmin:
                    # Need to see which value is smaller, number of transactions
                    # or the preset maximum same day transactions
                    n_sdmax_actual = min(n_sdmax, n_trans_left)
                    n_sd_trans = random.randint(n_sdmin, n_sdmax_actual)

                # Extend list by n-number of repeated date and iterate n number of times
                date_list.extend([date_picked]*n_sd_trans)
                # Extend list with n-number of random price between low and high that day
                price_list.extend([random.uniform(df_stock_low, df_stock_high) for i in range(n_sd_trans)])

                n_dates += n_sd_trans
                   
            # Random whether Buy or Sell (below threshold buy, above sell)
            buysell_list = ["Buy" if i < p_buy else "Sell" for i in np.random.random_sample(size = n_transaction)]

            # Get all the possible stocks
            share_possible = np.arange(stocks[stock]["min_trans"], stocks[stock]["max_trans"] + 1, stocks[stock]["step_trans"])
            
            # Randomly choose the number of stocks
            quantity_list = [random.choice(share_possible) for i in range(n_transaction)]
            
            # List of the stock
            id_list = [stock]*n_transaction
            
            # Convert the lists into dataframes
            df_stock_transact_loc = pd.DataFrame(list(zip(date_list, id_list, buysell_list, price_list, quantity_list)),
                                     columns = ["Date", "Stock ID", "Buy/Sell", "Unit Price", "Quantity"])
            
            df_stock_transact_loc = df_stock_transact_loc.sort_values(by = ["Date"])

            # First element must always be Buy if there are zero stocks to begin with
            if stocks[stock]["stock_num"] == 0:
                df_stock_transact_loc.iloc[0, df_stock_transact_loc.columns.get_loc("Buy/Sell")] = "Buy"
                
            n_stocks = stocks[stock]["stock_num"]
                
            # For each transaction, adjust to ensure the shares make sense (e.g. no negative shares)
            for index in range(n_transaction):
                # Get the quantity
                quantity = df_stock_transact_loc.iloc[index, df_stock_transact_loc.columns.get_loc("Quantity")]
                
                # First, if this is the last index, and it is a final sell (i.e. sell off all stocks at the end)
                if index == n_transaction - 1 and stocks[stock]["final_sell"] == True:
                    # Change the final element to Sell and then change the quantity to be the remaining amount
                    df_stock_transact_loc.iloc[index, df_stock_transact_loc.columns.get_loc("Buy/Sell")] = "Sell"
                    df_stock_transact_loc.iloc[index, df_stock_transact_loc.columns.get_loc("Quantity")] = n_stocks
                    n_stocks = 0
                # If the transaction is Buy
                elif df_stock_transact_loc.iloc[index, df_stock_transact_loc.columns.get_loc("Buy/Sell")] == "Buy":
                    # add the quantity to the cumulative
                    n_stocks += quantity
                # If there are no more stocks left and it is a sell
                elif n_stocks == 0:
                    # Change to buy
                    df_stock_transact_loc.iloc[index, df_stock_transact_loc.columns.get_loc("Buy/Sell")] = "Buy"
                    n_stocks += quantity
                # If the quantity to sell is less than the amount of shares that is being held
                elif quantity > n_stocks:
                    # Change the quantity to be the remaining
                    df_stock_transact_loc.iloc[index, df_stock_transact_loc.columns.get_loc("Quantity")] = n_stocks
                    n_stocks = 0
                # For other sells, just subtract the quantity directly
                else:
                    n_stocks -= quantity

            # Creates new column for net shares and cumulative shares
            df_stock_transact_loc["Net Share"] = df_stock_transact_loc.apply(net_share, axis = 1)
            df_stock_transact_loc["Cumulative Share"] = df_stock_transact_loc["Net Share"].cumsum()
            
            # Calculates settlement amount using the transaction percentage fee 
            df_stock_transact_loc["Settlement Amount"] = df_stock_transact_loc.apply(settlement_calc, axis = 1, p_transact = p_transact)

            df_stock_transact = pd.concat([df_stock_transact, df_stock_transact_loc], ignore_index = True)
    # Simplified output without extra columns
    df_return = df_stock_transact[["Date", "Stock ID", "Buy/Sell", "Unit Price", "Quantity", "Settlement Amount"]]
    
    # If the user wants to export excel
    if export_xlsx == True:
        time = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        df_return.to_excel(f'StockInputGenerate_{time}.xlsx')  

    return df_return

            
out = gen_input_main()
print(out)
    
import finnhub
import json
import os
import csv
import inspect
from datetime import datetime

"""
##delete files
import os
cwd = os.getcwd()
file_list = os.listdir(cwd)
for item in file_list:
    if "0" not in item:
        if "-" not in item:
            if ".csv" in item:
                print(item)    
                os.remove(item)

"""

# Get the current working directory
def finnhub_earnings(start, end, file):
    directory = os.getcwd()
    in_directory = os.listdir(directory)
    start_date = start
    end_date = end
    file_name = file

    if file_name + ".json" in in_directory:
        print("already got it")
    if file_name + ".json" not in in_directory:
        finnhub_client = finnhub.Client(
            api_key="cupjchpr01qk8dnkc8qgcupjchpr01qk8dnkc8r0")
        #print(finnhub_client.earnings_calendar(_from="2025-02-18", to="2025-02-18", symbol="", international=False))
        future = finnhub_client.earnings_calendar(_from=start_date,
                                                  to=end_date,
                                                  symbol="",
                                                  international=False)
        # Save the response to a JSON file
        with open(file_name + ".json", 'w') as json_file:
            json.dump(future, json_file, indent=4)
        print("Earnings data has been saved to " + file_name + ".json")
        print("request made")


def stocks_from_finnhub_data(output):
    with open(file_name + ".json", 'r') as json_file:
        data = json.load(json_file)
        keys = []
        for key in data.keys():
            keys.append(key)
        #print(keys)
        #print(keys[0])
        list = data[keys[0]]
        stocks = []
        for item in list:
            #print(item)
            new = []
            symbol = item["symbol"]
            if len(symbol) > 4:
                continue

            hour = item["hour"]
            if len(hour) == 0:
                continue
            new.append(item["symbol"])
            new.append(item["date"])
            new.append(hour)
            stocks.append(new)
    stocks.reverse()
    print(len(stocks))
    #for item in stocks:
    #    print(item)

    with open(output, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(stocks)
    print(output + " file saved successfully!")


def gen_match_file(google_volume_price_file, output_file, variable, base_list):
    price_volume = []
    with open(google_volume_price_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            price_volume.append(row)  # Add each row to the list
    vp2 = []
    for counter, item in enumerate(
            price_volume, start=1):  # start=1 will start the counter from 1
        #print(f"{counter} Item: {item}")
        symbol = item[4]
        if len(symbol) > 4 or len(symbol) == 0:
            continue
        vp = item[0]
        vp = int(float(vp))
        new = [vp, symbol]
        vp2.append(new)
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(vp2)
    future = []
    # Open and read the CSV file
    with open(variable, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            future.append(row)  # Add each row to the list
    #print(future)
    vp2 = []
    # Open and read the CSV file
    with open(output_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            vp2.append(row)  # Add each row to the list
    #print(vp2)
    look_at = []
    for val in future:
        stock1 = val[0]
        for val2 in vp2:
            stock2 = val2[1]
            how_much = val2[0]
            if stock1 == stock2:
                new = []
                new.append(int(val2[0]))
                new.append(val2[1])
                new.append(val[0])
                new.append(val[1])
                new.append(val[2])
                look_at.append(new)
    look_at.sort()
    look_at.reverse()
    current_line = inspect.currentframe().f_lineno
    print(f"Current line number: {current_line}")
    for item in look_at:
        print(item)
    with open(base_list, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(look_at)
    print(base_list + " file saved successfully!")


def get_earnings_dates(match_file):
    look_at = []
    with open(match_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            look_at.append(row)  # Add each row to the list
    #get earnings dates
    from pathlib import Path
    directory_path = Path('')  # Change this to your directory
    files = [f.name for f in directory_path.iterdir() if f.is_file()]
    #print(files)
    import yfinance as yf
    for item in look_at:
        check_stock = item[1]
        check_file = check_stock + "-dates.csv"
        if check_file not in files:
            ticker = check_stock
            stock = yf.Ticker(ticker)
            earnings_dates = stock.earnings_dates
            import pandas as pd
            df = pd.DataFrame(earnings_dates)
            df_reset = df.reset_index()
            list_with_proper_index = [df_reset.columns.tolist()
                                      ] + df_reset.values.tolist()
            list_with_proper_index[0] = [''] + list_with_proper_index[0][1:]
            print(item)
            print(check_file)
            #print(item, look_at.index(item), len(look_at))
            with open(check_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(list_with_proper_index)
            print(len(look_at))
            #place = item.index(look_at)
            #print(place)
            import asyncio
            seconds = 5
            #print(look_at.index(item))
            async def wait_seconds(how_long):
                print("Waiting for " + str(how_long) + " seconds...")
                await asyncio.sleep(seconds)
                print("Done waiting!")
            # Running the async function
            asyncio.run(wait_seconds(seconds))


def get_history(match_file):
    match_list = []
    with open(match_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            match_list.append(row)  # Add each row to the list
    from pathlib import Path
    directory_path = Path('')  # Change this to your directory
    files = [f.name for f in directory_path.iterdir() if f.is_file()]
    import yfinance as yf
    import pandas as pd
    for item in match_list:
        #print(item)
        stock = item[1]
        check_file = stock + "-history.csv"
        if check_file not in files:
            ticker_symbol = stock
            stock = yf.Ticker(ticker_symbol)
            data = stock.history(period='5y')
            # Display the data
            #print(str(data[0:100]))
            #print(type(data))
            df = pd.DataFrame(data)
            # Reset the index and move the index column to the left to align correctly
            df_reset = df.reset_index()
            # Convert DataFrame to list of lists with the index aligned properly
            list_with_proper_index = [df_reset.columns.tolist()
                                      ] + df_reset.values.tolist()
            # Now, shift the first column (row index) so that it aligns with the data
            list_with_proper_index[0] = [''] + list_with_proper_index[0][1:]
            price_data = list_with_proper_index
            for a in range(0,len(price_data)):
                for b in range(0,len(price_data[a])):
                    val = price_data[a][b]
                    if type(val)==pd.Timestamp:
                        price_data[a][b] = price_data[a][b].strftime("%Y-%m-%d")
                    if type(val)==float:
                        new = str(price_data[a][b])
                        new = new[0:new.find(".")+3]
                        price_data[a][b] = float(new)
            print(price_data[a])

            print("over")
            #for item in (list_with_proper_index):
            #    print(item)
            with open(check_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(list_with_proper_index)
            print(check_file)
            print(item, match_list.index(item), len(match_list))
            import asyncio
            async def wait_10_seconds():
                print("Waiting for 10 seconds...")
                await asyncio.sleep(5)
                print("Done waiting!")
            # Running the async function
            asyncio.run(wait_10_seconds())


def prices_around_earnings(match_file):
    match_list = []
    with open(match_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            match_list.append(row)  # Add each row to the list
    match_list.reverse()
    for item in match_list:
        symbol = item[1]
        earnings_dates = []
        dates_file = symbol + "-dates.csv"
        with open(dates_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                earnings_dates.append(row)  # Add each row to the list
        ###start of generate list of earnings dates for each stock
        dates_list = []
        object_current_datetime = datetime.now()
        for item in earnings_dates:
            date_string = item[0][0:item[0].find(" ")]
            #date_string = item[0]
            if len(date_string) > 0:
                object_earnings_date = datetime.strptime(
                    date_string, "%Y-%m-%d")
                if object_earnings_date < object_current_datetime:
                    dates_list.append(date_string)
        #print(symbol)
        #print(dates_list)
        ###end of generate list of earnings dates for each stock
        ###get prices of the stock
        list_prices = []
        prices_file = symbol + "-history.csv"
        with open(prices_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                list_prices.append(row)  # Add each row to the list
        continue_list=  []
        reverse_list = []
        for val in dates_list:
            days_surrounding = []
            for val2 in list_prices:
                if val in val2[0]:
                    index_before=list_prices.index(val2)-1
                    index_after=list_prices.index(val2)+1
                    day_before = list_prices[index_before]
                    day_listed = val2
                    day_after = list_prices[index_after]
                    vol_day_of = int(day_listed[5])
                    vol_day_after = int(day_after[5])
                    day_before = ["       "]+day_before
                    if vol_day_of>vol_day_after:
                        day_listed = ["max_vol"]+day_listed
                        day_after = ["       "]+day_after
                    if vol_day_of<vol_day_after:
                        day_listed = ["       "]+day_listed
                        day_after = ["max_vol"]+day_after

                    days_surrounding.append(day_before)
                    days_surrounding.append(day_listed)
                    days_surrounding.append(day_after)
            for a in range(0,len(days_surrounding)):
                days_surrounding[a]=days_surrounding[a][0:7]
            #print(symbol)
            for a in range(0,len(days_surrounding)):
                item =  days_surrounding[a]
                #print(symbol,item)
                if "max_vol" in item:
                    morning = float(item[2])
                    close_day_before = float(days_surrounding[a-1][5])
                    gap = round(float(((morning/close_day_before)-1)*100),2)
                    continuance=""
                    reversal=""
                    day_high = float(item[3])
                    day_low = float(item[4])
                    if gap>0:
                        continue_value = day_high
                        reverse_value = day_low
                    if gap<0:
                        continue_value = day_low
                        reverse_value = day_high
                    con_cent = round(float(((abs(continue_value/morning))-1)*100),2)
                    rev_cent = round(float(((reverse_value/morning)-1)*100),2)
                    try:
                        ratio_con_rev=abs(round(con_cent/rev_cent,2))
                    except:
                        ratio_con_rev=2
                    try:
                        ratio_rev_con=abs(round(rev_cent/con_cent,2))   
                    except:
                        ratio_rev_con=2
                    #print(symbol,item)
                    changes = {
                        "gap": gap,
                        "open": morning,
                        "day-1": close_day_before,
                        "day_high": day_high,
                        "day_low": day_low,
                        "ratio_con_rev": ratio_con_rev,
                        "ratio_rev_con": ratio_rev_con,
                        "con_cent": con_cent,
                        "continue_max": continue_value,
                        "rev_cent": rev_cent,
                        "reverse_max": reverse_value,
                    }
                    """
                    print ("gap",changes['gap'],changes['open'],changes['day-1'])
                    print ("continue%",changes['con_cent'],changes['continue_max'])
                    print ("reverse%",changes['rev_cent'],changes['reverse_max'])
                    print ("con_ratio",changes['ratio_con_rev'])
                    print ("rev_ratio",changes['ratio_rev_con'])
                    """
                    continue_list.append(ratio_con_rev)
                    reverse_list.append(ratio_rev_con)

        # Check if all values are over 2
        #print(continue_list)
        #print(reverse_list)

        min_count = 4
        min_ratio = 0
        print(symbol)
        if len(continue_list)>min_count:
            if min(continue_list)>min_ratio:
                print(continue_list)
        if len(reverse_list)>min_count:
            if min(reverse_list)>min_ratio:
                print(reverse_list)

def specific_day(day_in_question, file_to_load):
    list = []
    # Open and read the CSV file
    with open(file_to_load, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(row)  # Add each row to the list
    #print(list)
    correct_date = []
    from datetime import datetime, timedelta
    date_str = day_in_question
    # Parse the string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    previous_day = date_obj - timedelta(days=1)
    previous_day_str = previous_day.strftime("%Y-%m-%d")
    day_after = date_obj + timedelta(days=1)
    after_day_str = previous_day.strftime("%Y-%m-%d")


    for a,val in enumerate(list):
        if day_in_question in val or previous_day_str in val or after_day_str in val:
            correct_date.append(val)

    print(correct_date)
    print(day_in_question)
    for a,val in enumerate(correct_date):
        print(val)
        """
    previous_day_str = previous_day.strftime("%Y-%m-%d")
    print(previous_day_str)
    output = []
    for item in list:
        item[0] = int(item[0])
        if day_in_question in item and "bmo" in item:
            output.append(item)
        if previous_day_str in item and "amc" in item:
            output.append(item)
    output.sort()
    output.reverse()
    #for item in output:
    #    print(item)
    """

start_date = "2025-02-01"
end_date = "2025-02-30"
file_name = start_date + "." + end_date
match_file = "0match.csv"
earnings_in_period = "0earnings_in_period.csv"


finnhub_earnings(start_date, end_date, file_name)
stocks_from_finnhub_data(earnings_in_period)
gen_match_file('0vp_google_data.csv', "0vol_pri.csv", earnings_in_period,
               match_file)
get_earnings_dates(match_file)
get_history(match_file)
prices_around_earnings(match_file)
specific_day("2025-02-26", match_file)
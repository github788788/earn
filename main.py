
import json
import os
import csv
import inspect
from datetime import datetime
import time
import sys
import shutil

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


def get_earn_dates(match_file):
    look_at = []
    with open(match_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            look_at.append(row)  # Add each row to the list
    #get earnings dates
    from pathlib import Path
    cwd = os.getcwd()
    edgar_folder = cwd+"//sec-edgar-filings"    
    files = os.listdir(edgar_folder)    
    from sec_edgar_downloader import Downloader
    dl = Downloader("MyCompanyName", "my.email@domain.com")
    print(files)
    cwd = os.getcwd()
    edgar_folder = os.path.join(cwd, "sec-edgar-filings")
    for a,val in enumerate(look_at):
        check_stock = val[1]
        stock = check_stock
        #print (a,len(look_at),check_stock)
        #print("check_stock =",check_stock)
        #check_file = check_stock
        if check_stock not in files:
            print("now getting 8k for")
            print(a,len(look_at),"check_stock =",check_stock)
            ticker_symbol = check_stock
            dl.get("8-K", ticker_symbol)
            print("now gotten 8k for stock "+ticker_symbol)
            #print("and waiting 5 seconds for next one!")
            #for a in range(0,5):
            #    print(a)
            #    time.sleep(1)
    #stocks = os.listdir(edgar_folder)
            #for a,stock in enumerate(stocks):
            print(stock)
            stock_folder = os.path.join(edgar_folder,stock,"8-K")
            print(stock_folder)
            earn_dates = os.listdir(stock_folder)
            print(earn_dates)                       
            for b,date in enumerate(earn_dates):
                print(a,len(look_at),b,len(earn_dates))
            #print(earn_dates)
                if "-25-" not in date:
                    if "-24-" not in date:
                        if "-23-" not in date:
                            if "-22-" not in date:
                                if "-21-" not in date:
                                    if "-20-" not in date:
                                        #print(a,len(look_at),b,len(earn_dates))
                                        #print(date)
                                        to_delete = os.path.join(stock_folder,date)
                                        print(to_delete)
                                        shutil.rmtree(to_delete)
            earn_dates = os.listdir(stock_folder)
            for b,date in enumerate(earn_dates):
                print(a,len(look_at),b,len(earn_dates))
                check_file = os.path.join(stock_folder,date,"full-submission.txt")
                print(check_file)
                with open(check_file, 'r') as file:
                    content = file.read()  # Read the entire content of the file
                    #print(content)
                    if "Results of Operations and Financial Condition" not in content:
                        print("has been deleted!")
                        print(check_file)
                        to_delete = os.path.join(stock_folder,date)
                        shutil.rmtree(to_delete)
                        """
                    else:
                        with open(check_file, "w") as file:
                            file.write(content[0:1000])   
                            """                 
    




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
                        #print(stock)
                        print(new)
                        #print(price_data[a][b])
                        #print(price_data[a])
                        try:
                            price_data[a][b] = float(new)
                        except:
                            continue
            print(price_data[a])
        
            print("over")
            #for item in (list_with_proper_index):
            #    print(item)
            list_with_proper_index.reverse()
            with open(check_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(list_with_proper_index)
            print(check_file)
            print(match_list.index(item), len(match_list),item)
            import asyncio
            async def wait_10_seconds():
                print("Waiting for 5 seconds...")
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
    cwd = os.getcwd()
    edgar_folder = cwd+"//sec-edgar-filings"
    #edgar_stocks = os.listdir(edgar_folder)
    print(match_list)
    double_continue = []
    double_reverse = []
    for a,match in enumerate(match_list): 
        print(a,len(match_list),match)
        symbol = match[1]
        stock = match[1]
        k8_dir = edgar_folder+"//"+stock+"//8-K"
        try:
            k8_list = os.listdir(k8_dir)
        except:
            continue
        earnings_dates = []
        for b,k8_code in enumerate(k8_list):
            if "-25-" not in k8_code and "-24-" not in k8_code and "-23-" not in k8_code: 
                continue
            file_to_load = k8_dir+"//"+k8_code+"//full-submission.txt"
            with open(file_to_load, 'r') as file:
                content = file.read()  # Read the entire content of the file
                #print(content)
                if "Results of Operations and Financial Condition" in content and "Financial Statements and Exhibits" in content:
                    what_to_find = "FILED AS OF DATE:"
                    dates_start = content.find(what_to_find)
                    date_end = content.find("\n",dates_start)
                    date = content[dates_start:date_end]
                    earnings_dates.append(date)
        earnings_dates.sort()
        earnings_dates.reverse()
        earnings_dates=earnings_dates[0:8]
        earnings_dates1 = earnings_dates
        earn_dates2 = []
        for b,date in enumerate(earnings_dates1):
            new = date.replace("FILED AS OF DATE:","")
            new = new.replace("\t","")
            #print(new)
            #new = new[0:4]+"-"+new[4:6]+"-"+new[6:8]
            earn_dates2.append(new)
        #print(earnings_dates1)
        print(earn_dates2)
        dates_list = earn_dates2
        object_current_datetime = datetime.now()    
        list_prices = []
        prices_file = symbol + "-history.csv"
        with open(prices_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                list_prices.append(row)  # Add each row to the list
        #print(list_prices)
        continue_list=  []
        reverse_list = []
        for specific_date in dates_list:
            #print("specific_date",specific_date)
            days_surrounding = []
            for day_prices in list_prices:
                day_prices[0] = day_prices[0].replace("-","")
                if specific_date in day_prices[0]:
                    #print("match! earn_date = ",specific_date,day_prices[0])
                    index_before=list_prices.index(day_prices)-1
                    index_after=list_prices.index(day_prices)+1
                    day_before = list_prices[index_before]
                    day_listed = day_prices
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
            #print(days_surrounding)
            for c in range(0,len(days_surrounding)):
                days_surrounding[c]=days_surrounding[c][0:7]
                #print (days_surrounding[a])
            for c in range(0,len(days_surrounding)):
                item =  days_surrounding[c]
                #print(symbol,item)
                if "max_vol" in item:
                    morning = float(item[2])
                    close_day_before = float(days_surrounding[c-1][5])
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
                    print (symbol,"gap",changes['gap'],changes['day-1'],changes['open'])
                    print ("continue%",changes['con_cent'],changes['continue_max'])
                    print ("reverse%",changes['rev_cent'],changes['reverse_max'])
                    print ("con_ratio",changes['ratio_con_rev'])
                    print ("rev_ratio",changes['ratio_rev_con'])
                    """
                    continue_list.append(ratio_con_rev)
                    reverse_list.append(ratio_rev_con)

        # Check if all values are over 2
        print(continue_list)
        print(reverse_list)
        print("len(dates_list)",len(dates_list))


        min_count = 4
        min_ratio = 2
        print(symbol)
        if len(continue_list)>min_count:
            if min(continue_list)>min_ratio:
                double_continue.append(symbol)
        if len(reverse_list)>min_count:
            if min(reverse_list)>min_ratio:
                double_reverse.append(symbol)

    print("double_continue",double_continue)
    print("double_reverse",double_reverse)

def specific_day(start_day,end_day, file_to_load):
    list = []
    # Open and read the CSV file
    with open(file_to_load, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(row)  # Add each row to the list
    #print(list)
    correct_date = []
    from datetime import datetime, timedelta
    start_date_str = start_day
    end_date_str = end_day
    # Parse the string to a datetime object
    start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d")
    #previous_day = date_obj - timedelta(days=1)
    #previous_day_str = previous_day.strftime("%Y-%m-%d")
    #day_after = date_obj + timedelta(days=1)
    #after_day_str = previous_day.strftime("%Y-%m-%d")
    for a,val in enumerate(list):
        #if day_in_question in val or previous_day_str in val or after_day_str in val:
        check_date_str = val[3]   
        check_date_obj = datetime.strptime(check_date_str, "%Y-%m-%d")
        if check_date_obj>=start_date_obj:
             if check_date_obj<=end_date_obj:
                correct_date.append(val)
            
    #print(correct_date)
    #print(day_in_question)
    correct_date = correct_date[0:30]
    for a,val in enumerate(correct_date):
        print(val)

start_date = "2025-02-01"
end_date = "2025-02-20"
file_name = start_date + "." + end_date
match_file = "0match.csv"
earnings_in_period = "0earnings_in_period.csv"

finnhub_earnings(start_date, end_date, file_name)
stocks_from_finnhub_data(earnings_in_period)
gen_match_file('0vp_google_data.csv', "0vol_pri.csv", earnings_in_period,
               match_file)
get_earn_dates(match_file)
get_history(match_file)
prices_around_earnings(match_file)
specific_day(start_date,end_date, match_file)

"""
do function that erases value if it has less than 4 earnings per stock
"""
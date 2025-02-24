import os,shutil
cwd = os.getcwd()
edgar_folder = os.path.join(cwd, "sec-edgar-filings")
stocks = os.listdir(edgar_folder)
for a,stock in enumerate(stocks):
    print(stock)
    stock_folder = os.path.join(edgar_folder,stock,"8-K")
    print(stock_folder)
    earn_dates = os.listdir(stock_folder)
    print(earn_dates)                       
    for b,date in enumerate(earn_dates):
        print(a,len(stocks),b,len(earn_dates))
    #print(earn_dates)
        if "-25-" not in date:
            if "-24-" not in date:
                if "-23-" not in date:
                    if "-22-" not in date:
                        if "-21-" not in date:
                            if "-20-" not in date:
                                #print(a,len(stocks),b,len(earn_dates))
                                #print(date)
                                to_delete = os.path.join(stock_folder,date)
                                print(to_delete)
                                shutil.rmtree(to_delete)
    for b,date in enumerate(earn_dates):
        print(a,len(stocks),b,len(earn_dates))
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
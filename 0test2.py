import os,shutil
cwd = os.getcwd()
edgar_folder = os.path.join(cwd, "sec-edgar-filings")
stocks = os.listdir(edgar_folder)
for a,stock in enumerate(stocks):
    #print(stock)
    stock_folder = os.path.join(edgar_folder,stock,"8-K")
    #print(stock_folder)
    earn_dates = os.listdir(stock_folder)
    #print(earn_dates)                       
    for b,date in enumerate(earn_dates):
        print(a,len(stocks),b,len(earn_dates))
        check_file = os.path.join(stock_folder,date,"full-submission.txt")
        print(check_file)
        with open(check_file, 'r') as file:
            content = file.read()  # Read the entire content of the file
            if len(content)>1001:
                print(len(content))
                with open(check_file, "w") as file:
                    file.write(content[0:1000]) 
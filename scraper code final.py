import requests
import pandas as pd
from time import sleep 
import os

###
# ANNOUNCEMENT: when scraping for other elections, make sure to change the year and the querry to the candidates for that election cycle
###


# Query GDELT Doc API for recent US articles
url = "https://api.gdeltproject.org/api/v2/doc/doc"
days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 4] # number of days in each month to make the nested for loops easier to implement
# november only has ten days because we don't need to get articles from past election day

year = 2024 ### CHANGE THIS DEPENDING ON THE ELECTION CYCLE
candidates = "trump AND harris" ### CHANGE THIS DEPENDING ON THE ELECTION CYCLE

# creating folders for the year if it already doesn't exist
path = f"us_articles\\{year} election cycle"
try:
    os.makedirs(path)
    print(f"Folders '{path}' created successfully.")
except FileExistsError:
    print(f"Folders '{path}' already exist.")
except OSError as e:
    print(f"Error creating folders: {e}")

### loop through jan-nov
for month in range(2,12): # exclude december bc the election results are out by then
    
    # creating folders for each month if it doesnt exist already
    path = f"us_articles\\{year} election cycle\\month {month}"
    try:
        os.makedirs(path)
        print(f"Folders '{path}' created successfully.")
    except FileExistsError:
        print(f"Folders '{path}' already exist.")
    except OSError as e:
        print(f"Error creating folders: {e}")

    ### each day gets its own dataset
    for day in range(1, days_in_month[month-1]+1): #plus one error on the months bc the list indexes starting with 0, but january is represented by 1 and plus one error on the number of days in the month because range() is non inclusive at the end
        
        # code to reset the DFs and adding a header only
        response = requests.get(url, params={"query":"icecream","mode":"artlist","maxrecords": 1,"format": "json"})
        
        sleeptime = 45 # sometimes the api softlocks us from making requests, so we have to wait it out
        while response.status_code == 429:
            print(f"sleeping for {sleeptime} seconds, wait 5 seconds my ass")
            sleep(sleeptime)
            response = requests.get(url, params=params)
            sleeptime += 5

        data = response.json()
        article = data.get("articles", [])
        me = pd.DataFrame(article)
        me=me.drop(0)
        me.to_csv(f"C:\\Users\\Woochoel Shin\\Pictures\\Ezras stuff temporary\\coding\\Stemforall\\us_articles\\{year} election cycle\\month {month}\\{year}-{month}-{day}_gdelt_articles.csv", index=False)#, quotechar=""")
        
        # changes start and end to be modified by fstrings, not math. 
        # this means you can now start the scraping process at any date by adjusting the range of the nested for loops
        start = int(f"{year}{month:02d}{day:02d}000000")
        end = int(f"{year}{month:02d}{day:02d}003000")

        ### scrape every hour within a day, then add it to the "day" csv file
        for hour in range(0,24): #idr why this starts at 0 while the other two loops start at 1
            
            # reaching out to the api
            params = {
                "query": f"{candidates} AND sourcelang:english AND theme:ELECTION AND sourcecountry:US",
                "mode": "artlist",
                "maxrecords": 250,
                "format": "json",
                "sort": "datedesc",
                "STARTDATETIME" : start, 
                "ENDDATETIME" : end #for some reason, gdelt gives us articles 45 minutes past the endtime i give it
            }
            
            response = requests.get(url, params=params)

            # waiting out the softlock, previously thought to be 45 sec, but when we increased the wait time to 45, we still ended up waiting for a total of 520 seconds. 
            # new hypothesis is now 500 seconds
            sleeptime = 500
            while response.status_code == 429:
                print(f"sleeping for {sleeptime} seconds, wait 5 seconds my ass")
                sleep(sleeptime)
                response = requests.get(url, params=params)
                sleeptime += 5

            if response.status_code != 200:
                print("Error:", response.status_code)
                print(response.text)
                exit()

            data = response.json()
            articles = data.get("articles", [])

            # Convert to DataFrame
            df = pd.DataFrame(articles)

            # append this hour's worth of articles to the day csv
            df.to_csv(f"C:\\Users\\Woochoel Shin\\Pictures\\Ezras stuff temporary\\coding\\Stemforall\\us_articles\\{year} election cycle\\month {month}\\{year}-{month}-{day}_gdelt_articles.csv", mode='a', header=False, index=False)#, quotechar=""")
            
            # print the number of articles that we downloaded from that hour
            # print(f"{hour}. Saved {str(len(df))} articles from time {start} to {end}")

            # move up by an hour. the time resets when start,end is set
            start += 10000
            end += 10000

        # stupid method to index the entire thing. reads the entire csv, then it replaces that same csv but now with indexes
        df_day = pd.read_csv(f"C:\\Users\\Woochoel Shin\\Pictures\\Ezras stuff temporary\\coding\\Stemforall\\us_articles\\{year} election cycle\\month {month}\\{year}-{month}-{day}_gdelt_articles.csv")
        df_day.to_csv(f"C:\\Users\\Woochoel Shin\\Pictures\\Ezras stuff temporary\\coding\\Stemforall\\us_articles\\{year} election cycle\\month {month}\\{year}-{month}-{day}_gdelt_articles.csv", header=True, index=True)

        # prints number of articles downloaded on each day
        print(f"day {day} done: {len(df_day)} articles downloaded")

    # keep track of what months are done
    print(f"month {month} done")
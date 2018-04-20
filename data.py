import requests
from bs4 import BeautifulSoup
import json
import sqlite3 as sqlite

from requests_oauthlib import OAuth1
from secrets import twitter_api_key
from secrets import twitter_api_secret
from secrets import twitter_access_token
from secrets import twitter_access_token_secret


consumer_key = twitter_api_key
consumer_secret = twitter_api_secret
access_token = twitter_access_token
access_secret = twitter_access_token_secret


#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)

## cache codes
# on startup, try to load the cache from file
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}


def get_unique_key(url):
  return url


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)

def make_request_using_cache(url, params=None):
    header = {'User-Agent': 'SI_CLASS'}
    if params is None:
        unique_ident = get_unique_key(url)
    else:
        unique_ident = params_unique_combination(url, params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        if params is None:
            resp = requests.get(url, headers=header)
        else:
            resp = requests.get(url, params, auth=auth)

        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]



def get_data_crawl():
    #
    result = {}
    ## first get the list of all states abbr
    master_url = 'https://spotcrime.com'
    index_page_url = master_url + '/mi/ann+arbor/daily'
    index_page_text = make_request_using_cache(index_page_url)
    page_soup = BeautifulSoup(index_page_text, 'html.parser')
    view_more = page_soup.find(title='View older data')

    ## open up 'view more' to crawl the data from 2017 - 2018
    view_more_url = master_url + view_more['href']
    view_more_page_text = make_request_using_cache(view_more_url)
    page_soup_2 = BeautifulSoup(view_more_page_text, 'html.parser')
    crimes_list = page_soup_2.find(class_='main-content-column').find_all('ol')
    # print(len(crimes_list))
    counter = 1
    # print("before loop")
    for segment in crimes_list:
        for date in segment:
            # print("In the loop")
            cur_result = []
            cur_date_url = date.find('a')['href']
            cur_date_args = cur_date_url.split('/')
            ## weed out data before 2017
            temp_year = cur_date_args[-1].split('-')[0]
            temp_month = cur_date_args[-1].split('-')[1]
            temp_day = cur_date_args[-1].split('-')[2]
            if (temp_year >= '2017') or (temp_year >= '2016' and temp_month >= '09' and temp_day >= '20'):
                print(counter)
                counter += 1
                cur_date = cur_date_args[-1]
                crime_record_per_day_url = master_url + cur_date_url
                # print("current url: ", crime_record_per_day_url)
                # print(crime_record_per_day_url)
                crime_record_per_day_text = make_request_using_cache(crime_record_per_day_url)
                page_soup_3 = BeautifulSoup(crime_record_per_day_text, 'html.parser')
                crimes_list_per_day = page_soup_3.find(class_='main-content-column').find_all('tr')
                # print(crimes_list_per_day)
                # break
                for single_crime in crimes_list_per_day:
                    # print(single_crime)
                    temp_result = []
                    table_cells = single_crime.find_all('td')
                    if not table_cells:
                        table_cells = single_crime.find_all('th')
                        for i in range(5):
                            temp_result.append(table_cells[i].text.strip())
                            result['title_row'] = temp_result
                        continue
                    # print(table_cells)
                    for i in range(5):
                        if i != 4:
                            temp_result.append(table_cells[i].text.strip())
                        else:
                            detail_url = table_cells[i].find('a')['href']
                            crime_detail_url = master_url + detail_url
                            crime_detail_text = make_request_using_cache(crime_detail_url)
                            page_soup_4 = BeautifulSoup(crime_detail_text, 'html.parser')
                            case_number_wrapper = page_soup_4.find(class_='dl-horizontal').find_all('dd')
                            temp_result.append(case_number_wrapper[4].text.strip())
                            # temp_result.append(table_cells[i])
                    cur_result.append(temp_result)
                result[cur_date] = temp_result

        # print(crimes_list_per_day)
        # break

    print(json.dumps(result, indent=4))
    del result['title_row']
    return result


def get_crimes_data(crawl_data_dict):
    results = []
    for item in crawl_data_dict:
        cur_value_list = crawl_data_dict[item]
        if cur_value_list[1] not in results:
            results.append(cur_value_list[1])
    return results


## this function will return the parameter of crimecases_data
def get_crime_access_data(crawl_data_dict):
    ## results = [['theft', CaseNumber, Year, Month, Day, Address]]
    results = []
    for item in crawl_data_dict:
        dates_list = item.split('-')
        # print(dates_list)
        temp_result = []
        cur_value_list = crawl_data_dict[item]
        ## add 'theft'
        temp_result.append(cur_value_list[1])
        temp_result.append(cur_value_list[-1])
        temp_result.append(dates_list[0])
        temp_result.append(dates_list[1])
        temp_result.append(dates_list[2])
        temp_result.append(cur_value_list[-2])
        results.append(temp_result)
    return results





def process_twitter_data(crime_type):
    ## crime_tweets_data = [['theft', TweetText, Year, Month, DayNum, DayStr, RetweetCount]]
    results = []
    search_query = crime_type + " michigan"
    cur_base_url = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {'q': search_query, 'count': 30}

    cur_response = json.loads(make_request_using_cache(cur_base_url, params=params))
    # result_tweets = []

    for item in cur_response['statuses']:
        temp_result = []
        # 1. crime_type
        temp_result.append(crime_type)
        # 2. TweetText
        temp_result.append(item['text'])
        temp_date = item['created_at']
        # print(temp_date)
        temp_date = temp_date.split(" ")
        # 3. Year
        temp_result.append(temp_date[5])
        # 4. Month
        temp_result.append(temp_date[1])
        # 5. Day_number
        temp_result.append(temp_date[2])
        # 6. Day_string
        temp_result.append(temp_date[0])
        # 7. retweet count
        temp_result.append(item['retweet_count'])
        results.append(temp_result)
    # print(results)
    return results


# def get_data_twitter():




def create_db():
    conn = sqlite.connect('crimes.db')
    cur = conn.cursor()

    # Code below provided for your convenience to clear out the big10 database
    # This is simply to assist in testing your code.  Feel free to comment it
    # out if you would prefer
    statement = '''
        DROP TABLE IF EXISTS 'Crimes';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'CrimeCases';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'CrimeTweets';
    '''
    cur.execute(statement)
    conn.commit()

    # Your code to create the tables in the dB goes here

    statement = '''
        CREATE TABLE 'Crimes' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'CrimeName' TEXT
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'CrimeCases' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'CrimeType' INTEGER,
            'CaseNumber' TEXT,
            'Year' TEXT,
            'Month' TEXT,
            'Day' TEXT,
            'Address' TEXT,
            FOREIGN KEY(CrimeType) REFERENCES Crimes(Id)
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'CrimeTweets' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'CrimeTypeTweet' INTEGER,
                'TweetText' TEXT,
                'Year' TEXT,
                'Month' TEXT,
                'DayNum' TEXT,
                'DayStr' TEXT,
                'RetweetCount' TEXT,
                FOREIGN KEY(CrimeTypeTweet) REFERENCES Crimes(Id)
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

# these three parameters are all list of lists
def populate_db(crimes_data, crimecases_data, crime_tweets_data):
    conn = sqlite.connect('crimes.db')
    cur = conn.cursor()

    ## populate crimes table
    for item in crimes_data:
        insertion = (None, item)
        statement = 'INSERT INTO "Crimes" '
        statement += 'VALUES (?, ?)'
        cur.execute(statement, insertion)

    ## create a mapping of crime_type to crime id in Crimes table
    ## e.g, "theft" : 1
    crime_dict = {}
    statement = '''SELECT Id, CrimeName From Crimes'''
    cur.execute(statement)
    for item in cur:
        crime_dict[item[1]] = item[0]

    print(crime_dict)

    ## populate crimecases table
    ## crimes_data = [['theft', CaseNumber, Year, Month, Day, Address]]
    for item in crimecases_data:
        insertion = (None, crime_dict[item[0]], item[1], item[2], item[3], item[4], item[5])
        statement = 'INSERT INTO "CrimeCases" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

    ## populate crimetweets table
    ## crime_tweets_data = [['theft', TweetText, Year, Month, DayNum, DayStr, RetweetCount]]
    for item in crime_tweets_data:
        insertion = (None, crime_dict[item[0]], item[1], item[2], item[3], item[4], item[5], item[6])
        statement = 'INSERT INTO "CrimeTweets" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


## main program
if __name__=="__main__":
    # print("here")
    crimes_data_param = get_data_crawl()

    # process the raw data returned back
    crimes_data = get_crimes_data(crimes_data_param)
    crimecases_data = get_crime_access_data(crimes_data_param)

    # get tweets data
    theft_data = process_twitter_data("Theft")
    assault_data = process_twitter_data("Assault")
    robbery_data = process_twitter_data("Robbery")
    arrest_data = process_twitter_data("Arrest")
    crime_tweets_data = theft_data + assault_data + robbery_data + arrest_data

    ## create the database
    create_db()

    ## populate the database
    populate_db(crimes_data, crimecases_data, crime_tweets_data)

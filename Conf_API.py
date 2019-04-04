import requests, json, datetime
from datetime import date, timedelta
from requests.auth import HTTPBasicAuth

def conf_test(year, month, day):
    host = "companyurl.atlassian.net"
    username = "user@companyurl.com"
    api_key = "padVOcwy3jty3O2BsyNHxSI5"

    ##Confluence uses unix epoch time stamps which is milliseconds seconds Jan, 1st 1970.
    ##https://currentmillis.com/ -> Useful site for conversions
    ##1 second = 1000 milliseconds
    ##1 day = 86400 seconds
    ##7 days = 604,800 seconds
    ##7 days = 604,800,000 milliseconds
    ##14 days = 1,209,600

    ##14 days = 1,209,600,000 milliseconds
    #Supply the date and retrieves the timestamp in milliseconds
    timestamp = int((datetime.datetime(year, month, day, 0, 0).timestamp()) * 1000)
    
    #get current time in unix epoch milliseconds since confluence uses miliseconds.
    current_time = int((datetime.datetime.timestamp(datetime.datetime.now())) * 1000)

    one_week = 604800000
    start_time = timestamp - one_week

    url = f"https://{host}/wiki/rest/api/audit?startDate={str(start_time)}&endDate={str(current_time)}"

    auth = HTTPBasicAuth(username, api_key)

    headers = {
       "Accept": "application/json"
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       auth=auth
    )

    data = response.json()
    return data

def time_diff(year, month, day):
    '''
    subtract the current date by 7 days.
    dt = date.today() - timedelta(7)
    >>>dt
    datetime.date(2019, 4, 3)
    >>>str(dt).split('-')
    ['2019', '04', '03']

    >>>str(date.today()).split('-')
    ['2019', '04', '04']
    >>>str(date.today() - timedelta(7)).split('-')
    ['2019', '03', '28']
    '''
    timestamp = int((datetime.datetime(year, month, day, 0, 0).timestamp() * 1000))
    date = datetime.date(year, month, day)
    last_week = date - timedelta(7)
    dt = str(last_week).split('-')
    week_prior_timestamp = int((datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 0, 0).timestamp() * 1000))
    
    print(f"7 days prior is {dt[1]} {dt[2]} {dt[0]}")
    print(f"The first timestamp is {timestamp}, and one week prior is {week_prior_timestamp}")
    print(f"The difference between the two timestamps is {timestamp - week_prior_timestamp}")
    return ''


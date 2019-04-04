import requests, json, datetime
from datetime import date, timedelta
from requests.auth import HTTPBasicAuth

def epoch_convert(timestamp):
    '''
    Converts timestamp in milliseconds to a human readable time format.

    >>>epoch_convert(1554215125000)
    2019-04-02 10:25:25
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    date_time = datetime.datetime.fromtimestamp(float(timestamp)/1000.)
    return date_time.strftime(time_format) 


def conf_test(year=0, month=0, day=0):
    '''
    Outpus the following data to a file:

    Test User:
    Test Company
    (host)/wiki/spaces/Test Company/pages/773095435
    2019-04-04 13:18:02
    Test Company1
    (host)/wiki/spaces/Test Company1/pages/930316631
    2019-04-04 13:07:44
    Test Company2
    (host)/wiki/spaces/Test Company2/pages/930316651
    2019-04-04 13:05:17
    Test Company3
    (host)/wiki/spaces/Test Company3/pages/466616422/
    2019-04-04 13:03:41
    Total Updates: 4

    '''
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
    #timestamp = int((datetime.datetime(year, month, day, 0, 0).timestamp()) * 1000)
    
    ##get current time in unix epoch milliseconds since confluence uses miliseconds.
    ##current_time = int((datetime.datetime.timestamp(datetime.datetime.now())) * 1000)
    ##
    ##one_day = 86400000
    ##one_week = 604800000
    ##start_time = timestamp - one_day

    #url = f"https://{host}/wiki/rest/api/audit?startDate={str(start_time)}&endDate={str(current_time)}"
    #url = f"https://{host}/wiki/rest/api/audit?startDate=1550984400000&endDate=1551330000000"
    url = f"https://{host}/wiki/rest/dashboardmacros/1.0/updates.json?maxResults=100&tab=all&showProfilePic=true&labels=&spaces=&users=&types=&category=&spaceKey="

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

##    data['changeSets'][0]['modifier']['fullName'] = User's Full Name
##    data['changeSets'][0]['recentUpdates'][0]['spaceName'] = Company Name / Name of Space
##    data['changeSets'][0]['recentUpdates'][0]['urlPath'] = Link to the page
##    data['changeSets'][0]['recentUpdates'][0]['lastModificationDate'] = Update Time

    with open('test.txt', 'a') as f:
        for x in range(len(data['changeSets'])):
            name = data['changeSets'][x]['modifier']['fullName'] + ":"
            f.write(name)
            f.write('\n')
            total_updates = 0
            for y in range(len(data['changeSets'][x]['recentUpdates'])):
                total_updates += 1
                company = data['changeSets'][x]['recentUpdates'][y]['spaceName']
                url = host + data['changeSets'][x]['recentUpdates'][y]['urlPath']
                time = epoch_convert(data['changeSets'][x]['recentUpdates'][y]['lastModificationDate'])
                f.write(company)
                f.write('\n')
                f.write(url)
                f.write('\n')
                f.write(time)
                f.write('\n')
            f.write("Total Updates: " + str(total_updates))
            f.write('\n')
            f.write('\n')

    return ''

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



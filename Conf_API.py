##https://currentmillis.com/ -> Useful site for time conversions
##https://jsonformatter.org/json-viewer -> Useful site for parsing JSON

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


def conf_test():
    '''
  
    host = "companyurl.atlassian.net"
    username = "user@companyurl.com"
    api_key = "padVOcwy3jty3O2BsyNHxSI5"

    ##Confluence uses unix epoch time stamps which is milliseconds seconds Jan, 1st 1970.
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
    '''

##    data['changeSets'][0]['modifier']['fullName'] = User's Full Name
##    data['changeSets'][0]['recentUpdates'][0]['spaceName'] = Company Name / Name of Space
##    data['changeSets'][0]['recentUpdates'][0]['urlPath'] = Link to the page
##    data['changeSets'][0]['recentUpdates'][0]['lastModificationDate'] = Update Time


    #read json data from file (used as a test instead of calling the api)
    host = "companyurl.atlassian.net"
    with open('dict.json') as f:
        data = json.load(f)
        
    #write json data to a file
    myjson = json.dumps(data)
    with open('dict.json', 'w') as f:
        f.write(myjson)

    #get a list of all the modification dates:
    mod_dates = []
    for x in range(len(data['changeSets'])):
        for y in range(len(data['changeSets'][x]['recentUpdates'])):
            mod_dates.append(data['changeSets'][x]['recentUpdates'][y]['lastModificationDate'])

    mod_dates_prev = []	   
    with open('mod_dates.txt') as f:
        reader = f.read().splitlines()
        for row in reader:
            mod_dates_prev.append(row)

    missing_mod_dates = []
    for x in mod_dates:
        if str(x) not in mod_dates_prev:
            missing_mod_dates.append(x)
    #print(missing_mod_dates)    
    
    my_dict = {}
    with open('test.txt', 'a') as f:
        companies = []
        urls = []
        times = []
        names = []
        for x in range(len(data['changeSets'])):
            for y in range(len(data['changeSets'][x]['recentUpdates'])):
                if data['changeSets'][x]['recentUpdates'][y]['lastModificationDate'] in missing_mod_dates:
                    names.append(data['changeSets'][x]['modifier']['fullName'])
                    companies.append(data['changeSets'][x]['recentUpdates'][y]['spaceName'])                   
                    urls.append(host + data['changeSets'][x]['recentUpdates'][y]['urlPath'])                   
                    times.append(epoch_convert(data['changeSets'][x]['recentUpdates'][y]['lastModificationDate']))



    with open('mod_dates.txt', 'w') as f:
        for x in mod_dates:
            f.write(str(x))
            f.write('\n')

    return ''

conf_test()

##Create the following dictionary:"
##    {
##      user 1
##		{
##		name = user 1
##		companies = [],
##		urls = [],
##		times = [],
##		}
##	user 2
##		{
##		name = user 2
##		companies = [],
##		urls = [],
##		times = []
##		}
##      user 3 etc..
##    }
##
##        
##        my_dict = {i:0 for i in list(set(names))}
##        print(my_dict)
##        for the_name in names:
##                my_dict[the_name] = my_dict[the_name] + 1
##        print(my_dict)
##
##        data_dict = {}
##        for x in my_dict:
##            data_dict[x] = {}
##            data_dict[x]['name'] = x
##            data_dict[x]['companies'] = []
##            data_dict[x]['urls'] = []
##            data_dict[x]['times'] = []
##            for y in range(len(names)):
##                if names[y] == data_dict[x]['name']:
##                    data_dict[x]['companies'].append(companies[y])
##                    data_dict[x]['urls'].append(urls[y])
##                    data_dict[x]['times'].append(times[y])
##
##    data_dict_json = json.dumps(data_dict)
##    with open('data_dict.json', 'w') as f:
##        f.write(data_dict_json)                
                    #my_dict[name].append(company)
                    #my_dict[name].append(url)


##def time_diff(year, month, day):
##    '''
##    subtract the current date by 7 days.
##    dt = date.today() - timedelta(7)
##    >>>dt
##    datetime.date(2019, 4, 3)
##    >>>str(dt).split('-')
##    ['2019', '04', '03']
##
##    >>>str(date.today()).split('-')
##    ['2019', '04', '04']
##    >>>str(date.today() - timedelta(7)).split('-')
##    ['2019', '03', '28']
##    '''
##    timestamp = int((datetime.datetime(year, month, day, 0, 0).timestamp() * 1000))
##    date = datetime.date(year, month, day)
##    last_week = date - timedelta(7)
##    dt = str(last_week).split('-')
##    week_prior_timestamp = int((datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 0, 0).timestamp() * 1000))
##    
##    print(f"7 days prior is {dt[1]} {dt[2]} {dt[0]}")
##    print(f"The first timestamp is {timestamp}, and one week prior is {week_prior_timestamp}")
##    print(f"The difference between the two timestamps is {timestamp - week_prior_timestamp}")
##    return ''




##https://currentmillis.com/ -> Useful site for time conversions
##https://jsonformatter.org/json-viewer -> Useful site for parsing JSON

import requests, json, datetime, csv, sqlite3
from datetime import date, timedelta
from requests.auth import HTTPBasicAuth

def epoch_convert(timestamp):
    '''
    Converts timestamp in milliseconds to a human readable time format.

    >>>epoch_convert(1554215125000)
    2019-04-02 10:25:25
    '''
    time_format = "%Y-%m-%d %H:%M:%S"
    date_time = datetime.datetime.fromtimestamp(float(timestamp)/1000)
    return date_time.strftime(time_format) 


def get_conf_update():
    '''
    Calls the Confluence API to retrieve data from {host}/wiki/discover/all-updates
    Returns data in a dictionary. Also returns the host we defined.

    Optional:
    Instead of calling the API each time the data needs to be tested,
    You can save the data to a file.
    
    #write json data to a file
    my_data = json.dumps(data)
    with open('dict1.json','w') as f:
        f.write(my_data)

    #read json data from file
    with open('dict.json') as f:
        data = json.load(f)    
    '''
  
    host = "https://companyurl.atlassian.net"
    username = "user@companyurl.com"
    api_key = "padVOcwy3jty3O2BsyNHxSI5"
    
    url = f"{host}/wiki/rest/dashboardmacros/1.0/updates.json?maxResults=100&tab=all&showProfilePic=true&labels=&spaces=&users=&types=&category=&spaceKey="

    auth = HTTPBasicAuth(username, api_key)

    headers = {"Accept": "application/json"}
    response = requests.request("GET",url,headers=headers,auth=auth)

    data = response.json()
    return host, data

def check_previous_entries():
    '''
    Tries to open up confluence_updates.csv if possible to read contents.
    If it doesn't exist, it gets created with a header row.
    Appends the most recent 100 timestamps to a list.
    This is used to compare against the new entries received from an API.
    This is important because we get the most recent 100 updates, but there may only have
    been 5 new entries since the last time we called and we don't want to write all 100
    to a file resulting in a lot of duplicate entries.
    Consdier this program might be run as often as every two hours.
    '''
    try:
        with open('confluence_updates.csv') as f:
            csv_reader = csv.reader(f)
    except FileNotFoundError:
        with open('confluence_updates.csv', 'a', newline = '') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['NAME','EMAIL','TIME','EPOCH_TIME','COMPANY','TITLE','URL'])

    with open('confluence_updates.csv') as f:
        csv_reader = csv.reader(f)
        mod_dates_prev = []
        #Read the CSV file in reverse so that we're checking against new entries.:
        for row in reversed(list(csv.reader(f))):
            if row[0] == 'NAME':
                continue
            mod_dates_prev.append(str(row[3]))
            if len(mod_dates_prev) == 100:
                break
    return mod_dates_prev

def confluence_to_csv():
    '''
    Parses through the JSON and extracts all the useful fields.
    These fields are then appended to confluence_updates.csv provided
    that they aren't already in that file.

    Examples of data returned:
    data['changeSets'][0]['modifier']['fullName'] = User's Full Name
    data['changeSets'][x]['modifier']['email'] = Email Address
    data['changeSets'][0]['recentUpdates'][0]['spaceName'] = Company Name / Name of Space
    data['changeSets'][x]['recentUpdates'][y]['title'] = Title of Page
    data['changeSets'][0]['recentUpdates'][0]['urlPath'] = Link to the page
    data['changeSets'][0]['recentUpdates'][0]['lastModificationDate'] = Modified Time in Epoch Format
    epoch_convert(data['changeSets'][x]['recentUpdates'][y]['lastModificationDate'] = Takes the Epoch Time and converts to human readable
    '''
    #First check the most recent 100 entries to compare against
    mod_dates_prev = check_previous_entries()
    
    #Call the API and get back most recent 100 entries in a dictionary
    host, data = get_conf_update()
    
    names = []
    email_addresses = []
    companies = []
    titles = []
    urls = []
    times = []
    mod_dates = []    
    
    for x in range(len(data['changeSets'])):
        for y in range(len(data['changeSets'][x]['recentUpdates'])):
            if str(data['changeSets'][x]['recentUpdates'][y]['lastModificationDate']) not in mod_dates_prev:
                names.append(data['changeSets'][x]['modifier']['fullName'])
                email_addresses.append(data['changeSets'][x]['modifier']['email'])
                companies.append(data['changeSets'][x]['recentUpdates'][y]['spaceName'])
                titles.append(data['changeSets'][x]['recentUpdates'][y]['title'])
                urls.append(host + data['changeSets'][x]['recentUpdates'][y]['urlPath'])                   
                times.append(epoch_convert(data['changeSets'][x]['recentUpdates'][y]['lastModificationDate']))
                mod_dates.append(data['changeSets'][x]['recentUpdates'][y]['lastModificationDate'])
    
    #The API returns the lists with the most recent update first. However,
    #we want to append the most recent update to the end of the csv file.
    #We therefore have to reverse all the lists we acquired from the API.
    names.reverse()
    email_addresses.reverse()
    companies.reverse()
    titles.reverse()
    urls.reverse()
    times.reverse()
    mod_dates.reverse()

    #Write all new updates to a csv file
    with open('confluence_updates.csv', 'a', newline = '') as f:
        csv_writer = csv.writer(f)
        for x in range(len(companies)):
            csv_writer.writerow([names[x], email_addresses[x], times[x], mod_dates[x], companies[x], titles[x], urls[x],])

    #Connect to database, if it doesn't exist it will be created
    conn = sqlite3.connect('Confluence_Updates.db')
    c = conn.cursor()
    #If the database has no table, this will create it (This should only really execute once)
    c.execute("CREATE TABLE IF NOT EXISTS conf_table(name TEXT,email TEXT,time TEXT,epochtime REAL,company TEXT,title TEXT,url TEXT)")
    #Write all new updates to the database
    for x in range(len(companies)):
        c.execute("INSERT INTO conf_table (name,email,time,epochtime,company,title,url) VALUES (?,?,?,?,?,?,?)",
                  (names[x], email_addresses[x], times[x], mod_dates[x], companies[x], titles[x], urls[x]))
        conn.commit()
    #Close the connections
    c.close()
    conn.close()

    return ''
    

confluence_to_csv()

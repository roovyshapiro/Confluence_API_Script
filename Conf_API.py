def conf_test():
    import requests, json, datetime
    from requests.auth import HTTPBasicAuth

    host = ""
    username = ""
    api_key = ""

    ##Confluence uses unix epoch time stamps which is milliseconds seconds Jan, 1st 1970.
    ##1 second = 1000 milliseconds
    ##1 day = 86400 seconds
    ##7 days = 602,000 seconds
    ##7 days = 602,000,000 milliseconds
    ##14 days = 1,209,600
    ##14 days = 1,209,600,000 milliseconds

    current_time = int((datetime.datetime.timestamp(datetime.datetime.now())) * 1000)
    two_weeks = 1209600000
    start_time = current_time - two_weeks
    end_time = current_time

    url = f"https://{host}/wiki/rest/api/audit?startDate={str(start_time)}&endDate={str(end_time)}"

    auth = HTTPBasicAuth(username, api_key)

    #get current time in unix epoch milliseconds since confluence uses miliseconds.

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

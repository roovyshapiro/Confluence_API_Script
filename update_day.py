##Trying to organize Dates.
##Prints a dictionary with this format:
##{5: [datetime.datetime(2019, 4, 5, 12, 28, 19),
##     datetime.datetime(2019, 4, 5, 12, 29, 46),
##     datetime.datetime(2019, 4, 5, 16, 48, 37)],
## 6: [datetime.datetime(2019, 4, 6, 18, 40, 14),
##     datetime.datetime(2019, 4, 6, 18, 40, 42)],
## 7: [datetime.datetime(2019, 4, 7, 12, 36, 59)],
## 8: [datetime.datetime(2019, 4, 8, 9, 25, 20),
##     datetime.datetime(2019, 4, 8, 10, 7, 26),
##     datetime.datetime(2019, 4, 8, 12, 40, 43),

import csv, pprint, datetime

timeslist = []
with open('confluence_updates.csv') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)
    full_list = list(csv_reader)

for x in range(len(full_list)):
    up_date = datetime.datetime.strptime(full_list[x][2],'%Y-%m-%d %H:%M:%S')
    timeslist.append(up_date)

day_list = []
for x in timeslist:
    day_list.append(x.day)

day_dict = {i:[] for i in set(day_list)}
for day in day_dict.keys():
    for datetime_object in timeslist:
        if day == datetime_object.day:
            day_dict[day].append(datetime_object)

pprint.pprint(day_dict)

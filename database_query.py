##Small Script to ouput all the contributors in a specified time frame
##ordered by most amount of edits
##
##EXAMPLE:
##2019-04-01 to 2019-05-1
##The total amount of updates is 592.
##
##Doug Jones - 232
##Roovy Shapiro - 125
##Karl Birdly - 100
##James Franklin - 89
##George Coiler - 44
##Sam Glassberg - 2
import sqlite3, pprint

start_time = '2019-04-01'
end_time = '2019-05-1'
sqlite_db = 'Confluence_Updates_BAK.db'

conn = sqlite3.connect(sqlite_db)
cur = conn.cursor()

cur.execute("SELECT * from conf_table WHERE time > ?  AND time < ? ", (start_time, end_time))
mytest = cur.fetchall()
conn.close()

namelist = []
for row in mytest:
    namelist.append(row[0])

namelist_dict = {i : 0 for i in namelist}

for name in namelist:
    namelist_dict[name] += 1

print(f"{start_time} to {end_time}")
print(f"The total amount of updates is {len(mytest)}.\n")

for key, value in sorted(namelist_dict.items(), key=lambda x:x[1], reverse = True):
    print(f"{key} - {value}")



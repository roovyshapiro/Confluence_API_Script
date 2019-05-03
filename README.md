# Confluence_API_Script

This script uses Atlassian's Cloud Confluence API to retrieve and store data from every page creation or update.
This is the data that can be found at: https://companyurl.atlassian.net/wiki/discover/all-updates

This data is then outputted into a csv file and a SQLite database.       
This script is intended be run on an hourly schedule to continuously update the csv and database file.

Data analysis can be performed on these files to show who's contributing the most to Confluence.

In order for this to work properly, you'll need a Cloud Confluence site hostname, username and API Key.
That data can then replace the sample data in these variables:

~~~~
    host = "https://companyurl.atlassian.net"
    username = "user@companyurl.com"
    api_key = "padVOcwy3jty3O2BsyNHxSI5"
~~~~

See here for more information about Atlassian's Cloud Confluence:
https://www.atlassian.com/software/confluence

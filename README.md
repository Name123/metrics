Generate performance metrics data, provide API for access.


# ----- Deployment: ------
sudo apt-get install python3 sqlite3 libsqlite3-dev 

cd metrics

pip3 install -r requirements.txt

# ----- Create and populate the database: ------

sqlite3 data/metrics.db < sql/init.sql
python3 tools/populate.py -s 1000 -db data/metrics.db

# ----- Run app: ------

python3 app.py -port=8888 -db=data/metrics.db

# ----- Run tests: ------
python3 test_api.py

# ----- Access API: ------

1.) GET /list - returns the records filtered by parameters of query string:

"date_min", "date_max" - range of dates formatted like %Y.%m.%dT%H:%M:%S
"sort" - ascending sort by given column
"channel", "campaign", "country", "os" - filter by given columns

Example:
$ curl "http://127.0.0.1:7777/list?date_min=2019.02.16T00:00:00&date_max=2019.02.16T15:00:00&sort=os&channel=channel_1&os=mac"

2.) GET /count - returns counts of records grouped by given column

Example:
$ curl "http://127.0.0.1:7777/count?group=country"

Several query parameters can be specified by typing a parameter several times.
Examples:

$ curl "http://127.0.0.1:7777/count?group=country&group=os"
$ curl "http://127.0.0.1:7777/list?channel=channel_1&channel=channel_2"

Data is returned in JSON format.

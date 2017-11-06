# log-analysis

## Requirements
- Python Environment
- Postgres db
- psycopg2


## Installation and working
- Clone the repo
```git clone https://github.com/juluahamed/log-analysis.git```
- Populate the database with the script from udacity course
- Create views by running following scripts
* ```create view error as select DISTINCT(DATE(time)) as date, count(*) as num from log where log.status != '200 OK' group by date;```

* ```create view total_request as select DISTINCT(DATE(time)) as date, count(*) as num from log group by date;```
- Run the program 
```python log_analysis.py```
- The interactive shell program takes in options from user and outputs the answer on screen


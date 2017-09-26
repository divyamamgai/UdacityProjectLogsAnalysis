# Udacity Project - Logs Analysis

### Usage

```
python report.py ACTION
```

Actions which can be performed are:

**1** - Compute the most popular three articles of all time

**2** - Compute the most popular article authors of all time

**3** - Compute the days with more than 1% of requests leading to error

### Setup

Before using the module execute the following command to create the required database views -

```
psql -d DATABASE_NAME -f views.sql
```

### Requirements

psycopg2
# Search Tool for OpenPayments Data [Live Link](https://open-payments-b12b9f711a94.herokuapp.com/search/)

## User Story
Users can query the most recent data from OpenPayments datasets for analysis and export to Excel if needed.

## Requirements
- This app utilizes a PostgreSQL database. When running locally create a new database called 'openpayments'

- Elasticsearch is used to search the database and create an index of the database for a typeahead search feature. Create an Elasticsearch server instance running on localhost:9200 for local testing. 

- There are also local environment variables that are utilized below:
    - SECRET_KEY (Django setting for securing signed data)
    - ELASTICSEARCH_HOST (URL for elasticsearch server instance)
    - ELASTICSEARCH_USERNAME (For HTTP Auth)
    - ELASTICSEARCH_PASSWORD (For HTTP Auth)

## Setup

Initially you will need to import the data into your postgres database. That can be done by running the import_payments command as follows.
```
python manage.py import_payments
```

After you will need to index the data into the elasticsearch client instance for the search typeahead.
```
python manage.py search_index --rebuild
```

The `import_payments` command is made to check the `modified` field on the metastore data from the OpenPayments API. If there is a more current date available, then data will be updated based on the `change_type` field of each record. 

On a deployed app, such as one hosted on Heroku. The `import_payments` command can be set to run daily and check for any updates.

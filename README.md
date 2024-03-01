# Search Tool for OpenPayments Data

## User Story
Users can query the most recent data from OpenPayments datasets for analysis and export to Excel if needed.


## Requirements
- This app utilizes a PostgreSQL database. When running locally create a new database called 'openpayments'

- Elasticsearch is used to search the database and create an index of the database for a typeahead search feature. Create an Elasticsearch server instance running on localhost:9200 for local testing. 

- There are also local environment variables that are utilized below:
    - SECRET_KEY (Django setting for securing signed data)
    - ELASTICSEARCH_HOST (URL for elasticsearch server instance)

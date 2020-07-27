**A**
store_data.py

The code in this page is to clean the excel data and store the data into a database (mysql)

- Clean Data by removing Column B of excel data as it consist of a image which will affect the data when processing
- remove empty column and row
- Convert the n.a. data into the mean value in the row 

create_metadata.py

The code in this page is to retrieve data from the database and extract key metadata. Display the metadata by creating a web dashboard using Dash

Instruction to run the code
1) pip install dash
2) pip install dash_bootstrap_components
3) pip install dash_core_components
4) pip install dash_html_components
5) pip install pandas
6) pip install pandas
7) pip install mysql.connector

Run the file it will generate a Localhost URL: http://127.0.0.1:8050/

The metadata dashboard will display. This is a Proof of Concept (POC) thus i did not include all the dashboard data


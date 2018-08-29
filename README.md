# Introduction 
This repo contains a python script that can run queries on the Twinfield webservice and export the data as a CSV file.

# Getting Started
- To use, first enter your Twinfield credentials in 'authentication.py' file by entering the credential strings between the quotes.
- Next, specify a Query within the string variable in 'query.py'. This needs to be the XML coded query. An example query is contained in 'query.py'. For instructions on how to build other queries please check https://c3.twinfield.com/webservices/documentation/#/
- Now you can run 'twinfield.py'. The output will be written to twinfield.xml (raw xml output) and twinfield.csv (parsed xml to csv)
- The script has some minimal logging output in 'twinfield.log', you can tweak it by editing the logger in 'twinfield.py'
- The repo contains example output files exported from the twinfield demo environment.

#!/bin/bash

# get the website with database images
URL=$(curl -sS 'http://ergast.com/mrd/db/')

# find the last update date with regex
CURRENT_DATE=$(echo "$URL" | grep -o -P '(?<=last updated on: ).*?(?=</p>)')

# condition creating a txt just for the initial load
if [ ! -f ./date.txt ]; then
    echo 'initial load'> ./date.txt
fi 

# read last saved date
LAST_DATE=$(cat ./date.txt)

# create a directory for database (and docker volume) if not exists
mkdir -p db

# if scrapped date is different than the last date in the file, download and uzip the database, update the date in the file, send a message to the webhook, log it
# else log no change
if [ "$CURRENT_DATE" != "$LAST_DATE" ]; then
    curl -sS 'http://ergast.com/downloads/f1db_csv.zip' --output f1db_csv.zip && unzip -qq -o f1db_csv.zip -d ./csvs && 
    rm f1db_csv.zip && # download the archive, decompress it and remove zip
    # insert every csv file into sqlite db
    for f in ./csvs/*.csv;
    do
        sqlite3 ./db/f1db.db ".mode csv" ".import $f $(basename $f .csv)" ".exit"
    done &&
    rm -r ./csvs # remove directory with csvs
    echo "$CURRENT_DATE" > ./date.txt && # replace the date stored in the text file
    curl -sS -X POST -H "Content-Type: application/json" -d '{"message": "ready to serve"}' http://f1analytics-webhook:5010/webhook && # send a post request to the web hook
    echo "$(date "+%m-%d-%Y %T") : Data updated" # log the update message
else
    echo "$(date "+%m-%d-%Y %T") : No change" # log the no change message
fi



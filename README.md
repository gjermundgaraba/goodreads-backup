# Goodreads Backup
Python script to back up your Goodreads shelves.

Uses the Goodreads API's to fetch data.

The reasoning for writing this script was that Goodreads seems to have some pretty buggy apps, and I don't completly trust them with keeping all my data safe. My to-read list is especially important for me to not lose.

The script fetches all your books from all shelves and saves them to seperate CSV files.

The script is written with Python 3.

### Usage

Before running the script, update the config.ini file with your GoodReads API key and the user you want to backup.

Run the script to create your backup:

```
$ python application.py
```

You might have to use python3 instead of python, depending on your system.

#### User ID

You can also send in the user id as the first argument to the script.

#### Location

As the second argument you can specify a location for your backup. 

Right now the script is requiring you to have the user id as the first argument if you want to specify the location
## Condo Booking

Python CRON script to run everyday at 12am.

### Website

https://grandeur8.net

## Instructions

1. Run pip install -r requirements.txt
2. Create venv folder
3. $ source venv/bin/activate
4. cd src
5. python main.py

```console
$ sh condo_booking.sh
```

### CRON

Add to crontab.

```
1 0 * * * /path/to/directory/condo_booking.sh
```

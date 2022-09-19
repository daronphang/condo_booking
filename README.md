## Condo Booking

Python CRON script to run everyday at 12am.

### Website

https://grandeur8.net

## How Booking Works

1. Ensure CRON job is set to run at 23:59:00.
2. Code triggers two functions concurrently with async/await.
3. first function is to secure login session, so that it does not attempt to login before booking (synchronous) which reduces chances of securing a booking.
4. Second function will wait for 58s i.e. 2s before 00:00:00, and send 15 POST requests to the server at 0.2s interval (similar to DDoS). This function assumes session cookies have been secured.

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

Add to crontab. For logging, need provide absolute path, unable to use os or pathlib modules.

```
1 0 * * * /path/to/directory/condo_booking.sh
```

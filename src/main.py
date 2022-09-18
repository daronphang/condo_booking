import logging
import os
from book_court import BookCourt

# for CRON jobs, to write to /tmp folder

log_path = '/tmp/book_condo.log'

def setup_logger():
    # configure logging
    formatter = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    logging.basicConfig(format=formatter, filename=log_path, level=logging.INFO)
    logging.info('initializing CRON...')


if __name__ == '__main__':
    setup_logger()
    BookCourt().execute()
    logging.info('completed...')
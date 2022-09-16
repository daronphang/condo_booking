import logging
from book_court import BookCourt

def setup_logger():
    # configure logging
    formatter = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    logging.basicConfig(format=formatter, filename='book_condo.log', level=logging.INFO)
    logging.info('initializing CRON...')


if __name__ == '__main__':
    setup_logger()
    BookCourt().execute()
    logging.info('completed...')

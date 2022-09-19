import logging
import os
import asyncio
from pathlib import Path
from book_court import BookCourt



path = Path(os.getcwd())
log_path = f'{path.parent.absolute()}/condo_booking/book_condo.log'

# for CRON jobs, need specify the absolute path directly, path returned is /home/$USER
log_path = '/home/daronphang/Documents/coding_projects/condo_booking/book_condo.log'

def setup_logger():
    # configure logging
    formatter = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    logging.basicConfig(format=formatter, filename=log_path, level=logging.INFO)
    logging.info('initializing CRON...')


if __name__ == '__main__':
    setup_logger()
    asyncio.run(BookCourt().execute())
    logging.info('completed...')
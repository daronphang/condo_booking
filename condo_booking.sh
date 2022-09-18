# shell script to run in CRON
#! /bin/sh

absolutePath="/home/daronphang/Documents/coding_projects/condo_booking/"

. "$absolutePath"venv/bin/activate
python "$absolutePath"/src/main.py
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Checking last modification on both .db files and overwriting the old one with the most recent

import os.path
import datetime
import shutil



def main():
    trigger_time = datetime.datetime.now()
    formatted_date = "{} - {} - {} at {}h{}".format(trigger_time.day, trigger_time.month, trigger_time.year, trigger_time.hour, trigger_time.minute)
    web_db = "/usr/lib/cgi-bin/books.db"
    local_db = "/home/damien/dev/natte_biblio/books.db"
    web = os.path.getmtime(web_db)
    local = os.path.getmtime(local_db)
    web_mod = datetime.datetime.fromtimestamp(web)
    local_mod = datetime.datetime.fromtimestamp(local)
    time_difference = web_mod - local_mod
    time_diff_s = time_difference / datetime.timedelta(minutes=1)

    if time_diff_s > 0:
        # copy web_db
        print(" {} - COPYING {} TO {}".format(formatted_date, web_db, local_db) )
        shutil.copy2(web_db, local_db)
    elif time_diff_s < 0:
        # copy local_db
        print(" {} - COPYING {} TO {}".format(formatted_date, local_db, web_db) )
        shutil.copy2(local_db, web_db)
    else:
        print("{} DB ALREADY UP-TO-DATE".format(formatted_date) )
    return 0

if __name__ == '__main__':
    main()


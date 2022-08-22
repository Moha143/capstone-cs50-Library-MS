from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from .functions import bookborrow


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(bookborrow, 'interval', seconds=5)
    scheduler.start()

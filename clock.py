import os
from apscheduler.schedulers.blocking import BlockingScheduler
from requests import get

from functions import checker


sched = BlockingScheduler()

# 因為經費有限，只能在每天的上午7點到晚上6點半運作
@sched.scheduled_job('cron', hour='7-17', minute='*/5')
def scheduled_job():
  get(os.environ["url"])

  checker()

sched.start()

from apscheduler.schedulers.blocking import BlockingScheduler

from main import do_job

sched = BlockingScheduler()

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=8)
@sched.scheduled_job('interval', seconds=5)
def scheduled_job():
    print('This job is run every weekday at 8am.')
    do_job()

sched.start()

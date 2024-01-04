from fastapi import APIRouter, BackgroundTasks
from db.statistics import schedule_summary_messages_task
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

scheduler.add_job(schedule_summary_messages_task, 'interval', seconds = 4)





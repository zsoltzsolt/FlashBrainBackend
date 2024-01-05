from fastapi import APIRouter, BackgroundTasks
from db.statistics import schedule_summary_messages_task
from apscheduler.schedulers.background import BackgroundScheduler
import os

scheduler = BackgroundScheduler()

scheduler.add_job(schedule_summary_messages_task, 'interval', days = int(os.environ.get("EMAIL_SEND_INTERVAL")))





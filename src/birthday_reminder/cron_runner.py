"""A file for manipulating Cron"""

import logging
import os
from crontab import CronTab

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

cron = CronTab(user=os.environ.get('USER', os.environ.get('USERNAME')))


def get_cron_job():
    """Get the Cron job"""

    job = cron.new(command="birthday_reminder data/MOCK_DATA.csv -c")
    job.day.every(1)
    return job


def job_exists():
    """Check if Cron job exists"""

    job = cron.find_command("birthday_reminder")

    if not list(job):
        logger.warning("The Cron job is not registered, run the 'birthday_reminder register' command.")
        return False
    return True


def create_cron_job():
    """Register new Cron job"""

    if not job_exists():
        job = get_cron_job()
        logger.info("Registering a cron job")
        try:
            cron.write()
            job.is_valid()
        except IOError as e:
            logger.error("Encountered error: ", e)
        else:
            logger.info("The job was registered successfully.")
    else:
        logger.info("Job already exists")


def remove_job():
    """Remove existing Cron jobs"""

    if job_exists():
        for i in cron.find_command("birthday_reminder"):
            cron.remove(i)
            cron.write()
            logger.info("Job was removed")
    else:
        logger.info("Job does not exist")

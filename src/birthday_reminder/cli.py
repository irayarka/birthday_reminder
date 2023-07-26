"""Main script"""

import argparse
import logging

from birthday_reminder.cron_runner import create_cron_job, remove_job
from birthday_reminder.utils import birthday_checker, send_multiple_reminders
from birthday_reminder.validator import Validator

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_arguments():
    """Define the arguments"""

    parser = argparse.ArgumentParser(description="Birthday reminder")
    parser.add_argument("filename", type=str, nargs="?", const=True, help="The list of birthdays.")
    parser.add_argument("--validate", "-v", nargs="?", const=True,
                        help="Validate birthdays data")
    parser.add_argument("--check", "-c", nargs="?", const=True,
                        help="Check for birthdays, send reminders.")
    parser.add_argument("--register", nargs="?", const=True, help="Add to cron.")
    parser.add_argument("--remove", nargs="?", const=True, help="Remove reminders from cron.")
    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.filename:
        validator = Validator(args.filename)
        if args.validate:
            if validator.validate():
                logger.info("The file contains no errors")

        if args.check:
            validator.load()
            birthdays = birthday_checker(validator.data)
            names = [person["birthday_person"]["name"] for person in birthdays]
            if names:
                logger.info(
                    f"{', '.join(names)} {'has' if len(birthdays) == 1 else 'have'} a birthday in 7 days!"
                )
            else:
                logger.info("No one has upcoming birthdays :(")

            send_to = [person for person in validator.data if person["name"] not in names]
            send_multiple_reminders(send_to, birthdays)

    if args.register:
        create_cron_job()

    if args.remove:
        remove_job()

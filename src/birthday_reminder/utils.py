"""A file for utilities"""

import os
from datetime import datetime

from birthday_reminder.email_service import EmailService


def birthday_checker(data):
    """
    Checks for upcoming birthdays
    returning the birthday person data and the days left
    """

    upcoming_birthdays = []
    today = datetime.now()
    curr_day_number = today - datetime(today.year, 1, 1)

    for record in data:

        birthday_day_number = record["birth_date"] - datetime(record["birth_date"].year, 1, 1)
        difference_days = birthday_day_number.days - curr_day_number.days

        if 0 <= difference_days <= 7:
            upcoming_birthdays.append({"birthday_person": record, "days_left": difference_days})

    return upcoming_birthdays


def send_multiple_reminders(send_to, birthdays):
    """Sends reminders about multiple birthdays to multiple receivers"""

    login = os.getenv("EMAIL_LOGIN")
    password = os.getenv("EMAIL_PASSWORD")

    email_service = EmailService(login, password)

    for person in send_to:
        for birthday in birthdays:
            email_service.send(person, birthday)

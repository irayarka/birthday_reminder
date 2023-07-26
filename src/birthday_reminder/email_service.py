"""A file that contains a class for an email service"""

import logging
import smtplib

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class EmailService:
    """A service for email manipulation"""

    def __init__(self, login, password):

        self._host = "sandbox.smtp.mailtrap.io"
        self._port = 2525
        self._sender = "BirthdayReminder <BirthdayReminder@fake.com>"

        self._server = smtplib.SMTP(self._host, self._port)

        self.__login = login
        self.__password = password

        self._body_template = """
        Hi {name},
        This is a reminder that {name_of_birthday_person} will be celebrating their
        birthday on {date}.
        There are {amount_of_days} days left to get a present!
        """
        self._message_template = """\
        Subject: Birthday Reminder: {name_of_birthday_person}'s birthday on {date}
        To: {receiver} <{receiver_email}>
        From: {sender}
        {body}"""

        self.__perform_login()

    def __perform_login(self):
        """Perform login to the email server"""

        self._server.login(self.__login, self.__password)

    def _compose_body(self, receiver_data, birthday_person_data):
        """Compose the body of an email"""

        body = self._body_template.format(
            name=receiver_data["name"],
            name_of_birthday_person=birthday_person_data["birthday_person"]["name"],
            date="{day}.{month}".format(
                day=birthday_person_data["birthday_person"]["birth_date"].day,
                month=birthday_person_data["birthday_person"]["birth_date"].month,
            ),
            amount_of_days=birthday_person_data["days_left"],
        )

        return body

    def _compose_message(self, receiver_data, birthday_person_data, body):
        """Compose the whole message"""

        message = self._message_template.format(
            name_of_birthday_person=birthday_person_data["birthday_person"]["name"],
            date="{day}.{month}".format(
                day=birthday_person_data["birthday_person"]["birth_date"].day,
                month=birthday_person_data["birthday_person"]["birth_date"].month,
            ),
            receiver=receiver_data["name"],
            receiver_email=receiver_data["email"],
            sender=self._sender,
            body=body,
        )

        return message

    def send(self, receiver_data, birthday_person_data, retries=3):
        """Send an email"""

        receiver = f"{receiver_data['name']} <{receiver_data['email']}>"

        body = self._compose_body(receiver_data, birthday_person_data)
        message = self._compose_message(receiver_data, birthday_person_data, body)
        failure = None

        for retry in range(retries):

            try:
                failure = self._server.sendmail(self._sender, receiver, message)
                logger.info(f"Email sending success: {not failure}")
            except (
                    smtplib.SMTPHeloError,
                    smtplib.SMTPRecipientsRefused,
                    smtplib.SMTPSenderRefused,
                    smtplib.SMTPDataError,
                    smtplib.SMTPNotSupportedError
            ):
                logger.warning("SMTP error, retrying")
            break

        if failure:
            logger.error(
                f"Couldn't send email to {failure[receiver_data['email']]}\n"
                f"Reason: {failure[receiver_data['email']][1]}"
            )

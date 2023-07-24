"""A file that contains a birthdays file validator"""

import logging
from datetime import datetime

from birthday_reminder.loader import Loader

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Validator(Loader):
    """Validates the birthday data"""

    def __init__(self, filename):
        super().__init__(filename)

    def _validate_parsing(self):
        """Validates the file is parsed without errors"""

        try:
            self.load()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def _validate_missing(self):
        """Validates there are no missing fields in the file"""

        valid = True
        for record in self._data:
            if not all(record.values()):
                logger.error(f"A record {str(record)} contains missing fields")
                valid = False
        return valid

    def _validate_birthdate(self):
        """Validates all birth dates are in the past"""

        valid = True
        for record in self._data:
            if record["birth_date"] > datetime.now():
                logger.error(f"Date {record['birth_date']} is not in the past")
                valid = False
        return valid

    def validate(self):
        """Validates if all three validation conditions match"""

        return self._validate_parsing() and self._validate_missing() and self._validate_birthdate()

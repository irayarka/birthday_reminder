"""A file that contains the class that loads the data from file to dictionary"""

import json
import logging
from csv import DictReader
from datetime import datetime

import yaml

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Loader:
    """Loads the data from file to dictionary"""

    def __init__(self, filename):
        self.filename = filename

        self.m_d_format = "%m-%d"
        self.y_m_d_format = "%Y-%m-%d"

        self._data = []

    def load(self):
        """A method to load the data from 3 different filetypes"""

        file_format = self.filename.split(".")[-1]
        parsers = {
            "csv": DictReader,
            "json": json.load,
            "yaml": yaml.safe_load,
        }

        with open(self.filename) as f:
            self._data = list(parsers[file_format](f))

        self._load_date()

    def _load_date(self):
        """A method to load the date as datetime object instead string"""

        for record in self._data:
            date_object = datetime.now()
            try:
                date_object = datetime.strptime(record["birth_date"], self.y_m_d_format)
            except ValueError:
                try:
                    date_object = datetime.strptime(record["birth_date"], self.m_d_format)
                except ValueError:
                    logger.error(f"Could not parse date of birth: {record['birth_date']}")
            finally:
                record.update({"birth_date": date_object})

    @property
    def data(self):
        """Data getter"""

        return self._data

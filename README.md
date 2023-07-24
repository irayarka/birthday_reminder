Birthday reminder
=======================

Installation
-----

```bash
# Navigate to working directory
cd birthday_reminder

#Install the CLI
pip3 install .
```

Main commands
-----

```bash
# Validate file errors
birthday_reminder data/MOCK_DATA.csv -v

# Check for upcoming birthdays
birthday_reminder data/MOCK_DATA.json -c
```

Crontab
-----
```bash
# Add a daily job
birthday_reminder --register

# Remove the jobs
birthday_reminder --remove
```
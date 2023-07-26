from setuptools import find_packages, setup

with open("README.md", encoding="UTF-8") as f:
    readme = f.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name="birthday_reminder",
    version="1.0.0",
    description="Command line birthday reminder utility",
    long_descripFtion=readme,
    author="Iryna Yarka",
    author_email="iryna.yarka@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[requirements],
    entry_points={
        "console_scripts": "birthday_reminder=birthday_reminder.cli:main"
    },
)

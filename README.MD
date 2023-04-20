# Automate the TimeSheeet   
[![automate_time_sheet](https://github.com/Beatrix-droid/selenium-python/actions/workflows/timesheet.yml/badge.svg)](https://github.com/Beatrix-droid/selenium-python/actions/workflows/timesheet.yml)

This is a python robot built on selenium that fills in my time sheet each week. The robot does not take into accoutn sick days and Bank holidays and will not request annual leave for you. Annual leave, bank holidays and sick leave need to be managed manually.

The project is contains 3 files:

* a _main.py_ script that utilises selenium to open a browser, log into the portal and fill in the timesheet, complete with logs that inform the user how the execution of the job proceeds, and screenshots pointing to the source of error in case the job fails. 

* a _timesheet.yaml_ github action that runs every day at 10:00 UTC time and triggers the main.py file to run, committing any new files and logs to the repo. main.py's logs will be visible in the logs of this action, and any geckodriver logs and screenshots in case of job failure will also be committed to the repo.

* a _gitleaks-action.yaml_ that scans the repo every time a file is committed to it, outputting the findings in the logs. Gitleaks is a SAST tool for detecting and preventing hardcoded secrets like passwords, API keys, and tokens in git repos. It is used to ensure check that no sensitive data has been exposed by the robot or the user when files are committed to the repo.

gitleaks action:
[![gitleaks](https://github.com/Beatrix-droid/selenium-python/actions/workflows/gitleaks-action.yaml/badge.svg)](https://github.com/Beatrix-droid/selenium-python/actions/workflows/gitleaks-action.yaml)

To use this robot to automate your timesheet, the only things that you need to do is fork this repo, and create two repository level secrets. One secret will be named USERNAME and will contain the username you use to access the portal. The other will be called PASSWORD and will contain the password used to enter the portal.GitHub Secrets are encrypted and allow you to store sensitive information, such as access tokens, in your repository. They are exposed only to selected actions and are not passed to workflows that are triggered by a pull request from a fork of this repository.


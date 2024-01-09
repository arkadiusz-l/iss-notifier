# ISS Notifier
This application was created in May 2023 in order to improve my programming skills.\
It uses [Selenium](https://www.selenium.dev).

## Description
This application is used to notify interested persons about the upcoming Internatial Space Station (ISS) flyby.\
To do this, the program scrapes a website, extracts the necessary information, parses it, and then sends it via email to the interested.\
Since I did it for my Polish friends, flyby search works only for locations in Poland.\
Also the notifications are sent in Polish language.

## Installation
Clone the repo or download the [latest release](https://github.com/arkadiusz-l/iss-notifier/releases/latest).
Install the requirements by typing `pip install -r requirements.txt`.

## Usage
* Fill in the details of the sender mailbox in the `.env.dist` file. They will be used as environment variables.
* Add interested persons (called "Subscribers") in the `main.py` file.
* Set the location for which the flyby will be checked in the `main.py` file.
* This application uses the Gecko driver for Firefox browser. If you want to use a different browser driver, please visit this [Selenium website](https://www.selenium.dev/documentation/webdriver/browsers).

## Project Status
In progress...

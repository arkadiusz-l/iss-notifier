# ISS Notifier
This application was created in May 2023 in order to improve my programming skills.\
It uses [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/).

## Description
This application is used to notify interested persons about the upcoming
[Internatial Space Station (ISS)](https://en.wikipedia.org/wiki/International_Space_Station)
or other satellites flyby (for example [Starlink](https://en.wikipedia.org/wiki/Starlink) "train").

Currently, the application scrapes a webpage, extracts the necessary information, parses it, and then sends it via email to the interested.\
**Note**: Since I did it for my Polish friends, the notifications are sent in Polish language.

It should work with any satellite that has an ID in the [NORAD catalog](https://en.wikipedia.org/wiki/Satellite_Catalog_Number).\
Some sites where you can search for a NORAD ID for satellites:
- https://celestrak.org/NORAD/elements/
- https://www.satflare.com/search.asp
- https://in-the-sky.org/search.php?s=&searchtype=Spacecraft&satorder=0

### History
The application was created in response to my and my friends' needs for e-mail/SMS notifications
about the upcoming flyby of the International Space Station.

## Installation
3 options to choose from:
#### I. PyCharm or IntelliJ IDEA with the "Python Community Edition" plugin
1. Create a New Project with the virtual environment, for example **Virtualenv**.
2. Open the IDE terminal.
3. Type:
   ```
   git clone git@github.com:arkadiusz-l/iss-notifier.git
   ```
   or
   ```
   git clone https://github.com/arkadiusz-l/iss-notifier.git
   ```
4. Navigate to the program's directory by typing:
   ```
   cd iss-notifier
   ```
5. Make sure that you are inside the virtual environment - you should see `(venv)` before the path.
6. Type:
   ```
   pip install -r requirements.txt
   ```
   to install the required dependencies necessary for the program to run.

#### II. Downloading source code/release
1. Download the [latest release](https://github.com/arkadiusz-l/iss-notifier/releases/latest)
   in a .zip archive.
2. Unpack the downloaded archive in a directory of your choice.
3. Open the terminal.
4. Navigate to the directory with the unpacked program by typing:
   ```
   cd directoryname
   ```
5. Type:
   ```
   python -m venv venv
   ```
   to create virtual environment and wait for confirmation.
6. If you are on Windows, type:
   ```
   venv\Scripts\activate
   ```
   If you are on Linux or macOS, type:
   ```
   source venv/bin/activate
   ```
7. Make sure that you are inside the virtual environment - you should see `(venv)` before the path.
8. Type:
   ```
   pip install -r requirements.txt
   ```
   to install the required dependencies necessary for the program to run.

#### III. Cloning repository
1. Open the terminal.
2. Create a new directory by typing:
   ```
   mkdir directoryname
   ```
3. Navigate to that directory by typing:
   ```
   cd directoryname
   ```
4. Type:
   ```
   git clone git@github.com:arkadiusz-l/iss-notifier.git
   ```
   or
   ```
   git clone https://github.com/arkadiusz-l/iss-notifier.git
   ```

## Usage
1. Navigate to the program's directory by typing:
   ```
   cd iss-notifier
   ```
2. Type:
   ```
   python -m venv venv
   ```
   to create virtual environment and wait for confirmation.
3. If you are on Windows, type:
   ```
   venv\Scripts\activate
   ```
   If you are on Linux or macOS, type:
   ```
   source venv/bin/activate
   ```
4. Make sure that you are inside the virtual environment - you should see `(venv)` before the path.
5. Add or edit interested persons (called **Subscribers**) in the `subscribers.json` file.
6. Rename `.env.dist` file to `.env` and fill in the details of the sender mailbox. They will be used as environment variables.
7. Now you can run the program by typing:
   ```
   python main.py
   ```
8. After using the program, exit the virtual environment by typing:
   ```
   deactivate
   ```
9. The `(venv)` should disappear.

## Project Status
In progress...

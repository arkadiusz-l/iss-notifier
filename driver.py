from selenium import webdriver


class Driver:
    """Represents a driver for scrapper"""

    def __init__(self) -> None:
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--headless')
        self.webdriver = webdriver.Firefox(options=self.options)

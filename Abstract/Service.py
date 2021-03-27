import logging
from os import environ
from time import sleep
from urllib.parse import unquote

from Interfaces.MySqlInterface import MySqlInterface
from Interfaces.RabbitMqInterface import RabbitMqInterface


class Service():

    def __init__(self):
        self.data_path = environ["CONTAINER_DATA_PATH"]
        self.idle_t = int(environ["IDLE_TIME"])

    # Set up
    def get_logger(self, name) -> logging.Logger:
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def associate(self) -> None:
        """Associate service with required interfaces.""" 
        self.q = RabbitMqInterface()
        self.db = MySqlInterface()
    
    # Timing methods
    def wait(self, interval: int) -> None: 
        sleep(interval)
    
    # String Methods
    def fname(self, url: str) -> str:
        """Return the file name associated with an URL. Assumes html if no file extension."""
        fname: str = url.split("/")[-1].replace("File:", "")
        return fname if (fname.endswith("html") or fname.endswith("svg")) else f"{fname}.html"

    def fname_text(self, fname: str) -> str:
        """Return file name as normalized, unencoded text."""
        text = ".".join(fname.split(".")[:-1])
        text = unquote(text)
        text = self.standardize_dashes(text)
        for char in ["_", "-"]:
            text = text.replace(char, " ")
        return text

    def complete_url(self, href: str) -> str:
        """
        Returns URL with scheme, hostname, and no anchors.
        
        Anchor stripping is naive and assumes no dynamic URLS.
        """
        href = href.split("#")[0] if "#" in href else href  
        if href.startswith("http"):
            return href
        elif href.startswith("//"):
            return f"https:{href}"
        elif href.startswith("/"):
            return f"https://en.wikipedia.org{href}"
        else:
            self.log.warning(f"complete_url() FAILURE: {href}")

    def standardize_dashes(self, text: str) -> str:
        """Replaces all types of dashes with hyphens."""
        for dash in ["–", "‒"]:
            text = text.replace(dash, "-")
        return text

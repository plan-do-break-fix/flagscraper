from bs4 import BeautifulSoup
import os.path
from os import environ
import requests
import time
from typing import Union

from Interfaces.MySqlInterface import MySqlInterface
from Interfaces.RabbitMqInterface import RabbitMqInterface
from Abstract.Service import Service

class Agent(Service):

    def __init__(self):
        super().__init__()
        self.throttle_t = int(environ["WEB_THROTTLE_TIME"])
        self.log = self.get_logger("WebAgent")

    def cycle(self) -> None:
        url = self.q.dequeue("web")
        if url:
            resp = self.fetch(url)
            if resp: 
                if self.save_content(self.fname(url), resp.content):
                    self.db.mark_as_downloaded(url)
                    self.log.info(f"{self.fname(url)} written to disk.")
                    self.q.enqueue()
                    self.wait(self.throttle_t)
        else:
            self.log.info("Nothing in web queue.")
            self.wait(self.idle_t)

    def get_true_url(self, url: str) -> str:
        """
        Returns Wikipedia file download URL.

        Wikipedia URLs containing 'File:' link to a page about the file, not the file itself.
        """
        soup: BeautifulSoup = BeautifulSoup(requests.get(url).content, features="html.parser")
        link_href: str = [a.attrs["href"] for a in soup.find_all("a") if a.text == "Original file"][0]
        return self.complete_url(link_href)

    def fetch(self, url: str) -> Union[requests.Response, bool]:
        """Return the response from an HTTP GET request, or False on HTTP error."""
        url: str = self.complete_url(url)
        if "/File:" in url:
            url = self.get_true_url(url)
        resp: requests.Response = requests.get(url)
        if 200 <= resp.status_code < 300:
            return resp
        elif 400 <= resp.status_code < 500:
            self.log.error(f"{url} returned {resp.status_code} error.")
        elif 500 <= resp.status_code < 600:
            self.log.warning(f"{url} returned {resp.status_code} error.")
        return False

    def save_content(self, fname: str, data) -> bool:
        target_path = f"{self.data_path}/{fname.split('.')[-1]}/{fname}"
        if os.path.exists(target_path):
            self.log.warning("")
            return False
        else:
            try:
                with open(target_path, "wb") as _file:
                    _file.write(data)
            except IOError:
                return False
            self.log.info("")
            return True


if __name__ == "__main__":
    agent = Agent()
    agent.associate()
    while True:
        agent.cycle()
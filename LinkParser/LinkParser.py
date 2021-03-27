from bs4 import BeautifulSoup, Tag
import re
from typing import List

from Abstract.Service import Service


class Parser(Service):

    def __init__(self):
        super().__init__()
        self.log = self.get_logger("LinkParser")
        self.current_html = None

        self.match_terms = [
            "bandera",
            "bandiera",
            "banner",
            "ensign",
            "flag",
            "jack",
            "standard"
        ]
        self.unmatch_page_terms = [
            "(flag maker)"
        ]
        self.unmatch_svg_terms = [f"{i}s" for i in self.match_terms] + [
            "comparison",
            "construct",
            "corvata",
            "dimensions",
            "display",
            "hoist",
            "incorrect",
            "parade",
            "pennant",
            "pennon",
            "presentation",
            "proportions",
            "protocol",
            "reverse",
            "scheme",
            "specification",
            "template",
            "vertically",
            "wrong"
        ]
        self.unmatch_svg_regexes = [
            "as used(?! by)",
            "(from|of) (the )?flag"
        ]
        self.allowed_domains = [
            "commons.wikimedia.org",
            "upload.wikimedia.org",
            "en.wikipedia.org"
        ]
        self.allowed_special_page_types = [
            "Category",
            "File",
            "Portal"
        ]


    def load_html(self, url: str) -> str:
        fname = self.fname(url)
        try:
            with open(f"{self.project_root}/data/html/{fname}", "r") as html_f:
                return html_f.read()
        except FileNotFoundError as err:
            self.log.error(err)
            return ""

    def cycle(self) -> None:
        url = self.q.dequeue("parse")
        if url:
            self.current_html = self.fname(url)
            self.log.info("Parsing {self.fname(url)} for links.")
            html = self.load_html(url)
            link_urls = self.find_flag_links(self.find_links(html))
            for link_url in link_urls:
                    if link_url.endswith("svg"):
                        if not self.db.url_exists(link_url):
                            # new flag link found
                            self.db.new_flag_url(link_url)
                            self.log.info(f"{self.fname(link_url)} added to flags table.")
                            self.q.enqueue(link_url, "web")
                        else:
                            # check for new flag link encounter
                            if not self.db.encounter_exists(link_url, url):
                                self.db.new_encounter(link_url, url)
                    else:
                        if not self.db.url_exists(link_url):
                            # new flag-related page link found
                            self.db.new_page_url(link_url)
                            self.log.info(f"{self.fname(link_url)} added to pages table.")
                            self.q.enqueue(link_url, "web")

        else:
            self.current_html = None
            self.log.info("Nothing in parse queue.")
            self.wait(self.idle_t)
        

    def find_links(self, html: str) -> List[Tag]:
        """Returns bs4 Tag for each allowed link in page."""
        if html:
            soup = BeautifulSoup(html, features="html.parser")
            links = [a for a in soup.find_all("a") if "href" in a.attrs]
            links = [a for a in links if not a.attrs["href"].startswith("#")]
            links = [a for a in links if self.is_allowed_domain(
                                      self.complete_url(a.attrs["href"]))]
            return [a for a in links if self.is_allowed_page_type(a.attrs["href"])]
        else:
            return []

    def find_flag_links(self, link_tags: List[Tag]) -> List[str]:
        """Returns list of unique links to download to project storage."""
        if link_tags:
            urls = [link.attrs["href"] for link in filter(self.is_flag_link, link_tags)]
            urls += [link.attrs["href"] for link in filter(self.is_flag_page_link, link_tags)]
            urls = [link for link in set(urls)]
            return urls
        else:
            return []

    #
    def make_link_text(self, link):
        link_text = " ".join([
            self.fname_text(self.fname(self.complete_url(link.attrs["href"]))).lower(),
            self.associated_text(link, self.current_html)]).lower()
        return link_text
    #

    # Filter methods #  -  Return bool

    def is_flag_link(self, link: Tag) -> bool:
        """Returns true if URL in link is to a flag svg page, false otherwise."""
        if not link.attrs["href"].endswith("svg"):
            return False
        link_text = self.make_link_text(link)
        if any([term in link_text for term in self.unmatch_svg_terms]):
            return False
        if any([term in link_text for term in self.match_terms]):
            if not any([re.search(ex, link_text) for ex in self.unmatch_svg_regexes]):
                return True

    def is_flag_page_link(self, link: Tag) -> bool:
        """Returns true if URL in link is a page about flags, false otherwise."""
        link_text = self.make_link_text(link)
        for term in self.unmatch_page_terms:
            if term in link_text:
                return False
        for term in self.match_terms:
            if term in link_text:
                return True

    def is_allowed_domain(self, url: str) -> bool:
        """
        Returns true is the domain is whitelisted, false otherwise.
        
        Used to limit scraping scope to specific wikipedia subdomains.
        """
        hostname = url.split("/")[2]
        return any(domain in hostname for domain in self.allowed_domains)

    def is_allowed_page_type(self, url: str) -> bool:
        """Limit scopes to normal wiki pages and types in allowed_special_page_types."""
        if "?" in url:                                      # dynamic urls
            return False
        if ":" not in url[8:]:                              # normal type page
            return True
        else:
            for page_type in self.allowed_special_page_types:
                if f"/{page_type}:" in url:                 # allowed special type
                    return True
            return False                                    # other special type


    # Context methods #  -  Retrieve text associated with a given link

    def link_is_inline_thumbnail(self, link: Tag) -> bool:
        return True if link.find_parent("div", {"class": "thumbinner"}) else False

    def inline_thumbnail_text(self, link: Tag) -> str:
        caption = link.parent.find("div", {"class": "thumbcaption"}) #if thumb else ""
        return caption.text.strip() if caption else ""

    def link_is_gallerybox_thumbnail(self, link: Tag) -> bool:
        return True if link.find_parent("li", {"class": "gallerybox"}) else False

    def gallerybox_thumbnail_text(self, link: Tag) -> str:
        thumb = link.find_parent("div", {"class": "thumb"})
        gallerytext = thumb.find_next_sibling("div", {"class": "gallerytext"}) if thumb else ""
        return gallerytext.text.strip() if gallerytext else ""

    def link_is_thumbnail_in_list(self, link: Tag) -> bool:
        return True if (link.parent.name == "span"
                        and link.parent.has_attr("class")
                        and link.parent["class"][0] == "noresize"
                        and link.parent.parent.name == "td"
                        ) else False

    def thumbnail_in_list_text(self, link: Tag) -> str:
        table_row = link.find_parent("tr")
        cell_texts = [td.text.strip() for td in table_row.find_all("td")] if table_row else []
        return " ".join(cell_texts).strip() if cell_texts else ""

    def link_is_main_infobox_thumbnail(self, link: Tag) -> bool:
        return True if (link.find_parent("table", {"class": "infobox"})
                        and link.find("img")
                        and link.find("img").has_attr("width")
                        and link.find("img").attrs["width"] == "255"
                        ) else False

    def main_infobox_thumbnail_text(self, link: Tag) -> str:
        current = link.find_parent("tr")
        texts = []
        while not current.next_sibling.has_attr("style"):
            current = current.next_sibling
            texts.append(current.find("td").text.strip())
        return " ".join(texts)

    def link_is_other_infobox_thumbnail(self, link: Tag) -> bool:
        return True if (link.find_parent("table", {"class": "infobox"})
                        and link.find("img")
                        and link.find("img").has_attr("width")
                        and link.find("img").attrs["width"] == "158"
                        ) else False

    def other_infobox_thumbnail_text(self, link: Tag) -> str:
        caption = link.parent.find("div")
        return " ".join([i for i in caption.stripped_strings]) if caption else ""

    def associated_text(self, link: Tag, page_url: str) -> str:
        """Returns text that accompanies link."""
        if link.has_attr("class") and link.attrs["class"][0] == "image":
            if self.link_is_thumbnail_in_list(link):
                return self.thumbnail_in_list_text(link)
            elif self.link_is_inline_thumbnail(link):
                return self.inline_thumbnail_text(link)
            elif self.link_is_gallerybox_thumbnail(link):
                return self.gallerybox_thumbnail_text(link)
            elif self.link_is_main_infobox_thumbnail(link):
                return self.main_infobox_thumbnail_text(link)
            elif self.link_is_other_infobox_thumbnail(link):
                return self.other_infobox_thumbnail_text(link)
            else:
                return ""
        else:
            return link.text.strip()

if __name__ == "__main__":
    parser = Parser()
    parser.associate()
    while True:
        parser.cycle()

import unittest
from bs4 import Tag
from LinkParser import LinkParser
from os import environ


class LinkParserTestCase_FindLinks_FlagOfItaly(unittest.TestCase):

    def setUp(self):
        lf = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/Flag_of_Italy.html") as _f:
            self.all_links = lf.find_links(_f.read())

    def test_find_links_length(self):
        self.assertEqual(1263, len(self.all_links))

    def test_find_links_type(self):
        self.assertEqual(set([Tag]), set([type(link) for link in self.all_links]))

    def test_find_link_all_have_href(self):
        hrefs = [link.attrs["href"] for link in self.all_links if link.attrs["href"]]
        self.assertEqual(len(hrefs), len(self.all_links))

    def test_find_links_no_local_anchors(self):
        anchors = [link for link in self.all_links if link.attrs["href"].startswith("#")]
        self.assertEqual([], anchors)


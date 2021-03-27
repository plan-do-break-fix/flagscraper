import unittest
from bs4 import BeautifulSoup
from LinkParser import LinkParser
from os import environ


class LinkParserTestCase_IsFlag_FlagOfEstonia(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/Flag_of_Estonia.html") as _f:
            self.soup = BeautifulSoup(_f.read(), features="html.parser")

    def test_is_flag_link_flag_of_estonia(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_Estonia.svg"})
        self.assertTrue(self.p.is_flag_link(tag))

    def test_is_flag_link_flag_of_estonia_president(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_President_of_Estonia.svg"})
        self.assertTrue(self.p.is_flag_link(tag))

    def test_is_flag_link_vertical_flag_of_estonia(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_Estonia_(vertical).svg"})
        self.assertFalse(self.p.is_flag_link(tag))

    def test_is_flag_page_link_tartu_university(self):
        tag = self.soup.find("a", {"href": "/wiki/University_of_Tartu"})
        self.assertFalse(self.p.is_flag_link(tag))

    def test_is_flag_page_link_national_flag(self):
        tag = self.soup.find("a", {"href": "/wiki/National_flag"})
        self.assertTrue(self.p.is_flag_page_link(tag))


class LinkParserTestCase_IsFlag_FlagOfFrance(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/Flag_of_France.html") as _f:
            self.soup = BeautifulSoup(_f.read(), features="html.parser")

    def test_is_flag_link_shade_comparison(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_France_(shade_comparison).svg"})
        self.assertFalse(self.p.is_flag_link(tag))


class LinkParserTestCase_IsFlag_FlagOfItaly(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/Flag_of_Italy.html") as _f:
            self.soup = BeautifulSoup(_f.read(), features="html.parser")

    def test_is_flag_link_standard_of_italian_pres(self):
        tag = self.soup.find("a", {"href": "/wiki/Presidential_Standard_of_Italy"})
        self.assertTrue(self.p.is_flag_page_link(tag))

    def test_is_flag_link_wiki_gif(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Mexico_Italy_flag_differences.gif"})
        self.assertFalse(self.p.is_flag_link(tag))

    def test_is_flag_link_italian_cockade(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Coccarda_ITALIA.svg"})
        self.assertFalse(self.p.is_flag_link(tag))


class LinkParserTestCase_IsFlag_FlagOfPakistan(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/Flag_of_Pakistan.html") as _f:
            self.soup = BeautifulSoup(_f.read(), features="html.parser")

    def test_is_flag_page_link_flag_of_pres(self):
        tag = self.soup.find("a", {"href": "/wiki/Flag_of_the_President_of_Pakistan"})
        self.assertTrue(self.p.is_flag_page_link(tag))

    def test_is_flag_construction_diagram(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_Pakistan_Construction.svg"})
        self.assertFalse(self.p.is_flag_link(tag))


class LinkParserTestCase_IsFlag_ListOfItalianFlags(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/List_of_Italian_flags.html") as _f:
            self.soup = BeautifulSoup(_f.read(), features="html.parser")

    def test_is_flag_page_link_flag_of_italy(self):
        tag = self.soup.find("a", {"href": "/wiki/Flag_of_Italy"})
        self.assertTrue(self.p.is_flag_page_link(tag))

    def test_is_flag_link_flag_of_italy(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_Italy.svg"})
        self.assertTrue(self.p.is_flag_link(tag))

    def test_is_flag_link_italian_civil_ensign(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Civil_Ensign_of_Italy.svg"})
        self.assertTrue(self.p.is_flag_link(tag))

    def test_is_flag_link_italian_naval_jack(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Naval_Jack_of_Italy.svg"})
        self.assertTrue(self.p.is_flag_link(tag))



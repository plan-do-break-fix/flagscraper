import unittest
from LinkParser import LinkParser


class LinkParserTestCase_IsAllowedDomain(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()

    def test_is_allowed_domain_wiki_page(self):
        url = "https://en.wikipedia.org/wiki/Nordic_countries"
        self.assertTrue(self.p.is_allowed_domain(url))

    def test_is_allowed_domain_wiki_jpg(self):
        url = "https://en.wikipedia.org/wiki/File:E%C3%9CSi_ajalooline_lipp.jpg"
        self.assertTrue(self.p.is_allowed_domain(url))

    def test_is_allowed_domain_wiki_svg(self):
        url = "https://en.wikipedia.org/wiki/File:Flag_of_Estonia.svg"
        self.assertTrue(self.p.is_allowed_domain(url))

    def test_is_allowed_domain_wiki_commons(self):
        url = "https://commons.wikimedia.org/wiki/Category:National_flag_of_Estonia"
        self.assertTrue(self.p.is_allowed_domain(url))

    def test_is_allowed_domain_wiki_file_link(self):
        url = "https://upload.wikimedia.org/wikipedia/commons/8/8f/Flag_of_Estonia.svg"
        self.assertTrue(self.p.is_allowed_domain(url))

    def test_is_allowed_domain_de_wiki(self):
        url = "https://de.wikipedia.org/wiki/Flagge_Estlands"
        self.assertFalse(self.p.is_allowed_domain(url))

    def test_is_allowed_domain_wikidata(self):
        url = "https://www.wikidata.org/wiki/Special:EntityPage/Q211930"
        self.assertFalse(self.p.is_allowed_domain(url))

    def test_is_allowed_domain_estonia_site(self):
        url = "https://www.riigiteataja.ee/en/eli/525062018002/consolide"
        self.assertFalse(self.p.is_allowed_domain(url))

    def test_is_allowed_domain_archive_org(self):
        url = "https://web.archive.org/web/20100905055806/http://www.estonianfreepress.com/estonian-flag/"
        self.assertFalse(self.p.is_allowed_domain(url))


class LinkParserTestCase_IsAllowedPageType(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()

    def test_is_allowed_page_type_wiki_page(self):
        url = "https://en.wikipedia.org/wiki/Flag_of_Estonia"
        self.assertTrue(self.p.is_allowed_page_type(url))

    def test_is_allowed_page_type_wiki_file_page(self):
        url = "https://en.wikipedia.org/wiki/Flag_of_Estonia#/media/File:Flag_of_Estonia.svg"
        self.assertTrue(self.p.is_allowed_page_type(url))

    def test_is_allowed_page_type_wiki_file_link(self):
        url = "https://upload.wikimedia.org/wikipedia/commons/c/ca/Flag_of_the_Rotalia.svg"
        self.assertTrue(self.p.is_allowed_page_type(url))

    def test_is_allowed_page_type_wiki_category(self):
        url = "https://en.wikipedia.org/wiki/Category:National_flags"
        self.assertTrue(self.p.is_allowed_page_type(url))

    def test_is_allowed_page_type_wiki_portal(self):
        url = "https://en.wikipedia.org/wiki/Portal:Estonia"
        self.assertTrue(self.p.is_allowed_page_type(url))

    def test_is_allowed_page_type_help(self):
        url = "https://en.wikipedia.org/wiki/Help:Contents"
        self.assertFalse(self.p.is_allowed_page_type(url))

    def test_is_allowed_page_type_special(self):
        url = "https://en.wikipedia.org/wiki/Special:Random"
        self.assertFalse(self.p.is_allowed_page_type(url))

    def test_is_allowed_page_type_wiki_meta(self):
        url = "https://en.wikipedia.org/wiki/Wikipedia:Contact_us"
        self.assertFalse(self.p.is_allowed_page_type(url))

    def test_is_allowed_page_type_template(self):
        url = "https://en.wikipedia.org/wiki/Template:Flags_of_Europe"
        self.assertFalse(self.p.is_allowed_page_type(url))

    def test_is_allowed_page_type_template_talk(self):
        url = "https://en.wikipedia.org/wiki/Template_talk:Flags_of_Europe"
        self.assertFalse(self.p.is_allowed_page_type(url))



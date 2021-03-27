import unittest
from Abstract import Service


class AbstractServiceTestCase_Fname(unittest.TestCase):

    def setUp(self):
        self.s = Service.Service()

    def test_fname_flag_of_japan(self):
        url = "https://en.wikipedia.org/wiki/File:Flag_of_Japan.svg"
        expected = "Flag_of_Japan.svg"
        self.assertEqual(expected, self.s.fname(url))

    def test_fname_flag_of_hong_kong(self):
        url = "https://en.wikipedia.org/wiki/File:Flag_of_Hong_Kong.svg"
        expected = "Flag_of_Hong_Kong.svg"
        self.assertEqual(expected, self.s.fname(url))

    def test_fname_pioneer_battalions(self):
        url = "https://en.wikipedia.org/wiki/File:%E4%B8%AD%E5%9B%BD%E5%B0%91%E5%B9%B4%E5%85%88%E9%94%8B%E9%98%9F%E9%98%9F%E6%97%97_(%E5%A4%A7%E9%98%9F%E6%97%97).svg"
        expected = "%E4%B8%AD%E5%9B%BD%E5%B0%91%E5%B9%B4%E5%85%88%E9%94%8B%E9%98%9F%E9%98%9F%E6%97%97_(%E5%A4%A7%E9%98%9F%E6%97%97).svg"
        self.assertEqual(expected, self.s.fname(url))



class AbstractServiceTestCase_FnameText(unittest.TestCase):

    def setUp(self):
        self.s = Service.Service()

    def test_fname_text_pioneer_battalions(self):
        fname = "%E4%B8%AD%E5%9B%BD%E5%B0%91%E5%B9%B4%E5%85%88%E9%94%8B%E9%98%9F%E9%98%9F%E6%97%97_(%E5%A4%A7%E9%98%9F%E6%97%97).svg"
        expected = "中国少年先锋队队旗 (大队旗)"
        self.assertEqual(expected, self.s.fname_text(fname))

class AbstractServiceTestCase_CompleteUrl(unittest.TestCase):

    def setUp(self):
        self.s = Service.Service()

    def test_complete_url_wiki_flag_of_italy(self):
        href = "/wiki/File:Flag_of_Italy.svg"
        url = "https://en.wikipedia.org/wiki/File:Flag_of_Italy.svg"
        self.assertEqual(url, self.s.complete_url(href))

    def test_complete_url_already_complete(self):
        href = "https://en.wikipedia.org/wiki/Flag_of_the_Estonian_Soviet_Socialist_Republic"
        url = "https://en.wikipedia.org/wiki/Flag_of_the_Estonian_Soviet_Socialist_Republic"
        self.assertEqual(url, self.s.complete_url(href))



class AbstractServiceTestCase_StandardizeDashes(unittest.TestCase):

    def setUp(self):
        self.s = Service.Service()

    def test_standardize_dashes_en(self):
        text = "Marxism–Leninism is a communist ideology"
        expected = "Marxism-Leninism is a communist ideology"
        self.assertEqual(expected, self.s.standardize_dashes(text))

    def test_standardize_dashes_multi(self):
        text = "Flag of the Kingdom of Piedmont-Sardinia (1851–1861)"
        expected = "Flag of the Kingdom of Piedmont-Sardinia (1851-1861)"
        self.assertEqual(expected, self.s.standardize_dashes(text))



import unittest
from bs4 import BeautifulSoup
from LinkParser import LinkParser
from os import environ


class LinkParserTestCase_ContextMethods_FlagOfChina(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/Flag_of_China.html") as _f:
            self.soup = BeautifulSoup(_f.read(), features="html.parser")

    # link_is_inline_thumbnail #

    def test_link_is_main_infobox_thumbnail_flag_of_china(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_People%27s_Republic_of_China.svg"})
        self.assertTrue(self.p.link_is_main_infobox_thumbnail(tag))

    def test_link_is_other_infobox_thumbnail_flag_of_china(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_People%27s_Republic_of_China.svg"})
        self.assertFalse(self.p.link_is_other_infobox_thumbnail(tag))

    def test_link_is_thumbnail_in_list_flag_of_china(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_People%27s_Republic_of_China.svg"})
        self.assertFalse(self.p.link_is_thumbnail_in_list(tag))

    def test_link_is_gallerybox_thumbnail_flag_of_china(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_People%27s_Republic_of_China.svg"})
        self.assertFalse(self.p.link_is_gallerybox_thumbnail(tag))

    def test_link_is_inline_thumbnail_original_design(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Zeng_Liansong%27s_proposal_for_the_PRC_flag.svg"})
        self.assertTrue(self.p.link_is_inline_thumbnail(tag))

    def test_link_is_thumbnail_in_list_original_design(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Zeng_Liansong%27s_proposal_for_the_PRC_flag.svg"})
        self.assertFalse(self.p.link_is_thumbnail_in_list(tag))

    def test_link_is_gallerybox_thumbnail_original_design(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Zeng_Liansong%27s_proposal_for_the_PRC_flag.svg"})
        self.assertFalse(self.p.link_is_gallerybox_thumbnail(tag))

    def test_link_is_inline_thumbnail_mao_proposal(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Mao_Zedong%27s_proposal_for_the_PRC_flag.svg"})
        self.assertTrue(self.p.link_is_inline_thumbnail(tag))

    def test_link_is_inline_thumbnail_sidebyside_left(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Chinese-army_Wuhan_flag_(1911-1928)_18_dots.svg"})
        self.assertTrue(self.p.link_is_inline_thumbnail(tag))

    def test_link_is_inline_thumbnail_sidebyside_right(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Chinese-army_Wuhan_flag_(1911-1928)_19_dots.svg"})
        self.assertTrue(self.p.link_is_inline_thumbnail(tag))


    # inline_thumbnail_text #

    def test_inline_thumbnail_text_original_design(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Zeng_Liansong%27s_proposal_for_the_PRC_flag.svg"})
        expected = "The original design submitted by Zeng Liansong"
        self.assertEqual(expected, self.p.inline_thumbnail_text(tag))

    def test_inline_thumbnail_text_mao_proposal(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Mao_Zedong%27s_proposal_for_the_PRC_flag.svg"})
        expected = "The \"Yellow River\" flag design originally preferred by Mao Zedong."
        self.assertEqual(expected, self.p.inline_thumbnail_text(tag))

    def test_inline_thumbnail_text_sidebyside_left(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Chinese-army_Wuhan_flag_(1911-1928)_18_dots.svg"})
        expected = ""           # caption for side-by-side thumbs may not be specific, may contains plurals, etc.
        self.assertEqual(expected, self.p.inline_thumbnail_text(tag))

    def test_inline_thumbnail_text_sidebyside_right(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Chinese-army_Wuhan_flag_(1911-1928)_19_dots.svg"})
        expected = ""           # caption for side-by-side thumbs may not be specific, may contains plurals, etc.
        self.assertEqual(expected, self.p.inline_thumbnail_text(tag))


    # link_is_gallerybox_thumbnail #

    def test_link_is_gallerybox_thumbnail_roc_proposal_1(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_(draft_1).svg"})
        self.assertTrue(self.p.link_is_gallerybox_thumbnail(tag))

    def test_link_is_thumbnail_in_list_roc_proposal_1(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_(draft_1).svg"})
        self.assertFalse(self.p.link_is_thumbnail_in_list(tag))

    def test_link_is_inline_thumbnail_roc_proposal_1(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_(draft_1).svg"})
        self.assertFalse(self.p.link_is_inline_thumbnail(tag))

    def test_link_is_main_infobox_thumbnail_roc_proposal_1(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_(draft_1).svg"})
        self.assertFalse(self.p.link_is_main_infobox_thumbnail(tag))

    def test_link_is_other_infobox_thumbnail_roc_proposal_1(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_(draft_1).svg"})
        self.assertFalse(self.p.link_is_other_infobox_thumbnail(tag))

    def test_link_is_gallerybox_thumbnail_roc_proposal_2(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_(draft_2).svg"})
        self.assertTrue(self.p.link_is_gallerybox_thumbnail(tag))

    def test_link_is_gallerybox_thumbnail_roc_proposal_3(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_Army.svg"})
        self.assertTrue(self.p.link_is_gallerybox_thumbnail(tag))

    def test_link_is_gallerybox_thumbnail_roc_proposal_4(self):
        tag = self.soup.find_all("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China.svg"})[2]
        self.assertTrue(self.p.link_is_gallerybox_thumbnail(tag))


    # gallerybox_thumbnail_text #

    def test_link_is_gallerybox_thumbnail_roc_proposal_1(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_(draft_1).svg"})
        expected = "Teo Eng Hock and his wife's proposal 1 for the ROC flag."
        self.assertEqual(expected, self.p.gallerybox_thumbnail_text(tag))

    def test_link_is_gallerybox_thumbnail_roc_proposal_2(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_(draft_2).svg"})
        expected = "Proposal 2 for the ROC flag."
        self.assertEqual(expected, self.p.gallerybox_thumbnail_text(tag))

    def test_link_is_gallerybox_thumbnail_roc_proposal_3(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China_Army.svg"})
        expected = "Proposal 3 for the ROC flag, later adopted as the Flag of the Republic of China Army."
        self.assertEqual(expected, self.p.gallerybox_thumbnail_text(tag))

    def test_link_is_gallerybox_thumbnail_roc_proposal_4(self):
        tag = self.soup.find_all("a", {"href": "/wiki/File:Flag_of_the_Republic_of_China.svg"})[2]
        expected = "Proposal 4 for the ROC flag, later officially adopted as the national flag."
        self.assertEqual(expected, self.p.gallerybox_thumbnail_text(tag))


class LinkParserTestCase_ContextMethods_FlagOfItaly(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/Flag_of_Italy.html") as _f:
            self.soup = BeautifulSoup(_f.read(), features="html.parser")

    def test_link_is_main_infobox_thumbnail(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_Italy.svg"})
        self.assertTrue(self.p.link_is_main_infobox_thumbnail(tag))

    def test_link_is_other_infobox_thumbnail(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Civil_Ensign_of_Italy.svg"})
        self.assertTrue(self.p.link_is_other_infobox_thumbnail(tag))

    def test_main_infobox_thumbnail_text(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_Italy.svg"})
        expected = "Tricolore National flag 2:3 18 June 1946 (birth of the Italian Republic) A vertical tricolour of green, white and red"
        self.assertEqual(expected, self.p.main_infobox_thumbnail_text(tag))

    def test_other_infobox_thumbnail_text(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Civil_Ensign_of_Italy.svg"})
        expected = "Variant flag of Italian Republic"
        self.assertEqual(expected, self.p.other_infobox_thumbnail_text(tag))

class LinkParserTestCase_ContextMethods_FlagOfJapan(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/Flag_of_Japan.html") as _f:
            self.soup = BeautifulSoup(_f.read(), features="html.parser")

    def test_link_is_inline_thumbnail_old_flag(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_Japan_(1870%E2%80%931999).svg"})
        self.assertTrue(self.p.link_is_inline_thumbnail(tag))

    def test_link_is_inline_thumbnail_mourning_flag(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Japan_mourning_flag.svg"})
        self.assertTrue(self.p.link_is_inline_thumbnail(tag))

    def test_inline_thumbnail_text_old_flag(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Flag_of_Japan_(1870%E2%80%931999).svg"})
        expected = "Flag of Japan (1870–1999)."
        self.assertEqual(expected, self.p.inline_thumbnail_text(tag))

    def test_inline_thumbnail_text_mourning_flag(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Japan_mourning_flag.svg"})
        expected = "Diagram published with Regulation 1 from 1912 (Raising Mourning Flag for the Emperor)"
        self.assertEqual(expected, self.p.inline_thumbnail_text(tag))

    def test_link_is_gallerybox_thumbnail_war_flag(self):
        tag = self.soup.find("a", {"href": "/wiki/File:War_flag_of_the_Imperial_Japanese_Army_(1868%E2%80%931945).svg"})
        self.assertTrue(self.p.link_is_gallerybox_thumbnail(tag))

    def test_gallerybox_thumbnail_text_war_flag(self):
        tag = self.soup.find("a", {"href": "/wiki/File:War_flag_of_the_Imperial_Japanese_Army_(1868%E2%80%931945).svg"})
        expected = "Pre-WWII peace treaty War flag of the Imperial Japanese Army (1868–1945) (十六条旭日旗)"
        self.assertEqual(expected, self.p.gallerybox_thumbnail_text(tag))


class LinkParserTestCase_ContextMethods_ListOfItalianFlags(unittest.TestCase):

    def setUp(self):
        self.p = LinkParser.Parser()
        with open(f"{environ['CONTAINER_DATA_PATH']}/html/List_of_Italian_flags.html") as _f:
            self.soup = BeautifulSoup(_f.read(), features="html.parser")

    def test_link_is_thumbnail_in_list_civil_ensign(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Civil_Ensign_of_Italy.svg"})
        self.assertTrue(self.p.link_is_thumbnail_in_list(tag))

    def test_link_is_thumbnail_in_list_state_ensign(self):
        tag = self.soup.find("a", {"href": "/wiki/File:State_Ensign_of_Italy.svg"})
        self.assertTrue(self.p.link_is_thumbnail_in_list(tag))

    def test_thumbnail_in_list_text_civil_ensign(self):
        tag = self.soup.find("a", {"href": "/wiki/File:Civil_Ensign_of_Italy.svg"})
        expected = "9 November 1947 Civil ensign The flag of Italy with a shield divided into four squares representing the four Maritime Republics: Venice (represented by the Lion of St. Mark, top left), Genoa (top right), Amalfi (bottom left), and Pisa (represented by their respective crosses). The ensign is similar to the one used by the Italian Navy, with the exception that the lion of Venice is carrying no sword, the emblem is not crowned, and the book of the Gospel is open."
        self.assertEqual(expected, self.p.thumbnail_in_list_text(tag))

    def test_thumbnail_in_list_text_state_ensign(self):
        tag = self.soup.find("a", {"href": "/wiki/File:State_Ensign_of_Italy.svg"})
        expected = "24 October 2003 State ensign The flag of Italy with the State Emblem."
        self.assertEqual(expected, self.p.thumbnail_in_list_text(tag))

    def test_associated_text_state_ensign(self):
        tag = self.soup.find("a", {"href": "/wiki/File:State_Ensign_of_Italy.svg"})
        expected = "24 October 2003 State ensign The flag of Italy with the State Emblem."
        self.assertEqual(expected, self.p.associated_text(tag, None))


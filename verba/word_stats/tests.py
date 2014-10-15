from django.test import TestCase
from verba.word_stats.utils import text_to_words, words_analysis
from collections import Counter


class Utils_test(TestCase):
    def test_text_to_words(self):
        """
        Tests if function correctly converts text to words list;
        Removes all punctuation, digits, spaces and blank lines;
        :return:
        """
        text = " Hello,  heLlo wORLD!48 2,6 1-5 2*6 !1! the world is mine1 " \
               "HE11O, \/\/0R1D!!! world_again "
        result = ['hello', 'hello', 'world', 'the', 'world', 'is', 'mine',
                  'he', 'o', 'r', 'd', 'world', 'again']
        self.assertEqual(text_to_words(text), result)

    def test_words_analysis1(self):
        """
        Tests if function correctly returns list of known words and Counter
        dictionary with words and their frequency in list of words;
        Words less than 2 letters will be ignored;
        No 'extra' features selected;
        No known words in user's dictionary;
        :return:
        """
        test_words = ['hello', 'hello', 'forever', 'i', 'young', 'i', 'am',
                      'i', 'going', 'spells', 'attachments',
                      'killed', 'diving', 'fitness', 'situated', 'starts']
        result = [], Counter(
            {'hello': 2, 'forever': 1, 'attachments': 1, 'starts': 1,
             'am': 1, 'young': 1,
             'killed': 1, 'situated': 1, 'going': 1, 'fitness': 1, 'diving': 1,
             'spells': 1})

        self.assertEqual(words_analysis(
            test_words,
            three_letters=False,
            only_base=False,
            known_words=[]), result)

    def test_words_analysis2(self):
        """
        Tests if function correctly returns list of known words and Counter
        dictionary with words and their frequency in list of words;
        Words less than 2 letters will be ignored;
        No 'extra' features selected;
        Some words in user's dictionary;
        :return:
        """
        test_words = ['hello', 'hello', 'forever', 'i', 'young', 'young',
                      'i', 'am', 'i', 'going', 'spells', 'attachments',
                      'killed', 'diving', 'fitness', 'situated', 'starts']
        result = ['hello', 'going', 'spells'], Counter(
            {'young': 2, 'forever': 1, 'attachments': 1, 'starts': 1, 'am': 1,
             'killed': 1, 'situated': 1, 'fitness': 1, 'diving': 1})
        known_words = ['hello', 'spells', 'going']
        self.assertEqual(words_analysis(
            test_words,
            three_letters=False,
            only_base=False,
            known_words=known_words), result)

    def test_words_analysis3(self):
        """
        Tests if function correctly returns list of known words and Counter
        dictionary with words and their frequency in list of words;
        Words less than 3 letters will be ignored;
        '3 letters' extra feature selected;
        Some words in user's dictionary;
        :return:
        """
        test_words = ['hello', 'hello', 'forever', 'i', 'young', 'young',
                      'i', 'am', 'i', 'going', 'spells', 'attachments',
                      'killed', 'diving', 'fitness', 'situated', 'starts']
        result = ['hello', 'going', 'spells'], Counter(
            {'young': 2, 'forever': 1, 'attachments': 1, 'starts': 1,
             'situated': 1, 'fitness': 1, 'diving': 1, 'killed': 1})
        known_words = ['hello', 'spells', 'going']
        self.assertEqual(words_analysis(
            test_words,
            three_letters=True,
            only_base=False,
            known_words=known_words), result)

    def test_words_analysis4(self):
        """
        Tests if function correctly returns list of known words and Counter
        dictionary with words and their frequency in list of words;
        Words less than 3 letters will be ignored;
        '3 letters' extra feature selected;
        'Stem' extra feature selected;
        Some words in user's dictionary;
        :return:
        """
        test_words = ['hello', 'hello', 'forever', 'i', 'young', 'young',
                      'i', 'am', 'i', 'going', 'spells', 'attachments',
                      'killed', 'diving', 'fitness', 'situated', 'starts']
        result = ['hello'], Counter(
            {'young': 2, 'forev': 1, 'fit': 1, 'attach': 1, 'dive': 1,
             'spell': 1, 'situat': 1, 'start': 1,  'kill': 1})
        known_words = ['hello', 'spells', 'going']
        self.assertEqual(words_analysis(
            test_words,
            three_letters=True,
            only_base=True,
            known_words=known_words), result)

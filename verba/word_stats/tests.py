from django.test import TestCase
from verba.word_stats.utils import text_to_words


class Utils_test(TestCase):
    def test_text_to_words(self):
        text = "HellO, wORLD 1,0"
        self.assertEqual(text_to_words(text), ['hello', 'world'])

    def test_words_analysis(self):
        test_words = ['hello', 'hello', 'forever', 'i', 'young', 'i', 'am',
                      'i', 'going', 'spells', 'attachments',
                      'killed', 'diving', 'fitness', 'situated', 'starts']
        result1 = [], Counter(
            {'i': 3, 'hello': 2, 'forever': 1, 'attachments': 1, 'starts': 1,
             'am': 1, 'young': 1,
             'killed': 1, 'situated': 1, 'going': 1, 'fitness': 1, 'diving': 1,
             'spells': 1})

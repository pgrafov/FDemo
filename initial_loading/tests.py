import os
import unittest

from django.core.management import call_command

from main.models import Word


class CommandsTestCase(unittest.TestCase):
    def setUp(self):
        self.file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'tmp.txt')
        with open(self.file, 'wb') as file_:
            for word in ['lion', 'snow', 'fish', 'fish', 'fi-&?-sh']:
                file_.write(word + '\n')

    def tearDown(self):
        os.remove(self.file)
        Word.objects.all().delete()

    def test_can_load_words(self):
        call_command('load_words', self.file, verbosity=2)
        word_count = Word.objects.all().count()
        assert word_count == 3, 'Loaded %s words, expected 3' % word_count

    def test_loading_words_for_the_second_time_has_no_effect(self):
        call_command('load_words', self.file)
        word_count_before = Word.objects.all().count()
        call_command('load_words', self.file)
        word_count_after = Word.objects.all().count()
        assert (word_count_before == word_count_after), \
            'Loading words for the second time doesn\'t work as expected'

    def test_shell_command_cleans_the_wordlist(self):
        '''Verify that shell command clears the wordlist
           by converting all words to lowercase, and removing
           characters that are not [0-9a-z]'''
        with open(self.file, 'wb') as file_:
            file_.write('~ClEaN mE!~')
        call_command('load_words', self.file)
        word_count = Word.objects.all().count()
        assert word_count == 1, 'Loaded %s words, expected 1' % word_count
        cleaned = str(Word.objects.all()[0])
        expected = 'cleanme'
        assert cleaned == expected, \
            'Cleaning doesn\'t work as expected: got - %s, expected - %s' \
            % (cleaned, expected)

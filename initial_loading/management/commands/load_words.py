"""
A shell command that cleans the wordlist and loads
it into the database. This command takes one mandatory argument:
path to the file with words
"""

import re

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from main.models import Word


class Command(BaseCommand):
    help = 'Loads file with initial words (wordlist.txt)'

    def add_arguments(self, parser):
        parser.add_argument('file', help='file containing list of words')

    def handle(self, *args, **options):
        verbose = options['verbosity'] > 1
        file_with_words = options['file']
        regex = re.compile(r"[^0-9a-z]*")
        count = 0
        with open(file_with_words, 'rb') as file_:
            if verbose:
                print "Loaded words:"
            for line in file_:
                cleaned_word = regex.sub('', line.lower().strip())
                if cleaned_word:
                    try:
                        word = Word(title=cleaned_word)
                        word.save()
                        if verbose:
                            print str(count+1) + ".", cleaned_word
                            count += 1
                    except IntegrityError:
                        pass

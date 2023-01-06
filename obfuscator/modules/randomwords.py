import os
import pathlib
import random
import re
import string
import urllib.request
from pygments import highlight
from pygments.token import *
from pygments.formatter import Formatter
from pygments.lexers.dotnet import VbNetLexer

class IsVbSyntax(Formatter):
    def __init__(self):
        super().__init__()
        self.is_vb = False
        # https://pygments.org/docs/tokens/#module-pygments.token
        self._known_token_types = (
            Keyword, Literal, Operator, Punctuation, Comment,
        )
    
    def is_known_token(self, ttype):
        for known_type in self._known_token_types:
            if is_token_subtype(ttype, known_type):
                return True
        return False
    
    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            if self.is_known_token(ttype):
                self.is_vb = True

def is_vb_syntax(buf):
    dummy_formatter = IsVbSyntax()
    highlight(buf, VbNetLexer(), dummy_formatter)
    return dummy_formatter.is_vb

class RandomWords:
    def __init__(self, wordlist_files=[], wordlist_urls=[]):
        self.allowed_chars = string.ascii_letters + string.digits
        self.disallowed_chars = re.compile('[^a-zA-Z0-9]')

        # /home/user/.local/share/dict, C:\Users\user\.local\share\dict
        self.wordlist_basedir = os.environ.get('XDG_DATA_HOME') \
                                or os.path.join(pathlib.Path.home(), f'.local{os.sep}share')
        self.wordlist_dir = os.path.join(self.wordlist_basedir, 'dict')
        self.wordlist_file = os.path.join(self.wordlist_dir, "words")
        self._init_wordlist_dirs(self.wordlist_dir)

        # to skip files, assign param wordlist_files=None
        self.wordlist_files = [
            '/usr/share/dict/words',
            '/usr/dict/words',
        ]
        self._init_wordlist_files(wordlist_files)

        # to skip urls, assign param wordlist_files=None
        self.wordlist_urls = [
            'https://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain',
            'https://www.mit.edu/~ecprice/wordlist.10000',
        ]
        self._init_wordlist_urls(wordlist_urls)

        self._init_wordlist()
    
    def _init_wordlist(self, force_build=False):
        words = set()
        write_file = False
        self.unique_words = None
        
        if not os.path.exists(self.wordlist_file) or force_build:
            for path in self.wordlist_files:
                if not os.path.isfile(path):
                    continue
                with open(path, 'r') as f:
                    for word in filter(lambda w: w, map(self._process_word_data, iter(f.readline, ''))):
                        words.add(word)

            for url in self.wordlist_urls:
                for word in filter(lambda w: w, map(self._process_word_data, self.download_words(url).splitlines())):
                    words.add(word)
            
            if words:
                write_file = True
        else:
            with open(self.wordlist_file, 'r') as f:
                for word in filter(lambda w: w, map(self._process_word_data, iter(f.readline, ''))):
                    words.add(word)
        
        self.words = list(words.copy())
        self.unique_words = list(words.copy())

        if write_file:
            with open(self.wordlist_file, 'w') as f:
                f.write("\n".join(self.words))
        
    def _init_wordlist_dirs(self, path):
        if os.path.exists(path):
            return
        os.makedirs(path)
    
    def _init_wordlist_files(self, wordlist_files):
        if wordlist_files is None:
            self.wordlist_files = []
        elif isinstance(wordlist_files, list) and wordlist_files:
            self.wordlist_files = list(wordlist_files)

    def _init_wordlist_urls(self, wordlist_urls):
        if wordlist_urls is None:
            self.wordlist_urls = []
        elif isinstance(wordlist_urls, list) and wordlist_urls:
            self.wordlist_urls = list(wordlist_urls)

    def _process_word_data(self, data):
        word = self.disallowed_chars.sub('', data)
        if not word:
            return ''
        if is_vb_syntax(word):
            return ''  # ;-) ;-)
        return word
 
    def download_words(self, url):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
        data = ''
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = response.read().decode()
        return data

    def random_word(self, random_cap=False):
        word = random.choice(self.words)
        if random_cap and random.randint(0, 1):
            return word.capitalize()
        return word

    def random_unique_word(self, random_cap=False):
        idx = random.randint(0, len(self.unique_words))
        word = self.unique_words.pop(idx)
        if random_cap and random.randint(0, 1):
            return word.capitalize()
        return word

    def random_alphanum(self, a, b):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(a, b)))

    def random_alpha(self, a, b):
        return ''.join(random.choices(string.ascii_letters, k=random.randint(a, b)))

if __name__ == '__main__':
    rw = RandomWords()
    print(rw.random_word())
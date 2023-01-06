import random
import re
import string
from pygments import highlight
from pygments.lexers.dotnet import VbNetLexer

from obfuscator.modules.formatters.variable_names_formatter import VariableNamesFormatter
from obfuscator.modules.randomwords import RandomWords

class Randomizer:
    def __init__(self, script, use_random_words=True, use_unique_values=True):
        self.script = script
        self.rand = {}
        self.use_random_words = use_random_words
        self.use_unique_values = use_unique_values
        self.RandomWords = RandomWords()
        self.unique_rands = {}

    def random_choice(self, unique=None, random_word=None):
        random_word = random_word or self.use_random_words
        unique = unique or self.use_unique_values
        
        if random_word:
            if unique:
                ret = self.RandomWords.random_unique_word()
            else:
                ret = self.RandomWords.random_word()
        else:
            if unique:
                word = None
                while word in self.unique_rands or not word:
                    word = self.RandomWords.random_alpha(12, 15)
                self.unique_rands[word] = None
                ret = word
            else:
                ret = self.RandomWords.random_alpha(12, 15)
        return ret

    def run(self):
        self.map_variable_names_to_random_names()
        formatter = VariableNamesFormatter(self.rand)
        self.script.code = highlight(self.script.code, VbNetLexer(), formatter)

    def map_variable_names_to_random_names(self):
        functions = re.finditer("(Function|Sub)[ ]+(\w+)\(", self.script.code)
        for function_name in functions:
            self.rand[function_name.group(2)] = self.random_choice()
        parameters = re.finditer("(?:Function|Sub)[ ]+\w+\(((?:\w+[ ]+As[ ]+\w+(?:, )*)*)\)", self.script.code)
        for parameter in parameters:
            parameter_names = re.finditer("(?:(\w+)[ ]+As[ ]+\w+(?:, )*)", self.script.code)
            for parameter_name in parameter_names:
                print("parameter found: " + parameter_name.group(1))
                self.rand[parameter_name.group(1)] = self.random_choice()
        variables = re.finditer("^\s*(Dim|Set)[ ]+(\w+)", self.script.code, flags=re.MULTILINE)
        for variable_name in variables:
            self.rand[variable_name.group(2)] = self.random_choice()

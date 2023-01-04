import random
import string
from pygments.formatter import Formatter
from pygments.token import Token


class VariableNamesFormatter(Formatter):
    def __init__(self, rand):
        super().__init__()
        self.rand = rand
        self.excluded_function_names = [
            'AutoOpen',  # Word
            'Workbook_Open',  # Excel
        ]

    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            if ttype == Token.Name.Function \
            and value in self.excluded_function_names:
                outfile.write(value)
                continue
            
            if (ttype == Token.Name or ttype == Token.Name.Function) and value in self.rand and value != "AutoOpen":
                outfile.write(self.rand[value])
            else:
                outfile.write(value)

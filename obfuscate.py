#!/usr/bin/env python3

import argparse
import sys

from termcolor import colored

from obfuscator.document import Document
from obfuscator.obfuscator import Obfuscator


def main():
    parser = argparse.ArgumentParser(description='VBA script obfuscator.')
    parser.add_argument('input_file', type=str, action='store',
                        help='path of the file containing the VBA script to obfuscate.')
    parser.add_argument('output_file', type=str, action='store',
                        help='path of the file to store the result.')
    parser.add_argument('--use-random-words', dest='use_random_words', action='store_true', default=False,
                        help='use random words instead of random values (sourced from file system and http)')
    parser.add_argument('--use-unique-values', dest='use_unique_values', action='store_true', default=False,
                        help='randomly generated values should be unique')
    args = parser.parse_args()

    try:
        script = Document(args.input_file)
    except (OSError, IOError) as e:
        print(colored("Can't open the file named {}".format(args.input_file), "red"))
        print(e)
        sys.exit(1)

    obfuscator = Obfuscator(script, use_random_words=args.use_random_words, use_unique_values=args.use_unique_values)
    obfuscator.obfuscate()

    try:
        script.store(args.output_file)
    except (OSError, IOError) as e:
        print(colored("Can't store result in file named {}".format(args.output_file), "red"))
        print(e)
        sys.exit(1)

    print(colored("{} obfuscation complete !\nResult stored in {}"
                  .format(args.input_file, args.output_file), "green"))


if __name__ == "__main__":
    main()

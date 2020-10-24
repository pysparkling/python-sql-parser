import sys

from antlr4 import InputStream

from sqlparser.baseparser import build_parser
from sqlparser.utils import print_tree


def string_to_ast(string, rule, case_insensitive=True, ignore_missing_identifier_quotes=True, debug=False):
    parser = build_string_parser(string, ignore_missing_identifier_quotes, case_insensitive)
    tree = getattr(parser, rule)()
    if debug:
        sys.stderr.flush()
        print_tree(tree)
        sys.stdout.flush()
    return tree


def build_string_parser(string, case_insensitive=True, ignore_missing_identifier_quotes=True):
    string_as_stream = InputStream(string)
    parser = build_parser(string_as_stream, case_insensitive, ignore_missing_identifier_quotes)
    return parser


__all__ = ["string_to_ast", "build_string_parser"]

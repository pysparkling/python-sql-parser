import logging

from antlr4 import InputStream

from sqlparser.internalparser import build_parser
from sqlparser.utils import print_tree


def string_to_ast(string, rule, *, strict_mode=False, debug=False):
    parser = build_string_parser(string, strict_mode)
    tree = getattr(parser, rule)()
    if debug:
        print_tree(tree, printer=logging.warning)
    return tree


def build_string_parser(string, strict_mode=False):
    string_as_stream = InputStream(string)
    parser = build_parser(string_as_stream, strict_mode)
    return parser


__all__ = ["string_to_ast", "build_string_parser"]

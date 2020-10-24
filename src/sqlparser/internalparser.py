import antlr4

from antlr4.error.ErrorListener import ErrorListener

from sqlparser.generated.SqlBaseLexer import SqlBaseLexer
from sqlparser.generated.SqlBaseParser import SqlBaseParser


class RemoveIdentifierBackticks(antlr4.ParseTreeListener):
    @staticmethod
    def exitQuotedIdentifier(ctx):
        def identity(token):
            return token

        return identity

    @staticmethod
    def enterNonReserved(ctx):
        def add_backtick(token):
            return "`{0}`".format(token)

        return add_backtick


class ParseErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SqlSyntaxError("Parse error", msg)


class UpperCaseCharStream:
    """
    Make SQL token detection case insensitive, allowing identifier without backticks to be seen as e.g. column names
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def getText(self, interval, *args):
        if args or (self.size() > 0 and (interval.b - interval.a >= 0)):
            return self.wrapped.getText(interval, *args)
        else:
            return ""

    def LA(self, i: int):
        la = self.wrapped.LA(i)
        if la == 0 or la == -1:
            return la
        else:
            return ord(chr(la).upper())

    def __getattr__(self, item):
        return getattr(self.wrapped, item)


def build_parser(stream, strict_mode):
    if not strict_mode:
        stream = UpperCaseCharStream(stream)
    lexer = SqlBaseLexer(stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ParseErrorListener())
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = SqlBaseParser(token_stream)
    parser.addParseListener(RemoveIdentifierBackticks())
    parser.removeErrorListeners()
    parser.addErrorListener(ParseErrorListener())
    return parser


class SqlSyntaxError(Exception):
    pass

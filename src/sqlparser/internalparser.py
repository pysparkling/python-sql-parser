import antlr4
from antlr4 import RecognitionException

from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.ErrorStrategy import BailErrorStrategy
from antlr4.error.Errors import ParseCancellationException

from sqlparser.generated.SqlBaseLexer import SqlBaseLexer
from sqlparser.generated.SqlBaseParser import SqlBaseParser


class RemoveIdentifierBackticks(antlr4.ParseTreeListener):
    @staticmethod
    def exitQuotedIdentifier(ctx):  # pylint: disable=invalid-name,unused-argument
        def identity(token):
            return token

        return identity

    @staticmethod
    def enterNonReserved(ctx):  # pylint: disable=invalid-name,unused-argument
        def add_backtick(token):
            return "`{0}`".format(token)

        return add_backtick


class ParseErrorListener(ErrorListener):
    def syntaxError(
            self, recognizer, offendingSymbol, line, column, msg, e
    ):  # pylint: disable=invalid-name,no-self-use,too-many-arguments
        raise SqlSyntaxError("Parse error", msg)


class UpperCaseCharStream:
    """
    Make SQL token detection case insensitive and allow identifier without
    backticks to be seen as e.g. column names
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def getText(self, interval, *args):  # pylint: disable=invalid-name
        if args or (self.size() > 0 and (interval.b - interval.a >= 0)):
            return self.wrapped.getText(interval, *args)
        return ""

    def LA(self, i: int):  # pylint: disable=invalid-name
        token = self.wrapped.LA(i)
        if token in (0, -1):
            return token
        return ord(chr(token).upper())

    def __getattr__(self, item):
        return getattr(self.wrapped, item)


class ExplicitBailErrorStrategy(BailErrorStrategy):
    """
    Bail Error Strategy throws a ParseCancellationException,
    This strategy simply throw a more explicit exception
    """
    def recover(self, recognizer, e: RecognitionException):
        try:
            super(ExplicitBailErrorStrategy, self).recover(recognizer, e)
        except ParseCancellationException:
            raise SqlParsingError from e


class EarlyBailSqlLexer(SqlBaseLexer):
    def recover(self, re: RecognitionException):
        raise SqlLexicalError from re


def build_parser(stream, strict_mode=False, early_bail=True):
    if not strict_mode:
        stream = UpperCaseCharStream(stream)
    if early_bail:
        lexer = EarlyBailSqlLexer(stream)
    else:
        lexer = SqlBaseLexer(stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ParseErrorListener())
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = SqlBaseParser(token_stream)
    parser.addParseListener(RemoveIdentifierBackticks())
    parser.removeErrorListeners()
    parser.addErrorListener(ParseErrorListener())
    if early_bail:
        parser._errHandler = ExplicitBailErrorStrategy()
    return parser


class SqlParsingError(Exception):
    pass


class SqlLexicalError(SqlParsingError):
    pass


class SqlSyntaxError(SqlParsingError):
    pass

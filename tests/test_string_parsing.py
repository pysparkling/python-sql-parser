from unittest import TestCase

from sqlparser import string_to_ast, SqlSyntaxError
from sqlparser.parsing import parse_statement
from sqlparser.utils import tree_to_strings


class TestStringParsing(TestCase):
    maxDiff = None

    def test_parse_statement(self):
        tree = parse_statement(
            'select * from table where column like "%Python%"',
            converter=tree_to_strings,
            debug=True
        )
        self.assertEqual(
            tree,
            ['|SingleStatementContext',
             '|-StatementDefaultContext',
             '|--QueryContext',
             '|---QueryTermDefaultContext',
             '|----QueryPrimaryDefaultContext',
             '|-----RegularQuerySpecificationContext',
             '|------SelectClauseContext',
             '|-------TerminalNodeImpl[select]',
             '|-------NamedExpressionSeqContext',
             '|--------NamedExpressionContext',
             '|---------ExpressionContext',
             '|----------PredicatedContext',
             '|-----------ValueExpressionDefaultContext',
             '|------------StarContext',
             '|-------------TerminalNodeImpl[*]',
             '|------FromClauseContext',
             '|-------TerminalNodeImpl[from]',
             '|-------RelationContext',
             '|--------TableNameContext',
             '|---------MultipartIdentifierContext',
             '|----------ErrorCapturingIdentifierContext',
             '|-----------IdentifierContext',
             '|------------UnquotedIdentifierContext',
             '|-------------NonReservedContext',
             '|--------------TerminalNodeImpl[table]',
             '|-----------RealIdentContext',
             '|---------TableAliasContext',
             '|------WhereClauseContext',
             '|-------TerminalNodeImpl[where]',
             '|-------PredicatedContext',
             '|--------ValueExpressionDefaultContext',
             '|---------ColumnReferenceContext',
             '|----------IdentifierContext',
             '|-----------UnquotedIdentifierContext',
             '|------------NonReservedContext',
             '|-------------TerminalNodeImpl[column]',
             '|--------PredicateContext',
             '|---------TerminalNodeImpl[like]',
             '|---------ValueExpressionDefaultContext',
             '|----------ConstantDefaultContext',
             '|-----------StringLiteralContext',
             '|------------TerminalNodeImpl["%Python%"]',
             '|---QueryOrganizationContext',
             '|-TerminalNodeImpl[<EOF>]']
        )

    def test_strict_mode_reject(self):
        with self.assertRaises(SqlSyntaxError) as ctx:
            string_to_ast(
                'select * from table where column like "%Python%"',
                rule='singleStatement',
                strict_mode=True
            )
        self.assertEqual(
            ctx.exception.args[0],
            'Parse error'
        )
        self.assertEqual(
            ctx.exception.args[1][:30],
            "mismatched input 's' expecting"
        )

    def test_strict_mode(self):
        ast = string_to_ast(
            'SELECT * FROM `table` WHERE `column` LIKE "%Python%"',
            rule='singleStatement',
            strict_mode=True
        )
        stringified_tree = tree_to_strings(ast)
        self.assertEqual(
            stringified_tree,
            ['|SingleStatementContext',
             '|-StatementDefaultContext',
             '|--QueryContext',
             '|---QueryTermDefaultContext',
             '|----QueryPrimaryDefaultContext',
             '|-----RegularQuerySpecificationContext',
             '|------SelectClauseContext',
             '|-------TerminalNodeImpl[SELECT]',
             '|-------NamedExpressionSeqContext',
             '|--------NamedExpressionContext',
             '|---------ExpressionContext',
             '|----------PredicatedContext',
             '|-----------ValueExpressionDefaultContext',
             '|------------StarContext',
             '|-------------TerminalNodeImpl[*]',
             '|------FromClauseContext',
             '|-------TerminalNodeImpl[FROM]',
             '|-------RelationContext',
             '|--------TableNameContext',
             '|---------MultipartIdentifierContext',
             '|----------ErrorCapturingIdentifierContext',
             '|-----------IdentifierContext',
             '|------------QuotedIdentifierAlternativeContext',
             '|-------------QuotedIdentifierContext',
             '|--------------TerminalNodeImpl[`table`]',
             '|-----------RealIdentContext',
             '|---------TableAliasContext',
             '|------WhereClauseContext',
             '|-------TerminalNodeImpl[WHERE]',
             '|-------PredicatedContext',
             '|--------ValueExpressionDefaultContext',
             '|---------ColumnReferenceContext',
             '|----------IdentifierContext',
             '|-----------QuotedIdentifierAlternativeContext',
             '|------------QuotedIdentifierContext',
             '|-------------TerminalNodeImpl[`column`]',
             '|--------PredicateContext',
             '|---------TerminalNodeImpl[LIKE]',
             '|---------ValueExpressionDefaultContext',
             '|----------ConstantDefaultContext',
             '|-----------StringLiteralContext',
             '|------------TerminalNodeImpl["%Python%"]',
             '|---QueryOrganizationContext',
             '|-TerminalNodeImpl[<EOF>]']
        )

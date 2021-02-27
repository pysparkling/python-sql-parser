[![PyPI Latest Release](https://img.shields.io/pypi/v/pythonsqlparser.svg)](https://pypi.org/project/pythonsqlparser/)
[![License](https://img.shields.io/pypi/l/pythonsqlparser.svg)](https://github.com/pysparkling/python-sql-parser/blob/main/LICENSE)
[![Travis Build Status](https://travis-ci.org/pysparkling/python-sql-parser.svg?branch=main)](https://travis-ci.org/pysparkling/python-sql-parser)
# SQL Parser
This package convert SQL string into a syntax tree object.

These objects can then be manipulated via Python's code.

The SQL syntax used is the one used by Apache Spark, based on Presto's one.

It is defined in [src/sqlparser/grammar/SqlBase.g4](https://github.com/pysparkling/python-sql-parser/blob/main/src/sqlparser/grammar/SqlBase.g4).

### Usage

```python
from sqlparser import parse_statement
from sqlparser.utils import print_tree
tree = parse_statement('SELECT * FROM table WHERE column LIKE "%Python%"')
print_tree(tree)
```

Result (each line is a node of the tree):
```
|SingleStatementContext
|-StatementDefaultContext
|--QueryContext
|---QueryTermDefaultContext
|----QueryPrimaryDefaultContext
|-----RegularQuerySpecificationContext
|------SelectClauseContext
|-------TerminalNodeImpl[SELECT]
|-------NamedExpressionSeqContext
|--------NamedExpressionContext
|---------ExpressionContext
|----------PredicatedContext
|-----------ValueExpressionDefaultContext
|------------StarContext
|-------------TerminalNodeImpl[*]
|------FromClauseContext
|-------TerminalNodeImpl[FROM]
|-------RelationContext
|--------TableNameContext
|---------MultipartIdentifierContext
|----------ErrorCapturingIdentifierContext
|-----------IdentifierContext
|------------UnquotedIdentifierContext
|-------------NonReservedContext
|--------------TerminalNodeImpl[table]
|-----------RealIdentContext
|---------TableAliasContext
|------WhereClauseContext
|-------TerminalNodeImpl[WHERE]
|-------PredicatedContext
|--------ValueExpressionDefaultContext
|---------ColumnReferenceContext
|----------IdentifierContext
|-----------UnquotedIdentifierContext
|------------NonReservedContext
|-------------TerminalNodeImpl[column]
|--------PredicateContext
|---------TerminalNodeImpl[LIKE]
|---------ValueExpressionDefaultContext
|----------ConstantDefaultContext
|-----------StringLiteralContext
|------------TerminalNodeImpl["%Python%"]
|---QueryOrganizationContext
|-TerminalNodeImpl[<EOF>]
```

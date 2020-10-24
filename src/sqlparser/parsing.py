from sqlparser.stringparser import string_to_ast


def parse_sql(string, rule, converter, debug=False):
    tree = string_to_ast(string, rule, debug=debug)
    return converter(tree) if converter else tree


def parse_statement(string, converter=None, debug=False):
    return parse_sql(string, 'singleStatement', converter, debug)


def parse_expression(string, converter=None, debug=False):
    return parse_sql(string, 'singleExpression', converter, debug)


def parse_table_identifier(string, converter=None, debug=False):
    return parse_sql(string, 'singleTableIdentifier', converter, debug)


def parse_multipart_identifier(string, converter=None, debug=False):
    return parse_sql(string, 'singleMultipartIdentifier', converter, debug)


def parse_function_identifier(string, converter=None, debug=False):
    return parse_sql(string, 'singleFunctionIdentifier', converter, debug)


def parse_data_type(string, converter=None, debug=False):
    return parse_sql(string, 'singleDataType', converter, debug)


def parse_table_schema(string, converter=None, debug=False):
    return parse_sql(string, 'singleTableSchema', converter, debug)

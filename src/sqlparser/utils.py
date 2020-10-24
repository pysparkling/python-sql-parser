def print_tree(tree, printer=print):
    for line in tree_to_strings(tree, indent=0):
        printer(line)


def tree_to_strings(tree, indent=0):
    node_as_string = type(tree).__name__ + (("[" + tree.symbol.text + "]") if hasattr(tree, "symbol") else "")
    result = ["|" + "-" * indent + node_as_string]
    if hasattr(tree, 'children') and tree.children:
        for c in tree.children:
            result += tree_to_strings(c, indent + 1)
    return result

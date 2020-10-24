def print_tree(tree):
    print(type(tree).__name__)
    print_sub_tree(tree, indent=0)


def print_sub_tree(tree, indent=0):
    for c in tree.children:
        print(
            "|" + "-" * indent,
            type(c).__name__,
            ("[" + c.symbol.text + "]") if hasattr(c, "symbol") else ""
        )
        if hasattr(c, 'children') and c.children:
            print_sub_tree(c, indent + 2)

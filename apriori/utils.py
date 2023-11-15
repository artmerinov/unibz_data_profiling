class TreeNode:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.left = None
        self.right = None

def build_binary_tree(mapping):
    root = TreeNode(name='root', code=None)

    for item_name, item_code in mapping.items():
        current = root

        for ch in item_code:
            if ch == '0':
                if not current.left:
                    current.left = TreeNode(None, None)
                current = current.left
            elif ch == '1':
                if not current.right:
                    current.right = TreeNode(None, None)
                current = current.right

        current.name = item_name
        current.code = item_code

    return root

def print_tree(root, level=0, prefix="Root: "):
    if root:
        name_str = root.name if root.name is not None else "None"
        code_str = root.code if root.code is not None else "None"
        print(" " * (level * 4) + prefix + f"{name_str} ({code_str})")
        if root.left or root.right:
            print_tree(root.left, level + 1, "L --- ")
            print_tree(root.right, level + 1, "R --- ")
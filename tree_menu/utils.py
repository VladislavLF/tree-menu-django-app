def build_menu_tree(items):
    tree = {}
    children = {}

    for item in items:
        item.children_list = []
        children.setdefault(item.parent_id, []).append(item)

    def attach_children(parent):
        for child in children.get(parent.id, []):
            parent.children_list.append(child)
            attach_children(child)

    for item in items:
        if item.parent_id is None:
            tree[item.id] = item
            attach_children(item)

    return tree

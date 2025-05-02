# VALIDATION

from btree import BTree
import random


def inorder_traversal(node):
    """Return a flat list of keys from an in-order traversal of this node."""
    result = []
    # For each key, first traverse its left child (if any), then the key itself
    for i, key in enumerate(node.keys):
        if node.children:
            result.extend(inorder_traversal(node.children[i]))
        result.append(key)
    # Finally, traverse the rightmost child
    if node.children:
        result.extend(inorder_traversal(node.children[-1]))
    return result


def valid_key_count(node):
    bad_node = None
    if len(node.keys) < (node.order - 1) // 2 or len(node.keys) > node.order - 1:
        bad_node = node.keys

    for i, key in enumerate(node.keys):
        if node.children:
            bad_node = valid_key_count(node.children[i])
            if bad_node:
                return bad_node
    if node.children:
        bad_node = valid_key_count(node.children[-1])
    return bad_node


def equal_trees(node1, node2):
    """Check if two B-trees are equal."""
    if len(node1.keys) != len(node2.keys):
        return False
    if node1.keys != node2.keys:
        return False
    if len(node1.children) != len(node2.children):
        return False
    for child1, child2 in zip(node1.children, node2.children):
        if not equal_trees(child1, child2):
            return False
    return True


def validate_btree(bt: BTree[int], insert_log: list[int]):
    # 1) Existence
    missing = [x for x in insert_log if not bt.exists(x)]
    if missing:
        print(
            f"ERROR: {len(missing)} values not found in tree! Sample missing: {missing[:10]}"
        )
    else:
        print("✓ All inserted values exist in the B-tree.")
    # 1.5) Non-Existence
    not_inserted = [
        x
        for x in "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5))
        if x not in insert_log
    ]
    # not_inserted = [x for x in random.sample(range(1, 10001), 100) if x not in insert_log]
    false_positives = [x for x in not_inserted if bt.exists(x)]
    if false_positives:
        print(
            f"ERROR: {len(false_positives)} values incorrectly found in tree! Sample: {false_positives[:10]}"
        )
    else:
        print("✓ All non-inserted values correctly not found in the B-tree.")

    # 2) Valid # of keys in each node
    bad_node = valid_key_count(bt.root)
    if bad_node:
        print(f"ERROR: Node {bad_node} has invalid number of keys.")
    else:
        print("✓ All nodes have valid number of keys.")

    # 3) Orderring
    tree_keys = inorder_traversal(bt.root)
    expected = sorted(set(insert_log))
    if tree_keys != expected:
        print("ERROR: In-order traversal does not match sorted insert set.")
        # Find first mismatch
        for i, (a, b) in enumerate(zip(tree_keys, expected)):
            if a != b:
                print(f"  At index {i}: tree has {a}, expected {b}")
                break
        # If one list is longer
        if len(tree_keys) != len(expected):
            print(
                f"  Lengths differ: tree={len(tree_keys)} vs expected={len(expected)}"
            )
    else:
        print("✓ In-order traversal matches sorted insert set.")

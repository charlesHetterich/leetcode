from typing import Generic, TypeVar, List, Optional
from sortedcontainers import SortedList, SortedKeyList

"""
# Notes

## Order t B-tree
B is "branching factor" or "order". Meant for large volumes of data (SQL databases, etc.)

- ordered tree (always know what direction to go down tree to search for a value)
- b-tree node often same size as disk page or block
- root node always stays in primary memory (RAM)

- The root has up to 2t keys & up to 2t + 1 children
- All other nodes have between t and 2t keys. Non-leaf nodes with k keys have k + 1 children
- Balanced: all leaves are at the same height

### Runtime

"""

K = TypeVar('T')

class BTreeNode(Generic[K]):
    def __init__(self, order: int, keys: List[K] = []):
        self.order = order
        self.keys = SortedList(keys)
        self.children: list[BTreeNode[K]] = []

    def self_insert(self, key: K) -> tuple[K, 'BTreeNode[K]'] | tuple[None, None]:
        self.keys.add(key)
        if len(self.keys) > self.order - 1:
            mid_index = len(self.keys) // 2
            mid_key = self.keys.pop(mid_index)
            
            # split keys
            rhs_node = BTreeNode[K](self.order, self.keys[mid_index:])
            self.keys = SortedList(self.keys[:mid_index])

            # split children
            if len(self.children) > 0:
                rhs_node.children = self.children[mid_index + 1:]
                self.children = self.children[:mid_index + 1]

            return mid_key, rhs_node
        return None, None

    def insert(self, key: K) -> tuple[K, 'BTreeNode[K]'] | tuple[None, None]:
        """Insert a key into node. If full, remove & return middle key"""
        # Index of interest
        idx = self.keys.bisect_left(key)

        # If key exists here, do nothing
        if idx < len(self.keys) and self.keys[idx] == key:
            return None, None

        # If leaf node, insert here
        if len(self.children) == 0:
            return self.self_insert(key)
        
        # recurse to child & capture potential middle key
        middle_key, new_rhs_child = self.children[idx].insert(key)
        if middle_key is not None:
            self.children.insert(idx + 1, new_rhs_child)
            return self.self_insert(middle_key)
        return None, None

    def delete(self, key: K) -> bool:
        """Delete a key from node"""
        pass

    def exists(self, key: K) -> bool:
        """Check if key exists in node"""
        idx = self.keys.bisect_left(key)
        if idx < len(self.keys) and self.keys[idx] == key:
            return True
        if len(self.children) == 0:
            return False
        return self.children[idx].exists(key)


class BTree(Generic[K]):
    def __init__(self, order: int):
        self.root = BTreeNode[K](order)
        self.order = order

    def insert(self, key: K):
        middle_key, new_rhs = self.root.insert(key)
        if middle_key is not None:
            # root was full, so we need to create a new root
            new_root = BTreeNode[K](self.order)
            new_root.self_insert(middle_key)
            new_root.children = [self.root, new_rhs]
            self.root = new_root


    def exists(self, key: K) -> bool:
        return self.root.exists(key)

    def delete(self, key: K) -> Optional[K]:
        pass

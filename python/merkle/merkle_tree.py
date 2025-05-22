"""
# Notes
Notes on Merkle structures as well as Substrate storage in general

> Substrate uses a base-16, (patricia) radix merkle tree.


- Substrate uses a key-value database to store **trie nodes** (trie nodes or radix-tree nodes ?)
    - And I assume this is where real, concrete data lives as well?
    - The path of the trie is given by the literal key (e.g. "alice_balance", "system_block", "system_era")
        - In the notes/visualization only strings "a-z+{_}" are used. But I know that we can use arbitrary data as keys in substrate. How does this work ?
        - My naive guess is that the trie path, in reality, is given by the *SCALE encoded* key perhaps?
> Instead of alphabet, we use the base-16 representation of everything.
        - Okay yep so keys can be arbitrary data and the trie path is given by the data encoded to hex
        - ***which is why each node has 16 children. Yes yes the # of children per node in a trie is given directly by the # of possible characters for a key***

    - key to a trie node is given by its hash (its hash being *influenced* by that node itself as well as all of its children (the children's hashes that is) recursively)
    - from [this example](https://polkadot-blockchain-academy.github.io/pba-content/current/syllabus/4a-Protocol_On-Chain/Substrate/3-Merklized-Storage-slides.html#/14) my guess is that this is NOT any kind of scale encoding— it is just the raw BE hex/nibbles/4-bits of the data.

#### Resources
    - [FRAME Storage](https://polkadot-blockchain-academy.github.io/pba-content/current/syllabus/4a-Protocol_On-Chain/FRAME/2-FRAME_Basics/FRAME_Storage-slides.html#/)
    - [Merklized Storage Slides PBA6](https://polkadot-blockchain-academy.github.io/pba-content/current/syllabus/4a-Protocol_On-Chain/Substrate/3-Merklized-Storage-slides.html#/)
    - [DB & Merklized Storage | *more detailed*](https://polkadot-blockchain-academy.github.io/pba-content/cambridge-2022/syllabus/4-Substrate/4.5-Db_and_Merklized_Storage/4.5-Db_and_Merklized_Storage_Slides.html#/)
    - [Latest YT Lecture](https://www.youtube.com/watch?v=gNRaHA47PEc&t=4898s)
    - [Radix Tree Visualization Tool](https://www.cs.usfca.edu/~galles/visualization/RadixTree.html)
"""

import hashlib
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any


EncodablePrim = str | bytes | bytearray | int | float | bool
Encodable = EncodablePrim | list[EncodablePrim] | tuple[EncodablePrim, ...]


def encode(key: Encodable) -> bytes:
    """Encode a key to bytes."""
    if isinstance(key, str):
        return key.encode("utf-8")
    elif isinstance(key, (bytes, bytearray)):
        return key
    elif isinstance(key, bool):
        return b"1" if key else b"0"
    elif isinstance(key, (int, float)):
        return str(key).encode("utf-8")
    elif isinstance(key, list):
        return b"".join(encode(k) for k in key)
    elif isinstance(key, tuple):
        return b"".join(encode(k) for k in key)
    else:
        raise TypeError(f"Unsupported key type: {type(key)}")


def hash(data: Encodable) -> hashlib.blake2b:
    return hashlib.blake2b(encode(data))


class TrieBase(Enum):
    BASE16 = 16
    BASE4 = 4
    BASE2 = 2


def key_from_bytes(bytes: bytes, base: TrieBase = TrieBase.BASE16) -> str:
    """Convert a byte key to a string key."""
    if base == TrieBase.BASE16:
        return bytes.hex()
    elif base == TrieBase.BASE4:
        return "".join([f"{b >> i & 0b11}" for b in bytes for i in range(6, -1, -2)])
    elif base == TrieBase.BASE2:
        return "".join(bin(b)[2:].zfill(8) for b in bytes)
    else:
        raise ValueError(f"Unsupported base: {base}")


@dataclass
class MerkleNode:
    """
    Represents a node in a Merkle tree.

    Attributes:
        children (dict[str, hashlib.blake2b]): A dictionary where keys are patricia trie paths given as
                                               partial keys, and values are the hashes of the child nodes,
                                               which give the keys in a KVDB.
        value (Optional[bytes]): The value stored in the node, if any.

    Assumptions:
        - All keys in `children` have at lest one character
    """

    children: dict[str, hashlib.blake2b] = {}
    value: Optional[Any] = None

    def hash(self) -> hashlib.blake2b:
        """Hash of [header, key, children, value]"""
        pass
        # return hashlib.blake2b((self.partial_key, self.child_hashes, self.value))


def best_prefix(s1, s2):
    """Find the longest common prefix of two strings"""
    prefix = []
    for c1, c2 in zip(s1, s2):
        if c1 == c2:
            prefix.append(c1)
        else:
            break
    return "".join(prefix)


class MerklizedStorage:
    """
    Provable Key-value DB queried with Patricia Trie Merkle based algorithm
    """

    def __init__(self, base: TrieBase = TrieBase.BASE16):
        """Initialize storage with root"""
        self.base = base
        self.KVDB: dict[hashlib.blake2b, MerkleNode] = {}
        root = MerkleNode()
        self.root_hash = root.hash()
        self.KVDB[self.root_hash] = root

    def pth_from_key(self, key: Encodable) -> str:
        """Convert a key to a Patricia Trie path."""
        return key_from_bytes(encode(key), self.base)

    def read(self, db_key: hashlib.blake2b) -> Optional[MerkleNode]:
        """Read a node from the database given its hash"""
        return self.KVDB.get(db_key)

    def write(
        self, node: MerkleNode, old_db_key: Optional[hashlib.blake2b] = None
    ) -> hashlib.blake2b:
        """Write a node to the database given its hash"""
        if old_db_key:
            del self.KVDB[old_db_key]
        new_hash = node.hash()
        self.KVDB[new_hash] = node
        return new_hash

    def get_node(self, key: Encodable) -> Optional[MerkleNode]:
        """Get the value for a given key"""
        pth = self.pth_from_key(key)

        # Start traversal at root node (expect root to exist)
        node = self.read(self.root_hash)
        while pth:
            # Select next child
            next_node = None
            for partial_key, child_hash in node.children.items():
                if pth[0] == partial_key[0]:
                    if pth.startswith(partial_key):
                        next_node = self.read(child_hash)
                        pth = pth[len(partial_key) :]
                    break

            # If we're here, that means we expected to traverse deeper but failed.
            # Ignore current `node` & return `None`
            if not next_node:
                return None
            node = next_node

        # If we reach here, we have found the node we expected
        return node

    def get(self, key: Encodable):
        """Get the value for a given key"""
        node = self.get_node(key)
        if node:
            return node.value
        return None

    def set(self, key: Encodable, value):
        """
        Insert or update KVDB entry with new data given its key, and re-hash all nodes along the trie path
        """
        pth = self.pth_from_key(key)

        edge, node = "", self.read(self.root_hash)
        node_stack: list[tuple[str, MerkleNode]] = []
        uedge, uhash = None, None
        while not uedge:
            node_stack.append((edge, node))
            # Select next child
            for partial_key, child_hash in node.children.items():
                # Found child path. Stop loop here.
                if pth[0] == partial_key[0]:
                    # Compare prefixes
                    pfx = best_prefix(pth, partial_key)
                    pth = pth[len(pfx) :]

                    # Continue traversal
                    if pth and len(pfx) == len(partial_key):
                        # Found child node. Continue traversal
                        edge = partial_key
                        node = self.read(child_hash)

                    # Split current node
                    elif pth and len(pfx) < len(partial_key):
                        pass

                    # Exact match— overwrite value
                    elif not pth and len(pfx) == len(partial_key):
                        # Found node. Update value
                        node.value = value
                        uedge = key
                        uhash = self.write(node, child_hash)
                    break
            # Add new leaf to current node
            else:
                node.children[pth] = hash(value)
                node.value = value
                uedge = key
                uhash = self.write(node, child_hash)
                break

        # Update hashes up the stack

    def delete(self, key: Encodable) -> None:
        """
        Delete value from KVDB given its key, and re-hash all nodes along the merkle path
        """
        pth = self.pth_from_key(key)
        node_stack = []

    def prove(self, key: Encodable, value: bytes) -> bool:
        t_pth = self.pth_from_key(key)
        pass

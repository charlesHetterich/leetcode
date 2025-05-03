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
from typing import Optional


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
    key: str
    child_hashes: list[hashlib.blake2b]
    value: Optional[bytes] = None

    def hash(self) -> hashlib.blake2b:
        return hashlib.blake2b((self.key, self.child_hashes, self.value))


class MerklizedStorage:
    """Provable Key-value DB queried with merkle structure"""

    def __init__(self, base: TrieBase = TrieBase.BASE16):
        self.KVDB: dict[str, MerkleNode] = {}

    def get(self, key: Encodable) -> Optional[bytes]:
        """Get the value for a given key."""
        encoded_key = encode(key)
        return self.KVDB.get(encoded_key.hex(), None)

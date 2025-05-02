"""
# Notes
SCALE *(Simple Concatinated Aggregate Little-Endian)* is a serialization format used in Substrate.


- Little Endian: *a byte order where the least significant byte of a multi-byte value is stored at the lowest memory address*
    - within one BYTE:   MOST  significant BIT  first, LEAST significant BIT  last
    - across MULTI-BYTE: LEAST significant BYTE first, MOST  significant BYTE last

example: 39884979
  HEX                --> 0x26098B3
  OCTET              --> [02 60 98 B3] # 4 BYTES
  LITTLE ENDIAN      --> [B3 98 60 02]
                          B    3    9    8    6    0    0    2
  LITTLE ENDIAN BITS --> [1011 0011 1001 1000 0110 0000 0000 0010] # 32 BITS



#### Resources
- [Latest YT SCALE lecture](https://www.youtube.com/watch?v=6N6BopyYKq4)
- [Polkadot Data Encoding Docs](https://docs.polkadot.com/polkadot-protocol/basics/data-encoding/#scale-codec-libraries)
- [Rust Codec (main implementation)](https://github.com/paritytech/parity-scale-codec)
- [Python SCALE Codec](https://github.com/JAMdotTech/py-scale-codec)
- [Shawn's Substrate Utils](https://www.shawntabrizi.com/substrate-js-utilities/)
"""

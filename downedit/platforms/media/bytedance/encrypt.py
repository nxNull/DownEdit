import urllib
import math
import time
import random
from urllib.parse import urlparse

__all__ = ['Kb', "SM3"]


IV = [
    0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
    0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e
]
T = [0x79cc4519, 0x7a879d8a]


def _rotl(x: int, n: int) -> int:
    """
    Left rotate a 32-bit integer x by n bits.
    """
    n %= 32
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def _ff(j: int, x: int, y: int, z: int) -> int:
    """
    Boolean function FF_j(X, Y, Z) for SM3.
    """
    if 0 <= j < 16:
        return (x ^ y ^ z) & 0xFFFFFFFF
    elif 16 <= j < 64:
        return ((x & y) | (x & z) | (y & z)) & 0xFFFFFFFF
    else:
        raise ValueError("Invalid j for bool function FF")


def _gg(j: int, x: int, y: int, z: int) -> int:
    """
    Boolean function GG_j(X, Y, Z) for SM3.
    """
    if 0 <= j < 16:
        return (x ^ y ^ z) & 0xFFFFFFFF
    elif 16 <= j < 64:
        return ((x & y) | (~x & 0xFFFFFFFF & z)) & 0xFFFFFFFF
    else:
        raise ValueError("Invalid j for bool function GG")


def _p0(x: int) -> int:
    """
    Permutation function P_0(X) for SM3.
    """
    return (x ^ _rotl(x, 9) ^ _rotl(x, 17)) & 0xFFFFFFFF


def _p1(x: int) -> int:
    """
    Permutation function P_1(X) for SM3.
    """
    return (x ^ _rotl(x, 15) ^ _rotl(x, 23)) & 0xFFFFFFFF


class SM3:
    """
    Implementation of the SM3 cryptographic hash function.
    """
    reg: list[int]
    chunk: bytearray
    size: int

    def __init__(self):
        self.reg = [0] * 8
        self.chunk = bytearray()
        self.size = 0
        self.reset()

    def reset(self):
        """
        Resets the hash state to its initial values.
        """
        self.reg = list(IV)
        self.chunk = bytearray()
        self.size = 0

    def _string_to_bytes(self, s: str) -> bytes:
        """
        Encodes a string to bytes using UTF-8.
        Note: The original JS used a specific combination of encodeURIComponent
        and decoding hex escapes, which is unusual. This Python version uses
        standard UTF-8 encoding, which is the common practice. If exact byte-for-byte
        compatibility with the JS function is needed, its logic must be precisely replicated.
        """
        return s.encode('utf-8')

    def write(self, e: str | bytes | bytearray | list[int]):
        """
        Updates the hash state with the input data.

        Args:
            e: The input data (string, bytes, bytearray, or list of ints).
            Strings will be UTF-8 encoded.
        """
        if isinstance(e, str):
            a = self._string_to_bytes(e)
        elif isinstance(e, list):

            a = bytes(x & 0xFF for x in e)
        elif isinstance(e, bytearray):
            a = bytes(e)
        elif isinstance(e, bytes):
            a = e
        else:
            raise TypeError(
                "Input must be str, bytes, bytearray, or list[int]")

        self.size += len(a)
        a_idx = 0

        fill_needed = 64 - len(self.chunk)
        if fill_needed > 0:
            can_fill = min(fill_needed, len(a))
            self.chunk.extend(a[:can_fill])
            a_idx += can_fill

        if len(self.chunk) == 64:
            self._compress(bytes(self.chunk))
            self.chunk = bytearray()

        while a_idx + 64 <= len(a):
            block = a[a_idx: a_idx + 64]
            self._compress(block)
            a_idx += 64

        if a_idx < len(a):
            self.chunk.extend(a[a_idx:])

    def _compress(self, block: bytes):
        """
        Processes a 64-byte block.
        """
        if len(block) != 64:
            raise ValueError("Compress error: Block must be 64 bytes")

        W = [0] * 68
        W_prime = [0] * 64

        for i in range(16):
            W[i] = int.from_bytes(block[i*4:i*4+4], 'big')

        for j in range(16, 68):
            term1 = _p1(W[j - 16] ^ W[j - 9] ^ _rotl(W[j - 3], 15))
            term2 = _rotl(W[j - 13], 7)
            W[j] = (term1 ^ term2 ^ W[j - 6]) & 0xFFFFFFFF

        for j in range(64):
            W_prime[j] = (W[j] ^ W[j + 4]) & 0xFFFFFFFF

        A, B, C, D, E, F, G, H = self.reg

        for j in range(64):
            Tj = T[0] if 0 <= j < 16 else T[1]
            SS1 = _rotl((_rotl(A, 12) + E + _rotl(Tj, j)) & 0xFFFFFFFF, 7)
            SS2 = (SS1 ^ _rotl(A, 12)) & 0xFFFFFFFF
            TT1 = (_ff(j, A, B, C) + D + SS2 + W_prime[j]) & 0xFFFFFFFF
            TT2 = (_gg(j, E, F, G) + H + SS1 + W[j]) & 0xFFFFFFFF
            D = C
            C = _rotl(B, 9)
            B = A
            A = TT1
            H = G
            G = _rotl(F, 19)
            F = E
            E = _p0(TT2)

            A &= 0xFFFFFFFF
            B &= 0xFFFFFFFF
            C &= 0xFFFFFFFF
            D &= 0xFFFFFFFF
            E &= 0xFFFFFFFF
            F &= 0xFFFFFFFF
            G &= 0xFFFFFFFF
            H &= 0xFFFFFFFF

        self.reg[0] = (self.reg[0] ^ A) & 0xFFFFFFFF
        self.reg[1] = (self.reg[1] ^ B) & 0xFFFFFFFF
        self.reg[2] = (self.reg[2] ^ C) & 0xFFFFFFFF
        self.reg[3] = (self.reg[3] ^ D) & 0xFFFFFFFF
        self.reg[4] = (self.reg[4] ^ E) & 0xFFFFFFFF
        self.reg[5] = (self.reg[5] ^ F) & 0xFFFFFFFF
        self.reg[6] = (self.reg[6] ^ G) & 0xFFFFFFFF
        self.reg[7] = (self.reg[7] ^ H) & 0xFFFFFFFF

    def _fill(self):
        """
        Pads the message according to SM3 standard.
        """
        msg_len_bits = self.size * 8
        self.chunk.append(0x80)

        current_len_mod_64 = len(self.chunk) % 64
        padding_zeros = (56 - current_len_mod_64 + 64) % 64
        self.chunk.extend([0] * padding_zeros)

        self.chunk.extend(msg_len_bits.to_bytes(8, 'big'))

    def sum(self, e: str | bytes | bytearray | list[int] | None = None, t: str = 'hex') -> str | list[int]:
        """
        Calculates the SM3 hash.

        Args:
            e: Optional input data to hash directly. If provided, the state is reset first.
            t: Output format ('hex' for hex string, 'bytes' for list of byte integers).

        Returns:
            The SM3 hash digest in the specified format.
        """
        if e is not None:
            self.reset()
            self.write(e)

        self._fill()

        chunk_view = memoryview(self.chunk)
        for i in range(0, len(chunk_view), 64):
            self._compress(bytes(chunk_view[i:i+64]))

        if t == 'hex':
            result = "".join(f"{reg_val:08x}" for reg_val in self.reg)
        elif t == 'bytes':
            result_bytes = bytearray(32)
            for i in range(8):
                result_bytes[i*4: i*4+4] = self.reg[i].to_bytes(4, 'big')
            result = list(result_bytes)
        else:
            raise ValueError(
                "Unsupported output format: choose 'hex' or 'bytes'")

        self.reset()
        return result


class Kb:
    @staticmethod
    def encode(data: bytes) -> str:
        hex_chars = "0123456789abcdef"
        result = ""
        for b in data:
            result += hex_chars[(b >> 4) & 15] + hex_chars[b & 15]
        return result

    @staticmethod
    def decode(hex_str: str) -> bytearray:
        """
        Convert a hexadecimal string to a bytearray.

        Args:
            hex_str (str): The hexadecimal string to convert.

        Returns:
            bytearray: The resulting bytearray from the conversion.
        """
        lookup = {
            **{str(i): i for i in range(10)},
            **{chr(87 + i): i for i in range(10, 16)}
        }

        length = len(hex_str) >> 1
        result = bytearray(length)

        i = 0
        for j in range(0, len(hex_str), 2):
            result[i] = (lookup[hex_str[j]] << 4) | lookup[hex_str[j + 1]]
            i += 1

        return result

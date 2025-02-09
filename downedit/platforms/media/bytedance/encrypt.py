import binascii
from math import ceil
import random
from typing import List, Union

__all__ = ['Hash']

IV = [
    0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
    0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E,
]

T_J = [
    0x79cc4519, 0x7a879d8a
]

def _rotl(x: int, n: int) -> int:
    """
    Rotate x left by n bits.
    """
    return ((x << n) & 0xFFFFFFFF) | ((x >> (32 - n)) & 0xFFFFFFFF)


def _sm3_ff_j(x: int, y: int, z: int, j: int) -> int:
    """
    SM3 function FFj.
    """
    if 0 <= j < 16:
        return x ^ y ^ z
    elif 16 <= j < 64:
        return (x & y) | (x & z) | (y & z)
    raise ValueError("j must be between 0 and 63")


def _sm3_gg_j(x: int, y: int, z: int, j: int) -> int:
    """
    SM3 function GGj.
    """
    if 0 <= j < 16:
        return x ^ y ^ z
    elif 16 <= j < 64:
        return (x & y) | (~x & z)
    raise ValueError("j must be between 0 and 63")


def _sm3_p_0(x: int) -> int:
    """
    SM3 function P0.
    """
    return x ^ _rotl(x, 9) ^ _rotl(x, 17)


def _sm3_p_1(x: int) -> int:
    """
    SM3 function P1.
    """
    return x ^ _rotl(x, 15) ^ _rotl(x, 23)


def _sm3_cf(v_i: list[int], b_i: list[int]) -> list[int]:
    """
    SM3 compression function.
    """

    w = []
    for i in range(0, 16):
        w.append(int.from_bytes(bytes(b_i[i*4:(i+1)*4]), byteorder='big'))

    for j in range(16, 68):
        w.append(_sm3_p_1(w[j - 16] ^ w[j - 9] ^ _rotl(w[j - 3], 15)) ^ _rotl(w[j - 13], 7) ^ w[j - 6])

    w_prime = [w[i] ^ w[i + 4] for i in range(64)]

    a, b, c, d, e, f, g, h = v_i

    for j in range(64):
        ss1 = _rotl((_rotl(a, 12) + e + _rotl(T_J[j // 16], j)) & 0xFFFFFFFF, 7)
        ss2 = ss1 ^ _rotl(a, 12)
        tt1 = (_sm3_ff_j(a, b, c, j) + d + ss2 + w_prime[j]) & 0xFFFFFFFF
        tt2 = (_sm3_gg_j(e, f, g, j) + h + ss1 + w[j]) & 0xFFFFFFFF
        d = c
        c = _rotl(b, 9)
        b = a
        a = tt1
        h = g
        g = _rotl(f, 19)
        f = e
        e = _sm3_p_0(tt2)

    v_j = [a, b, c, d, e, f, g, h]
    return [(v_j[i] ^ v_i[i]) & 0xFFFFFFFF for i in range(8)]


def _sm3_hash(msg: bytes) -> str:
    """
    SM3 hashing function.
    """
    msg_len = len(msg)
    msg_bits = msg_len * 8

    padded_msg = list(msg)
    padded_msg.append(0x80)
    pad_len = (64 - (msg_len + 1) % 64) % 64
    padded_msg.extend([0] * pad_len)
    padded_msg.extend((msg_bits).to_bytes(8, byteorder='big'))

    blocks = [padded_msg[i:i+64] for i in range(0, len(padded_msg), 64)]

    v = IV[:]
    for block in blocks:
        v = _sm3_cf(v, block)

    return ''.join(f"{x:08x}" for x in v)


def sm3_kdf(z: str, klen: int) -> str:
    """
    SM3 Key Derivation Function (KDF).
    """
    klen = int(klen)
    ct = 1
    rcnt = ceil(klen / 32)
    zin = list(binascii.a2b_hex(z))

    hash_output = ""
    for i in range(rcnt):
        msg = zin + list(ct.to_bytes(4, byteorder='big'))
        hash_output += _sm3_hash(bytes(msg))
        ct += 1
    return hash_output[:klen * 2]

class Hash:
    """
    A utility class for cryptographic operations.
    """

    @staticmethod
    def bytes_to_list(data: bytes) -> list[int]:
        """
        Converts a bytes object to a list of integers.
        """
        return list(data)

    @staticmethod
    def sm3_hash(msg: bytes) -> str:
        """
        Computes the SM3 hash of the input bytes.
        """
        return _sm3_hash(msg)

    @staticmethod
    def sm3_to_array(data: str | list) -> list[int]:
        """
        Converts an SM3 hash string to a list of integers.
        """
        if isinstance(data, str):b = data.encode("utf-8")
        else: b = bytes(data)

        h = Hash.sm3_hash(Hash.bytes_to_list(b))

        return [int(h[i: i + 2], 16) for i in range(0, len(h), 2)]

    @staticmethod
    def to_ord_str(s: str) -> str:
        """
        Convert a string to an ASCII code string.

        Args:
            s (str): Input string.

        Returns:
            str: Converted ASCII code string.
        """
        return "".join([chr(i) for i in s])

    @staticmethod
    def to_ord_array(s: str) -> List[int]:
        """
        Convert a string to a list of ASCII codes.

        Args:
            s (str): Input string.

        Returns:
            List[int]: Converted list of ASCII codes.
        """
        return [ord(char) for char in s]

    @staticmethod
    def to_char_str(s: str) -> str:
        """
        Convert a list of ASCII codes to a string.

        Args:
            s (str): List of ASCII codes.

        Returns:
            str: Converted string.
        """
        return "".join([chr(i) for i in s])

    @staticmethod
    def to_char_array(s: str) -> List[int]:
        """
        Convert a string to a list of ASCII codes.

        Args:
            s (str): Input string.

        Returns:
            List[int]: Converted list of ASCII codes.
        """
        return [ord(char) for char in s]

    @staticmethod
    def js_shift_right(val: int, n: int) -> int:
        """
        Implement the unsigned right shift operation in JavaScript.

        Args:
            val (int): Input value.
            n (int): Number of bits to shift right.

        Returns:
            int: Value after right shift.
        """
        return (val % 0x100000000) >> n

    @staticmethod
    def generate_random_bytes(length: int = 3) -> str:
        """
        Generate a pseudo-random byte string to obfuscate the data.

        Args:
            length (int): Length of the byte sequence to generate.

        Returns:
            str: pseudo-random byte string.
        """

        def generate_byte_sequence() -> List[str]:
            _rd = int(random.random() * 10000)
            return [
                chr(((_rd & 255) & 170) | 1),
                chr(((_rd & 255) & 85) | 2),
                chr((Hash.js_shift_right(_rd, 8) & 170) | 5),
                chr((Hash.js_shift_right(_rd, 8) & 85) | 40),
            ]

        result = []
        for _ in range(length):
            result.extend(generate_byte_sequence())

        return "".join(result)

class Crypto:
    """
    The CryptoUtility class provides utility methods for encryption and encoding, including SM3 hashing, adding salt, Base64 encoding, and RC4 encryption.
    """

    def __init__(self, salt: str, custom_base64_alphabet: List[str]):
        """
        Initialize the CryptoUtility class.

        Args:
            salt (str): Encryption salt).
            custom_base64_alphabet (List[str]): Custom Base64 alphabet.
        """
        self.salt = salt
        self.base64_alphabet = custom_base64_alphabet

        self.big_array = [
            121, 243,  55, 234, 103,  36,  47, 228,  30, 231, 106,   6, 115,  95,  78, 101, 250, 207, 198,  50,
            139, 227, 220, 105,  97, 143,  34,  28, 194, 215,  18, 100, 159, 160,  43,   8, 169, 217, 180, 120,
            247,  45,  90,  11,  27, 197,  46,   3,  84,  72,   5,  68,  62,  56, 221,  75, 144,  79,  73, 161,
            178,  81,  64, 187, 134, 117, 186, 118,  16, 241, 130,  71,  89, 147, 122, 129,  65,  40,  88, 150,
            110, 219, 199, 255, 181, 254,  48,   4, 195, 248, 208,  32, 116, 167,  69, 201,  17, 124, 125, 104,
             96,  83,  80, 127, 236, 108, 154, 126, 204,  15,  20, 135, 112, 158,  13,   1, 188, 164, 210, 237,
            222,  98, 212,  77, 253,  42, 170, 202,  26,  22,  29, 182, 251,  10, 173, 152,  58, 138,  54, 141,
            185,  33, 157,  31, 252, 132, 233, 235, 102, 196, 191, 223, 240, 148,  39, 123,  92,  82, 128, 109,
             57,  24,  38, 113, 209, 245,   2, 119, 153, 229, 189, 214, 230, 174, 232,  63,  52, 205,  86, 140,
             66, 175, 111, 171, 246, 133, 238, 193,  99,  60,  74,  91, 225,  51,  76,  37, 145, 211, 166, 151,
            213, 206,   0, 200, 244, 176, 218,  44, 184, 172,  49, 216,  93, 168,  53,  21, 183,  41,  67,  85,
            224, 155, 226, 242,  87, 177, 146,  70, 190,  12, 162,  19, 137, 114,  25, 165, 163, 192,  23,  59,
              9,  94, 179, 107,  35,   7, 142, 131, 239, 203, 149, 136,  61, 249,  14, 156
        ]

    @staticmethod
    def sm3_to_array(input_data: Union[str, List[int]]) -> List[int]:
        """
        Calculate the SM3 hash value of the request body and convert the result to an array of integers.

        Args:
            input_data (Union[str, List[int]]): Input data.

        Returns:
            List[int]: Array of integers representing the hash value.
        """
        if isinstance(input_data, str):
            input_data_bytes = input_data.encode("utf-8")
        else:
            input_data_bytes = bytes(input_data)

        hex_result = Hash.sm3_hash(Hash.bytes_to_list(input_data_bytes))

        return [int(hex_result[i : i + 2], 16) for i in range(0, len(hex_result), 2)]

    def add_salt(self, param: str) -> str:
        """
        Add salt to the string parameter.

        Args:
            param (str): Input string.

        Returns:
            str: String with added salt.
        """
        return param + self.salt

    def process_param(
        self, param: Union[str, List[int]], add_salt: bool
    ) -> Union[str, List[int]]:
        """
        Process input parameter and add salt if needed.

        Args:
            param (Union[str, List[int]]): Input parameter.
            add_salt (bool): Whether to add salt.

        Returns:
            Union[str, List[int]]: Processed parameter.
        """
        if isinstance(param, str) and add_salt:
            param = self.add_salt(param)
        return param

    def params_to_array(
        self, param: Union[str, List[int]], add_salt: bool = True
    ) -> List[int]:
        """
        Get the hash array of the input parameter.

        Args:
            param (Union[str, List[int]]): Input parameter.
            add_salt (bool): Whether to add salt.

        Returns:
            List[int]: Hash array.
        """
        processed_param = self.process_param(param, add_salt)
        return self.sm3_to_array(processed_param)

    def transform_bytes(self, bytes_list: List[int]) -> str:
        """
        Encrypt/decrypt the input byte list and return the processed string.

        Args:
            bytes_list (List[int]): Input byte list.

        Returns:
            str: Processed string.
        """
        bytes_str = Hash.to_char_str(bytes_list)
        result_str = []
        index_b = self.big_array[1]
        initial_value = 0

        for index, char in enumerate(bytes_str):
            if index == 0:
                initial_value = self.big_array[index_b]
                sum_initial = index_b + initial_value

                self.big_array[1] = initial_value
                self.big_array[index_b] = index_b
            else:
                sum_initial = initial_value + value_e

            char_value = ord(char)
            sum_initial %= len(self.big_array)
            value_f = self.big_array[sum_initial]
            encrypted_char = char_value ^ value_f
            result_str.append(chr(encrypted_char))

            value_e = self.big_array[(index + 2) % len(self.big_array)]
            sum_initial = (index_b + value_e) % len(self.big_array)
            initial_value = self.big_array[sum_initial]
            self.big_array[sum_initial] = self.big_array[
                (index + 2) % len(self.big_array)
            ]
            self.big_array[(index + 2) % len(self.big_array)] = initial_value
            index_b = sum_initial

        return "".join(result_str)

    def base64_encode(self, input_string: str, selected_alphabet: int = 0) -> str:
        """
        Encode the input string using a custom Base64 alphabet.

        Args:
            input_string (str): Input string.
            selected_alphabet (int): Selected custom Base64 alphabet index.

        Returns:
            str: Encoded string.
        """

        binary_string = "".join(["{:08b}".format(ord(char)) for char in input_string])

        padding_length = (6 - len(binary_string) % 6) % 6
        binary_string += "0" * padding_length

        base64_indices = [
            int(binary_string[i : i + 6], 2) for i in range(0, len(binary_string), 6)
        ]

        output_string = "".join(
            [self.base64_alphabet[selected_alphabet][index] for index in base64_indices]
        )

        output_string += "=" * (padding_length // 2)

        return output_string

    def abogus_encode(self, abogus_bytes_str: str, selected_alphabet: int) -> str:
        """
        Encode the input byte string using a custom Base64 alphabet, and add shifts and padding.

        Args:
            abogus_bytes_str (str): Input byte string.
            selected_alphabet (int): Selected custom Base64 alphabet index.

        Returns:
            str: Encoded string.
        """
        abogus = []

        for i in range(0, len(abogus_bytes_str), 3):
            if i + 2 < len(abogus_bytes_str):
                n = (
                    (ord(abogus_bytes_str[i]) << 16)
                    | (ord(abogus_bytes_str[i + 1]) << 8)
                    | ord(abogus_bytes_str[i + 2])
                )
            elif i + 1 < len(abogus_bytes_str):
                n = (ord(abogus_bytes_str[i]) << 16) | (
                    ord(abogus_bytes_str[i + 1]) << 8
                )
            else:
                n = ord(abogus_bytes_str[i]) << 16

            for j, k in zip(range(18, -1, -6), (0xFC0000, 0x03F000, 0x0FC0, 0x3F)):
                if j == 6 and i + 1 >= len(abogus_bytes_str):
                    break
                if j == 0 and i + 2 >= len(abogus_bytes_str):
                    break
                abogus.append(self.base64_alphabet[selected_alphabet][(n & k) >> j])

        abogus.append("=" * ((4 - len(abogus) % 4) % 4))
        return "".join(abogus)

    @staticmethod
    def rc4_encrypt(key: bytes, plaintext: str) -> bytes:
        """
        Encrypt data using the RC4 algorithm.

        Args:
            key (bytes): Encryption key.
            plaintext (str): Plaintext data.

        Returns:
            bytes: Encrypted data.
        """
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        i = j = 0
        ciphertext = []
        for char in plaintext:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            ciphertext.append(ord(char) ^ K)

        return bytes(ciphertext)
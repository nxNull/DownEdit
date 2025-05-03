import json
import time
import base64
import hashlib

from typing import List, Union
import urllib.parse

from downedit.platforms.media.bytedance.encrypt import Kb
from downedit.service.fingerprint import Fingerprint
from downedit.service.serialization import format_mm_version
from downedit.service.user_agents import UserAgent

__all__ = ["TikTokXBogus"]

class TikTokXBogus:
    """
    A class to generate the X-Bogus value for a given URL path.
    """
    BASE_KEY = {
        "s0": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
        "s1": "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
        "s2": "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="
    }

    def __init__(self) -> None:
        pass

    @staticmethod
    def Ab24(key: str, data: str) -> str:
        """
        RC4 encryption algorithm
        """
        s = list(range(256))
        j = 0
        result = ""

        # KSA (Key Scheduling Algorithm)
        for i in range(256):
            j = (j + s[i] + ord(key[i % len(key)])) % 256
            s[i], s[j] = s[j], s[i]

        # PRGA (Pseudo-Random Generation Algorithm)
        i = j = 0
        for char in data:
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            result += chr(ord(char) ^ s[(s[i] + s[j]) % 256] & 255)

        return result

    @staticmethod
    def VM231(text: str, base_index: str) -> str:
        base_chars = TikTokXBogus.BASE_KEY[base_index]

        result = ""
        i = 0

        while i + 3 <= len(text):
            char1 = ord(text[i]) & 0xFF
            i += 1
            char2 = ord(text[i]) & 0xFF
            i += 1
            char3 = ord(text[i]) & 0xFF
            i += 1

            triplet = (char1 << 16) | (char2 << 8) | char3

            result += base_chars[(triplet >> 18) & 0x3F]
            result += base_chars[(triplet >> 12) & 0x3F]
            result += base_chars[(triplet >> 6) & 0x3F]
            result += base_chars[triplet & 0x3F]

        if i < len(text):
            char1 = ord(text[i]) & 0xFF
            i += 1
            remaining = (char1 << 16) | ((ord(text[i]) & 0xFF << 8) if i < len(text) else 0)

            result += base_chars[(remaining >> 18) & 0x3F]
            result += base_chars[(remaining >> 12) & 0x3F]

            if i < len(text):
                result += base_chars[(remaining >> 6) & 0x3F]
            else:
                result += "="
            result += "="

        return result

    @staticmethod
    def VM112(array: List[int]) -> str:
        """
        Convert an array of integers to a string using a specific encoding.
        """
        buffer = bytearray(19)

        buffer[0] = array[0]
        buffer[1] = array[10]
        buffer[2] = array[1]
        buffer[3] = array[11]
        buffer[4] = array[2]
        buffer[5] = array[12]
        buffer[6] = array[3]
        buffer[7] = array[13]
        buffer[8] = array[4]
        buffer[9] = array[14]
        buffer[10] = array[5]
        buffer[11] = array[15]
        buffer[12] = array[6]
        buffer[13] = array[16]
        buffer[14] = array[7]
        buffer[15] = array[17]
        buffer[16] = array[8]
        buffer[17] = array[18]
        buffer[18] = array[9]

        return ''.join(chr(b) for b in buffer)

    @staticmethod
    def VM108(arg0: int, arg1: int) -> str:
        """
        Convert two integers to a string representation.
        """
        buffer = bytearray(3)

        buffer[0] = arg0 // 256
        buffer[1] = arg0 % 256
        buffer[2] = arg1 % 256

        return ''.join(chr(b) for b in buffer)

    @staticmethod
    def get_x_bogus(url: str = "", user_agent: str = "") -> str:
        """
        Signs the URL so it can be fetched normally.
        The user agent given to this function MUST
        be the same when performing the actual request.

        Args:
            url: The URL to sign
            user_agent: The user agent to use

        Returns:
            A signed URL
        """
        init_hash = 'd41d8cd98f00b204e9800998ecf8427e'
        query = url

        def MD5(string: Union[str, bytes]) -> str:
            if isinstance(string, str):
                string = string.encode('utf-8')
            return hashlib.md5(string).hexdigest()

        hash1 = MD5(query)
        decode1 = Kb.decode(hash1)
        hash2 = MD5(decode1)
        decode2 = Kb.decode(hash2)

        init_hash_decoded = Kb.decode(init_hash)
        hash_init_hash_decoded = MD5(init_hash_decoded)
        decode_hash_init_hash_decoded = Kb.decode(hash_init_hash_decoded)

        init_encryption_key = TikTokXBogus.VM108(1, 0)

        encrypted_user_agent = TikTokXBogus.Ab24(init_encryption_key, user_agent)
        encoded_encrypted_user_agent = TikTokXBogus.VM231(encrypted_user_agent, 's0')
        hash_encoded_encrypted_user_agent = MD5(encoded_encrypted_user_agent)
        decode_hash_encoded_encrypted_user_agent = Kb.decode(hash_encoded_encrypted_user_agent)

        now = int(time.time())

        values_array = [
            64,
            1 // 256,
            1 % 256,
            0,
            decode2[14],
            decode2[15],
            decode_hash_init_hash_decoded[14],
            decode_hash_init_hash_decoded[15],
            decode_hash_encoded_encrypted_user_agent[14],
            decode_hash_encoded_encrypted_user_agent[15],
            (now >> 24) & 0xFF,
            (now >> 16) & 0xFF,
            (now >> 8) & 0xFF,
            now & 0xFF,
            (1508145731 >> 24) & 0xFF,
            (1508145731 >> 16) & 0xFF,
            (1508145731 >> 8) & 0xFF,
            1508145731 & 0xFF
        ]

        key = 0
        for val in values_array:
            key ^= val

        values_array2 = [
            values_array[0],
            values_array[2],
            values_array[4],
            values_array[6],
            values_array[8],
            values_array[10],
            values_array[12],
            values_array[14],
            values_array[16],
            key,
            values_array[1],
            values_array[3],
            values_array[5],
            values_array[7],
            values_array[9],
            values_array[11],
            values_array[13],
            values_array[15],
            values_array[17],
        ]

        str_val = TikTokXBogus.VM112(values_array2)
        str_key = chr(255)
        ans = TikTokXBogus.Ab24(str_key, str_val)

        def VM110(arg0: int, arg1: int, arg2: str) -> str:
            return chr(arg0) + chr(arg1) + arg2

        return TikTokXBogus.VM231(VM110(2, 255, ans), "s2")
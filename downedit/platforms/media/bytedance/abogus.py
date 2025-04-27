import math
import time
import random

from downedit.platforms.media.bytedance.encrypt import SM3


class DouyinAbogus:

    @staticmethod
    def rc4_encrypt(plaintext: str, key: str) -> str:
        """
        Encrypts/decrypts plaintext using RC4 with the given key.
        Handles strings by interpreting char codes as bytes.

        Args:
            plaintext: The string to encrypt/decrypt.
            key: The secret key string.

        Returns:
            The resulting string (may contain non-printable characters).
        """
        s = list(range(256))
        j = 0
        key_bytes = key.encode('latin-1')
        key_len = len(key_bytes)

        for i in range(256):
            j = (j + s[i] + key_bytes[i % key_len]) % 256
            s[i], s[j] = s[j], s[i] # Swap

        i = 0
        j = 0
        cipher_bytes = bytearray()
        plaintext_bytes = plaintext.encode('latin-1')

        for k in range(len(plaintext_bytes)):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            t = (s[i] + s[j]) % 256
            cipher_byte = s[t] ^ plaintext_bytes[k]
            cipher_bytes.append(cipher_byte)


        return cipher_bytes.decode('latin-1')

    @staticmethod
    def get_long_int(round_num: int, long_str: str) -> int:
        """
        Helper function for result_encrypt. Reads 3 bytes as a 24-bit integer.
        Handles potential index errors by treating missing chars as having code 0.
        """
        idx = round_num * 3
        byte1 = ord(long_str[idx]) if idx < len(long_str) else 0
        byte2 = ord(long_str[idx + 1]) if idx + 1 < len(long_str) else 0
        byte3 = ord(long_str[idx + 2]) if idx + 2 < len(long_str) else 0
        return (byte1 << 16) | (byte2 << 8) | byte3

    @staticmethod
    def result_encrypt(long_str: str, num_key: str) -> str:
        """
        Custom base64-like encoding using specific alphabets.

        Args:
            long_str: The input string (interpreted as bytes via char codes).
            num_key: Key ('s0' to 's4') to select the encoding alphabet.

        Returns:
            The encoded string.
        """
        s_obj = {
            's0': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=',
            's1': 'Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=',
            's2': 'Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=',
            's3': 'ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe',
            's4': 'Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe'
        }

        constant = {
            0: 0xfc0000,
            1: 0x03f000,
            2: 0x000fc0,
            3: 0x00003f,
            'str': s_obj[num_key]
        }
        alphabet = constant['str']
        result = []
        lound = 0

        num_input_bytes = len(long_str)
        num_output_chars = math.ceil(num_input_bytes / 3) * 4

        long_int = DouyinAbogus.get_long_int(lound, long_str)

        for i in range(num_output_chars):
            current_lound = i // 4
            if current_lound != lound:
                lound = current_lound
                long_int = DouyinAbogus.get_long_int(lound, long_str)

            key = i % 4
            temp_int = 0
            if key == 0:
                temp_int = (long_int & constant[0]) >> 18
            elif key == 1:
                temp_int = (long_int & constant[1]) >> 12
            elif key == 2:
                temp_int = (long_int & constant[2]) >> 6
            elif key == 3:
                temp_int = long_int & constant[3]

            input_byte_idx = (i // 4) * 3 + (key * 6 // 8)
            if input_byte_idx >= num_input_bytes:
                if alphabet == s_obj['s0'] and '=' in alphabet:
                    result.append('=')
                else:
                    result.append(alphabet[temp_int])
            else:
                result.append(alphabet[temp_int])

        expected_len_no_pad = math.floor(num_input_bytes / 3) * 4
        remainder = num_input_bytes % 3
        if remainder == 1:
            expected_len_no_pad += 2
        elif remainder == 2:
            expected_len_no_pad += 3

        return "".join(result[:expected_len_no_pad])

    @staticmethod
    def gener_random(random_val: float, option: list[int]) -> list[int]:
        """
        Generates 4 'randomized' bytes based on input float and options.
        """
        random_int = int(random_val)
        return [
            (random_int & 0xFF & 0xAA) | (option[0] & 0x55),
            (random_int & 0xFF & 0x55) | (option[0] & 0xAA),
            ((random_int >> 8) & 0xFF & 0xAA) | (option[1] & 0x55),
            ((random_int >> 8) & 0xFF & 0x55) | (option[1] & 0xAA)
        ]

    @staticmethod
    def generate_rc4_bb_str(url_search_params: str, user_agent: str, window_env_str: str, suffix="cus", Arguments=[0, 1, 14]) -> str:
        """
        Generates the core encrypted string based on various inputs.
        """
        sm3 = SM3()
        start_time_ms = int(time.time() * 1000)

        url_search_params_list = sm3.sum(sm3.sum(url_search_params + suffix, t='bytes'), t='bytes')
        cus_list = sm3.sum(sm3.sum(suffix, t='bytes'), t='bytes')

        rc4_key_ua = bytes([0, 1, 14]).decode('latin-1')
        encrypted_ua = DouyinAbogus.rc4_encrypt(user_agent, rc4_key_ua)
        base64_like_ua = DouyinAbogus.result_encrypt(encrypted_ua, 's3')
        ua_list = sm3.sum(base64_like_ua, t='bytes')

        end_time_ms = int(time.time() * 1000)

        b = {
            8: 3,
            10: end_time_ms,
            15: {
                'aid': 6383, 'pageId': 6241, 'boe': False, 'ddrt': 7,
                'paths': {'include': [{}, {}, {}, {}, {}, {}, {}], 'exclude': []},
                'track': {'mode': 0, 'delay': 300, 'paths': []},
                'dump': True, 'rpU': ''
            },
            16: start_time_ms,
            18: 44,
            19: [1, 0, 1, 5]
        }

        b[20] = (b[16] >> 24) & 0xFF
        b[21] = (b[16] >> 16) & 0xFF
        b[22] = (b[16] >> 8) & 0xFF
        b[23] = b[16] & 0xFF

        b[24] = (b[16] >> 32) & 0xFF
        b[25] = (b[16] >> 40) & 0xFF

        arg0, arg1, arg2 = Arguments[0], Arguments[1], Arguments[2]
        b[26] = (arg0 >> 24) & 0xFF
        b[27] = (arg0 >> 16) & 0xFF
        b[28] = (arg0 >> 8) & 0xFF
        b[29] = arg0 & 0xFF

        b[30] = (arg1 >> 8) & 0xFF
        b[31] = arg1 & 0xFF
        b[32] = (arg1 >> 24) & 0xFF
        b[33] = (arg1 >> 16) & 0xFF

        b[34] = (arg2 >> 24) & 0xFF
        b[35] = (arg2 >> 16) & 0xFF
        b[36] = (arg2 >> 8) & 0xFF
        b[37] = arg2 & 0xFF

        b[38] = url_search_params_list[21] if len(url_search_params_list) > 21 else 0
        b[39] = url_search_params_list[22] if len(url_search_params_list) > 22 else 0
        b[40] = cus_list[21] if len(cus_list) > 21 else 0
        b[41] = cus_list[22] if len(cus_list) > 22 else 0
        b[42] = ua_list[23] if len(ua_list) > 23 else 0
        b[43] = ua_list[24] if len(ua_list) > 24 else 0

        b[44] = (b[10] >> 24) & 0xFF
        b[45] = (b[10] >> 16) & 0xFF
        b[46] = (b[10] >> 8) & 0xFF
        b[47] = b[10] & 0xFF
        b[48] = b[8]
        b[49] = (b[10] >> 32) & 0xFF
        b[50] = (b[10] >> 40) & 0xFF

        page_id = b[15]['pageId']
        aid = b[15]['aid']
        b[51] = page_id
        b[52] = (page_id >> 24) & 0xFF
        b[53] = (page_id >> 16) & 0xFF
        b[54] = (page_id >> 8) & 0xFF
        b[55] = page_id & 0xFF

        b[56] = aid
        b[57] = aid & 0xFF
        b[58] = (aid >> 8) & 0xFF
        b[59] = (aid >> 16) & 0xFF
        b[60] = (aid >> 24) & 0xFF

        window_env_bytes = window_env_str.encode('utf-8')
        window_env_list = list(window_env_bytes)
        b[64] = len(window_env_list)
        b[65] = b[64] & 0xFF
        b[66] = (b[64] >> 8) & 0xFF

        b[69] = 0
        b[70] = b[69] & 0xFF
        b[71] = (b[69] >> 8) & 0xFF

        xor_keys_for_72 = [
            18, 20, 26, 30, 38, 40, 42, 21, 27, 31, 35, 39, 41, 43, 22,
            28, 32, 36, 23, 29, 33, 37, 44, 45, 46, 47, 48, 49, 50, 24,
            25, 52, 53, 54, 55, 57, 58, 59, 60, 65, 66, 70, 71
        ]
        checksum = 0
        for k in xor_keys_for_72:

            checksum ^= b.get(k, 0)
        b[72] = checksum & 0xFF

        bb_keys = [
            18, 20, 52, 26, 30, 34, 58, 38, 40, 53, 42, 21, 27, 54, 55,
            31, 35, 57, 39, 41, 43, 22, 28, 32, 60, 36, 23, 29, 33, 37,
            44, 45, 59, 46, 47, 48, 49, 50, 24, 25, 65, 66, 70, 71
        ]
        bb = [b.get(k, 0) for k in bb_keys]
        bb.extend(window_env_list)
        bb.append(b[72])

        bb_bytes = bytes(x & 0xFF for x in bb)
        bb_str = bb_bytes.decode('latin-1')

        rc4_key_final = bytes([121]).decode('latin-1')

        return DouyinAbogus.rc4_encrypt(bb_str, rc4_key_final)

    @staticmethod
    def generate_random_str() -> str:
        """
        Generates a 12-byte random string using gener_random.
        """
        random_str_list = []

        random_str_list.extend(DouyinAbogus.gener_random(random.random() * 10000, [3, 45]))
        random_str_list.extend(DouyinAbogus.gener_random(random.random() * 10000, [1, 0]))
        random_str_list.extend(DouyinAbogus.gener_random(random.random() * 10000, [1, 5]))

        random_bytes = bytes(x & 0xFF for x in random_str_list)
        return random_bytes.decode('latin-1')

    @staticmethod
    def get_a_bogus(
        url_params: str,
        fingerprint: str,
        user_agent: str
    ) -> str:
        """
        Generates the final signature string based on URL and User-Agent.

        Args:
            url_params: The full URL string.
            fingerprint: The fingerprint string.
            user_agent: The User-Agent string.

        Returns:
            The generated signature string.
        """

        # fingerprint = '1536|747|1536|834|0|30|0|0|1536|834|1536|864|1525|747|24|24|Win32'
        arguments = [0, 1, 14]

        random_part = DouyinAbogus.generate_random_str()
        rc4_bb_part = DouyinAbogus.generate_rc4_bb_str(
            url_params,
            user_agent,
            fingerprint,
            suffix="cus",
            Arguments=arguments
        )

        result_str = random_part + rc4_bb_part

        return DouyinAbogus.result_encrypt(result_str, 's4')
import hashlib
import random
import re
import secrets
import time


class KuaiShouHash:

    # Reference:
    # https://s2-111422.kwimgs.com/kos/nlav111422/pc-vision/js/app.e64212cd.js

    def __init__(self, app_key="10001001", secret_key="f2fff381c551a8dcdb765e316f3d44ac"):
        self._app_key = app_key
        self._secret_key = secret_key

    def generate_web_did(self):
        """
        Generates a 'did' cookie value in the format:
        'web_<32-character-hex-string>'.

        Returns:
            str: A generated 'did' value.
        """
        return f"web_{secrets.token_hex(16)}"

    def generate_did(self):
        """
        Generate device ID (DID) for KuaiShou.
        """
        random_number = int(random.random() * 1e9)
        random_hex = ''.join(random.choices("0123456789ABCDEF", k=7))
        return f"web_{random_number}{random_hex}"

    @staticmethod
    def replace_char(match):
        char = match.group(0)
        random_value = random.randint(0, 15)
        if char == 'x':
            return format(random_value, 'x')
        elif char == 'y':
            return format((random_value & 3) | 8, 'x')

    def generate_uuid(self):
        """
        Generate a UUID (Universally Unique Identifier) format
        """
        template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
        return re.sub(r'[xy]', self.replace_char, template)

    def generate_sign(self, input_string):
        """
        Generate a sign based on the input string.
        """
        input_bytes = input_string.encode('utf-8')
        md5_hash = hashlib.md5()
        md5_hash.update(input_bytes)
        return md5_hash.hexdigest()

    def generate_custom_sign(self):
        """
        Example of generating a custom sign based on class variables.
        """
        sign_input = self._app_key + self._secret_key + str(int(time.time()))
        return self.generate_sign(sign_input)


if __name__ == "__main__":
    kuai_shou_did = KuaiShouHash()
    print(kuai_shou_did.generate_did())
    print(kuai_shou_did.generate_web_did())
    print(kuai_shou_did.generate_uuid())
    print(kuai_shou_did.generate_custom_sign())

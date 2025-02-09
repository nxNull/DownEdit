from asyncio import run
from json import dumps
from random import randint
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from time import time
from typing import TYPE_CHECKING
from typing import Union
from urllib.parse import quote

from downedit.platforms.bytedance.xbogus import XBogus


REFERER = "https://www.tiktok.com/"
API = "https://mssdk-ttp2.tiktokw.us/web/report"

DATA = {
    "magic": 538969122,
    "version": 1,
    "dataType": 8,
    "strData": "34t+6IAQRGtGe1FA5AcCk5dF4BPSdOUxHFrxQI/mc8lc6NeBHzKmffyCfYVR0/gmUQb1xgAxQoircKpjgKGVh/PeMOzKDC7GjC"
                "yEH33nvZRoSd/BBSxV5dFRXJrx4eVr7YDIzc8Wob07R2N3fQB0cHugw9gIr5ZGezCgs8/utmiOPLVtnjafmzUzwnVqTTap6CaL"
                "YH+3/enUnDW2BjIbsAVafxjIRITqnll6HkkyMAfEM/lpEFg5e8nMpNQvNePkOPcOzgCMLFsGXE3b7MUpc7wWOcHDeEk5PrboTE"
                "7zXVhL4ltQ6sIOifa2RaK42zoebKCnDW3HxCyH/AqpROkLBTkBgcYdB3c3IneEkbZZWkzpoiq1181P++PMAY6mggLOLWDNPBa7"
                "/KJhcGr7GFBWVM2WWnJHscE8fETUiqwBsVgQ5PaZvL5o3/rBPJqM4Nmb+m00BWeNemhfRv6xVgTtWb8eB4kbrQOesRnFdZjBOY"
                "WtTFKWtr35x8pMzpwCN3cueSADXOWBeJPQk0/lPouPwe4AROlLQuSNvOaKSCHhj1AzzpQ5rl3ricyymxuCDl0kTVc7yzySaMgT"
                "isN0F/qBmfNj+w1Y99Mbvmy4hefvjwhwDlCOmrTDiB4Fkk9q0Z8ziUrvOjl2dgfEruStmEXwjryi4klcxcR+uk82mSt6CrEijM"
                "AgqsNrKKGjOi/WGnEXskDANEqjEms3Iy3xfLD0ywHaPwYzFOxmjgKO+XQcPS9+5V2pKRLQrqJIASWOQbgbOwUcysSEmzsl/vFg"
                "H4NU0pMa6nDP4xknfIjyIeoUHJbjFsOSlcJUMTnDxG8wltmvyJ/e+idnAUybMugJ/KBMHHB4ruHS8USpo7kLxgje/KhyuD/34H"
                "soFAEB7F9LEz1UHdncKjTPQjVltMRRc2SF5LrTOAdcz4Q5MXrwg+0FHz8k4LEFx1OOUREyoT33OPrACV8pCk6t5qF7UosrIOCc"
                "gBWA2CyLd+/ap2C+86BNLbLR00B9suZJZ8JzbdvKO4Qd3XkcxraX9orFoEjlDiA/Jyvgw11B2mKcYKdq1X5/6oJz2x0XGNvwuc"
                "PcINPPerICRMsTRZdel+dOnKMJ99RtkxNHHHyGhDUf3entFTumuG8ME0OK9eEhzSwRGiF5VUC2zDUzfKteKqlP2tSU0pdMiHGG"
                "l96y6GD92mTSWrly8SE7P8tbluIe0OYuvXAWQ0IIK555CZ1GZfJjXlWIVIsFb1OyEfTsS1fRhKqXBYmwt1RNrAI90hNwMGXS+L"
                "OAu5qIXO7SyHsxmtDhaRFtLfsBrREkiGFDoV1Rp1vPe5zkb8EVEP8vXjRD6V71JxrLl7bM1Z/ro87MDu7cVF6+bF36Mh3kJZ8E"
                "z0rpmDjy5L2oKcJoixX32O1OAbgKHrdRZlxAebV7tQgNbhm36uGtl1ibbW6VuzNSuZB9DiD56GhptWuFurC1wGmg3FjYoQwSTT"
                "A9VWTpfliutUTsZLfRG2ephN4epy5vURO56Oct4DoHR2PCHCToqddk9ODDmzA2vLUUTkEnZhxHcP8c0+sXRWHfGxbiw13mpKa/"
                "k8+ghz7D2MJyhIhMTNZcUcUp77NA2WeRsfIFKGaPPzIBLejtKA2mshP8OMUPChhmaqNMic2rqx0DarcWmrUjn8XS63F7drGopY"
                "2PN7+SDGi8xLjigyaxRX/cv0+Z6A8/sOFW4pkhCJqoh10YJnyOgRBHZ21qox1D+nZ9Sw2lpHzz14uVzw2FHXRqJSeHno5LrUH3"
                "H0iQha6UGpKTUAhI8Kn1HgbQo/zsKDtRD2jinYhNH9NSHxj6Ojy0Xx5gIaB0KA/a/rTJcqlWXWpEFKLVsMVez7U3p4/QtMG05D"
                "AFrPT4oX0ebjvH0UJR+rUO/CWsHGwjrXos9dE2TruKCtt/4yVpfaGiBru9qyawcjYuCgY6CWn44mPyUX9C/yJUy5cQ1SEhJ7nw"
                "Id1ydS95OYFE/FvAotc1UqFKYUj6R6TAaGn8z3twad2JYg340nuBLvKAQV3bqky02Z7YouDQg2vyX9jEbDXThO5qxXoSsuvgh4"
                "P1a84Au4AfW2qJstzAyiqMtkOs8N1j0Bx31OGUX+L9NtdM+rHVkXxCuVDoiJSWVUkhChEU+Mhqc83R4Nilh4GZxPAbv56bwVF7"
                "jCReLImjsnauXj8e2g5WcC5QpfTkBL6Ii2fmUACgustVr86iB+vfLZGbNH4CrQb+navzVq+7yOO9RH0KHcM7H52+ziwc5flSfW"
                "lqTQ/QO0rJ21iy2WnWBGu7Gz5Sw1u0QElO1bL/WuwW3jSNa05Yh1M0Htf0VJBiLXbCk//XfM/JSvlE0Rn+fFnfmAqiKgLFBlG0"
                "U1ZFS3OM//y0pMEQYHFVmeBaFe2gjpy43jXK5p9uFtBiqyOzkaABI9x0fwS8VuIEmdmqu2AbXn4wJQJ/hE+SZMigU49K4FjNsO"
                "Wid1xLrxl1GbZ3MLlMRRPNIf/Qgsd3pdB8pM9UyoaVEgTVqupN5/aGwrMGbX1mirq1uyaS6OFw7HyXp6bOzd4PdNqEPn05vCoi"
                "lwVA35KTkIcognCRM9MHndrmeYlKfliKsyjSEizVcKm9d7Kk89lFqVehFmxjLkxsYwoEr7U9ZuHnkG10mRlIUO5dMA9shcFYac"
                "hZ3jDpi9WoM6iaEuFD71k9MGC0lzhR2O+tHIyyXGO8C14/xB7PpFc/syo/7wC4LIXAXQn1zWzbCx9n5aBRwyG7ggtlKdo+qWmF"
                "9+x0+2Y5BF4BPnGcYnPK0UTWit+9/jpP2HC6MeHLhPA8BcjYcFKhUA9L387U3qIkSiAGbPXRTYoso5n5VN7A93r0lzdwayCnJP"
                "VtrFwICXjHPw/ySzO02/s/F6xlIqE2h8ZsFVRL2nHJR6D8OXVxvXzrULrw7BITPcVcUyiZH65WuDhDSqhDsM8QcgNQngVqGRAL"
                "5TClHuq4NzslQP3etXsbY8TV75nvoo3mHTzoWBKBYZNGRWZBHUhG1PmWBzr9aczuHYvOeH0dWP14CKmg4bjgBwKsBBewmofmz4"
                "Sm6BNkxF+mnZdXLboqijcjXle3uMyhAHW5mHEhrDvGbhC7QcQTVPdbpgIZrHtQUdj1N6phNTYOmDxkEIh66T2kVkCKdwu51Stm"
                "V7RqJMv5lZWNmHFnj/e4+vD7HktDPtU6O8BI6LsEzVUzgwNMiioceDZaK2XsQ8HzVOhR9PsSfeYoEMQc/myIeOup+CtZZkPJrx"
                "e9dx6IEypaFrKADAyActSW49GdjubMo+98L/8csDz0oxRxfIJRy6zNmVAQ8zQ44Gf397sVG5Vq9hm+iLNDM3E8PXIeNnjj4TGG"
                "ArwHqvVy9iUri5kycjmZh4RujGXg2ERB3s3k6Zmen/ugO3PIO/ZglOk8cAtreLasoCT5wwpZ11JuSEAmuGZPiSEPB8lzsB1ESh"
                "UZ2ycVGclhYATqaz8mld/YhZS75T4lwlmiCoTnOIUp3KHbwVJHb6GxmNMu4cq7CYwNSdrG7jG6Zrp5w7Mx9Vp3LLIUBsH3kOOy"
                "gRNCGxZ7tmiABzJlA98GOdzzF2HwrsrsCiF2R0J2Fpud+J0qQdD/O9NRH8iU0Mae+WYH98tAz+hMEo45UBZBPZ6ady+Kr0FyT1"
                "CPsh3pnF6R+C73eeOAwEhaPMAoCp8aov8ynaAikh6yhV9mbLreVdByKNL9oOmq1yEK3awk4+dnQMfzKmAwxZXEsNApMBYoeXy8"
                "cpJJpVGMUJBuZSBLgCGcAmJLuOby93xf6YH5NcwmgjRuHrF3AEl9oaFvG0TEUyK3MCF7vuitDPHDZGl0N07A4YfsQLhcja7pXO"
                "fRUIh5KVff+nLLyq2LLqO4YKGQM8Mxj7fyy4k6SYN1FNUkeXDOtbOeOVcd31eMzyfePOpForEq9dGdISVV/KZxTkK+nmvqqHYB"
                "+u0/MWRMvfw2RmKKJKzGhYT4T0qangh33sMGGLDtrg0fm+c+M7jpgRHKZbMhmfAlL/lGVtmHzy6qa8/xho47CoxYQRjXub3LNB"
                "h1/pX72zP3oTGJkbfo+sJaOPT3fILydGQR7zTIw7CYaVNwr70YhJ8odStwSVbhNKcWNtKzYpZCXaySMQ0hu64wG/GY7YBU64v/"
                "/rPi0ByRVIzUjfmLpRJRCxbW13xzjzc4e2PaBzFHFHk3l3y7MFjQS8ntfjeMTpCowemB7AXBzTbL+ZSkS6wzp2rHrXXl9s+rF7"
                "tVxSRBJPXx1wZVevJYYyBhu/fPxWrTFSEeZnP3dOcU21xTxjd75mSoW4nn4rDOix2I4Hu2t3R9IVsdv+xhsoPNHmjM4rCqTLSW"
                "xkB+DOv/tXeC7+VxET4bCWp7RgQdyy1QJfbO9EF0GYqC3iYojyXRHsjDCe1ThiEi4rG/HcukHrP40YECkvfn/pTDn7xJ1okMTZ"
                "SsxmrTMeS0zjtnhIo+BE==",
    "tspFromClient": 0
}

TOKEN = (
    "tWQyeNlnPlknDEh8suUhZQhOedOgAgRyQJGp4rCHrxTAlMS3wk9xGJ_Wrc2fgkPRVzkIr8fJw7VTjFcQ7glTWBCbL28_ptAMDlD1jI3a"
    "ZtgbaTxz36EXh0eiNDKGzI1PEweGi6we6L7_z7gvKoIxRWKm"
)

class MsTokenTikTok(MsToken):

    @classmethod
    async def get_real_ms_token(
            cls,
            headers: dict,
            token="",
            proxy: str = None,
            **kwargs,
    ) -> dict | None:
        params = {cls.NAME: token}
        
        xb = XBogus(user_agent=user_agent)
        if token:
            headers |= {"Cookie": f"{cls.NAME}={token}"}
            params["X-Bogus"] = quote(
                XBogusTikTok().get_x_bogus(
                    params, user_agent=headers.get(
                        "User-Agent", USERAGENT)), safe="")
        return await cls._get_ms_token(
            params,
            headers,
            proxy,
            **kwargs,
        )
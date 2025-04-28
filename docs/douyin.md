# 🛠️ Step-by-Step Guide

![Douyin](https://github.com/user-attachments/assets/be74f49d-4bab-4a67-b3c5-e7a4a31dae79)


Follow these steps to use the tool:

## 1. 🔐 Get Cookies from Browser

You need your browser cookies for `douyin.com` to authenticate.

**How to get them:**

*   **Easiest Way (Use a Browser Extension):**
    - Log in to `douyin.com`.
    - Use an extension like [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) (available for Chrome/Firefox) to view and copy your cookies for the site.

*   **Manual Way (Use Developer Console):**
    - Go to `douyin.com`.
    - Open Developer Tools (`F12` or Right-click -> Inspect).
    - Go to the `Console` tab.
    - Type `document.cookie` and press Enter.
    - Copy the entire output string.

**Then:** Paste the copied cookie string into the tool's input field.

**Example:**
```text
Enter User Cookies: __ac_referer=https://www.douyin.com/root/search/cute%20girl?aid=5d7317aa-f838-44cb-ab24-89f4eaae303a&type=general; douyin.com; UIFID_TEMP=4be83ecefa579a300714166db9e569bafd8689fc248d1e190e384db8df203b81ea646495483afebeeb970c91b03763d2841691e786ca7c29273c8e61221080ee749cdf3bdf88484be6d1cae4fae1fe15; hevc_supported=true; dy_swidth=1920; dy_sheight=1080; fpk1=U2FsdGVkX19WXEWVwWdRkE1qTjGsBouQgGkipaQ26z/WVWDjoJ360eUN3y97eFi1+ksdNWsmUY3Irn+fIJP1pg==; fpk2=33d0f257a817d1ca4c4381b87f8ad83f; xgplayer_user_id=445115889666; s_v_web_id=verify_m9yetfb7_WXAaXLLu_jSji_4YLr_ARUV_pLSCqXKeocLy; passport_csrf_token=961f9f9e8d7aaf2a997bbffa7d3f5aa4; passport_csrf_token_default=961f9f9e8d7aaf2a997bbffa7d3f5aa4; __security_mc_1_s_sdk_cert_key=83d219c5-47c2-9605; __security_mc_1_s_sdk_sign_data_key_web_protect=efc08fd0-42c7-9a34; __security_mc_1_s_sdk_crypt_sdk=0c7ebdc5-40d0-904a; bd_ticket_guard_client_web_domain=2; __security_mc_1_s_sdk_sign_data_key_sso=9f851d6c-46fd-9a90; UIFID=4be83ecefa579a300714166db9e569bafd8689fc248d1e190e384db8df203b81ea646495483afebeeb970c91b03763d26ed383cf1c272e94d87b2db7d18aacd98e1f1dd0315e3124d5e3255fa6b1a201a4e93a3abd846b06ff8681a45d64ffc457ad5a18765c535fb8a39d4abafac2f42b28f6a5a7211b47877d3d3f20b6117aa49a553695fbe93be50e063c3e49b99cae0e1c19c6356d3d024669cbd1d0daeb; is_dash_user=1; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; download_guide=%223%2F20250426%2F0%22; WallpaperGuide=%7B%22showTime%22%3A1745683642341%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A28%2C%22cursor2%22%3A4%2C%22hoverTime%22%3A1745683642348%7D; __ac_nonce=0680f72be005677f6387e; __ac_signature=_02B4Z6wo00f01To7M-QAAIDAXara68iKdDU6GzdAACaE84; douyin.com; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; strategyABtestKey=%221745842879.395%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e5827292771273f27373731353d3d37313d30313234272927676c715a75776a716a666a69273f2763646976602778; bit_env=aiD7LTYoGTw3sLLbnIJC6TTUO5ayXevBYEcuQeQM1MHYdTmypjyRZLNAAOpi7mHwZF2Gbu59SkoRE2SeJvuox9q5s7_D4_M6B5CSGsIP8vCNXOMnbUu5IXC2-teBogHxxRGVpoTWr8d_ASFGm590RQSuFV6SPkX7vpV7KPZVcCiIqPG2K9YVUzzfvPZSu2EQP769_4_fCDhpvJOCfFfKjON3VXASZufUA-3iECDpZMnQgHTk7qDls63G2XEG68KyQAOVaOLI9QTBFl3JiWKSqwnGDqmCiDbI0OtY02lzdmw5zvpfr1G7oNHYoMLeKwCVBgjgq7F7iSKwsb9I41R-CsQXqqB2FIpqqxH_3RVyXwKEBg7X4-B_lkVhoOHuoov3tHO8pf3poZjMvIo-irfusTIoXjDT3zkr3FxKn1wicE4hooijhDrhSigYlAZTUDC6iM5BrNpqR5hzhRzyNVodl3PEdpthCN0BM7ElxNt26FvQOX81xQ4YdBpUEK3oDFTK; gulu_source_res=eyJwX2luIjoiOWNkZmZlMTNlNDYxYjgwZGM0Mzc0NDg5MmQ0OTQ1YWM4YzUzMjE0YzA3YzYxMTVjYzljMGE0NTY3MzEzZWM3OCJ9; passport_auth_mix_state=d01mwgnq32369eshy8sj0mwu5emx36oe77mb2z0cnje90qat; xg_device_score=7.787326758389049; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; biz_trace_id=c5a8e6f4; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCS0FVNzBoOUZPYlJwZEhwa0YybW9ndmR5WEFLZzFQbHZtY3ZEbjdZbFRhZVhWblNnN2c1Ui9xNU9VOW54V3grdzVyUGs1c005NGdHM1FVUTVDakhHQk09IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; IsDouyinActive=true
```

## 2. 🔗 Input the User Link

Paste the target user's profile URL into the input field.

**Example:**
```text
Enter User Url: https://www.douyin.com/user/MS4wLjABAAAAXH9jzyP7CY5qxu7eAjY02UdoKyQaZjPwubf01BneuYG-IWm2CReiOCarhS9tLEMf
```

## 3. ⬇️ Download the Data

Once the cookies and URL are submitted, the tool will automatically:
*   Fetch the user's data.
*   Download and save the data to a local directory.

📁 By default, files are saved to: `./douyin/user`

---

## Notes & Warnings

*   Do not share your cookies with unauthorized individuals. Your cookies grant access to your account.
*   Use this tool responsibly and ensure you comply with the website's terms of service. Misuse could lead to account restrictions.


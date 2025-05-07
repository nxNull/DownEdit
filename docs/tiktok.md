
# 🛠️ Step-by-Step Guide

![Tiktok](https://github.com/user-attachments/assets/42e3cac9-2033-4254-89a3-a2f09259f1e4)


Follow these steps to use the tool:

## 1. 🔐 Get Cookies from Browser

You need your browser cookies for `tiktok.com` to authenticate.

**How to get them:**

*   **Easiest Way (Use a Browser Extension):**
    - Log in to `tiktok.com`.
    - Use an extension like [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) (available for Chrome/Firefox) to view and copy your cookies for the site.

*   **Manual Way (Use Developer Console):**
    - Go to `tiktok.com`.
    - Open Developer Tools (`F12` or Right-click -> Inspect).
    - Go to the `Console` tab.
    - Type`document.cookie` and press Enter.
    - Copy the entire output string.

*   **See the picture below:**

![tiktok_cookie](https://github.com/user-attachments/assets/176bb06c-c2b8-4397-b24a-fbd93c8371f2)

**Then:** Paste the copied cookie string into the tool's input field.

`Note:  If the copied cookie doesn’t work, try obtaining it from a different API.`

**Example:**
```text
Enter User Cookies: '_ttp=2tl5b5MW06O0JfcU5omBD9zBPEu; delay_guest_mode_vid=5; passport_csrf_token=11bc7fe09acc5d574210ffcb2f0836e9; passport_csrf_token_default=11bc7fe09acc5d574210ffcb2f0836e9; last_login_method=QRcode; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; cookie-consent={%22optional%22:false%2C%22ga%22:false%2C%22af%22:false%2C%22fbp%22:false%2C%22lip%22:false%2C%22bing%22:false%2C%22ttads%22:false%2C%22reddit%22:false%2C%22hubspot%22:false%2C%22version%22:%22v10%22}; passport_fe_beating_status=true; perf_feed_cache={%22expireTimestamp%22:1746014400000%2C%22itemIds%22:[%227486592353453542687%22%2C%227493925618782932256%22%2C%227497063484245413127%22]}; msToken=ysiMlQtrrTyNr_W2tIFTkPFFdKmai2xcBfBAs7r9_g2E5ozdts5Dk2dFBgehJFgqUWJFVfHNcNxHYI3FEHI1n5DPPABc4uvA36qQcov4laO_CTMw0m94-eldxsLSYdfD6n9kmP-wYx6oYqw=; msToken=Icumn3rZzVTQa5nk5dBRuKQmc9fcn8y5Y9HOO49K412E740fUVTFNbIukrN_HvpmVAvqK7YmwQtgTGGPi3uPf7JjEDSWi12PspN-Cq_fAgxZQ2_DXzW-ZtbJBEerWjy6zsv6l8tgmBcR7rU='
```

## 2. 🔗 Input the User Link

Paste the target user's profile URL into the input field.

**Example:**
```text
Enter User Url: https://www.tiktok.com/@random.4.modnar_
```

## 3. ⬇️ Download the Data

Once the cookies and URL are submitted, the tool will automatically:
*   Fetch the user's data.
*   Download and save the data to a local directory.

📁 By default, files are saved to: `./tiktok/user`

---

## Notes & Warnings

*   Do not share your cookies with unauthorized individuals. Your cookies grant access to your account.
*   Use this tool responsibly and ensure you comply with the website's terms of service. Misuse could lead to account restrictions.


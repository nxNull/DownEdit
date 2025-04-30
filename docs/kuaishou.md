# 🛠️ Step-by-Step Guide

![Kuaishou](https://github.com/user-attachments/assets/fc2cf3c3-8816-4410-9fad-3ff62d7be443)

Follow these steps to use the tool:

## 1. 🔐 Get Cookies from Browser

You need your browser cookies for `kuaishou.com` to authenticate.

**How to get them:**

*   **Easiest Way (Use a Browser Extension):**
    - Log in to `kuaishou.com`.
    - Use an extension like [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) (available for Chrome/Firefox) to view and copy your cookies for the site.

*   **Manual Way (Use Developer Console):**
    - Go to `kuaishou.com`.
    - Open Developer Tools (`F12` or Right-click -> Inspect).
    - Go to the `Console` tab.
    - Type `document.cookie` and press Enter.
    - Copy the entire output string.

*   **See the picture below:**

![kauishou_cookie](https://github.com/user-attachments/assets/04cf7ae7-7547-4163-8519-f6480d3e561f)

**Then:** Paste the copied cookie string into the tool's input field.

**Example:**
```text
Enter User Cookies: kpf=PC_WEB; clientid=3; did=web_f6c75837d7aedc460700a0fb13be0ef6; kpn=KUAISHOU_VISION
```

## 2. 🔗 Input the User Link

Paste the target user's profile URL into the input field.

**Example:**
```text
Enter User Url: https://www.kuaishou.com/profile/3xndqj3zwhdd9e9
```

## 3. ⬇️ Download the Data

Once the cookies and URL are submitted, the tool will automatically:
*   Fetch the user's data.
*   Download and save the data to a local directory.

📁 By default, files are saved to: `./kuaishou/user`

---

## Notes & Warnings

*   Do not share your cookies with unauthorized individuals. Your cookies grant access to your account.
*   Use this tool responsibly and ensure you comply with the website's terms of service. Misuse could lead to account restrictions.

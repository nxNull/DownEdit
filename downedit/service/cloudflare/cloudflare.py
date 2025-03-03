import asyncio
import time

from dataclasses import dataclass
from collections import deque
from typing import Optional
from patchright.async_api import async_playwright

from downedit.utils import log

__all__ = ["Turnstile"]

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Turnstile Solver</title>
    <script
        src="https://challenges.cloudflare.com/turnstile/v0/api.js?onload=onloadTurnstileCallback"
        async defer
    ></script>
</head>
<body>
    <div class="cf-turnstile" data-sitekey="{sitekey}"></div>
</body>
</html>
"""

@dataclass
class CloudflareResult:
    status: str = "success"
    error: Optional[str] = None
    result: Optional[str] = None
    elapsed_time: Optional[float] = None

class BrowserPage:
    """
    A pool of browser pages.
    """

    def __init__(self, context):
        self.context = context
        self.min_size = 1
        self.max_size = 10
        self.in_use_pages: set = set()
        self._lock = asyncio.Lock()
        self.available_pages: deque = deque()

    async def initialize(self) -> None:
        """
        Initializes the pool with a minimum number of pages.
        """
        for _ in range(self.min_size):
            await self._add_new_page_to_pool()

    async def get_page(self):
        """
        Retrieves an available page or creates a new one if capacity allows.
        """
        async with self._lock:
            if not self.available_pages and len(self.in_use_pages) < self.max_size:
                await self._add_new_page_to_pool()

            while not self.available_pages:
                await asyncio.sleep(0.1)

            page = self.available_pages.popleft()
            self.in_use_pages.add(page)
            return page

    async def return_page(self, page) -> None:
        """
        Returns a page to the pool or closes it if excess pages exist.
        """
        async with self._lock:
            if page in self.in_use_pages:
                self.in_use_pages.remove(page)

            if self._should_close_page():
                await page.close()
            else:
                self.available_pages.append(page)

    async def _add_new_page_to_pool(self) -> None:
        """
        Adds a new page to the pool.
        """
        page = await self.context.new_page()
        self.available_pages.append(page)

    def _should_close_page(self) -> bool:
        """
        Determines whether to close a page based on pool size.
        """
        total_pages = len(self.in_use_pages) + len(self.available_pages)
        return total_pages > self.min_size and len(self.available_pages) > 1


class Turnstile:
    """
    A class to solve Cloudflare's Turnstile challenge.
    """

    def __init__(self, header: str = {}, proxy = None, html: str = HTML_TEMPLATE):
        self.html = html
        self.header = header
        self.proxy = proxy
        self.page_pool: BrowserPage | None = None
        self.browser = None
        self.context = None
        self.browser_args = [
            "--disable-blink-features=AutomationControlled",
        ]

    async def _initialize_browser(self) -> None:
        """
        Initialize the browser and create the page pool.
        """
        patchright = await async_playwright().start()
        self.browser = await patchright.chromium.launch(
            headless=False,
            args=self.browser_args
        )
        if self.header != {}:
            self.context = await self.browser.new_context(
                extra_http_headers=self.header,
                proxy=self.proxy
            )
        else:
            self.context = await self.browser.new_context()
        self.page_pool = BrowserPage(self.context)

        await self.page_pool.initialize()

    async def _setup_turnstile_page(self, page, url: str, sitekey: str) -> None:
        """
        prepare the page with turnstile widget.
        """
        validate_url = url + "/" if not url.endswith("/") else url
        html = self.html.format(sitekey=sitekey)
        # await page.goto(url)
        # await page.set_content(html)
        # await page.eval_on_selector("//div[@class='cf-turnstile']", "el => el.style.width = '70px'")
        await page.route(validate_url, lambda route: route.fulfill(body=html, status=200))
        await page.goto(validate_url)
        await page.eval_on_selector("//div[@class='cf-turnstile']", "el => el.style.width = '70px'")

    async def process(self, page, start_time: float) -> CloudflareResult:
        """
        Process the Turnstile challenge.
        """
        max_attempts = 10
        for _ in range(max_attempts):
            try:
                turnstile_response = await page.input_value("[name=cf-turnstile-response]")

                if turnstile_response != "":
                    element = await page.query_selector("[name=cf-turnstile-response]")
                    if element:
                        value = await element.get_attribute("value")
                        return CloudflareResult(
                            result=value,
                            elapsed_time=round(time.time() - start_time, 3),
                        )

                await page.click("//div[@class='cf-turnstile']", timeout=5000)
                await asyncio.sleep(0.7)

            except Exception as e:
                pass

        return CloudflareResult(
            status="failure",
            error="max attempts reached",
            result=None,
            elapsed_time=round(time.time() - start_time, 3),
        )

    async def solve(self, url: str, sitekey: str) -> CloudflareResult:
        """
        Solve the Turnstile challenge.
        """
        start_time = time.time()
        await self._initialize_browser()

        try:
            page = await self.page_pool.get_page()
            await self._setup_turnstile_page(page, url, sitekey)
            return await self.process(page, start_time)
        except Exception as e:
            log.error(f"error during turnstile solving: {e}")
            return CloudflareResult(
                status="error",
                error=str(e)
            )
        finally:
            if page:
                await page.goto("about:blank")
                await self.page_pool.return_page(page)
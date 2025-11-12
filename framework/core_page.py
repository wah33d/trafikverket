from playwright.sync_api import Page
from framework.browser import launch_browser
from framework.config import DEFAULT_BROWSER

class CorePage:
    def __init__(self, browser_choice: str = DEFAULT_BROWSER):
        self._playwright, self._browser = launch_browser(browser_choice)
        self._page: Page = self._browser.new_page()
        self._page.set_default_timeout(10000)

    @property
    def page(self) -> Page:
        return self._page

    def close(self):
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    def __getattr__(self, name):
        return getattr(self._page, name)

    def click_loaded(self, selector: str, timeout=10000):
        self._click_loaded(self._page, selector, timeout)

    def fill_loaded(self, selector: str, value: str, timeout=10000):
        self._fill_loaded(self._page, selector, value, timeout)

    def frame_click_loaded(self, frame, selector: str, timeout=10000):
        self._click_loaded(frame, selector, timeout)

    def frame_fill_loaded(self, frame, selector: str, value: str, timeout=10000):
        self._fill_loaded(frame, selector, value, timeout)

    def _click_loaded(self, target, selector: str, timeout=10000):
        element = target.wait_for_selector(selector, timeout=timeout)
        element.click()

    def _fill_loaded(self, target, selector: str, value: str, timeout=10000):
        input_elem = target.wait_for_selector(selector, timeout=timeout)
        input_elem.fill(value)

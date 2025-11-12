from playwright.sync_api import sync_playwright
from framework.config import (
    HEADLESS,
    DEFAULT_BROWSER,
    EDGE_EXECUTABLE_PATH,
    EDGE_USER_DATA_DIR,
    CHROME_EXECUTABLE_PATH,
    CHROME_USER_DATA_DIR,
    CHROMIUM_EXECUTABLE_PATH,
    CHROMIUM_USER_DATA_DIR,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
import subprocess


BROWSER_WIDTH = SCREEN_WIDTH - 150
BROWSER_HEIGHT = SCREEN_HEIGHT - 150


def kill_browser(process_name):
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", process_name],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"All running {process_name} processes killed.")
    except Exception as e:
        print(f"Failed to kill {process_name}: {e}")


def launch_browser(browser_choice: str = DEFAULT_BROWSER):
    p = sync_playwright().start()
    browser_choice = browser_choice.lower()

    browser_configs = {
        "chrome": (CHROME_USER_DATA_DIR, CHROME_EXECUTABLE_PATH, "chrome.exe"),
        "edge": (EDGE_USER_DATA_DIR, EDGE_EXECUTABLE_PATH, "msedge.exe"),
        "chromium": (CHROMIUM_USER_DATA_DIR, CHROMIUM_EXECUTABLE_PATH, "chrome.exe"),
    }

    if browser_choice not in browser_configs:
        p.stop()
        raise ValueError(f"Unknown browser: {browser_choice}")

    user_data_dir, executable_path, process_name = browser_configs[browser_choice]

    # kill_browser(process_name)

    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=HEADLESS,
        executable_path=executable_path,
        args=[f"--window-size={BROWSER_WIDTH},{BROWSER_HEIGHT}"],
        ignore_default_args=["--enable-automation"],
        viewport={"width": BROWSER_WIDTH, "height": BROWSER_HEIGHT},
        screen={"width": BROWSER_WIDTH, "height": BROWSER_HEIGHT}
    )

    page = browser.pages[0] if browser.pages else browser.new_page()
    page.set_viewport_size({"width": BROWSER_WIDTH, "height": BROWSER_HEIGHT})

    return p, browser

from playwright.sync_api import sync_playwright
from framework.config import (
    HEADLESS,
    DEFAULT_BROWSER,
    EDGE_EXECUTABLE_PATH,
    CHROME_EXECUTABLE_PATH,
    CHROMIUM_EXECUTABLE_PATH,
    EDGE_USER_DATA_DIR,
    CHROME_USER_DATA_DIR,
    CHROMIUM_USER_DATA_DIR,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
import subprocess

BROWSER_WIDTH = SCREEN_WIDTH - 150
BROWSER_HEIGHT = SCREEN_HEIGHT - 150


# Optional: kill browser process
def kill_browser(process_name: str):
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", process_name],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"All running {process_name} processes killed.")
    except Exception as e:
        print(f"Failed to kill {process_name}: {e}")


def launch_browser(browser_choice: str = DEFAULT_BROWSER):
    p = sync_playwright().start()
    browser_choice = browser_choice.lower()

    # Browser configuration:
    # executable path, process name, REAL user data directory
    browser_configs = {
        "chrome": (
            CHROME_EXECUTABLE_PATH,
            "chrome.exe",
            CHROME_USER_DATA_DIR,
        ),
        "edge": (
            EDGE_EXECUTABLE_PATH,
            "msedge.exe",
            EDGE_USER_DATA_DIR,
        ),
        "chromium": (
            CHROMIUM_EXECUTABLE_PATH,
            "chrome.exe",
            CHROMIUM_USER_DATA_DIR,
        ),
    }

    if browser_choice not in browser_configs:
        p.stop()
        raise ValueError(f"Unknown browser: {browser_choice}")

    executable_path, process_name, user_data_dir = browser_configs[browser_choice]

    print(f"\nLaunching {browser_choice} with REAL browser profile:")
    print(user_data_dir, "\n")

    # IMPORTANT:
    # Make sure browser is not already running with the same profile
    kill_browser(process_name)

    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,   # ✅ REAL profile
        executable_path=executable_path,
        headless=HEADLESS,
        args=[
            f"--window-size={BROWSER_WIDTH},{BROWSER_HEIGHT}",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ],
        ignore_default_args=["--enable-automation"],
        viewport={"width": BROWSER_WIDTH, "height": BROWSER_HEIGHT},
        screen={"width": BROWSER_WIDTH, "height": BROWSER_HEIGHT},
    )

    # Ensure a page exists
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.set_viewport_size({"width": BROWSER_WIDTH, "height": BROWSER_HEIGHT})

    return p, browser

import ctypes
import os

# --- Common base paths ---
LOCALAPP = os.getenv("LOCALAPPDATA", "")
PROGRAM_X86 = os.getenv("PROGRAMFILES(X86)", "")
PROGRAM_FILES = os.getenv("PROGRAMFILES", "")

# --- Browser executable paths ---
EDGE_EXECUTABLE_PATH = os.path.join(PROGRAM_X86, "Microsoft", "Edge", "Application", "msedge.exe")
CHROME_EXECUTABLE_PATH = os.path.join(PROGRAM_FILES, "Google", "Chrome", "Application", "chrome.exe")
CHROMIUM_EXECUTABLE_PATH = os.path.join(PROGRAM_FILES, "Google", "Chromium", "chrome.exe")

# --- Browser user data directories ---
EDGE_USER_DATA_DIR = os.path.join(LOCALAPP, "Microsoft", "Edge", "User Data")
CHROME_USER_DATA_DIR = os.path.join(LOCALAPP, "Google", "Chrome", "User Data")
CHROMIUM_USER_DATA_DIR = os.path.join(LOCALAPP, "Google", "Chromium", "User Data")

# --- Global settings ---
HEADLESS = False
DEFAULT_BROWSER = "edge"  # Options: "chrome", "edge", "chromium"


user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)
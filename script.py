import time
import threading
import winsound
from datetime import datetime
from framework.core_page import CorePage
import options

def start_beeping(stop_event):
    while not stop_event.is_set():
        winsound.Beep(1000, 300)

def wait_for_loader(page: CorePage):
    loader_selector = ".loader-container"
    loader = page.query_selector(loader_selector)
    if loader and loader.is_visible():
        page.wait_for_selector(loader_selector, state="detached", timeout=300000)
    time.sleep(2)

def login(page: CorePage):
    stop_event = threading.Event()
    beep_thread = threading.Thread(target=start_beeping, args=(stop_event,))

    logout_exists = page.query_selector("#desktop-logout-button")
    if logout_exists:
        stop_event.set()
        return
    
    beep_thread.start()
    
    login_button = page.query_selector("#desktop-login-button")
    if login_button:
        login_button.click()

    wait_for_loader(page)
    page.wait_for_selector("#dialog-outlet", timeout=15000)
    page.click("button.btn.btn-primary:has-text('Fortsätt')")
    wait_for_loader(page)
    page.wait_for_selector("#desktop-logout-button", timeout=30000)
    wait_for_loader(page)

    stop_event.set()
    beep_thread.join()

def open_booked_tests(page: CorePage):
    menu_btn = page.wait_for_selector('#desktop-menu-button', timeout=15000)
    menu_btn.click()
    page.wait_for_selector('#desktop-site-nav-menu.show', timeout=15000)
    page.wait_for_selector('#desktop-exams-button', timeout=15000).click()
    wait_for_loader(page)
    
def get_booked_date(page: CorePage):
    page.wait_for_selector("div.card-item.borderless", timeout=15000)
    cards = page.query_selector_all("div.card-item.borderless")
    for card in cards:
        heading = card.query_selector("h2")
        if heading and options.TEST in heading.inner_text():
            p_elem = card.query_selector("p:has(i.fa-clock)")
            if p_elem:
                date_text = p_elem.inner_text().replace("\xa0", " ").strip()
                print("Booked date:", date_text)
                return date_text
    return None

def open_ombooking(page: CorePage):
    page.wait_for_selector("div.card-item.borderless", timeout=20000)
    cards = page.query_selector_all("div.card-item.borderless")
    for card in cards:
        heading = card.query_selector("h2")
        if heading and options.TEST in heading.inner_text():
            button = card.query_selector("#id-button-canReschedule")
            if button:
                button.click()
                wait_for_loader(page)
                return True
    return False

def select_city(page: CorePage):
    # Split comma-separated cities and clean whitespace
    city_names = [c.strip() for c in options.CITY.split(",") if c.strip()]

    print(f"Opening city selection popup ...")
    page.wait_for_selector('button[id="select-location-search"]', timeout=20000).click()
    wait_for_loader(page)

    page.wait_for_selector("app-location-select-dialog", timeout=20000)
    wait_for_loader(page)

    for city_name in city_names:
        city_button = page.query_selector(f"button.select-item:has-text('{city_name}')")
        if not city_button:
            print(f"City not found: {city_name}")
            continue

        classes = city_button.get_attribute("class") or ""
        if "selected" not in classes:
            print(f"{city_name} not selected, selecting now...")
            city_button.click()
            wait_for_loader(page)
        else:
            print(f"{city_name} already selected.")

    confirm_button = page.query_selector("button.btn.btn-primary:has-text('Bekräfta')")
    confirm_button.click()
    page.wait_for_selector("app-location-select-dialog", state="detached", timeout=20000)
    wait_for_loader(page)

    print(f"City selection confirmed: {', '.join(city_names)}")


def select_car(page: CorePage):
    if options.TYPE.lower() == "theori":
        print("Theory test selected. No car booking needed.")
        return

    car_name = options.CAR
    print("Selecting car type...")
    select_elem = page.wait_for_selector("#vehicle-select", timeout=20000)
    select_elem.select_option(label=f"{car_name}")
    wait_for_loader(page)
    print(f"{car_name} selected.")


def get_earliest_date(page: CorePage):
    selector = "#results-desktop strong"
    page.wait_for_selector(selector, timeout=30000)
    
    full_text = page.inner_text(selector)
    parts = full_text.split()
    
    date_str = " ".join(parts[1:]).replace(",", "")
    
    months = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "maj": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "okt": "10", "nov": "11", "dec": "12"
    }
    
    day, month_name, year, time = date_str.split()
    month = months[month_name.lower()[:3]]
    
    dt = datetime.strptime(f"{year}-{month}-{day.zfill(2)} {time}", "%Y-%m-%d %H:%M")
    return dt.strftime("%Y-%m-%d %H:%M")

def compare_dates(available_date_str: str, target_date_str: str, earliest_allowed_str: str):
    available_date = datetime.strptime(available_date_str, "%Y-%m-%d %H:%M")
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d %H:%M")
    earliest_allowed = datetime.strptime(earliest_allowed_str, "%Y-%m-%d %H:%M")

    if available_date < earliest_allowed:
        return False

    return available_date < target_date


def rebook_first_available(page: CorePage):
    page.wait_for_selector("div.panel.mb-3", timeout=15000)
    first_panel = page.query_selector("div.panel.mb-3")
    first_panel.query_selector("button.btn.btn-primary").click()

    wait_for_loader(page)
    page.wait_for_selector("button#cart-continue-button", timeout=15000)
    page.query_selector("button#cart-continue-button").click()

    wait_for_loader(page)
    page.wait_for_selector("button#pay-invoice-button", timeout=15000)
    page.query_selector("button#pay-invoice-button").click()

    wait_for_loader(page)
    page.wait_for_selector("app-contact-details-dialog button.btn.btn-primary", timeout=15000)
    page.query_selector("app-contact-details-dialog button.btn.btn-primary").click()

def main():
    page = CorePage()
    try:
        while True:
            page.goto("https://fp.trafikverket.se/Boka/ng/")
            page.wait_for_load_state("domcontentloaded")
            wait_for_loader(page)

            login(page)
            open_booked_tests(page)

            booked_date = get_booked_date(page)
            open_ombooking(page)
            select_city(page)
            select_car(page)

            available_date = get_earliest_date(page)
            earliest_allowed = options.EARLIEST_DATE
            bookable = compare_dates(available_date, booked_date, earliest_allowed)

            print(f"Already Booked Date : {booked_date}")
            print(f"Earliest Next : {available_date}")
            print(f"Earliest Allowed : {earliest_allowed}")


            if bookable:
                rebook_first_available(page)
                print(f"New Date Booked")
            else:
                print(f"Cannot be booked. Retrying after 15 seconds")
                time.sleep(15)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Exiting...")

    finally:
        # Safe close - avoids crash if already closed
        try:
            page.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()

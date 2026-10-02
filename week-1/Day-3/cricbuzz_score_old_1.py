import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

URL = "https://www.cricbuzz.com/cricket-match/live-scores"


def get_score(page):
    """
    The current Cricbuzz score element is a div with both:
        cb-scr-wll-chvrn
        cb-lv-scrs-col

    We use :visible so Playwright does not select a hidden duplicate.
    """

    score_elements = page.locator(
        "div.cb-scr-wll-chvrn.cb-lv-scrs-col:visible"
    )

    try:
        score_elements.first.wait_for(state="visible", timeout=30000)
    except PlaywrightTimeoutError:
        print("\nCould not find the visible score element.")
        print("Current URL:", page.url)
        print("Page title:", page.title())

        # Diagnostic: show visible text so we can see whether
        # Cricbuzz returned the normal page or another page.
        print("\nVisible page text (first 2000 characters):")
        print(page.locator("body").inner_text()[:2000])

        raise

    # Inspect the visible score elements and choose one that
    # actually contains a cricket score pattern such as 237,
    # 21-2, 173-4, etc.
    count = score_elements.count()

    for i in range(count):
        text = score_elements.nth(i).inner_text().strip()

        if text and re.search(r"\d", text):
            return text

    raise RuntimeError(
        "The visible Cricbuzz score elements were found, "
        "but no score text was available."
    )


with sync_playwright() as p:

    # =========================================================
    # 1. HEADED RUN
    # =========================================================

    print("Starting headed Playwright run...")

    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    page.goto(URL, wait_until="domcontentloaded")

    print("Cricbuzz opened in headed mode.")

    score = get_score(page)

    print("\nSCORE FROM HEADED RUN:")
    print(score)

    page.screenshot(path="score.png", full_page=True)
    print("Screenshot saved as score.png")

    browser.close()

    # =========================================================
    # 2. HEADLESS RUN
    # =========================================================

    print("\nStarting headless Playwright run...")

    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    page.goto(URL, wait_until="domcontentloaded")

    headless_score = get_score(page)

    print("\nSCORE FROM HEADLESS RUN:")
    print(headless_score)

    print("\nHeadless run confirmed successfully.")

    browser.close()

from playwright.sync_api import sync_playwright

URL = "https://www.cricbuzz.com/cricket-match/live-scores"


def get_score(page):
    # The live-score page currently exposes score text in elements
    # with the class "cb-lv-scrs-col". We wait for that element
    # instead of waiting for a parent container.
    score_element = page.locator(".cb-lv-scrs-col").first

    score_element.wait_for(state="visible", timeout=30000)

    score = score_element.inner_text().strip()

    if not score:
        raise RuntimeError("Score element was found, but it contains no text.")

    return score


with sync_playwright() as p:

    # ---------------------------------------------------------
    # 1. HEADED RUN
    # ---------------------------------------------------------
    print("Starting headed Playwright run...")

    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    page.goto(URL, wait_until="domcontentloaded")
    print("Cricbuzz opened in headed mode.")

    # Wait for the actual score element.
    score = get_score(page)

    print("\nSCORE FROM HEADED RUN:")
    print(score)

    # Required screenshot.
    page.screenshot(path="score.png", full_page=True)
    print("Screenshot saved as score.png")

    browser.close()

    # ---------------------------------------------------------
    # 2. HEADLESS RUN
    # ---------------------------------------------------------
    print("\nStarting headless Playwright run...")

    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    page.goto(URL, wait_until="domcontentloaded")

    # Same element-based wait in headless mode.
    headless_score = get_score(page)

    print("\nSCORE FROM HEADLESS RUN:")
    print(headless_score)
    print("\nHeadless run confirmed successfully.")

    browser.close()

from playwright.sync_api import sync_playwright

URL = "https://www.cricbuzz.com/cricket-match/live-scores"


def find_score(page):
    page.locator("body").wait_for(
        state="visible",
        timeout=30000
    )

    # Inspect all visible elements containing numbers.
    elements = page.locator("body *:visible")
    count = elements.count()

    for i in range(count):
        try:
            text = " ".join(elements.nth(i).inner_text().split())

            # Look for common cricket score formats:
            # 123/4
            # 123-4
            # 123 & 456
            if text and (
                "/" in text
                or "-" in text
                or "&" in text
            ):
                import re

                if re.search(
                    r"\b\d{1,3}\s*(?:/|-|&)\s*\d{1,3}\b",
                    text
                ):
                    return text

        except Exception:
            pass

    return None


def run_cricbuzz(playwright, headless):
    mode = "HEADLESS" if headless else "HEADED"

    print("\n" + "=" * 60)
    print(f"STARTING {mode} RUN")
    print("=" * 60)

    browser = playwright.chromium.launch(
        channel="chrome",
        headless=headless
    )

    page = browser.new_page(
        viewport={
            "width": 1440,
            "height": 900
        }
    )

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=30000
    )

    page.locator("body").wait_for(
        state="visible",
        timeout=30000
    )

    print("URL:", page.url)
    print("TITLE:", page.title())

    # Check whether Cricbuzz/Akamai returned an error page.
    body_text = page.locator("body").inner_text()

    if "errors.edgesuite.net" in page.url:
        print("\nCricbuzz/Akamai returned an error page.")
        print("Headless access is being blocked.")
        return browser, page, None

    score = find_score(page)

    if score:
        print("\nSCORE:")
        print(score)
    else:
        print("\nNo score found on the returned page.")

    return browser, page, score


with sync_playwright() as p:

    # ======================================================
    # HEADED
    # ======================================================

    browser, page, headed_score = run_cricbuzz(
        p,
        headless=False
    )

    if headed_score:
        print("\nHEADED RUN SUCCESSFUL")
        print("Score:", headed_score)

        page.screenshot(
            path="score.png",
            full_page=True
        )

        print("Screenshot saved as score.png")
    else:
        print("\nHEADED RUN DID NOT FIND A SCORE.")

    browser.close()

    # ======================================================
    # HEADLESS
    # ======================================================

    browser, page, headless_score = run_cricbuzz(
        p,
        headless=True
    )

    if headless_score:
        print("\nHEADLESS RUN SUCCESSFUL")
        print("Score:", headless_score)
    else:
        print("\nHEADLESS RUN COULD NOT ACCESS THE SCORE PAGE.")

    browser.close()

    # ======================================================
    # RESULT
    # ======================================================

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print("Headed score  :", headed_score)
    print("Headless score:", headless_score)
    print("Screenshot    : score.png")

    if headed_score and headless_score:
        print("\nBoth headed and headless runs succeeded.")
    elif headed_score and not headless_score:
        print(
            "\nHeaded mode succeeded, but Cricbuzz/Akamai "
            "blocked the headless request."
        )
    else:
        print("\nCricbuzz score could not be retrieved.")

import requests
from bs4 import BeautifulSoup

# News website to scrape
URL = "https://www.bbc.com/news"

# Identify the request as coming from a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36"
}


def get_headlines():
    try:
        # Step 1: Fetch the webpage
        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=15
        )

        # Stop if the website returns an HTTP error
        response.raise_for_status()

        # Step 2: Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Step 3: Find headline elements
        headline_elements = soup.find_all(["h2", "h3"])

        # Step 4: Clean and remove duplicate headlines
        headlines = []
        seen = set()

        for element in headline_elements:
            headline = element.get_text(" ", strip=True)

            if headline and headline not in seen:
                seen.add(headline)
                headlines.append(headline)

            if len(headlines) == 5:
                break

        # Step 5: Print the top five headlines
        if not headlines:
            print("No headlines found. The website HTML may have changed.")
            return

        print("\nTop 5 Headlines from BBC News")
        print("-" * 40)

        for number, headline in enumerate(headlines, start=1):
            print(f"{number}. {headline}")

        if len(headlines) < 5:
            print(f"\nOnly {len(headlines)} headlines were found.")

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP Error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Request Error: {error}")

    except Exception as error:
        print(f"Unexpected Error: {error}")


if __name__ == "__main__":
    get_headlines()

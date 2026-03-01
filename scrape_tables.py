from playwright.sync_api import sync_playwright
import re

BASE_URL = "https://datadash.iitmandi.co.in/table?seed="
SEEDS = list(range(68, 78))  # 68 to 77


def extract_numbers_from_table(page):
    numbers = []

    # Only look inside tables
    cells = page.locator("table td").all()

    for cell in cells:
        text = cell.inner_text().strip()
        found_numbers = re.findall(r"-?\d+\.?\d*", text)

        for num_str in found_numbers:
            try:
                numbers.append(float(num_str))
            except:
                pass

    return numbers


def main():
    total_sum = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        page = browser.new_page()
        page.set_default_timeout(30000)

        for seed in SEEDS:
            url = f"{BASE_URL}{seed}"
            print(f"Scraping {url}...")

            try:
                page.goto(url, wait_until="domcontentloaded")

                # Give JS time to render
                page.wait_for_timeout(3000)

                # Check if table exists (avoid crash)
                if page.locator("table").count() == 0:
                    print(f"  No table found for seed {seed}")
                    continue

                numbers = extract_numbers_from_table(page)
                seed_sum = sum(numbers)

                print(
                    f"  Seed {seed}: Found {len(numbers)} numbers, sum = {seed_sum}"
                )

                total_sum += seed_sum

            except Exception as e:
                print(f"  Error scraping seed {seed}: {e}")

        browser.close()

    # IMPORTANT: Grader-friendly output
    print(f"TOTAL_SUM={int(total_sum)}")


if __name__ == "__main__":
    main()
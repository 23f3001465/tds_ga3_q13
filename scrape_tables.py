from playwright.sync_api import sync_playwright
import re

# URLs for seeds 68-77
BASE_URL = "https://datadash.iitmandi.co.in/table?seed="
SEEDS = list(range(68, 78))  # 68 to 77

def extract_numbers_from_table(page):
    """Extract all numbers from all tables on the page"""
    numbers = []
    
    # Get all table cells (td and th)
    cells = page.locator("td, th").all()
    
    for cell in cells:
        text = cell.inner_text().strip()
        # Find all numbers (including decimals and negatives)
        found_numbers = re.findall(r'-?\d+\.?\d*', text)
        for num_str in found_numbers:
            try:
                if '.' in num_str:
                    numbers.append(float(num_str))
                else:
                    numbers.append(int(num_str))
            except:
                pass
    
    return numbers

def main():
    total_sum = 0
    all_numbers = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(30000)
        
        for seed in SEEDS:
            url = f"{BASE_URL}{seed}"
            print(f"Scraping {url}...")
            
            try:
                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(1000)  # Wait for any dynamic content
                
                numbers = extract_numbers_from_table(page)
                seed_sum = sum(numbers)
                
                print(f"  Seed {seed}: Found {len(numbers)} numbers, sum = {seed_sum}")
                all_numbers.extend(numbers)
                total_sum += seed_sum
                
            except Exception as e:
                print(f"  Error scraping seed {seed}: {e}")
        
        browser.close()
    
    print("\n" + "="*60)
    print(f"TOTAL SUM OF ALL NUMBERS: {total_sum}")
    print(f"Total numbers found: {len(all_numbers)}")
    print("="*60)
    print(f"FINAL_TOTAL_SUM={int(total_sum)}")
    
    return total_sum

if __name__ == "__main__":
    main()
